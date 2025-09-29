#!/usr/bin/env bash
set -e  # exit immediately on error

# Python executable (adjust if needed, e.g. python3.11)
PYTHON="python3"

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "⚙️  Creating virtual environment in .venv..."
    $PYTHON -m venv .venv
else
    echo "✅ Virtual environment already exists."
fi

# Activate venv
echo "⚙️  Activating virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

# Upgrade pip
echo "⚙️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "⚙️  Installing packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️  No requirements.txt found, skipping package installation."
fi

echo "🎉 Environment ready. Run 'source .venv/bin/activate' to use it."
