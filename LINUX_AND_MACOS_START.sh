#!/bin/bash

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
major_version=$(echo $python_version | cut -d'.' -f1)
minor_version=$(echo $python_version | cut -d'.' -f2)

if [ "$major_version" -lt 3 ] || [ "$major_version" -eq 3 -a "$minor_version" -lt 10 ]; then
    echo "Error: Python 3.10 or higher is required."
    exit 1
fi

echo "Python version: $python_version"

# Install requirements
pip3 install -r requirements.txt

# Run main.py
python3 start_window.py