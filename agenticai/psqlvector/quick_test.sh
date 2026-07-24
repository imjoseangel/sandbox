#!/bin/bash

# Quick test script - runs core functionality tests only

DB_NAME="psqlvector_db"
DB_USER="postgres"

echo "Running Quick Tests"
echo "==================="
echo ""

# Test 1: Basic search
echo "Test 1: Basic Full-Text Search"
psql -U $DB_USER -h localhost -d $DB_NAME << EOF
SELECT id, title,
    ts_rank(search_vector, to_tsquery('english', 'article')) as rank
FROM articles
WHERE search_vector @@ to_tsquery('english', 'article')
ORDER BY rank DESC
LIMIT 5;
EOF

echo ""
echo "Test 2: Advanced Search Function"
psql -U $DB_USER -h localhost -d $DB_NAME << EOF
SELECT (results).id, (results).title, (results).author_name, (results).rank
FROM search_articles('article', page_size => 5);
EOF

echo ""
echo "Test 3: Ranked Results with Highlights"
psql -U $DB_USER -h localhost -d $DB_NAME << EOF
SELECT
    (results).id,
    (results).title,
    (results).rank,
    (results).highlight
FROM search_articles('article', page_size => 3);
EOF

echo ""
echo "Test 4: Row Count Statistics"
psql -U $DB_USER -h localhost -d $DB_NAME << EOF
SELECT 'Authors' as table_name, COUNT(*) as count FROM authors
UNION ALL
SELECT 'Articles', COUNT(*) FROM articles
UNION ALL
SELECT 'Tags', COUNT(*) FROM tags;
EOF

echo ""
echo "Quick tests completed!"
