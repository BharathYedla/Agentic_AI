#!/bin/bash

# Quick Start Script for Job Application Email Tracker
# This script helps you set up and run the tracker quickly

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║     Job Application Email Tracker - Quick Start              ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version found"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️  IMPORTANT: Please edit .env file with your credentials!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "You need to set:"
    echo "  1. OPENAI_API_KEY - Your OpenAI API key"
    echo "  2. EMAIL_ADDRESS - Your email address"
    echo "  3. EMAIL_PASSWORD - Your email app password"
    echo ""
    echo "For Gmail users:"
    echo "  - Enable 2FA: https://myaccount.google.com/security"
    echo "  - Generate App Password: https://myaccount.google.com/apppasswords"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
else
    echo "✓ .env file found"
fi
echo ""

# Validate configuration
echo "Validating configuration..."
if python3 -c "from utils.config import validate_config; exit(0 if validate_config() else 1)" 2>/dev/null; then
    echo "✓ Configuration is valid"
else
    echo "✗ Configuration validation failed!"
    echo "Please check your .env file and ensure all required fields are set."
    exit 1
fi
echo ""

# Initialize database
echo "Initializing database..."
python3 main.py --init-db
echo "✓ Database initialized"
echo ""

# Show menu
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete! 🎉                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "What would you like to do?"
echo ""
echo "1) Run one-time scan (last 7 days)"
echo "2) Run one-time scan (last 30 days)"
echo "3) Start continuous monitoring (checks every hour)"
echo "4) Start scheduled monitoring (checks every 30 minutes)"
echo "5) Launch dashboard"
echo "6) Exit"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "Running one-time scan (last 7 days)..."
        python3 main.py --mode once --days 7
        ;;
    2)
        echo ""
        echo "Running one-time scan (last 30 days)..."
        python3 main.py --mode once --days 30
        ;;
    3)
        echo ""
        echo "Starting continuous monitoring (Ctrl+C to stop)..."
        python3 main.py --mode continuous --interval 3600
        ;;
    4)
        echo ""
        echo "Starting scheduled monitoring (Ctrl+C to stop)..."
        python3 main.py --mode scheduled --interval 1800
        ;;
    5)
        echo ""
        echo "Launching dashboard..."
        echo "Dashboard will open in your browser at http://localhost:8501"
        streamlit run dashboard.py
        ;;
    6)
        echo ""
        echo "Goodbye! 👋"
        exit 0
        ;;
    *)
        echo ""
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "To view your data, run: streamlit run dashboard.py"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
