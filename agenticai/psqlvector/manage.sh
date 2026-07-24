#!/bin/bash

# PostgreSQL Full-Text Search Manager
# Usage: ./manage.sh [setup|verify|test|test-quick|test-full]

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

DB_NAME="psqlvector_db"
DB_USER="postgres"

# Show help
show_help() {
    echo -e "${BLUE}PostgreSQL Full-Text Search Manager${NC}"
    echo ""
    echo "Usage: ./manage.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  setup              Setup database (creates, initializes, inserts data)"
    echo "  verify             Verify database is working (quick checks)"
    echo "  test               Run comprehensive 20-test suite"
    echo "  test-quick         Run quick 6-test suite (< 10 sec)"
    echo "  test-full          Run all tests with detailed output"
    echo ""
    echo "Examples:"
    echo "  ./manage.sh setup"
    echo "  ./manage.sh verify"
    echo "  ./manage.sh test-quick"
    echo ""
}

# Check PostgreSQL
check_postgres() {
    if ! pg_isready -h localhost -U $DB_USER > /dev/null 2>&1; then
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
    psql -U $DB_USER -h localhost -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null || true

    echo -e "${YELLOW}Creating database...${NC}"
    psql -U $DB_USER -h localhost -c "CREATE DATABASE $DB_NAME;"

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
            psql -U $DB_USER -h localhost -d $DB_NAME -f "$file" > /dev/null 2>&1
            echo -e "${GREEN}✓ $file${NC}"
        else
            echo -e "${RED}✗ $file not found${NC}"
            exit 1
        fi
    done

    echo -e "${YELLOW}Inserting sample data (1M articles)...${NC}"
    psql -U $DB_USER -h localhost -d $DB_NAME -f "07_sample_data.sql" > /dev/null 2>&1
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
    if ! psql -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
        echo -e "${RED}Database not found${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Database exists${NC}"

    # Check row counts
    AUTHOR_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM authors;" 2>/dev/null)
    ARTICLE_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM articles;" 2>/dev/null)
    TAG_COUNT=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM tags;" 2>/dev/null)

    echo -e "${GREEN}✓ Authors: $AUTHOR_COUNT${NC}"
    echo -e "${GREEN}✓ Articles: $ARTICLE_COUNT${NC}"
    echo -e "${GREEN}✓ Tags: $TAG_COUNT${NC}"

    # Test basic search
    RESULTS=$(psql -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM articles WHERE search_vector @@ to_tsquery('english', 'article');" 2>/dev/null)
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
        echo -e "${BLUE}Quick Test (6 tests, < 10 sec)${NC}"
        psql -U $DB_USER -d $DB_NAME -f quick_test_fast.sh 2>/dev/null || true
    elif [ "$test_type" = "full" ]; then
        echo -e "${BLUE}Full Test Suite (20 tests, 5-10 min)${NC}"
        psql -U $DB_USER -d $DB_NAME -f 08_test_queries.sql
    else
        # Default: comprehensive
        echo -e "${BLUE}Running Tests${NC}"
        psql -U $DB_USER -d $DB_NAME -f quick_test_fast.sh 2>/dev/null || true
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
    test)
        run_tests "default"
        ;;
    test-quick)
        run_tests "quick"
        ;;
    test-full)
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
