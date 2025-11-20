#!/bin/bash

# JobTracker Backend Setup Script
# This script sets up the backend with all required dependencies and API integrations

echo "🚀 JobTracker Backend Setup"
echo "============================"
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "   cd ios_app/backend && ./setup.sh"
    exit 1
fi

# Step 1: Create virtual environment
echo "📦 Step 1: Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 2: Install dependencies
echo "📦 Step 2: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install additional packages for job APIs
echo "📦 Installing job API packages..."
pip install requests serpapi openai PyPDF2 python-docx python-magic beautifulsoup4

# Step 3: Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Step 3: Creating .env file..."
    cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost/jobtracker

# Redis
REDIS_URL=redis://localhost:6379

# JWT
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]

# External API Keys (YOU NEED TO FILL THESE IN)
RAPIDAPI_KEY=6401bda796mshfa6772638c4c2bep1237a4jsn20550c59dbb3
SERPAPI_KEY=your_serpapi_key_here
INDEED_PUBLISHER_ID=your_indeed_publisher_id_here
CLEARBIT_API_KEY=your_clearbit_key_here
OPENAI_API_KEY=your_openai_key_here

# Debug
DEBUG=True
EOF
    echo "✅ Created .env file"
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
else
    echo "✅ .env file already exists"
fi

# Step 4: Create services directory
echo "📁 Step 4: Creating services directory..."
mkdir -p services

# Step 5: Create requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "📝 Creating requirements.txt..."
    cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
redis==5.0.1
celery==5.3.4
requests==2.31.0
serpapi==0.1.5
openai==1.3.7
PyPDF2==3.0.1
python-docx==1.1.0
python-magic==0.4.27
beautifulsoup4==4.12.2
EOF
fi

# Step 6: Display next steps
echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. Edit .env file and add your API keys:"
echo "   - Get RapidAPI key from: https://rapidapi.com/"
echo "   - Get SerpAPI key from: https://serpapi.com/"
echo "   - Get Indeed Publisher ID from: https://www.indeed.com/publisher"
echo "   - Get Clearbit key from: https://clearbit.com/"
echo "   - Get OpenAI key from: https://platform.openai.com/"
echo ""
echo "2. Start PostgreSQL:"
echo "   brew services start postgresql"
echo ""
echo "3. Start Redis:"
echo "   redis-server"
echo ""
echo "4. Run database migrations:"
echo "   alembic upgrade head"
echo ""
echo "5. Start the backend:"
echo "   uvicorn main:app --reload"
echo ""
echo "6. Test the API:"
echo "   open http://localhost:8000/api/docs"
echo ""
echo "🎉 Happy coding!"
