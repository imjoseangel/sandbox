-- Authors table with search vector
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    bio TEXT,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(bio, '')), 'B')
    ) STORED
);

-- Articles table with search vector
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    subtitle TEXT,
    content TEXT NOT NULL,
    status article_status NOT NULL DEFAULT 'draft',
    author_id INTEGER REFERENCES authors(id),
    reading_time INTEGER,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(subtitle, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(content, '')), 'C')
    ) STORED
);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Article-Categories junction table
CREATE TABLE article_categories (
    article_id INTEGER REFERENCES articles(id),
    category_id INTEGER REFERENCES categories(id),
    PRIMARY KEY (article_id, category_id)
);

-- Article-Tags junction table
CREATE TABLE article_tags (
    article_id INTEGER REFERENCES articles(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (article_id, tag_id)
);
