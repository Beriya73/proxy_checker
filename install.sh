#!/bin/bash

# --- proxy_checker Installation Script ---
# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# GitHub repository URL
REPO_URL="https://github.com/Beriya73/proxy_checker.git"
# Directory where the program will be installed
INSTALL_DIR="$HOME/proxy_checker"
# The name for the command-line tool
COMMAND_NAME="proxy_checker"
# The path for the command's symbolic link
SYMLINK_PATH="$HOME/.local/bin/$COMMAND_NAME"

# --- Colors for fancy output ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting proxy_checker installation...${NC}"

# --- Step 1: Check for required dependencies (git, python3, venv) ---
echo -e "\n${YELLOW}Step 1: Checking dependencies...${NC}"

# Check for git
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install it to continue."
    echo "For Debian/Ubuntu: sudo apt install git"
    echo "For Fedora/CentOS: sudo dnf install git"
    exit 1
fi

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install it to continue."
    echo "For Debian/Ubuntu: sudo apt install python3"
    exit 1
fi

# Check for the venv module
if ! python3 -c "import venv" &> /dev/null; then
    echo "Error: The python3-venv module is not found."
    echo "For Debian/Ubuntu: sudo apt install python3-venv"
    echo "For Fedora/CentOS: sudo dnf install python3-virtualenv"
    exit 1
fi
echo "All dependencies are satisfied."


# --- Step 2: Clone the repository ---
echo -e "\n${YELLOW}Step 2: Cloning repository from GitHub...${NC}"
# If the directory already exists, remove it for a clean installation
if [ -d "$INSTALL_DIR" ]; then
    echo "Found an existing installation. Removing $INSTALL_DIR for a clean setup."
    rm -rf "$INSTALL_DIR"
fi
git clone "$REPO_URL" "$INSTALL_DIR"
echo "Repository successfully cloned to $INSTALL_DIR"


# --- Step 3: Set up Python virtual environment and install packages ---
echo -e "\n${YELLOW}Step 3: Setting up Python environment and installing packages...${NC}"
cd "$INSTALL_DIR"
# Create the virtual environment
python3 -m venv venv
# No need to activate the venv in a script; we can call python/pip directly
# Install all required packages
# IMPORTANT: It is highly recommended to add a requirements.txt file to the repo!
echo "Installing dependencies: loguru, aiohttp, aiohttp-socks, pydantic, pyyaml..."
venv/bin/pip install --upgrade pip > /dev/null # Upgrade pip silently
venv/bin/pip install loguru aiohttp aiohttp-socks pydantic pyyaml > /dev/null
echo "Python packages installed successfully."


# --- Step 4: Create the wrapper/launcher script ---
echo -e "\n${YELLOW}Step 4: Creating the executable launcher...${NC}"
# Use a HEREDOC to write the multi-line script content to a file
cat << 'EOF' > "$INSTALL_DIR/$COMMAND_NAME"
#!/bin/bash
# Find the ABSOLUTE PATH to the directory where the REAL script is located,
# even if it was launched via a symbolic link.
SCRIPT_DIR=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")

# Path to the Python interpreter inside the virtual environment
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"

# Path to the main Python script
PYTHON_SCRIPT="$SCRIPT_DIR/proxy_checker.py"

# Check if the Python interpreter exists in the venv
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Python interpreter not found in the virtual environment."
    echo "Please try reinstalling the program by running install.sh again."
    exit 1
fi

# Execute the Python script using the venv's interpreter, passing all arguments
exec "$VENV_PYTHON" "$PYTHON_SCRIPT" "$@"
EOF
echo "Launcher script '$COMMAND_NAME' created."


# --- Step 5: Make the script executable and create a symbolic link ---
echo -e "\n${YELLOW}Step 5: Making the command available system-wide...${NC}"
# Grant execute permissions to our launcher script
chmod +x "$INSTALL_DIR/$COMMAND_NAME"

# Create the ~/.local/bin directory if it doesn't exist
mkdir -p "$HOME/.local/bin"

# Remove any old symlink if it exists
rm -f "$SYMLINK_PATH"

# Create a new symbolic link
ln -s "$INSTALL_DIR/$COMMAND_NAME" "$SYMLINK_PATH"
echo "Command '$COMMAND_NAME' is now installed."


# --- Final Message ---
echo -e "\n${GREEN}======================================"
echo -e " proxy_checker installation complete! ✅"
echo -e "======================================${NC}"
echo "You can now run the program with the command:"
echo -e "  ${YELLOW}proxy_checker [arguments]${NC}"
echo ""
echo "For example:"
echo "  proxy_checker -h"
echo ""
echo -e "${YELLOW}IMPORTANT:${NC} If the command is not found, please restart your terminal or run:"
echo -e "  ${YELLOW}source ~/.profile${NC} or ${YELLOW}source ~/.bashrc${NC}"
echo ""
echo "To update the program, simply run this installation script again."
echo "To uninstall, run the following commands:"
echo "  rm -f $SYMLINK_PATH"
echo "  rm -rf $INSTALL_DIR"