#!/bin/bash
# Script to run API tests

# Ensure we're in the project root
cd "$(dirname "$0")/.."

echo "Running API tests..."
python3 cli/explorer_cli.py test
