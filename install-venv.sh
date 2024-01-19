# Get the Python interpreter path from VS Code settings
echo "Getting Python interpreter path from VS Code settings..."
PYTHON_PATH=$(jq -r '.["python.pythonPath"]' .vscode/settings.json)

# Create a virtual environment using the specified Python interpreter
echo "Creating a virtual environment using the specified Python interpreter..."
$PYTHON_PATH -m venv venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install libraries from requirements.txt
echo "Installing libraries from requirements.txt..."
pip install -r requirements.txt