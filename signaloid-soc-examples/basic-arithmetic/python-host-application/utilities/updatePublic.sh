#! /bin/bash

set -eu
set -o pipefail

OS_TYPE=$(uname | awk '{print tolower($0)}')
echo "Detected OS is $OS_TYPE."
if [ "$OS_TYPE" = "darwin" ];
then
	GNUSED=gsed
else
	GNUSED=/usr/bin/sed
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PUBLIC_REPO_URL="git@github.com:signaloid/C0-microSD-Hardware.git"
# TARGET=$(mktemp -d -t create-public)
TARGET="../C0-microSD-utilities"
# TARGET="./newRepo"

# Temporarily disable the mechanism for automatic git actions
# external_url=$(git -C "${SCRIPT_DIR}" remote get-url origin | sed 's/-Internal//')

echo "$SCRIPT_DIR"

# Check if the directory exists
if [ -d "$TARGET/.git" ]; then
    echo "Directory $TARGET already exists and is a git repository. Pulling the latest changes from the main branch."
    cd "$TARGET"
    git reset --hard HEAD
    git pull origin main
else
    echo "Directory $TARGET does not exist. Cloning the repository."
    git clone "$PUBLIC_REPO_URL" "$TARGET"
    echo "Repository cloned into $TARGET."
fi

# Remove tracked files (if any).
git -C "${TARGET}" rm -f '*' || true

# Remove untracked files.
git -C "${TARGET}" clean -fdx

# Should be no files left.
ls -a "${TARGET}"

# Copy files
cp    "$SCRIPT_DIR"/LICENSE               "$TARGET"
cp    "$SCRIPT_DIR"/README.md             "$TARGET"
cp    "$SCRIPT_DIR"/.gitignore            "$TARGET"
cp    "$SCRIPT_DIR"/C0_microSD_toolkit.py "$TARGET"
cp -r "$SCRIPT_DIR"/src                   "$TARGET"

# Switch to pulbic repo folder
cd "$TARGET"

# Sanitize README.md file
$GNUSED -i 's/-Internal//' README.md

# Delete lines betwween private flags on README.md
$GNUSED -i -n '1,/START __SIGNALOID_INTERNAL_ONLY__/p;/END __SIGNALOID_INTERNAL_ONLY__/,$p' README.md
$GNUSED -i '/START __SIGNALOID_INTERNAL_ONLY/,/END __SIGNALOID_INTERNAL_ONLY__/d' README.md

# Add all files
git add .
# Remove untracked files
git clean -fdx

printf "\n\nChecking for use of Internal:\n"
if grep -R -e '-Internal'; then
	echo "WARNING: see above for possible use of Internal"
else
	echo "No Internal files found"
fi

echo "DONE"
