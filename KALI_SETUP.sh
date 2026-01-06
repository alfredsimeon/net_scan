#!/bin/bash
# NET_SCAN - Kali Linux Setup Script
# This script will guide you through setup on Kali Linux

set -e  # Exit on any error

echo "=========================================="
echo "NET_SCAN - Kali Linux Installation Guide"
echo "=========================================="
echo ""

# Step 1: Update system
echo "[Step 1/7] Updating Kali system packages..."
sudo apt update
echo "✓ System updated"
echo ""

# Step 2: Install system dependencies
echo "[Step 2/7] Installing required system libraries..."
echo "Installing: python3-dev, libxml2-dev, libxslt1-dev, zlib1g-dev, build-essential"
sudo apt install -y python3-dev libxml2-dev libxslt1-dev zlib1g-dev build-essential
echo "✓ System libraries installed"
echo ""

# Step 3: Verify Python
echo "[Step 3/7] Verifying Python installation..."
python3 --version
echo "✓ Python verified"
echo ""

# Step 4: Delete old venv if it exists
echo "[Step 4/7] Preparing virtual environment..."
if [ -d "venv" ]; then
    echo "Found old venv directory, removing..."
    rm -rf venv
    echo "✓ Old venv removed"
fi
echo "Creating new virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Step 5: Activate venv and upgrade pip
echo "[Step 5/7] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

echo "[Step 5b/7] Upgrading pip..."
python3 -m pip install --upgrade pip setuptools wheel
echo "✓ pip upgraded"
echo ""

# Step 6: Install requirements
echo "[Step 6/7] Installing NET_SCAN dependencies..."
echo "This may take 5-10 minutes..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Step 7: Install Playwright
echo "[Step 7/7] Installing Playwright browsers..."
echo "This may take 5-10 minutes and download ~500MB..."
python -m playwright install
echo "✓ Playwright installed"
echo ""

# Final step: Install NET_SCAN
echo "[Final] Installing NET_SCAN package..."
pip install -e .
echo "✓ NET_SCAN installed"
echo ""

# Verification
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Verifying installation..."
net-scan --version
echo "✓ NET_SCAN is ready to use!"
echo ""
echo "Next steps:"
echo "1. Activate venv each time you use NET_SCAN:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run a test scan:"
echo "   net-scan scan https://example.com --profile quick"
echo ""
echo "3. View all commands:"
echo "   net-scan --help"
echo ""
