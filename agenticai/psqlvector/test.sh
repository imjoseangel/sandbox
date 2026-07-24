#!/bin/bash

# PostgreSQL Full-Text Search Test Script
# Runs all test queries

DB_NAME="psqlvector_db"
DB_USER="postgres"

echo "Running PostgreSQL Full-Text Search Tests"
echo "=========================================="
echo ""

# Check if database exists
if ! psql -U $DB_USER -h localhost -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Error: Database '$DB_NAME' not found"
    echo "Run ./setup.sh first"
    exit 1
fi

# Run test queries
psql -U $DB_USER -h localhost -d $DB_NAME -f "08_test_queries.sql"

echo ""
echo "Tests completed!"
