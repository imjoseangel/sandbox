#!/bin/bash

# PostgreSQL Full-Text Search Setup Script
# This script sets up the database and runs all SQL files in order

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

DB_NAME="psqlvector_db"
DB_USER="postgres"

echo -e "${YELLOW}PostgreSQL Full-Text Search Setup${NC}"
echo "=================================="

# Check if PostgreSQL is running
echo -e "${YELLOW}Checking PostgreSQL connection...${NC}"
if ! pg_isready -h localhost -U $DB_USER > /dev/null 2>&1; then
    echo -e "${RED}Error: PostgreSQL is not running or not accessible${NC}"
    echo "Start PostgreSQL and try again"
    exit 1
fi

# Drop existing database if it exists
echo -e "${YELLOW}Dropping existing database (if exists)...${NC}"
psql -U $DB_USER -h localhost -c "DROP DATABASE IF EXISTS $DB_NAME;" 2>/dev/null || true

# Create new database
echo -e "${YELLOW}Creating database: $DB_NAME${NC}"
psql -U $DB_USER -h localhost -c "CREATE DATABASE $DB_NAME;"

echo -e "${GREEN}Database created successfully${NC}"

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
        echo -e "${YELLOW}Running $file...${NC}"
        psql -U $DB_USER -h localhost -d $DB_NAME -f "$file" > /dev/null 2>&1
        echo -e "${GREEN}✓ $file${NC}"
    else
        echo -e "${RED}✗ $file not found${NC}"
        exit 1
    fi
done

echo -e "${YELLOW}Inserting sample data...${NC}"
psql -U $DB_USER -h localhost -d $DB_NAME -f "07_sample_data.sql" > /dev/null 2>&1
echo -e "${GREEN}✓ Sample data inserted${NC}"

echo ""
echo -e "${GREEN}Setup completed successfully!${NC}"
echo ""
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo ""
echo "To run tests, use:"
echo "  ./test.sh"
echo ""
echo "To connect directly, use:"
echo "  psql -U $DB_USER -h localhost -d $DB_NAME"
