#!/bin/bash
# Lab Control System - Deployment Checklist
# Use this to verify everything is ready for deployment

echo "================================"
echo "Lab Control System - Deployment Checklist"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check file existence
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 MISSING"
        return 1
    fi
}

# Function to check directory existence
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 directory exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 directory MISSING"
        return 1
    fi
}

echo "📁 Checking project structure..."
echo ""

# Check essential files
check_file "run.py"
check_file "create_db.py"
check_file "seed_db.py"
check_file "config.py"
check_file "requirements.txt"
check_file "monitoring_agent.py"
check_file "README.md"
check_file "IMPLEMENTATION_GUIDE.md"
check_file "CHANGES.md"
check_file "SQL_REFERENCE.md"

echo ""
echo "📂 Checking directories..."
check_dir "app"
check_dir "app/templates"
check_dir "venv" || echo -e "${YELLOW}⚠${NC} venv directory not found (create with: python -m venv venv)"

echo ""
echo "📄 Checking template files..."
check_file "app/templates/base.html"
check_file "app/templates/login.html"
check_file "app/templates/dashboard.html"
check_file "app/templates/systems.html"
check_file "app/templates/users.html"

echo ""
echo "🐍 Checking Python dependencies..."
if [ -f "venv/bin/python" ] || [ -f "venv/Scripts/python.exe" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment found"
    if command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1)
        echo -e "${GREEN}✓${NC} Python available: $PYTHON_VERSION"
    fi
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not found"
fi

echo ""
echo "💾 Checking database..."
if [ -f "lab.db" ]; then
    echo -e "${GREEN}✓${NC} lab.db exists"
    # Count tables
    if command -v sqlite3 &> /dev/null; then
        TABLES=$(sqlite3 lab.db ".tables" 2>/dev/null | wc -w)
        echo "  Database has $TABLES tables"
    fi
else
    echo -e "${YELLOW}⚠${NC} lab.db not found (run: python create_db.py)"
fi

echo ""
echo "🔐 Security Checklist..."
echo ""

echo "Checking SECRET_KEY in config.py..."
if grep -q "SECRET_KEY = os.environ.get" config.py; then
    echo -e "${GREEN}✓${NC} Using environment variable for SECRET_KEY"
else
    echo -e "${YELLOW}⚠${NC} Hardcoded SECRET_KEY found (change for production)"
fi

echo ""
echo "Checking password hashing..."
if grep -q "generate_password_hash\|check_password_hash" app/routes.py; then
    echo -e "${GREEN}✓${NC} Password hashing implemented"
else
    echo -e "${YELLOW}⚠${NC} Plaintext passwords detected (implement hashing for production)"
fi

echo ""
echo "Checking for hardcoded credentials..."
if grep -q "password.*==.*\"123\"" app/routes.py; then
    echo -e "${RED}✗${NC} Hardcoded credentials found!"
else
    echo -e "${GREEN}✓${NC} No obvious hardcoded credentials"
fi

echo ""
echo "📋 Functionality Checklist..."
echo ""

# Check for key functions
if grep -q "def log_audit" app/routes.py; then
    echo -e "${GREEN}✓${NC} Audit logging function exists"
else
    echo -e "${RED}✗${NC} Audit logging function missing"
fi

if grep -q "def get_system_health" monitoring_agent.py; then
    echo -e "${GREEN}✓${NC} Monitoring agent has health check function"
else
    echo -e "${RED}✗${NC} Monitoring agent incomplete"
fi

if grep -q "/api/systems" app/routes.py; then
    echo -e "${GREEN}✓${NC} API endpoints implemented"
else
    echo -e "${RED}✗${NC} API endpoints missing"
fi

echo ""
echo "📊 Documentation Checklist..."
echo ""

if [ -s "README.md" ] && grep -q "Features" README.md; then
    LINES=$(wc -l < README.md)
    echo -e "${GREEN}✓${NC} README.md ($LINES lines)"
else
    echo -e "${RED}✗${NC} README.md incomplete"
fi

if [ -s "IMPLEMENTATION_GUIDE.md" ]; then
    LINES=$(wc -l < IMPLEMENTATION_GUIDE.md)
    echo -e "${GREEN}✓${NC} IMPLEMENTATION_GUIDE.md ($LINES lines)"
else
    echo -e "${RED}✗${NC} IMPLEMENTATION_GUIDE.md missing"
fi

if [ -s "CHANGES.md" ]; then
    LINES=$(wc -l < CHANGES.md)
    echo -e "${GREEN}✓${NC} CHANGES.md ($LINES lines)"
else
    echo -e "${RED}✗${NC} CHANGES.md missing"
fi

if [ -s "SQL_REFERENCE.md" ]; then
    echo -e "${GREEN}✓${NC} SQL_REFERENCE.md available"
else
    echo -e "${YELLOW}⚠${NC} SQL_REFERENCE.md missing"
fi

echo ""
echo "================================"
echo "Deployment Ready Assessment"
echo "================================"
echo ""

# Summary
echo "✅ Ready for:"
echo "  • Local development testing"
echo "  • Small lab deployment (5-20 PCs)"
echo ""

echo "⚠️  Before production deployment:"
echo "  1. Implement password hashing"
echo "  2. Change SECRET_KEY"
echo "  3. Enable HTTPS/SSL"
echo "  4. Set DEBUG=False"
echo "  5. Configure backups"
echo "  6. Test monitoring agent deployment"
echo ""

echo "🚀 To get started:"
echo "  1. python seed_db.py     # Create test data"
echo "  2. python run.py         # Start server"
echo "  3. Visit http://localhost:5000"
echo "  4. Login: admin / admin123"
echo ""

echo "📚 For more info:"
echo "  • See IMPLEMENTATION_GUIDE.md for detailed setup"
echo "  • See CHANGES.md for what was modified"
echo "  • See SQL_REFERENCE.md for database queries"
echo ""
