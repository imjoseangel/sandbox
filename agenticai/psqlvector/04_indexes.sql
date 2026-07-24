-- Create GIN indexes for full-text search
CREATE INDEX authors_search_idx ON authors USING GIN (search_vector);
CREATE INDEX articles_search_idx ON articles USING GIN (search_vector);

-- Create indexes for filtering
CREATE INDEX articles_status_idx ON articles (status);
CREATE INDEX articles_published_at_idx ON articles (published_at);
CREATE INDEX articles_author_id_idx ON articles (author_id);
CREATE INDEX authors_id_idx ON authors (id);

-- Create trigram index for fuzzy matching on tags
CREATE INDEX tags_name_trgm_idx ON tags USING GIN (name gin_trgm_ops);

-- Create indexes for junction tables
CREATE INDEX article_categories_category_id_idx ON article_categories (category_id);
CREATE INDEX article_tags_tag_id_idx ON article_tags (tag_id);

-- Verify indexes
\di
