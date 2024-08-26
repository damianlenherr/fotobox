#!/bin/bash

# Step 1: Create a virtual environment named '.venv'
echo "Creating a virtual environment named '.venv'..."
python3 -m venv .venv

# Step 2: Activate the virtual environment
echo "Activating the virtual environment..."
source .venv/bin/activate

# Step 3: Upgrade pip to the latest version
echo "Upgrading pip to the latest version..."
pip install --upgrade pip

# Step 4: Install the necessary packages
echo "Installing the necessary packages: matplotlib, numpy, pillow..."
pip install matplotlib numpy pillow pillow_lut

# Step 5: Inform the user that the setup is complete
echo "Setup complete. Virtual environment created and packages installed."
