#!/bin/bash
# Run this from the root of your Site-AAALDV repo (senha branch)
# It will fix .gitignore, remove venv/.vscode/uploads from tracking, and commit.

set -e

echo "=== Updating .gitignore ==="
cat > .gitignore << 'GITIGNORE'
# Python
venv/
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# Environment variables
.env
.env.*

# Node
node_modules/

# Database
*.db
*.sqlite3

# Logs
*.log

# OS files
.DS_Store
Thumbs.db

# IDE / Editor
.vscode/
.idea/

# Uploads (managed by backend, not versioned)
backend/uploads/*
!backend/uploads/.gitkeep
GITIGNORE

echo "=== Removing backend/venv/ from tracking ==="
git rm -r --cached backend/venv/

echo "=== Removing .vscode/ from tracking ==="
git rm --cached .vscode/settings.json 2>/dev/null || true

echo "=== Removing backend/uploads (except .gitkeep) from tracking ==="
git rm --cached backend/uploads/*.jpg backend/uploads/*.jpeg backend/uploads/*.png backend/uploads/*.pdf backend/uploads/*.docx 2>/dev/null || true

echo "=== Staging .gitignore ==="
git add .gitignore

echo "=== Committing ==="
git commit -m "Limpa branch: corrige .gitignore e remove arquivos desnecessários do tracking

Remove backend/venv/, .vscode/, e backend/uploads/ do rastreamento git.
Atualiza .gitignore com entradas organizadas para Python, Node, IDE, uploads e OS."

echo "=== Pushing ==="
git push origin senha

echo "=== Done! Branch is clean. ==="
