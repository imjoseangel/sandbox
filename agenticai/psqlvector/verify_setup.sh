#!/bin/bash

# Verification script - checks if everything is set up correctly

DB_NAME="psqlvector_db"
DB_USER="postgres"

echo "PostgreSQL Full-Text Search - Setup Verification"
echo "================================================="
echo ""

# Check if database exists
if ! psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "❌ Database '$DB_NAME' not found"
    echo "   Run: ./setup.sh"
    exit 1
fi
echo "✅ Database exists"

# Check row counts
AUTHOR_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM authors;")
ARTICLE_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM articles;")
TAG_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM tags;")

echo "✅ Authors: $AUTHOR_COUNT"
echo "✅ Articles: $ARTICLE_COUNT"
echo "✅ Tags: $TAG_COUNT"

if [ "$ARTICLE_COUNT" -lt 1000 ]; then
    echo "⚠️  Only $ARTICLE_COUNT articles (expected 1,000,000)"
    echo "   Data insertion may still be in progress"
fi

echo ""
echo "Testing Searches:"
echo "---"

# Test 1: Basic search
RESULTS=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM articles WHERE search_vector @@ to_tsquery('english', 'article');")
if [ "$RESULTS" -gt 0 ]; then
    echo "✅ Basic search works ($RESULTS results for 'article')"
else
    echo "❌ Basic search failed"
fi

# Test 2: Ranked search
RESULTS=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM articles WHERE search_vector @@ to_tsquery('english', 'article & content');")
if [ "$RESULTS" -gt 0 ]; then
    echo "✅ AND search works ($RESULTS results for 'article & content')"
else
    echo "❌ AND search failed"
fi

# Test 3: OR search
RESULTS=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM articles WHERE search_vector @@ to_tsquery('english', 'article | title');")
if [ "$RESULTS" -gt 0 ]; then
    echo "✅ OR search works ($RESULTS results for 'article | title')"
else
    echo "❌ OR search failed"
fi

# Test 4: Highlights
RESULTS=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT ts_headline('english', 'This is an article', to_tsquery('english', 'article'), 'StartSel=<mark>, StopSel=</mark>, MaxWords=15, MinWords=1') as test;" 2>/dev/null)
if [[ $RESULTS == *"<mark>"* ]]; then
    echo "✅ Highlights work"
else
    echo "❌ Highlights failed"
fi

# Test 5: Indexes
INDEX_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM pg_indexes WHERE tablename IN ('articles', 'authors') AND indexname LIKE '%search%';")
if [ "$INDEX_COUNT" -ge 2 ]; then
    echo "✅ Indexes created ($INDEX_COUNT search indexes)"
else
    echo "❌ Indexes missing"
fi

echo ""
echo "Quick Commands to Try:"
echo "---"
echo "1. Simple search:"
echo "   psql -U postgres -d psqlvector_db -c \"SELECT id, title FROM articles WHERE search_vector @@ to_tsquery('english', 'article') LIMIT 5;\""
echo ""
echo "2. Ranked results:"
echo "   psql -U postgres -d psqlvector_db -c \"SELECT id, title, ts_rank(search_vector, to_tsquery('english', 'article')) as rank FROM articles WHERE search_vector @@ to_tsquery('english', 'article') ORDER BY rank DESC LIMIT 5;\""
echo ""
echo "3. With highlights:"
echo "   psql -U postgres -d psqlvector_db -c \"SELECT id, ts_headline('english', content, to_tsquery('english', 'article'), 'StartSel=<mark>, StopSel=</mark>, MaxWords=30, MinWords=1') as highlight FROM articles WHERE search_vector @@ to_tsquery('english', 'article') LIMIT 3;\""
echo ""
echo "4. Interactive:"
echo "   psql -U postgres -d psqlvector_db"
echo ""

if [ "$ARTICLE_COUNT" -eq 1000000 ]; then
    echo "✅ Setup Complete and Verified!"
else
    echo "⚠️  Setup is still in progress (data insertion ongoing)"
fi
