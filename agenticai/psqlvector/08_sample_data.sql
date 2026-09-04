-- Insert sample authors (1000 records)
INSERT INTO authors (name, bio, email)
SELECT
    'Author ' || i,
    'Bio for author ' || i || '. Specializes in technology, business, and innovation.',
    'author' || i || '@example.com'
FROM generate_series(1, 1000) i;

-- Insert sample categories
INSERT INTO categories (name, description)
VALUES
    ('Technology', 'Articles about tech, programming, and software'),
    ('Business', 'Business strategies, startups, and management'),
    ('Science', 'Scientific discoveries and research'),
    ('Arts', 'Creative and artistic content'),
    ('Health', 'Health, wellness, and medical topics');

-- Insert sample tags
INSERT INTO tags (name)
VALUES
    ('postgresql'),
    ('database'),
    ('search'),
    ('elasticsearch'),
    ('performance'),
    ('tutorial'),
    ('beginner'),
    ('advanced'),
    ('optimization'),
    ('fulltext');

-- Insert sample articles (1,000,000 records like the article example)
INSERT INTO articles (title, subtitle, content, author_id, status, published_at)
SELECT
    'Article Title ' || i,
    'Subtitle for article ' || i,
    'Content for article ' || i || ' ' || repeat('Lorem ipsum dolor sit amet. ', 100),
    (i % 1000) + 1,
    'published',
    timestamp '2020-01-01' + (random() * (now() - timestamp '2020-01-01'))
FROM generate_series(1, 1000000) i;

-- Link articles to categories randomly
INSERT INTO article_categories (article_id, category_id)
SELECT
    a.id,
    c.id
FROM articles a,
    (SELECT id FROM categories LIMIT 5) c
WHERE random() < 0.6;

-- Link articles to tags randomly
INSERT INTO article_tags (article_id, tag_id)
SELECT
    a.id,
    t.id
FROM articles a,
    (SELECT id FROM tags LIMIT 10) t
WHERE random() < 0.4;

-- Verify data insertion
SELECT 'Authors' as table_name, COUNT(*) as count FROM authors
UNION ALL
SELECT 'Articles', COUNT(*) FROM articles
UNION ALL
SELECT 'Categories', COUNT(*) FROM categories
UNION ALL
SELECT 'Tags', COUNT(*) FROM tags
UNION ALL
SELECT 'Article_Categories', COUNT(*) FROM article_categories
UNION ALL
SELECT 'Article_Tags', COUNT(*) FROM article_tags;
