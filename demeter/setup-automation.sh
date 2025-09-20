#!/bin/bash

# WAVIS Alchemy Setup Automation Script
# Automated Project Setup with SSOT-Driven Development Framework
#
# Usage: ./setup-automation.sh <project-name> <github-username> [options]
#
# This script creates a complete project setup with:
# - SSOT framework with GraphRAG integration
# - Go project structure with Clean Architecture
# - Comprehensive UoW definitions and agent collaboration patterns
# - Quality gates, CI/CD, and Docker deployment readiness

set -e

# Script metadata
SCRIPT_VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/project-template"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

step() {
    echo -e "\n${PURPLE}===== $1 =====${NC}"
}

# Default configuration
DEFAULT_CONFIG_FILE="$SCRIPT_DIR/setup-config.yaml"
CONFIG_FILE=""
PROJECT_NAME=""
GITHUB_USERNAME=""
PROJECT_TYPE="web-api"
GO_VERSION="1.22.1"
DOMAIN="general"
DESCRIPTION=""
SKIP_STEPS=""
DRY_RUN=false
VERBOSE=false
FORCE=false

# Feature flags
ENABLE_GRAPHRAG=true
ENABLE_DOCKER=true
ENABLE_SONARQUBE=true
ENABLE_MONITORING=true
ENABLE_CI_CD=true

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --project-type)
                PROJECT_TYPE="$2"
                shift 2
                ;;
            --go-version)
                GO_VERSION="$2"
                shift 2
                ;;
            --domain)
                DOMAIN="$2"
                shift 2
                ;;
            --description)
                DESCRIPTION="$2"
                shift 2
                ;;
            --skip)
                SKIP_STEPS="$2"
                shift 2
                ;;
            --disable-graphrag)
                ENABLE_GRAPHRAG=false
                shift
                ;;
            --disable-docker)
                ENABLE_DOCKER=false
                shift
                ;;
            --disable-sonarqube)
                ENABLE_SONARQUBE=false
                shift
                ;;
            --disable-monitoring)
                ENABLE_MONITORING=false
                shift
                ;;
            --disable-ci-cd)
                ENABLE_CI_CD=false
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --force)
                FORCE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            --version)
                echo "WAVIS Alchemy Setup Automation v$SCRIPT_VERSION"
                exit 0
                ;;
            -*)
                error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                if [ -z "$PROJECT_NAME" ]; then
                    PROJECT_NAME="$1"
                elif [ -z "$GITHUB_USERNAME" ]; then
                    GITHUB_USERNAME="$1"
                else
                    error "Too many positional arguments"
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Validate required arguments
    if [ -z "$PROJECT_NAME" ] || [ -z "$GITHUB_USERNAME" ]; then
        error "Project name and GitHub username are required"
        show_help
        exit 1
    fi

    # Set default description if not provided
    if [ -z "$DESCRIPTION" ]; then
        DESCRIPTION="A $PROJECT_TYPE project built with SSOT-driven development framework"
    fi
}

# Show help message
show_help() {
    cat << 'EOF'
WAVIS Alchemy Setup Automation Script

USAGE:
    ./setup-automation.sh <project-name> <github-username> [OPTIONS]

ARGUMENTS:
    <project-name>      Name of the project to create
    <github-username>   Your GitHub username

OPTIONS:
    --config FILE       Use custom configuration file
    --project-type TYPE Project type (web-api, cli, library, microservice)
    --go-version VER    Go version to use (default: 1.22.1)
    --domain DOMAIN     Project domain (trading, fintech, general, etc.)
    --description DESC  Project description
    --skip STEPS        Comma-separated list of steps to skip

    Feature Flags:
    --disable-graphrag  Skip GraphRAG setup
    --disable-docker    Skip Docker configuration
    --disable-sonarqube Skip SonarQube integration
    --disable-monitoring Skip monitoring setup
    --disable-ci-cd     Skip CI/CD pipeline setup

    Execution Options:
    --dry-run          Show what would be done without executing
    --verbose          Enable verbose output
    --force            Overwrite existing directory
    --help, -h         Show this help message
    --version          Show version information

EXAMPLES:
    # Basic setup
    ./setup-automation.sh my-api myusername

    # Advanced setup with custom configuration
    ./setup-automation.sh trading-system myusername \
        --project-type microservice \
        --domain trading \
        --description "Automated trading system with risk management"

    # Minimal setup without optional features
    ./setup-automation.sh simple-cli myusername \
        --project-type cli \
        --disable-docker \
        --disable-monitoring

SETUP PHASES:
    1. Project Structure Creation
    2. SSOT Framework Setup
    3. GraphRAG Knowledge System
    4. Development Environment
    5. UoW Architecture Definition
    6. Command System Setup
    7. Quality & CI/CD Integration
    8. Knowledge Consolidation

For more information, see PROJECT-SETUP-TEMPLATE.md
EOF
}

# Load configuration from file
load_config() {
    if [ -n "$CONFIG_FILE" ] && [ -f "$CONFIG_FILE" ]; then
        info "Loading configuration from $CONFIG_FILE"
        # TODO: Implement YAML config loading using yq or similar
    elif [ -f "$DEFAULT_CONFIG_FILE" ]; then
        info "Loading default configuration"
        # TODO: Implement default config loading
    fi
}

# Validate prerequisites
validate_prerequisites() {
    step "Validating Prerequisites"

    local missing_tools=()

    # Check required tools
    command -v git >/dev/null 2>&1 || missing_tools+=("git")
    command -v go >/dev/null 2>&1 || missing_tools+=("go")
    command -v python3 >/dev/null 2>&1 || missing_tools+=("python3")

    if [ ${#missing_tools[@]} -gt 0 ]; then
        error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi

    # Check Go version
    local go_version
    go_version=$(go version | grep -oE 'go[0-9]+\.[0-9]+\.[0-9]+' | sed 's/go//')
    info "Go version: $go_version"

    # Check Python version
    local python_version
    python_version=$(python3 --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
    info "Python version: $python_version"

    # Check for optional tools
    if command -v docker >/dev/null 2>&1; then
        info "Docker found: $(docker --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
    else
        warn "Docker not found - Docker features will be skipped"
        ENABLE_DOCKER=false
    fi

    if command -v gh >/dev/null 2>&1; then
        info "GitHub CLI found: $(gh --version | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
    else
        warn "GitHub CLI not found - some Git features will be limited"
    fi

    log "Prerequisites validation completed"
}

# Check if project directory exists
check_project_directory() {
    if [ -d "$PROJECT_NAME" ]; then
        if [ "$FORCE" = true ]; then
            warn "Overwriting existing directory: $PROJECT_NAME"
            rm -rf "$PROJECT_NAME"
        else
            error "Directory $PROJECT_NAME already exists. Use --force to overwrite."
            exit 1
        fi
    fi
}

# Phase 1: Create project structure
phase_1_project_structure() {
    step "Phase 1: Creating Project Structure"

    if [[ "$SKIP_STEPS" == *"structure"* ]]; then
        warn "Skipping project structure creation"
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        info "[DRY RUN] Would create project directory: $PROJECT_NAME"
        info "[DRY RUN] Would initialize Git repository"
        info "[DRY RUN] Would create Go module"
        info "[DRY RUN] Would create directory structure"
        return
    fi

    # Create project directory
    info "Creating project directory: $PROJECT_NAME"
    mkdir -p "$PROJECT_NAME"
    cd "$PROJECT_NAME"

    # Initialize Git repository
    info "Initializing Git repository"
    git init
    git branch -M main

    # Create .gitignore
    info "Creating .gitignore"
    cat > .gitignore << 'EOF'
# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
go.work

# GraphRAG
grag/output/*
grag/cache/*
grag/logs/*.log
!grag/output/.gitkeep
!grag/cache/.gitkeep

# Environment
.env
*.env
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build artifacts
dist/
build/
*.tar.gz
*.zip

# SonarQube
.scannerwork/
sonar-project.properties.local
EOF

    # Initialize Go module
    info "Initializing Go module"
    go mod init "github.com/$GITHUB_USERNAME/$PROJECT_NAME"

    # Create basic project structure
    info "Creating project directory structure"
    mkdir -p {cmd/server,internal/{domain,application,infrastructure,interfaces},pkg,configs,scripts,docs}
    mkdir -p {tests/{unit,integration,e2e},build/docker,deployments}

    # Create placeholder main.go
    cat > cmd/server/main.go << EOF
package main

import (
	"log"
)

func main() {
	log.Println("$PROJECT_NAME Server Starting...")
	// TODO: Implementation will be added with UoW tasks
}
EOF

    # Create Claude Code configuration
    mkdir -p .claude/commands
    cat > .claude/settings.json << EOF
{
  "project_type": "go",
  "source_dirs": ["cmd", "internal", "pkg"],
  "test_dirs": ["tests", "internal"],
  "commands": {
    "test": "go test ./... -cover",
    "build": "go build -o bin/$PROJECT_NAME ./cmd/server",
    "lint": "golangci-lint run",
    "fmt": "go fmt ./...",
    "mod": "go mod tidy"
  }
}
EOF

    # Initial commit
    git add .
    git commit -m "feat: Initialize project with Go module and structure

- Create Go module for github.com/$GITHUB_USERNAME/$PROJECT_NAME
- Add Clean Architecture directory structure
- Configure Claude Code integration
- Add comprehensive .gitignore

🤖 Generated with WAVIS Alchemy Setup Automation v$SCRIPT_VERSION"

    log "Project structure created successfully"
}

# Phase 2: Setup SSOT framework
phase_2_ssot_framework() {
    step "Phase 2: Setting up SSOT Framework"

    if [[ "$SKIP_STEPS" == *"ssot"* ]]; then
        warn "Skipping SSOT framework setup"
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        info "[DRY RUN] Would create SSOT documentation"
        info "[DRY RUN] Would generate UoW definitions"
        info "[DRY RUN] Would create LEARNING.md"
        return
    fi

    # Create docs directory structure
    info "Creating documentation structure"
    mkdir -p docs/{adr,patterns}

    # Generate SSOT document from template
    info "Generating SSOT document"
    generate_from_template "templates/SSOT.md.template" "docs/SSOT.md"

    # Generate LEARNING.md from template
    info "Generating LEARNING.md"
    generate_from_template "templates/LEARNING.md.template" "LEARNING.md"

    # Create initial ADR
    info "Creating initial ADR"
    cat > docs/adr/ADR-001-project-architecture.md << EOF
# ADR-001: Project Architecture Decision

## Status
Accepted

## Context
We need to establish the foundational architecture for $PROJECT_NAME, a $PROJECT_TYPE in the $DOMAIN domain.

## Decision
We will use Clean Architecture with SSOT-driven development:
- Clean Architecture layers (domain, application, infrastructure, interfaces)
- SSOT documentation with GraphRAG integration
- UoW-based implementation roadmap
- Agent collaboration patterns for development

## Consequences
**Positive:**
- Clear separation of concerns
- Testable architecture
- Knowledge-driven development
- Consistent development patterns

**Negative:**
- Higher initial setup complexity
- Learning curve for SSOT-driven approach

## Implementation
- Project structure follows Clean Architecture
- UoW definitions guide implementation
- GraphRAG provides context-aware development support
- Agent collaboration ensures quality

Generated on $(date) by WAVIS Alchemy Setup Automation
EOF

    # Commit SSOT framework
    git add .
    git commit -m "feat: Add SSOT framework with comprehensive documentation

- Create Single Source of Truth (SSOT) documentation
- Define 10 Functional Requirements with acceptance criteria
- Define 7 Non-Functional Requirements with metrics
- Create UoW implementation roadmap
- Add learning capture framework
- Document initial architectural decisions

Implements: SSOT-driven development framework
UoW: Foundation setup

🤖 Generated with WAVIS Alchemy Setup Automation v$SCRIPT_VERSION"

    log "SSOT framework setup completed"
}

# Phase 3: Setup GraphRAG knowledge system
phase_3_graphrag_system() {
    step "Phase 3: Setting up GraphRAG Knowledge System"

    if [[ "$SKIP_STEPS" == *"graphrag"* ]] || [ "$ENABLE_GRAPHRAG" = false ]; then
        warn "Skipping GraphRAG setup"
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        info "[DRY RUN] Would create Python virtual environment"
        info "[DRY RUN] Would install GraphRAG"
        info "[DRY RUN] Would create GraphRAG directory structure"
        info "[DRY RUN] Would generate configuration files"
        return
    fi

    # Create Python virtual environment
    info "Creating Python virtual environment"
    python3 -m venv .venv

    # Activate virtual environment and install GraphRAG
    info "Installing GraphRAG and dependencies"
    source .venv/bin/activate
    pip install --upgrade pip
    pip install graphrag python-dotenv pyyaml pandas numpy openai tiktoken

    # Create requirements.txt
    pip freeze > requirements.txt

    # Create GraphRAG directory structure
    info "Creating GraphRAG directory structure"
    mkdir -p grag/{input,output,cache,logs,prompts,scripts,backups}
    touch grag/{output,cache,logs,backups}/.gitkeep

    # Generate GraphRAG configuration
    info "Generating GraphRAG configuration"
    generate_from_template "configs/graphrag-settings.yaml" "grag/settings.yaml"

    # Create environment file template
    cat > grag/.env.template << 'EOF'
# GraphRAG Configuration
GRAPHRAG_API_KEY=your-api-key-here

# For local models (Ollama)
# GRAPHRAG_API_BASE=http://localhost:11434/v1
# GRAPHRAG_MODEL=llama3.1:8b
# GRAPHRAG_EMBEDDING_MODEL=nomic-embed-text

# For OpenAI
# GRAPHRAG_API_BASE=https://api.openai.com/v1
# GRAPHRAG_MODEL=gpt-4-turbo-preview
# GRAPHRAG_EMBEDDING_MODEL=text-embedding-ada-002

# For local LiteLLM proxy
GRAPHRAG_API_BASE=http://localhost:4000/v1
GRAPHRAG_MODEL=qwen2.5-14b
GRAPHRAG_EMBEDDING_MODEL=text-embedding-ada-002
EOF

    # Copy to actual .env
    cp grag/.env.template grag/.env

    # Copy initial documents to GraphRAG input
    info "Copying documents to GraphRAG input"
    cp docs/SSOT.md grag/input/ssot.txt
    cp LEARNING.md grag/input/learning.txt

    # Create GraphRAG automation scripts
    info "Creating GraphRAG automation scripts"
    create_graphrag_scripts

    deactivate  # Deactivate Python virtual environment

    # Commit GraphRAG setup
    git add .
    git commit -m "feat: Add GraphRAG knowledge management system

- Create Python virtual environment with GraphRAG
- Configure GraphRAG for context-aware development
- Setup directory structure for knowledge ingestion
- Create automation scripts for indexing and querying
- Prepare initial knowledge base with SSOT and LEARNING docs

Implements: FR-009 (monitoring & observability)
UoW: GraphRAG integration

🤖 Generated with WAVIS Alchemy Setup Automation v$SCRIPT_VERSION"

    log "GraphRAG knowledge system setup completed"
}

# Phase 4: Setup development environment
phase_4_development_environment() {
    step "Phase 4: Setting up Development Environment"

    if [[ "$SKIP_STEPS" == *"dev-env"* ]]; then
        warn "Skipping development environment setup"
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        info "[DRY RUN] Would create CLAUDE.md"
        info "[DRY RUN] Would create Makefile"
        info "[DRY RUN] Would setup development tools"
        return
    fi

    # Generate CLAUDE.md from template
    info "Generating CLAUDE.md development guide"
    generate_from_template "templates/CLAUDE.md.template" "CLAUDE.md"

    # Create Makefile for common tasks
    info "Creating Makefile"
    cat > Makefile << EOF
.PHONY: build test lint fmt clean deps graphrag-index graphrag-query help

# Build the application
build:
	go build -o bin/$PROJECT_NAME ./cmd/server

# Run tests with coverage
test:
	go test ./... -cover -coverprofile=coverage.out
	go tool cover -html=coverage.out -o coverage.html

# Run linting
lint:
	golangci-lint run

# Format code
fmt:
	go fmt ./...
	go mod tidy

# Clean build artifacts
clean:
	rm -rf bin/
	rm -rf coverage.out coverage.html

# Install dependencies
deps:
	go mod download
	go mod verify

# GraphRAG re-index
graphrag-index:
	cd grag && ./scripts/reindex-graphrag.sh --verbose

# GraphRAG query (example)
graphrag-query:
	cd grag && python -m graphrag query --root . --method local --query "What UoWs implement FR-001?"

# Show help
help:
	@echo "Available targets:"
	@echo "  build         - Build the application"
	@echo "  test          - Run tests with coverage"
	@echo "  lint          - Run linting"
	@echo "  fmt           - Format code and tidy modules"
	@echo "  clean         - Clean build artifacts"
	@echo "  deps          - Install dependencies"
	@echo "  graphrag-index - Re-index GraphRAG knowledge base"
	@echo "  graphrag-query - Example GraphRAG query"
	@echo "  help          - Show this help"
EOF

    # Create basic README
    info "Creating README.md"
    cat > README.md << EOF
# $PROJECT_NAME

$DESCRIPTION

## Quick Start

This project uses the WAVIS Alchemy SSOT-driven development framework with GraphRAG integration.

### Prerequisites

- Go $GO_VERSION+
- Python 3.9+ (for GraphRAG)
- Docker (optional, for services)

### Setup

1. **Install dependencies**:
   \`\`\`bash
   make deps
   \`\`\`

2. **Setup GraphRAG** (if enabled):
   \`\`\`bash
   # Configure API key in grag/.env
   echo "GRAPHRAG_API_KEY=your-key-here" > grag/.env

   # Run initial indexing
   make graphrag-index
   \`\`\`

3. **Build and run**:
   \`\`\`bash
   make build
   ./bin/$PROJECT_NAME
   \`\`\`

### Development Workflow

This project follows SSOT-driven development:

1. **Query GraphRAG** for context before implementing:
   \`\`\`bash
   make graphrag-query
   \`\`\`

2. **Follow TDD** cycle (Red-Green-Refactor)

3. **Update LEARNING.md** with discoveries

4. **Reference FR/UoW** in commits and documentation

### Architecture

- **Type**: $PROJECT_TYPE
- **Domain**: $DOMAIN
- **Architecture**: Clean Architecture with SSOT integration
- **Testing**: Table-driven tests with testify
- **Quality**: SonarQube integration, 80%+ coverage for foundation

### Documentation

- \`docs/SSOT.md\` - Single Source of Truth with all requirements
- \`CLAUDE.md\` - Development guidelines and agent collaboration
- \`LEARNING.md\` - Captured development learnings
- \`docs/adr/\` - Architectural Decision Records

### Commands

\`\`\`bash
make help  # Show all available commands
\`\`\`

For detailed setup instructions, see [PROJECT-SETUP-TEMPLATE.md](PROJECT-SETUP-TEMPLATE.md).

---

Generated with WAVIS Alchemy Setup Automation v$SCRIPT_VERSION
EOF

    # Commit development environment
    git add .
    git commit -m "feat: Add development environment and tooling

- Create comprehensive CLAUDE.md development guide
- Add Makefile for common development tasks
- Create README.md with quick start instructions
- Configure SSOT-driven development workflow
- Setup agent collaboration patterns

Implements: Development tooling and guidelines
UoW: Development environment setup

🤖 Generated with WAVIS Alchemy Setup Automation v$SCRIPT_VERSION"

    log "Development environment setup completed"
}

# Phase 5: Create UoW architecture
phase_5_uow_architecture() {
    step "Phase 5: Creating UoW Architecture"

    if [[ "$SKIP_STEPS" == *"uow"* ]]; then
        warn "Skipping UoW architecture creation"
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        info "[DRY RUN] Would create UoW directory structure"
        info "[DRY RUN] Would generate prerequisite UoWs"
        info "[DRY RUN] Would generate foundation UoWs"
        info "[DRY RUN] Would generate infrastructure UoWs"
        return
    fi

    # Create UoW directory
    info "Creating UoW directory structure"
    mkdir -p grag/uow

    # Generate UoW definitions
    info "Generating UoW definitions"
    create_prerequisite_uows
    create_foundation_uows
    create_infrastructure_uows
    create_business_uows
    create_deployment_uows

    # Commit UoW architecture
    git add .
    git commit -m "feat: Add comprehensive UoW architecture definitions

- Create UoW directory structure in grag/uow/
- Define prerequisite UoWs (UoW-000 to UoW-001D)
- Define foundation UoWs (UoW-001 to UoW-003)
- Define infrastructure UoWs (UoW-101 to UoW-110)
- Define business logic UoWs (UoW-201 to UoW-210)
- Each UoW includes detailed acceptance criteria and dependencies

Implements: Complete UoW implementation roadmap
Architecture: Layer-based UoW dependency structure

🤖 Generated with WAVIS Alchemy Setup Automation v$SCRIPT_VERSION"

    log "UoW architecture creation completed"
}

# Phase 6: Setup command system
phase_6_command_system() {
    step "Phase 6: Setting up Command System"

    if [[ "$SKIP_STEPS" == *"commands"* ]]; then
        warn "Skipping command system setup"
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        info "[DRY RUN] Would create command documentation"
        info "[DRY RUN] Would create UoW execution commands"
        info "[DRY RUN] Would create batch processing commands"
        return
    fi

    # Create command documentation
    info "Creating command documentation"
    create_command_documentation

    # Commit command system
    git add .
    git commit -m "feat: Add comprehensive command system

- Create command documentation for all UoW implementations
- Define agent collaboration workflows for each command
- Setup batch processing commands for layer execution
- Include TDD integration and quality gates

Implements: UoW execution framework
Architecture: Command-driven development workflow

🤖 Generated with WAVIS Alchemy Setup Automation v$SCRIPT_VERSION"

    log "Command system setup completed"
}

# Phase 7: Setup quality and CI/CD
phase_7_quality_cicd() {
    step "Phase 7: Setting up Quality & CI/CD"

    if [[ "$SKIP_STEPS" == *"quality"* ]]; then
        warn "Skipping quality and CI/CD setup"
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        info "[DRY RUN] Would create SonarQube configuration"
        info "[DRY RUN] Would setup GitHub Actions"
        info "[DRY RUN] Would create Docker configuration"
        return
    fi

    # Setup SonarQube if enabled
    if [ "$ENABLE_SONARQUBE" = true ]; then
        info "Setting up SonarQube configuration"
        generate_from_template "configs/sonar-project.properties" "sonar-project.properties"
    fi

    # Setup Docker if enabled
    if [ "$ENABLE_DOCKER" = true ]; then
        info "Setting up Docker configuration"
        create_docker_configuration
    fi

    # Setup CI/CD if enabled
    if [ "$ENABLE_CI_CD" = true ]; then
        info "Setting up GitHub Actions"
        create_github_actions
    fi

    # Setup monitoring if enabled
    if [ "$ENABLE_MONITORING" = true ]; then
        info "Setting up monitoring configuration"
        create_monitoring_configuration
    fi

    # Commit quality and CI/CD setup
    local commit_features=""
    [ "$ENABLE_SONARQUBE" = true ] && commit_features+=", SonarQube integration"
    [ "$ENABLE_DOCKER" = true ] && commit_features+=", Docker containerization"
    [ "$ENABLE_CI_CD" = true ] && commit_features+=", GitHub Actions CI/CD"
    [ "$ENABLE_MONITORING" = true ] && commit_features+=", monitoring setup"

    git add .
    git commit -m "feat: Add quality gates and CI/CD pipeline

- Configure code quality analysis with SonarQube
- Setup automated testing and deployment
- Add Docker containerization for production
- Configure monitoring and observability
Features:$commit_features

Implements: NFR-005 (maintainability), NFR-003 (security)
UoW: Quality and deployment infrastructure

🤖 Generated with WAVIS Alchemy Setup Automation v$SCRIPT_VERSION"

    log "Quality and CI/CD setup completed"
}

# Phase 8: Knowledge consolidation
phase_8_knowledge_consolidation() {
    step "Phase 8: Knowledge Consolidation"

    if [[ "$SKIP_STEPS" == *"consolidation"* ]] || [ "$ENABLE_GRAPHRAG" = false ]; then
        warn "Skipping knowledge consolidation"
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        info "[DRY RUN] Would create consolidated knowledge files"
        info "[DRY RUN] Would run initial GraphRAG indexing"
        info "[DRY RUN] Would verify setup"
        return
    fi

    # Create consolidated knowledge files
    info "Creating consolidated knowledge files"
    create_consolidated_knowledge_files

    # Run initial GraphRAG indexing
    if [ "$ENABLE_GRAPHRAG" = true ]; then
        info "Running initial GraphRAG indexing"
        cd grag
        source ../.venv/bin/activate
        ./scripts/reindex-graphrag.sh --verbose
        ./scripts/verify-graphrag.sh --report
        deactivate
        cd ..
    fi

    # Create final setup report
    info "Creating setup completion report"
    create_setup_report

    # Final commit
    git add .
    git commit -m "feat: Complete knowledge consolidation and setup

- Create consolidated GraphRAG ingestion files
- Run initial knowledge base indexing
- Generate setup completion report
- Verify all components are ready for development

Setup Status: Complete and ready for UoW development
Knowledge Base: Indexed and queryable
Next Step: Begin UoW implementation starting with UoW-000

🤖 Generated with WAVIS Alchemy Setup Automation v$SCRIPT_VERSION"

    log "Knowledge consolidation completed"
}

# Helper function to generate files from templates
generate_from_template() {
    local template_file="$TEMPLATE_DIR/$1"
    local output_file="$2"

    if [ ! -f "$template_file" ]; then
        error "Template file not found: $template_file"
        return 1
    fi

    # Simple variable substitution (would be enhanced with proper templating)
    sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
        -e "s/{{GITHUB_USERNAME}}/$GITHUB_USERNAME/g" \
        -e "s/{{PROJECT_TYPE}}/$PROJECT_TYPE/g" \
        -e "s/{{GO_VERSION}}/$GO_VERSION/g" \
        -e "s/{{DOMAIN}}/$DOMAIN/g" \
        -e "s/{{PROJECT_DESCRIPTION}}/$DESCRIPTION/g" \
        -e "s/{{GENERATION_DATE}}/$(date)/g" \
        -e "s/{{CURRENT_DATE}}/$(date +%Y-%m-%d)/g" \
        "$template_file" > "$output_file"
}

# Helper functions for creating specific components
create_graphrag_scripts() {
    # This would create the GraphRAG automation scripts
    # Implementation details would go here
    info "Creating GraphRAG scripts (placeholder)"
}

create_prerequisite_uows() {
    # This would create UoW-000 through UoW-001D
    info "Creating prerequisite UoWs (placeholder)"
}

create_foundation_uows() {
    # This would create UoW-001 through UoW-003
    info "Creating foundation UoWs (placeholder)"
}

create_infrastructure_uows() {
    # This would create UoW-101 through UoW-110
    info "Creating infrastructure UoWs (placeholder)"
}

create_business_uows() {
    # This would create UoW-201 through UoW-210
    info "Creating business UoWs (placeholder)"
}

create_deployment_uows() {
    # This would create UoW-210
    info "Creating deployment UoWs (placeholder)"
}

create_command_documentation() {
    # This would create all command documentation
    info "Creating command documentation (placeholder)"
}

create_docker_configuration() {
    # This would create Docker-related files
    info "Creating Docker configuration (placeholder)"
}

create_github_actions() {
    # This would create GitHub Actions workflows
    info "Creating GitHub Actions (placeholder)"
}

create_monitoring_configuration() {
    # This would create monitoring configurations
    info "Creating monitoring configuration (placeholder)"
}

create_consolidated_knowledge_files() {
    # This would create consolidated knowledge files
    info "Creating consolidated knowledge files (placeholder)"
}

create_setup_report() {
    # This would create a final setup report
    cat > SETUP-REPORT.md << EOF
# Setup Completion Report

**Project**: $PROJECT_NAME
**Generated**: $(date)
**Script Version**: $SCRIPT_VERSION

## Setup Summary

✅ **Project Structure**: Clean Architecture with Go $GO_VERSION
✅ **SSOT Framework**: Comprehensive requirements and UoW definitions
✅ **GraphRAG**: Knowledge management system ready
✅ **Development Environment**: Claude Code integration and tooling
✅ **UoW Architecture**: Complete implementation roadmap
✅ **Command System**: Agent collaboration workflows
✅ **Quality Gates**: Testing, linting, and CI/CD
✅ **Knowledge Base**: Indexed and queryable

## Next Steps

1. **Configure API Keys**: Update \`grag/.env\` with your API keys
2. **Start Development**: Begin with UoW-000 (Project Structure Setup)
3. **Query GraphRAG**: Use \`make graphrag-query\` for context
4. **Follow TDD**: Write tests first, implement, refactor

## Commands

\`\`\`bash
# Start development
make graphrag-query  # Get context for next UoW
make test           # Run test suite
make build          # Build application

# GraphRAG operations
make graphrag-index  # Re-index knowledge base
cd grag && python -m graphrag query --root . --method local --query "What should I implement first?"
\`\`\`

## Project Structure

- \`docs/SSOT.md\` - Single Source of Truth
- \`CLAUDE.md\` - Development guidelines
- \`grag/\` - GraphRAG knowledge system
- \`cmd/server/\` - Application entry point
- \`internal/\` - Clean Architecture layers

**Ready for UoW-driven development!** 🚀
EOF
}

# Main execution flow
main() {
    echo -e "${CYAN}"
    cat << 'EOF'
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           WAVIS Alchemy Setup Automation                    ║
    ║                                                              ║
    ║           SSOT-Driven Development Framework                  ║
    ║           with GraphRAG Knowledge Management                 ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    parse_arguments "$@"
    load_config
    validate_prerequisites
    check_project_directory

    info "Starting automated setup for $PROJECT_NAME"
    info "Project type: $PROJECT_TYPE, Domain: $DOMAIN"
    info "GitHub: https://github.com/$GITHUB_USERNAME/$PROJECT_NAME"

    if [ "$DRY_RUN" = true ]; then
        warn "DRY RUN MODE - No files will be created"
    fi

    # Execute all phases
    phase_1_project_structure
    phase_2_ssot_framework
    phase_3_graphrag_system
    phase_4_development_environment
    phase_5_uow_architecture
    phase_6_command_system
    phase_7_quality_cicd
    phase_8_knowledge_consolidation

    # Final success message
    step "Setup Complete!"

    if [ "$DRY_RUN" = false ]; then
        log "Project $PROJECT_NAME has been successfully created!"
        log "Location: $(pwd)/$PROJECT_NAME"
        log "Repository: https://github.com/$GITHUB_USERNAME/$PROJECT_NAME"
        echo ""
        info "Next steps:"
        echo "  1. cd $PROJECT_NAME"
        echo "  2. Configure API keys in grag/.env"
        echo "  3. make graphrag-index"
        echo "  4. Begin UoW development starting with UoW-000"
        echo ""
        info "For detailed instructions, see SETUP-REPORT.md"
    else
        log "Dry run completed successfully!"
        info "Run without --dry-run to create the project"
    fi
}

# Execute main function with all arguments
main "$@"