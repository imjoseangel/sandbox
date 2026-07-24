# Tested & Working Commands

All commands below have been verified to work with the database setup.

## Quick Test Commands

### 1. Simple Search

```bash
psql -U postgres -d psqlvector_db -c "SELECT id, title FROM articles WHERE search_vector @@ to_tsquery('english', 'article') LIMIT 5;"
```

### 2. Ranked Search

```bash
psql -U postgres -d psqlvector_db -c "SELECT id, title, ts_rank(search_vector, to_tsquery('english', 'article')) as rank FROM articles WHERE search_vector @@ to_tsquery('english', 'article') ORDER BY rank DESC LIMIT 5;"
```

### 3. Highlights

```bash
psql -U postgres -d psqlvector_db -c "SELECT id, ts_headline('english', content, to_tsquery('english', 'article'), 'StartSel=<mark>, StopSel=</mark>, MaxWords=15, MinWords=1') as highlight FROM articles WHERE search_vector @@ to_tsquery('english', 'article') LIMIT 3;"
```

### 4. Statistics

```bash
psql -U postgres -d psqlvector_db -c "SELECT COUNT(*) as total_articles, COUNT(DISTINCT author_id) as unique_authors FROM articles;"
```

### 5. Search with OR operator

```bash
psql -U postgres -d psqlvector_db -c "SELECT COUNT(*) as matches FROM articles WHERE search_vector @@ to_tsquery('english', 'article | content');"
```

### 6. Search with AND operator

```bash
psql -U postgres -d psqlvector_db -c "SELECT COUNT(*) as matches FROM articles WHERE search_vector @@ to_tsquery('english', 'article & content');"
```

### 7. Search with NOT operator

```bash
psql -U postgres -d psqlvector_db -c "SELECT COUNT(*) as matches FROM articles WHERE search_vector @@ to_tsquery('english', 'article & !title');"
```

## Important Keywords in Data

The sample data contains these searchable keywords:

- `article` - In all article titles
- `title` - In all article titles
- `subtitle` - In all article subtitles
- `content` - In all article content
- `lorem` - In content (from Lorem ipsum)
- `ipsum` - In content (from Lorem ipsum)
- `author` - In author bios and names

## Example Multi-Step Test Session

```bash
# Connect to database
psql -U postgres -d psqlvector_db

# Inside psql:

-- Check data
SELECT COUNT(*) FROM articles;
SELECT COUNT(*) FROM authors;
SELECT COUNT(*) FROM tags;

-- Simple search
SELECT id, title FROM articles WHERE search_vector @@ to_tsquery('english', 'article') LIMIT 5;

-- Ranked search
SELECT id, title, ts_rank(search_vector, to_tsquery('english', 'article')) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'article')
ORDER BY rank DESC
LIMIT 5;

-- With highlights
SELECT id, title,
  ts_headline('english', content, to_tsquery('english', 'article'),
    'StartSel=<mark>, StopSel=</mark>, MaxWords=30, MinWords=1') as snippet
FROM articles
WHERE search_vector @@ to_tsquery('english', 'article')
LIMIT 3;

-- Combined search
SELECT COUNT(*) as total_matches FROM articles
WHERE search_vector @@ to_tsquery('english', 'article & content');

-- Or search
SELECT COUNT(*) as total_matches FROM articles
WHERE search_vector @@ to_tsquery('english', 'article | title');

-- Negation search
SELECT COUNT(*) as total_matches FROM articles
WHERE search_vector @@ to_tsquery('english', 'article & !title');

-- Check author stats
SELECT a.name, COUNT(ar.id) as article_count
FROM authors a
LEFT JOIN articles ar ON a.id = ar.author_id
GROUP BY a.id, a.name
ORDER BY article_count DESC
LIMIT 10;

-- Exit
\q
```

## Batch Test Command

Run all at once:

```bash
psql -U postgres -d psqlvector_db << 'EOF'
SELECT 'Testing Full-Text Search' as test;
SELECT COUNT(*) as total_articles FROM articles;
SELECT id, title FROM articles WHERE search_vector @@ to_tsquery('english', 'article') LIMIT 3;
SELECT id, title, ts_rank(search_vector, to_tsquery('english', 'article')) as rank FROM articles WHERE search_vector @@ to_tsquery('english', 'article') ORDER BY rank DESC LIMIT 3;
SELECT COUNT(*) as matches_both FROM articles WHERE search_vector @@ to_tsquery('english', 'article & content');
SELECT COUNT(*) as matches_either FROM articles WHERE search_vector @@ to_tsquery('english', 'article | lorem');
EOF
```

## Performance Notes

- **1M articles**: Most queries < 1 second with GIN indexes
- **Search function** (`search_articles()`): Takes 5-30s for complex queries with 1M articles (normal, it's ranking all results)
- **Pagination**: Use `page_size => 20` and `page_number => 1,2,3...` to iterate results
- **Highlights**: Include `MinWords=1` to allow very short snippets

## Available Keywords for Testing

Try these in your own queries:

```sql
-- Single word
to_tsquery('english', 'article')

-- Multiple words (all must match)
to_tsquery('english', 'article & content')

-- Any word (at least one must match)
to_tsquery('english', 'article | title')

-- Exclude word
to_tsquery('english', 'article & !subtitle')

-- Prefix matching
to_tsquery('english', 'art:*')  -- matches 'article', 'artist', etc.

-- Combined
to_tsquery('english', '(article | content) & lorem')
```
