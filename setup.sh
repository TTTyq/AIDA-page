#!/bin/bash
set -e

echo "=== AIDA Project Setup Script ==="

# Update system packages
sudo apt-get update

# Install basic dependencies
sudo apt-get install -y curl wget build-essential

# Verify Node.js and npm
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# Verify Python 3.9
echo "Python version: $(python3.9 --version)"

# Install pip for Python 3.9 specifically
sudo apt-get install -y python3.9-distutils python3.9-venv
curl https://bootstrap.pypa.io/get-pip.py | python3.9

# Set working directory
cd /mnt/persist/workspace

# Setup root package dependencies
echo "Installing root package dependencies..."
npm install

# Setup backend
echo "Setting up backend..."
cd backend

# Create virtual environment using system python3.9
python3.9 -m venv venv
# Install pip in the venv
curl https://bootstrap.pypa.io/get-pip.py | ./venv/bin/python
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Created .env file from .env.example"
    else
        # Create basic .env file
        cat > .env << EOF
DATABASE_URL=mongodb://localhost:27017/aida
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
        echo "Created basic .env file"
    fi
fi

cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend
npm install
cd ..

# Setup docs
echo "Setting up docs..."
cd docs
npm install
cd ..

# Setup scraper dependencies
echo "Setting up scraper..."
cd scraper
if [ -f requirements.txt ]; then
    ../backend/venv/bin/pip install -r requirements.txt
fi
cd ..

# Create necessary data directories
mkdir -p data/artsy/images
mkdir -p data/artsy/checkpoints
mkdir -p data/logs

echo "=== Setup completed successfully ==="
echo "Backend virtual environment created at backend/venv"
echo "All dependencies installed"
echo "Note: MongoDB is not installed. The backend may fail to connect to database."