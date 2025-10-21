#!/bin/bash
#
# Ving (Visual Ping) Uninstallation Script
# Removes ving from /usr/local/bin
#

echo "🗑️  Ving Uninstallation Script"
echo "=============================="
echo ""

# Check if ving is installed
if [ ! -f "/usr/local/bin/ving" ]; then
    echo "❌ ving is not installed in /usr/local/bin"
    exit 1
fi

echo "Removing ving from /usr/local/bin..."

# Check if we need sudo
if [ -w /usr/local/bin ]; then
    rm /usr/local/bin/ving
else
    sudo rm /usr/local/bin/ving
fi

echo ""
echo "✅ Uninstallation complete!"
echo ""
echo "To reinstall, run: ./scripts/install.sh"

