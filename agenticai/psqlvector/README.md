# PostgreSQL Full-Text Search Setup & Tests

Complete setup for PostgreSQL Full-Text Search implementation with 1M test articles.

## Quick Start

### 1. Ensure PostgreSQL is Running
```bash
pg_isready
```

### 2. Run Setup
```bash
cd psqlvector
./manage.sh setup
```

This will:
- Create database `psqlvector_db`
- Create extensions (pg_trgm, unaccent)
- Create tables (authors, articles, categories, tags, junctions)
- Create indexes (GIN indexes for full-text search)
- Create search function with advanced filtering
- Insert **1,000,000 sample articles** and 1,000 authors (⚠️ Warning: takes 5-15 minutes depending on hardware)

### 3. Verify & Test

**Verify setup works:**
```bash
./manage.sh verify
```

**Quick tests (6 tests, ~10 seconds):**
```bash
./manage.sh test-quick
```

**Full test suite (20 tests, 5-10 minutes):**
```bash
./manage.sh test
```

**Help:**
```bash
./manage.sh help
```

## Files Overview

### SQL Files (run in order by setup.sh)
- `01_extensions.sql` - Enable pg_trgm and unaccent extensions
- `02_types.sql` - Create custom types (article_status, search_result)
- `03_tables.sql` - Create all tables with tsvector columns
- `04_indexes.sql` - Create GIN indexes for performance
- `05_triggers.sql` - Auto-update timestamps
- `06_search_function.sql` - Advanced search function with filters
- `07_sample_data.sql` - Insert test data
- `08_test_queries.sql` - 20 comprehensive test queries

### Scripts
- `manage.sh` - All-in-one manager with commands: setup, verify, test, test-quick

## Test Categories

The `08_test_queries.sql` includes:

1. **Basic Full-Text Search** (Tests 1-6)
   - tsvector representation
   - tsquery representation
   - Keyword, OR, AND, negation searches

2. **Ranking & Relevance** (Tests 7-8)
   - ts_rank() for relevance scoring
   - ts_headline() for highlighting results

3. **Advanced Search Function** (Tests 9-14)
   - Basic and multi-keyword search
   - Tag filtering
   - Date range filtering
   - Category filtering
   - Pagination

4. **Performance Analysis** (Tests 15-16)
   - EXPLAIN ANALYZE for query plans
   - Complex query analysis

5. **Fuzzy Matching** (Test 17)
   - Trigram similarity search

6. **Statistics** (Tests 18-20)
   - Article and author statistics
   - Tag usage statistics

## Direct Database Access

Connect to the database:
```bash
psql -U postgres -h localhost -d psqlvector_db
```

Run individual SQL files:
```bash
psql -U postgres -h localhost -d psqlvector_db -f 08_test_queries.sql
```

Run a single query:
```bash
psql -U postgres -h localhost -d psqlvector_db -c "SELECT * FROM search_articles('postgresql', page_size => 10);"
```

## Sample Queries

### Simple Search
```sql
SELECT * FROM search_articles('postgresql', page_size => 10);
```

### Search with Filters
```sql
SELECT * FROM search_articles(
    'database',
    tag_filter => ARRAY['postgresql', 'database'],
    min_date => CURRENT_TIMESTAMP - INTERVAL '1 year',
    page_size => 20
);
```

### Direct tsvector Search
```sql
SELECT id, title, 
    ts_rank(search_vector, to_tsquery('english', 'postgresql')) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'postgresql')
ORDER BY rank DESC
LIMIT 10;
```

### Search with Highlights
```sql
SELECT 
    id,
    title,
    ts_headline('english', content, to_tsquery('english', 'search'),
        'StartSel=<mark>, StopSel=</mark>, MaxWords=50') as snippet
FROM articles
WHERE search_vector @@ to_tsquery('english', 'search')
LIMIT 5;
```

## Key Concepts

**tsvector** - Preprocessed document for efficient indexing
- Format: `'lexeme':positions`
- Example: `'article':1 'postgresql':3 'search':5`

**tsquery** - Search query with operators
- AND: `query1 & query2`
- OR: `query1 | query2`
- NOT: `!query`
- Prefix: `query:*` (matches any word starting with query)

**ts_rank()** - Relevance scoring (0.0 to 1.0)

**ts_headline()** - Extract and highlight matching passages

**GIN Index** - Generalized Inverted Index for fast full-text search

## Performance Notes

- **1,000,000 articles** with full-text search (matches the article example)
- GIN indexes for O(log N) search performance
- Recent articles boost: 1.5x for last 7 days, 1.2x for last 30 days
- Supports filtering by tags, categories, dates, and authors
- Pagination support built-in
- Search function returns `search_result` composite type with: id, title, subtitle, author_name, published_at, rank, highlight

## Dataset Warning

**The setup inserts 1,000,000 articles.** This:
- Takes 5-15 minutes depending on system resources
- Requires ~500MB+ disk space
- Creates a realistic benchmark for performance testing

If you want faster setup for testing queries only, edit `07_sample_data.sql` and change:
```sql
FROM generate_series(1, 1000000) i;
```
to a smaller number like `100000` or `10000`.

## Cleanup

Drop the database:
```bash
psql -U postgres -h localhost -c "DROP DATABASE psqlvector_db;"
```

## Troubleshooting

### "psql: FATAL: Ident authentication failed"
Add `-U postgres` to specify user:
```bash
psql -U postgres -h localhost -d psqlvector_db
```

### "could not connect to server: Connection refused"
PostgreSQL is not running. Start it:
```bash
# macOS with Homebrew
brew services start postgresql

# Linux with systemd
sudo systemctl start postgresql
```

### "database "psqlvector_db" does not exist"
Run setup first:
```bash
./manage.sh setup
```

## References

- PostgreSQL FTS docs: https://www.postgresql.org/docs/current/textsearch.html
- PostgreSQL trigram docs: https://www.postgresql.org/docs/current/pgtrgm.html
