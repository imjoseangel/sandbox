-- ADVANCED PostgreSQL Full-Text Search Features

-- 1. PHRASE SEARCH WITH phraseto_tsquery
-- Matches exact word sequences rather than just word presence
CREATE OR REPLACE FUNCTION search_articles_phrase(
    search_phrase TEXT,
    page_size INTEGER DEFAULT 20
) RETURNS TABLE (
    id INTEGER,
    title TEXT,
    author_name TEXT,
    rank FLOAT4,
    highlight TEXT
) AS $$
DECLARE
    tsquery_var tsquery;
BEGIN
    -- Use phraseto_tsquery for exact phrase matching
    tsquery_var := phraseto_tsquery('english', search_phrase);

    RETURN QUERY
    SELECT
        a.id,
        a.title,
        auth.name,
        ts_rank(a.search_vector, tsquery_var) as rank,
        ts_headline('english', a.content, tsquery_var,
            'StartSel=<mark>, StopSel=</mark>, MaxWords=30, MinWords=1') as highlight
    FROM articles a
    JOIN authors auth ON a.author_id = auth.id
    WHERE a.status = 'published'
    AND a.search_vector @@ tsquery_var
    ORDER BY rank DESC
    LIMIT page_size;
END;
$$ LANGUAGE plpgsql;

-- 2. SEQUENCE SEARCH WITH <-> OPERATOR
-- Finds words in specific proximity and order
CREATE OR REPLACE FUNCTION search_articles_sequence(
    word1 TEXT,
    word2 TEXT,
    distance INTEGER DEFAULT 1
) RETURNS TABLE (
    id INTEGER,
    title TEXT,
    match_count BIGINT
) AS $$
DECLARE
    tsquery_var tsquery;
BEGIN
    -- Use <-> operator for sequence matching
    -- word1 <-> word2 matches words exactly next to each other
    -- word1 <-> word2 <-> word3 for longer sequences
    tsquery_var := to_tsquery('english',
        word1 || ' <' || distance || '> ' || word2);

    RETURN QUERY
    SELECT
        a.id,
        a.title,
        COUNT(*) as match_count
    FROM articles a
    WHERE a.status = 'published'
    AND a.search_vector @@ tsquery_var
    GROUP BY a.id, a.title
    ORDER BY match_count DESC;
END;
$$ LANGUAGE plpgsql;

-- 3. UNACCENT FUZZY SEARCH
-- Remove diacritics and accents for better matching
-- Useful for international content: café → cafe, naïve → naive
CREATE OR REPLACE FUNCTION search_articles_unaccented(
    search_query TEXT,
    page_size INTEGER DEFAULT 20
) RETURNS TABLE (
    id INTEGER,
    title TEXT,
    content_preview TEXT,
    rank FLOAT4
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.title,
        LEFT(a.content, 100) || '...' as content_preview,
        ts_rank(a.search_vector, to_tsquery('english', search_query)) as rank
    FROM articles a
    WHERE a.status = 'published'
    -- Remove accents from both the search vector and query
    AND unaccent(a.search_vector::text) @@ to_tsquery('english', unaccent(search_query))
    ORDER BY rank DESC
    LIMIT page_size;
END;
$$ LANGUAGE plpgsql;

-- 4. CUSTOM TEXT SEARCH CONFIGURATION
-- Create a custom configuration for specialized search needs
CREATE TEXT SEARCH CONFIGURATION custom_english (
    COPY = english
);

-- Override stopwords for domain-specific needs
-- Remove 'article' and 'database' from stopwords (keep them searchable)
ALTER TEXT SEARCH CONFIGURATION custom_english
    ALTER MAPPING FOR asciiword, asciihword, hword_asciipart
    WITH simple;

-- 5. SYNONYM DICTIONARY FOR TEXT SEARCH
-- Map similar terms to the same lexeme
CREATE TEXT SEARCH DICTIONARY synonym_dict (
    TEMPLATE = synonym,
    SYNONYMS = synonym_file
);

-- Alternative: Create synonym rules inline
CREATE TEXT SEARCH DICTIONARY synonyms (
    TEMPLATE = synonym,
    SYNONYMS = 'syn.dict'
);

-- 6. MATERIALIZED VIEW FOR FREQUENTLY SEARCHED CONTENT
-- Pre-compute and cache search results for performance
CREATE MATERIALIZED VIEW popular_articles_search AS
SELECT
    a.id,
    a.title,
    a.subtitle,
    auth.name as author_name,
    COUNT(DISTINCT ac.category_id) as category_count,
    COUNT(DISTINCT at.tag_id) as tag_count,
    a.published_at,
    ts_rank(a.search_vector, to_tsquery('english', 'article')) as relevance_score
FROM articles a
JOIN authors auth ON a.author_id = auth.id
LEFT JOIN article_categories ac ON a.id = ac.article_id
LEFT JOIN article_tags at ON a.id = at.article_id
WHERE a.status = 'published'
AND a.published_at > NOW() - INTERVAL '90 days'
GROUP BY a.id, a.title, a.subtitle, auth.name, a.published_at, a.search_vector
ORDER BY relevance_score DESC, a.published_at DESC;

-- Create index on materialized view
CREATE INDEX popular_articles_search_idx ON popular_articles_search (published_at DESC, relevance_score DESC);

-- Refresh the materialized view (run periodically)
-- REFRESH MATERIALIZED VIEW popular_articles_search;

-- 7. WEIGHTED FULL-TEXT SEARCH WITH CUSTOM WEIGHTS
-- Give different importance to different fields beyond A, B, C
CREATE OR REPLACE FUNCTION search_articles_custom_weights(
    search_query TEXT,
    title_weight FLOAT DEFAULT 10.0,
    subtitle_weight FLOAT DEFAULT 5.0,
    content_weight FLOAT DEFAULT 1.0,
    page_size INTEGER DEFAULT 20
) RETURNS TABLE (
    id INTEGER,
    title TEXT,
    weighted_rank FLOAT4
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.title,
        (
            ts_rank(
                setweight(to_tsvector('english', coalesce(a.title, '')), 'A') ||
                setweight(to_tsvector('english', coalesce(a.subtitle, '')), 'B') ||
                setweight(to_tsvector('english', coalesce(a.content, '')), 'C'),
                to_tsquery('english', search_query)
            ) *
            (
                CASE
                    WHEN a.title ILIKE '%' || search_query || '%' THEN title_weight
                    WHEN a.subtitle ILIKE '%' || search_query || '%' THEN subtitle_weight
                    ELSE content_weight
                END
            )
        )::FLOAT4 as weighted_rank
    FROM articles a
    WHERE a.status = 'published'
    AND a.search_vector @@ to_tsquery('english', search_query)
    ORDER BY weighted_rank DESC
    LIMIT page_size;
END;
$$ LANGUAGE plpgsql;

-- 8. AUTOCOMPLETE WITH TRIGRAM AND PREFIX
-- Fast prefix matching for search suggestions
CREATE OR REPLACE FUNCTION search_articles_autocomplete(
    prefix TEXT,
    limit_count INTEGER DEFAULT 10
) RETURNS TABLE (
    suggestion TEXT,
    match_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT ON (a.title)
        a.title as suggestion,
        COUNT(*) OVER (PARTITION BY a.title) as match_count
    FROM articles a
    WHERE a.status = 'published'
    AND (
        a.title ILIKE prefix || '%'
        OR
        a.title % prefix  -- trigram similarity
    )
    ORDER BY a.title
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- 9. SIMILARITY SEARCH USING TRIGRAM
-- Find similar articles based on content similarity
CREATE OR REPLACE FUNCTION find_similar_articles(
    article_id INTEGER,
    similarity_threshold FLOAT DEFAULT 0.3,
    limit_count INTEGER DEFAULT 10
) RETURNS TABLE (
    similar_id INTEGER,
    similar_title TEXT,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.title,
        similarity(a.content, (SELECT content FROM articles WHERE id = article_id)) as sim
    FROM articles a
    WHERE a.id != article_id
    AND a.status = 'published'
    AND similarity(a.content, (SELECT content FROM articles WHERE id = article_id)) > similarity_threshold
    ORDER BY sim DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- 10. STATISTICS AND PERFORMANCE MONITORING
CREATE OR REPLACE FUNCTION search_stats() RETURNS TABLE (
    metric_name TEXT,
    metric_value TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 'Total Articles'::TEXT, COUNT(*)::TEXT FROM articles
    UNION ALL
    SELECT 'Searchable Articles', COUNT(*)::TEXT FROM articles WHERE search_vector IS NOT NULL
    UNION ALL
    SELECT 'Published Articles', COUNT(*)::TEXT FROM articles WHERE status = 'published'
    UNION ALL
    SELECT 'Average Content Length', ROUND(AVG(LENGTH(content)))::TEXT FROM articles
    UNION ALL
    SELECT 'Articles with Tags', COUNT(DISTINCT article_id)::TEXT FROM article_tags
    UNION ALL
    SELECT 'Unique Authors', COUNT(DISTINCT author_id)::TEXT FROM articles
    UNION ALL
    SELECT 'Last Article Published', MAX(published_at)::TEXT FROM articles;
END;
$$ LANGUAGE plpgsql;

-- 11. DEBUGGING: ANALYZE TSVECTOR COMPOSITION
-- See exactly how tsvector is built for an article
CREATE OR REPLACE FUNCTION analyze_article_search_vector(
    article_id INTEGER
) RETURNS TABLE (
    field_name TEXT,
    vector_content TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 'Title'::TEXT, setweight(to_tsvector('english', a.title), 'A')::TEXT
    FROM articles a WHERE a.id = article_id
    UNION ALL
    SELECT 'Subtitle'::TEXT, setweight(to_tsvector('english', a.subtitle), 'B')::TEXT
    FROM articles a WHERE a.id = article_id
    UNION ALL
    SELECT 'Content'::TEXT, setweight(to_tsvector('english', LEFT(a.content, 500)), 'C')::TEXT
    FROM articles a WHERE a.id = article_id
    UNION ALL
    SELECT 'Combined'::TEXT, a.search_vector::TEXT
    FROM articles a WHERE a.id = article_id;
END;
$$ LANGUAGE plpgsql;
