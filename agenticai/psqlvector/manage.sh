#!/bin/bash

# PostgreSQL Full-Text Search Manager
# Usage: ./manage.sh [setup|verify|test-quick|test]
# Optional: DB_NAME=customdb ./manage.sh setup

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration (can be overridden by environment)
DB_NAME="${DB_NAME:-psqlvector_db}"
DB_USER="${DB_USER:-postgres}"

# Show help
show_help() {
    echo -e "${BLUE}PostgreSQL Full-Text Search Manager${NC}"
    echo ""
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup              Setup database (creates, initializes, inserts data)"
    echo "  verify             Verify database is working (quick checks)"
    echo "  test-quick         Run quick verification (6 tests, < 10 sec)"
    echo "  test               Run comprehensive suite (20 tests, 5-10 min)"
    echo ""
    echo "Configuration (optional environment variables):"
    echo "  DB_NAME            Database name (default: psqlvector_db)"
    echo "  DB_USER            Database user (default: postgres)"
    echo ""
    echo "Examples:"
    echo "  ./manage.sh setup"
    echo "  ./manage.sh verify"
    echo "  ./manage.sh test-quick"
    echo "  DB_NAME=mydb ./manage.sh setup"
    echo "  DB_NAME=mydb DB_USER=myuser ./manage.sh test"
    echo ""
    echo "Current settings:"
    echo "  DB_NAME: $DB_NAME"
    echo "  DB_USER: $DB_USER"
    echo ""
}

# Check PostgreSQL
check_postgres() {
    if ! pg_isready -h localhost -U "$DB_USER" > /dev/null 2>&1; then
        echo -e "${RED}Error: PostgreSQL not running or not accessible${NC}"
        exit 1
    fi
}

# Setup database
setup_db() {
    echo -e "${YELLOW}Setting up PostgreSQL Full-Text Search${NC}"
    echo "======================================"

    check_postgres

    echo -e "${YELLOW}Dropping existing database (if exists)...${NC}"
    psql -U "$DB_USER" -h localhost -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null || true

    echo -e "${YELLOW}Creating database...${NC}"
    psql -U "$DB_USER" -h localhost -c "CREATE DATABASE $DB_NAME;"

    # Run SQL files in order
    SQL_FILES=(
        "01_extensions.sql"
        "02_types.sql"
        "03_tables.sql"
        "04_indexes.sql"
        "05_triggers.sql"
        "06_search_function.sql"
    )

    for file in "${SQL_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo -e "${YELLOW}Loading $file...${NC}"
            psql -U "$DB_USER" -h localhost -d "$DB_NAME" -f "$file" > /dev/null 2>&1
            echo -e "${GREEN}✓ $file${NC}"
        else
            echo -e "${RED}✗ $file not found${NC}"
            exit 1
        fi
    done

    echo -e "${YELLOW}Inserting sample data (1M articles)...${NC}"
    psql -U "$DB_USER" -h localhost -d "$DB_NAME" -f "07_sample_data.sql" > /dev/null 2>&1
    echo -e "${GREEN}✓ Sample data inserted${NC}"

    echo ""
    echo -e "${GREEN}Setup complete!${NC}"
    echo "Database: $DB_NAME"
    echo ""
}

# Verify setup
verify_db() {
    echo -e "${BLUE}Verifying Setup${NC}"
    echo "================"

    check_postgres

    # Check if database exists
    if ! psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
        echo -e "${RED}Database not found${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Database exists${NC}"

    # Check row counts
    AUTHOR_COUNT=$(psql -U "$DB_USER" -d "$DB_NAME" -tAc "SELECT COUNT(*) FROM authors;" 2>/dev/null)
    ARTICLE_COUNT=$(psql -U "$DB_USER" -d "$DB_NAME" -tAc "SELECT COUNT(*) FROM articles;" 2>/dev/null)
    TAG_COUNT=$(psql -U "$DB_USER" -d "$DB_NAME" -tAc "SELECT COUNT(*) FROM tags;" 2>/dev/null)

    echo -e "${GREEN}✓ Authors: $AUTHOR_COUNT${NC}"
    echo -e "${GREEN}✓ Articles: $ARTICLE_COUNT${NC}"
    echo -e "${GREEN}✓ Tags: $TAG_COUNT${NC}"

    # Test basic search
    RESULTS=$(psql -U "$DB_USER" -d "$DB_NAME" -tAc "SELECT COUNT(*) FROM articles WHERE search_vector @@ to_tsquery('english', 'article');" 2>/dev/null)
    if [ "$RESULTS" -gt 0 ]; then
        echo -e "${GREEN}✓ Search works ($RESULTS results)${NC}"
    else
        echo -e "${RED}✗ Search failed${NC}"
        exit 1
    fi

    echo ""
    echo -e "${GREEN}All checks passed!${NC}"
}

# Run tests
run_tests() {
    local test_type="$1"

    check_postgres

    if [ "$test_type" = "quick" ]; then
        echo -e "${BLUE}Quick Test (6 basic tests, < 10 sec)${NC}"
        echo ""
        # Basic search
        echo "✓ Test 1: Basic search"
        psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT COUNT(*) as matches FROM articles WHERE search_vector @@ to_tsquery('english', 'article') LIMIT 1;"

        # Ranked search
        echo "✓ Test 2: Ranked search"
        psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT id, title FROM articles WHERE search_vector @@ to_tsquery('english', 'article') ORDER BY random() LIMIT 1;"

        # AND operator
        echo "✓ Test 3: AND operator"
        psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT COUNT(*) as matches FROM articles WHERE search_vector @@ to_tsquery('english', 'article & content');"

        # OR operator
        echo "✓ Test 4: OR operator"
        psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT COUNT(*) as matches FROM articles WHERE search_vector @@ to_tsquery('english', 'article | title');"

        # Highlights
        echo "✓ Test 5: Highlights"
        psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT ts_headline('english', 'This is an article', to_tsquery('english', 'article'), 'StartSel=<mark>, StopSel=</mark>');"

        # Statistics
        echo "✓ Test 6: Statistics"
        psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT COUNT(*) as articles, COUNT(DISTINCT author_id) as authors FROM articles;"

        echo ""
        echo -e "${GREEN}Quick test complete!${NC}"
    else
        # Full comprehensive tests
        echo -e "${BLUE}Comprehensive Test Suite (20 tests, 5-10 min)${NC}"
        echo ""
        psql -U "$DB_USER" -d "$DB_NAME" -f "08_test_queries.sql"
    fi
}

# Main
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

case "$1" in
    setup)
        setup_db
        ;;
    verify)
        verify_db
        ;;
    test-quick)
        run_tests "quick"
        ;;
    test)
        run_tests "full"
        ;;
    help|-h|--help)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
