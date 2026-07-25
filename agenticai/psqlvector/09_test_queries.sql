-- ============================================
-- BASIC FULL-TEXT SEARCH TESTS
-- ============================================

-- 1. Show what tsvector looks like
\echo '\n=== Test 1: Basic tsvector representation ==='
SELECT to_tsvector('english', 'The quick brown foxes are jumping over lazy dogs');

-- 2. Show what tsquery looks like
\echo '\n=== Test 2: Basic tsquery representation ==='
SELECT to_tsquery('english', 'postgresql & database');

-- 3. Simple keyword search
\echo '\n=== Test 3: Simple keyword search (article) ==='
SELECT id, title, author_id, published_at
FROM articles
WHERE search_vector @@ to_tsquery('english', 'article')
LIMIT 10;

-- 4. OR search
\echo '\n=== Test 4: OR search (article OR content) ==='
SELECT id, title, author_id
FROM articles
WHERE search_vector @@ to_tsquery('english', 'article | content')
LIMIT 10;

-- 5. AND search
\echo '\n=== Test 5: AND search (article AND content) ==='
SELECT id, title, author_id
FROM articles
WHERE search_vector @@ to_tsquery('english', 'article & content')
LIMIT 10;

-- 6. Negation search
\echo '\n=== Test 6: Negation search (article NOT title) ==='
SELECT id, title, author_id
FROM articles
WHERE search_vector @@ to_tsquery('english', 'article & !title')
LIMIT 10;

-- ============================================
-- RANKING AND RELEVANCE TESTS
-- ============================================

-- 7. Ranked search results
\echo '\n=== Test 7: Ranked search results ==='
SELECT
    id,
    title,
    ts_rank(search_vector, to_tsquery('english', 'article')) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'article')
ORDER BY rank DESC
LIMIT 10;

-- 8. Headline/highlight results
\echo '\n=== Test 8: Headline/highlight in results ==='
SELECT
    id,
    title,
    ts_headline('english', title, to_tsquery('english', 'article'),
        'StartSel=<mark>, StopSel=</mark>, MaxWords=15, MinWords=1') as highlighted_title
FROM articles
WHERE search_vector @@ to_tsquery('english', 'article')
LIMIT 5;

-- ============================================
-- ADVANCED SEARCH FUNCTION TESTS
-- ============================================

-- 9. Basic search using function
\echo '\n=== Test 9: Basic search using function ==='
SELECT (results).* FROM search_articles(
    'article',
    page_size => 5,
    page_number => 1
);

-- 10. Search with multiple keywords
\echo '\n=== Test 10: Search with multiple keywords ==='
SELECT (results).* FROM search_articles(
    'article content title',
    page_size => 5,
    page_number => 1
);

-- 11. Search with tag filter
\echo '\n=== Test 11: Search with tag filter ==='
SELECT (results).* FROM search_articles(
    'article',
    tag_filter => ARRAY['postgresql', 'database'],
    page_size => 5,
    page_number => 1
);

-- 12. Search with date range
\echo '\n=== Test 12: Search with date range (last 6 months) ==='
SELECT (results).* FROM search_articles(
    'article',
    min_date => CURRENT_TIMESTAMP - INTERVAL '6 months',
    max_date => CURRENT_TIMESTAMP,
    page_size => 5,
    page_number => 1
);

-- 13. Search with category filter
\echo '\n=== Test 13: Search with category filter ==='
SELECT (results).* FROM search_articles(
    'article',
    category_filter => ARRAY[1, 2],
    page_size => 5,
    page_number => 1
);

-- 14. Pagination test
\echo '\n=== Test 14: Pagination (page 1 vs page 2) ==='
SELECT (results).id, (results).title, (results).rank FROM search_articles(
    'article',
    page_size => 5,
    page_number => 1
);
SELECT '--- PAGE 2 ---' as separator;
SELECT (results).id, (results).title, (results).rank FROM search_articles(
    'article',
    page_size => 5,
    page_number => 2
);

-- ============================================
-- PERFORMANCE ANALYSIS
-- ============================================

-- 15. EXPLAIN ANALYZE for basic search
\echo '\n=== Test 15: Query plan for basic search ==='
EXPLAIN ANALYZE
SELECT * FROM articles
WHERE search_vector @@ to_tsquery('english', 'article')
LIMIT 10;

-- 16. EXPLAIN ANALYZE for complex search
\echo '\n=== Test 16: Query plan for complex search ==='
EXPLAIN ANALYZE
SELECT * FROM search_articles(
    'article content',
    tag_filter => ARRAY['article', 'content']
);

-- ============================================
-- TRIGRAM FUZZY MATCHING
-- ============================================

-- 17. Fuzzy tag search
\echo '\n=== Test 17: Fuzzy tag search (postgreesql typo) ==='
SELECT name,
    similarity(name, 'postgreesql') as sim
FROM tags
WHERE name % 'postgreesql'
ORDER BY sim DESC;

-- ============================================
-- STATISTICS AND ANALYSIS
-- ============================================

-- 18. Search statistics
\echo '\n=== Test 18: Search statistics ==='
SELECT
    COUNT(*) as total_articles,
    COUNT(DISTINCT author_id) as unique_authors,
    COUNT(DISTINCT CASE WHEN status = 'published' THEN 1 END) as published_count,
    MIN(published_at) as oldest_article,
    MAX(published_at) as newest_article
FROM articles;

-- 19. Author statistics
\echo '\n=== Test 19: Author statistics ==='
SELECT
    auth.name,
    COUNT(a.id) as article_count,
    COUNT(CASE WHEN a.status = 'published' THEN 1 END) as published_count
FROM authors auth
LEFT JOIN articles a ON auth.id = a.author_id
GROUP BY auth.id, auth.name
ORDER BY article_count DESC
LIMIT 10;

-- 20. Tag usage statistics
\echo '\n=== Test 20: Tag usage statistics ==='
SELECT
    t.name,
    COUNT(at.article_id) as usage_count
FROM tags t
LEFT JOIN article_tags at ON t.id = at.tag_id
GROUP BY t.id, t.name
ORDER BY usage_count DESC;

-- ============================================
-- ADVANCED FEATURES TESTS
-- ============================================

-- 21. Phrase search (exact word sequences)
\echo '\n=== Test 21: Phrase search ==='
SELECT * FROM search_articles_phrase('article content', page_size => 5);

-- 22. Sequence search (words in order with <-> operator)
\echo '\n=== Test 22: Sequence search ==='
SELECT * FROM search_articles_sequence('article', 'content', distance => 2);

-- 23. Unaccent search (handles accents/diacritics)
\echo '\n=== Test 23: Unaccent search ==='
SELECT * FROM search_articles_unaccented('article', page_size => 5);

-- 24. Custom weighted search
\echo '\n=== Test 24: Custom weighted search ==='
SELECT * FROM search_articles_custom_weights(
    'article',
    title_weight => 20.0,
    subtitle_weight => 10.0,
    content_weight => 1.0,
    page_size => 5
);

-- 25. Autocomplete suggestions
\echo '\n=== Test 25: Autocomplete suggestions ==='
SELECT * FROM search_articles_autocomplete('Article', limit_count => 5);

-- 26. Similar articles (trigram similarity)
\echo '\n=== Test 26: Find similar articles ==='
SELECT * FROM find_similar_articles(
    article_id => 1,
    similarity_threshold => 0.1,
    limit_count => 5
);

-- 27. Popular articles materialized view
\echo '\n=== Test 27: Popular articles view ==='
SELECT id, title, author_name, relevance_score
FROM popular_articles_search
LIMIT 5;

-- 28. Search statistics
\echo '\n=== Test 28: Search statistics ==='
SELECT * FROM search_stats();

-- 29. Analyze article search vector composition
\echo '\n=== Test 29: Analyze search vector composition ==='
SELECT * FROM analyze_article_search_vector(article_id => 1);

-- 30. Trigram similarity on tags (fuzzy matching)
\echo '\n=== Test 30: Fuzzy tag matching ==='
SELECT name, similarity(name, 'artical') as sim
FROM tags
WHERE name % 'artical'
ORDER BY sim DESC
LIMIT 5;
