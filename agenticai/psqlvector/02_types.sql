-- Create custom types
CREATE TYPE article_status AS ENUM ('draft', 'published', 'archived');

CREATE TYPE search_result AS (
    id INTEGER,
    title TEXT,
    subtitle TEXT,
    author_name TEXT,
    published_at TIMESTAMP WITH TIME ZONE,
    rank FLOAT4,
    highlight TEXT
);
