#!/bin/bash
# NET_SCAN - Kali Linux Setup Script for Python 3.13
# This script will guide you through setup on Kali Linux

set -e  # Exit on any error

echo "=========================================="
echo "NET_SCAN - Kali Linux Installation Guide"
echo "Python 3.13 Compatible"
echo "=========================================="
echo ""

# Step 1: Update system
echo "[Step 1/9] Updating Kali system packages..."
sudo apt update
echo "✓ System updated"
echo ""

# Step 2: Install system dependencies + build tools
echo "[Step 2/9] Installing required system libraries and build tools..."
echo "Installing: python3-dev, libxml2-dev, libxslt1-dev, zlib1g-dev, gcc, g++, and more..."
sudo apt install -y \
  python3-dev \
  libxml2-dev \
  libxslt1-dev \
  zlib1g-dev \
  build-essential \
  gcc \
  g++ \
  libssl-dev \
  libffi-dev \
  curl
echo "✓ System libraries and build tools installed"
echo ""

# Step 3: Install Rust (needed for pydantic-core)
echo "[Step 3/9] Installing Rust toolchain..."
if ! command -v rustup &> /dev/null; then
    echo "Rust not found. Installing rustup..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
    echo "✓ Rust installed"
else
    echo "✓ Rust already installed"
fi
echo ""

# Step 4: Verify Python
echo "[Step 4/9] Verifying Python installation..."
python3 --version
echo "✓ Python verified"
echo ""

# Step 5: Delete old venv if it exists
echo "[Step 5/9] Preparing virtual environment..."
if [ -d "venv" ]; then
    echo "Found old venv directory, removing..."
    rm -rf venv
    echo "✓ Old venv removed"
fi
echo "Creating new virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Step 6: Activate venv and upgrade pip
echo "[Step 6/9] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

echo "[Step 6b/9] Upgrading pip, setuptools, and wheel..."
python3 -m pip install --upgrade pip setuptools wheel
echo "✓ pip upgraded"
echo ""

# Step 7: Install requirements
echo "[Step 7/9] Installing NET_SCAN dependencies..."
echo "This may take 10-15 minutes due to package compilation..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Step 8: Install Playwright
echo "[Step 8/9] Installing Playwright browsers..."
echo "This may take 5-10 minutes and download ~500MB..."
python -m playwright install
echo "✓ Playwright installed"
echo ""

# Final step: Install NET_SCAN
echo "[Step 9/9] Installing NET_SCAN package..."
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
