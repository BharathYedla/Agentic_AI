#!/bin/bash

# Quick Test Script for Job Application Email Tracker
# This script runs a series of quick tests to verify your setup

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║     Job Agent - Quick Test Script                            ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠ Virtual environment not activated${NC}"
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source venv/bin/activate
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Virtual environment activated${NC}"
    else
        echo -e "${RED}✗ Failed to activate virtual environment${NC}"
        echo -e "${YELLOW}Please run: source venv/bin/activate${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Virtual environment is active${NC}"
fi

echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}✗ .env file not found${NC}"
    echo -e "${YELLOW}Creating .env from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created${NC}"
        echo -e "${YELLOW}⚠ Please edit .env file with your credentials before continuing${NC}"
        exit 1
    else
        echo -e "${RED}✗ .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

echo ""

# Check Python dependencies
echo -e "${BLUE}Checking dependencies...${NC}"
python -c "import agno" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ agno installed${NC}"
else
    echo -e "${RED}✗ agno not installed${NC}"
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

python -c "import openai" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ openai installed${NC}"
else
    echo -e "${RED}✗ openai not installed${NC}"
fi

python -c "from imap_tools import MailBox" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ imap-tools installed${NC}"
else
    echo -e "${RED}✗ imap-tools not installed${NC}"
fi

echo ""

# Initialize database
echo -e "${BLUE}Initializing database...${NC}"
python main.py --init-db
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database initialized${NC}"
else
    echo -e "${RED}✗ Database initialization failed${NC}"
    exit 1
fi

echo ""

# Run unit tests
echo -e "${BLUE}Running unit tests...${NC}"
echo ""
python test_agents.py
TEST_RESULT=$?

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║     Quick Test Complete                                       ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "  1. Run a one-time scan:    ${BLUE}python main.py --mode once${NC}"
    echo -e "  2. View the dashboard:     ${BLUE}python dashboard.py${NC}"
    echo -e "  3. Start monitoring:       ${BLUE}python main.py --mode scheduled${NC}"
    echo ""
else
    echo -e "${RED}✗ Some tests failed${NC}"
    echo -e "${YELLOW}Please check the error messages above and fix the issues${NC}"
    echo ""
fi

exit $TEST_RESULT
