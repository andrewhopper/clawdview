#!/bin/bash

# Create new project script
# Usage: ./tools/create-project.sh <name> [classification]
# Classification: personal, work, shared, oss, unspecified (default: unspecified)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if name provided
if [ -z "$1" ]; then
  echo -e "${RED}Error: Project name required${NC}"
  echo "Usage: ./tools/create-project.sh <name> [classification]"
  echo "Example: ./tools/create-project.sh my-awesome-idea personal"
  echo ""
  echo "Classifications: personal, work, shared, oss, unspecified (default)"
  exit 1
fi

NAME=$1
CLASSIFICATION=${2:-unspecified}

# Validate classification
case $CLASSIFICATION in
  personal|work|shared|oss|unspecified)
    ;;
  *)
    echo -e "${RED}Error: Invalid classification '${CLASSIFICATION}'${NC}"
    echo "Valid options: personal, work, shared, oss, unspecified"
    exit 1
    ;;
esac

# Generate 5-character random ID
RANDOM_ID=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 5 | head -n 1)

# Create project name with new convention: {name}-{5char}
PROJECT_NAME="${NAME}-${RANDOM_ID}"
PROJECT_DIR="projects/${CLASSIFICATION}/active"
PROJECT_PATH="${PROJECT_DIR}/${PROJECT_NAME}"

# Create directory structure
mkdir -p "${PROJECT_PATH}"/{src,tests,docs,public}
mkdir -p "${PROJECT_PATH}/src"/{components,utils,services}
mkdir -p "${PROJECT_DIR}"

echo -e "${YELLOW}Creating project: ${PROJECT_NAME}${NC}"
echo -e "${BLUE}Location: ${PROJECT_PATH}${NC}"

# Create .project file (JSON format)
cat > "${PROJECT_PATH}/.project" << EOF
{
  "name": "${PROJECT_NAME}",
  "id": "${RANDOM_ID}",
  "description": "${NAME} project",
  "current_phase": "SEED",
  "phase_number": 1,
  "status": "ACTIVE",
  "classification": "${CLASSIFICATION}",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "metadata": {
    "tech_stack": [],
    "tags": []
  },
  "phase_history": [
    {
      "phase": "SEED",
      "phase_number": 1,
      "started": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
      "completed": null
    }
  ]
}
EOF

# Create README.md
cat > "${PROJECT_PATH}/README.md" << EOF
# ${NAME}

## Purpose
[Brief description of what this project explores/demonstrates]

## Status
🟢 Active | Phase 1: SEED

## Tech Stack
- Framework/Library: TBD
- Key dependencies: TBD
- Infrastructure: TBD

## Quick Start
\`\`\`bash
cd ${PROJECT_PATH}
npm install
npm run dev
\`\`\`

## Demo
[Link to live demo or screenshots]

## Key Learnings
- TBD

## Next Steps
- [ ] Define core features
- [ ] Setup development environment
- [ ] Build MVP
- [ ] Test and iterate
EOF

# Create package.json
cat > "${PROJECT_PATH}/package.json" << EOF
{
  "name": "${PROJECT_NAME}",
  "version": "0.1.0",
  "description": "${NAME} project",
  "private": true,
  "scripts": {
    "dev": "echo 'Setup your dev script'",
    "build": "echo 'Setup your build script'",
    "test": "echo 'Setup your test script'"
  },
  "keywords": ["project", "experiment"],
  "author": "",
  "license": "MIT"
}
EOF

# Create .env.example
cat > "${PROJECT_PATH}/.env.example" << EOF
# Environment variables template
# Copy to .env and fill in values

# API Keys
# API_KEY=your_key_here

# Configuration
# NODE_ENV=development
# PORT=3000
EOF

# Create basic .gitignore
cat > "${PROJECT_PATH}/.gitignore" << EOF
# Dependencies
node_modules/
package-lock.json
yarn.lock

# Environment
.env
.env.local

# Build output
dist/
build/
.next/
out/

# Logs
*.log
npm-debug.log*

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
coverage/
.nyc_output/

# Python
__pycache__/
*.pyc
.venv/
venv/
EOF

# Create ARCHITECTURE.md
cat > "${PROJECT_PATH}/docs/ARCHITECTURE.md" << EOF
# ${NAME} - Architecture

## Overview
[High-level description of the system architecture]

## Technical Decisions

### Choice 1: [Technology/Pattern]
- **Decision**: What was decided
- **Rationale**: Why this choice
- **Alternatives Considered**: What else was evaluated
- **Trade-offs**: Pros and cons

## System Design
[Diagrams, component descriptions, data flow]

## Implementation Notes
[Key implementation details, gotchas, patterns used]

## Future Considerations
[What could be improved, scaled, or changed]
EOF

# Create basic index file
cat > "${PROJECT_PATH}/src/index.js" << EOF
// ${NAME}
// Entry point

console.log('${NAME} starting...');

// Your code here
EOF

echo -e "${GREEN}✅ Project created successfully!${NC}"
echo ""
echo "Next steps:"
echo "  1. cd ${PROJECT_PATH}"
echo "  2. Edit README.md with project details"
echo "  3. Setup your tech stack"
echo "  4. Start building!"
echo ""
echo "Files created:"
echo "  - ${PROJECT_PATH}/.project"
echo "  - ${PROJECT_PATH}/README.md"
echo "  - ${PROJECT_PATH}/package.json"
echo "  - ${PROJECT_PATH}/.env.example"
echo "  - ${PROJECT_PATH}/docs/"
echo "  - ${PROJECT_PATH}/src/"
echo ""
echo -e "${YELLOW}Happy building! 🚀${NC}"
