# Get the Python interpreter path from VS Code settings
echo "Getting Python interpreter path from VS Code settings..." | tee -a install.log
PYTHON_PATH=$(jq -r '.["python.pythonPath"]' .vscode/settings.json)

# Create a virtual environment using the specified Python interpreter |
echo "Creating a virtual environment using the specified Python interpreter..." | tee -a install.log
$PYTHON_PATH -m venv venv

# Activate the virtual environment
echo "Activating the virtual environment..." | tee -a install.log
source venv/bin/activate

# Install libraries from requirements.txt
echo "Installing libraries from requirements.txt..." | tee -a install.log
pip install -r requirements.txt