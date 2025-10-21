#!/bin/bash
#
# Ving (Visual Ping) Installation Script
# Installs ving as a standalone executable to /usr/local/bin
#

set -e  # Exit on error

echo "🚀 Ving Installation Script"
echo "============================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed." >&2
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

# Check Python version (3.7+)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.7"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"; then
    echo "❌ Error: Python ${PYTHON_VERSION} is not supported." >&2
    echo "Please install Python ${REQUIRED_VERSION} or higher."
    exit 1
fi

echo "✓ Found Python ${PYTHON_VERSION}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q pyinstaller

# Build executable
echo "🔨 Building executable..."
pyinstaller --onefile --name ving ving.py

# Install to system
echo "📍 Installing to /usr/local/bin..."
chmod +x dist/ving

# Check if we need sudo
if [ -w /usr/local/bin ]; then
    mv dist/ving /usr/local/bin/
else
    echo "   (Requires sudo for /usr/local/bin)"
    sudo mv dist/ving /usr/local/bin/
fi

# Deactivate virtual environment
deactivate

echo ""
echo "✅ Installation complete!"
echo ""
echo "Usage: ving [host]"
echo "Example: sudo ving google.com"
echo ""
echo "Note: ICMP packets require root privileges (sudo)"