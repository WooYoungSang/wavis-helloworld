# 🌾 Demeter WAVIS v1.3: Quick Reference Guide

Essential prompts and workflows for AI-First development with Zero Script Dependency.

---

## 🚀 Quick Setup

```bash
# 1. Copy framework template (30 seconds)
cp -r demeter/ /path/to/your-project/

# 2. Execute Phase 0 in Claude Code
# Copy and execute: demeter/prompts/phase0-project-init.md

# 3. Start AI-driven development
# Execute sequential prompts for complete automation
```

---

## 📋 Core AI Prompts

### Phase-Based Development

| Phase | Prompt | Purpose | Duration |
|-------|--------|---------|----------|
| **Phase 0** | `demeter/prompts/phase0-project-init.md` | Project initialization | 5 min |
| **Phase 1-2** | `demeter/prompts/phase1-2-ssot-management.md` | SSOT & UoW design | 15 min |
| **Phase 3-5** | `demeter/prompts/phase3-5-development.md` | Implementation | 60 min |
| **Phase 6-7** | `demeter/prompts/phase6-7-verification-deployment.md` | Quality & deploy | 15 min |

### Tool-Specific Prompts

| Tool | Prompt | Use Case |
|------|--------|----------|
| **SSOT Operations** | `demeter/prompts/tools/ssot-operations.md` | Requirements management |
| **UoW Management** | `demeter/prompts/tools/uow-management.md` | Task breakdown & tracking |
| **Quality Checks** | `demeter/prompts/tools/quality-checks.md` | Validation & testing |
| **Deployment Prep** | `demeter/prompts/tools/deployment-prep.md` | Docker-Compose deployment |
| **Agent Collaboration** | `demeter/prompts/tools/agent-collaboration.md` | Multi-agent workflows |

---

## 🤖 Agent Collaboration Commands

### Parallel Agent Execution

```markdown
# For independent UoWs (3+ acceptance criteria each)
"Launch 3 general-purpose agents in parallel to implement UoW-002, UoW-003, UoW-004"

# For different aspects of same feature
"Launch 2 agents in parallel: one for implementation, one for comprehensive testing"

# For complex features
"Launch general-purpose agent to implement UoW-005 which has 7 acceptance criteria"
```

### Sequential Agent Execution

```markdown
# For dependent UoWs
"Launch general-purpose agent to implement UoW-001, then launch another agent to implement UoW-002 which depends on UoW-001"

# For multi-step processes
"First launch agent for database design, then launch agent for API implementation, finally launch agent for integration testing"
```

### Agent Decision Matrix

| UoW Complexity | Acceptance Criteria | Command |
|----------------|-------------------|---------|
| **Simple** | 1-2 criteria | Direct implementation |
| **Medium** | 3-4 criteria | `"Launch general-purpose agent to implement UoW-XXX"` |
| **Complex** | 5+ criteria | `"Launch general-purpose agent to implement UoW-XXX which has N acceptance criteria"` |
| **Multiple Independent** | 3+ UoWs | `"Launch N agents in parallel to implement UoW-A, UoW-B, UoW-C"` |
| **Dependent Chain** | Sequential UoWs | `"Launch agent for UoW-A, then launch agent for UoW-B which depends on UoW-A"` |

---

## 🐳 Docker-Compose Commands

### Quick Deployment

```bash
# Single command deployment
docker-compose up -d

# View logs
docker-compose logs -f api

# Scale horizontally
docker-compose up -d --scale api=3

# Stop services
docker-compose down
```

### Development Workflow

```bash
# Development with hot reload
docker-compose -f docker-compose.dev.yml up

# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# With monitoring stack
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Docker health status
docker-compose ps

# Service logs
docker-compose logs api
```

---

## 📊 Development Workflow Patterns

### 1. Standard Feature Development

```markdown
# Step 1: Execute Phase 0 (if new project)
Execute: demeter/prompts/phase0-project-init.md

# Step 2: Define requirements
Execute: demeter/prompts/phase1-2-ssot-management.md

# Step 3: Implement with agents
Execute: demeter/prompts/phase3-5-development.md
"Launch 2 agents in parallel to implement UoW-002 and UoW-003"

# Step 4: Verify and deploy
Execute: demeter/prompts/phase6-7-verification-deployment.md
```

### 2. Quick API Development

```markdown
# For simple APIs (like Hello World)
1. Execute: demeter/prompts/phase0-project-init.md
2. Execute: demeter/prompts/phase1-2-ssot-management.md
3. Execute: demeter/prompts/phase3-5-development.md
4. Execute: demeter/prompts/phase6-7-verification-deployment.md

# Result: Complete API with tests and deployment in <2 hours
```

### 3. Complex Feature with Multiple UoWs

```markdown
# For features with 5+ UoWs
Execute: demeter/prompts/phase3-5-development.md
"Launch 3 general-purpose agents in parallel to implement UoW-010, UoW-011, UoW-012"
"Launch agent to implement UoW-013 which depends on UoW-010, UoW-011, UoW-012"

# Benefits: 50% time savings through parallel execution
```

### 4. Bug Fix Workflow

```markdown
# Quality-driven bug fixing
Execute: demeter/prompts/tools/quality-checks.md
"Identify and fix the bug in the authentication system"

# AI will automatically:
# - Analyze the issue
# - Suggest fixes
# - Implement solutions
# - Verify fixes
```

---

## 🏗️ Project Structure Reference

```
your-project/
├── src/                     # Source code (AI-generated)
├── tests/                   # Test files (AI-generated)
├── docs/                    # Documentation
│   ├── SSOT.md             # Single Source of Truth
│   └── API.md              # API documentation
├── docker-compose.yml      # Deployment configuration
├── Dockerfile              # Container configuration
├── requirements.txt        # Dependencies
├── graphrag/               # Knowledge accumulation
│   ├── knowledge/
│   │   ├── patterns/       # Reusable patterns
│   │   ├── lessons/        # Lessons learned
│   │   └── implementation/ # Implementation notes
│   └── index/              # GraphRAG index
├── CLAUDE.md              # AI development guidelines
├── LEARNING.md            # Progress tracking
└── README.md              # Project documentation
```

---

## 📝 SSOT Structure Quick Reference

### Minimal SSOT Template

```yaml
metadata:
  project_name: "Your Project"
  version: "1.0.0"
  tech_stack: "python-fastapi"  # or typescript-nextjs, go-gin

functional_requirements:
  FR-001:
    title: "Feature Name"
    description: "Feature description"
    acceptance_criteria:
      - "Criterion 1"
      - "Criterion 2"
      - "Criterion 3"

non_functional_requirements:
  NFR-001:
    title: "Performance Requirements"
    requirements:
      - "Endpoint response < 100ms"
      - "System handles 1000 RPS"

units_of_work:
  UoW-001:
    title: "Implementation Task"
    description: "Task description"
    references: ["FR-001", "NFR-001"]
    priority: "high"  # high, medium, low
    acceptance_criteria:
      - "AC 1: Given-When-Then format"
      - "AC 2: Specific measurable outcome"
      - "AC 3: Edge case handling"
    estimated_effort: "2 hours"
```

---

## 🔧 Technology Stack Quick Setup

### Python + FastAPI

```markdown
# AI-generated structure
Execute: demeter/prompts/phase0-project-init.md

# AI automatically creates:
# - FastAPI application with proper structure
# - Pydantic models for type safety
# - Comprehensive tests with pytest
# - Docker configuration
# - OpenAPI documentation
```

### TypeScript + Next.js

```markdown
# Specify in SSOT.md:
metadata:
  tech_stack: "typescript-nextjs"

# AI automatically creates:
# - React components with TypeScript
# - API routes with proper typing
# - Tests with Jest and React Testing Library
# - Docker configuration for Node.js
# - ESLint and Prettier configuration
```

### Go + Gin

```markdown
# Specify in SSOT.md:
metadata:
  tech_stack: "go-gin"

# AI automatically creates:
# - Gin handlers with proper structure
# - Go modules and dependencies
# - Tests with Go testing package
# - Multi-stage Docker build
# - Performance-optimized configuration
```

---

## 🚦 Quality Gates Reference

### Pre-Implementation Checklist

- [ ] Phase 0 executed (project initialized)
- [ ] Phase 1-2 executed (SSOT defined, UoWs planned)
- [ ] Agent collaboration strategy determined
- [ ] Technology stack specified in SSOT

### Post-Implementation Checklist

- [ ] Phase 3-5 executed (implementation complete)
- [ ] All acceptance criteria satisfied (100%)
- [ ] Tests passing (coverage >60% for demos, >80% for production)
- [ ] Performance requirements met
- [ ] Phase 6-7 executed (quality verified, deployment ready)

### Production Readiness Checklist

- [ ] Docker-Compose configuration tested
- [ ] Health checks working
- [ ] Security constraints enforced
- [ ] Monitoring ready (optional)
- [ ] Documentation complete

---

## 📈 Success Metrics Quick Check

### Development Efficiency

```markdown
# Expected improvements with v1.3:
# - Setup Time: 75% reduction (15 min vs 60 min)
# - Development Speed: 50% faster
# - Bug Rate: Near zero (AI-driven quality)
# - Test Coverage: 100% acceptance criteria coverage
# - Deployment: 95% faster (single command)
```

### Quality Indicators

```markdown
Execute: demeter/prompts/tools/quality-checks.md

# AI provides metrics like:
# ✅ UoW-001: 3/3 acceptance criteria satisfied
# ✅ Performance: <1ms (100x better than 100ms requirement)
# ✅ Tests: 17 test cases, all passing
# ✅ Security: Input validation implemented
# ✅ Deployment: Docker-Compose ready
```

---

## 🚨 Troubleshooting Quick Fixes

### Prompt Not Working

```bash
# 1. Verify prompt file exists
ls demeter/prompts/phase0-project-init.md

# 2. Copy entire content to Claude Code
# 3. Execute as single conversation
# 4. Don't break up the prompt into pieces
```

### Agent Collaboration Issues

```markdown
# Check agent collaboration guide
Execute: demeter/prompts/tools/agent-collaboration.md

# Common fixes:
# - Use "general-purpose" agent type
# - Specify clear UoW boundaries
# - Include acceptance criteria count for complex UoWs
```

### Docker-Compose Problems

```bash
# Common issues:
docker-compose down && docker-compose up -d  # Restart services
docker-compose logs api                       # Check logs
docker system prune -f                       # Clean Docker cache

# Port conflicts:
docker-compose down
lsof -i :8000  # Check what's using the port
# Kill conflicting process or change port
```

### Performance Issues

```markdown
Execute: demeter/prompts/tools/quality-checks.md
"Analyze performance bottlenecks and suggest optimizations"

# AI will identify and fix:
# - Slow database queries
# - Inefficient algorithms
# - Memory leaks
# - Network latency issues
```

---

## 🎯 Best Practices Checklist

### ✅ AI-First Development

- [ ] Always start with prompts, never write scripts
- [ ] Use agent collaboration for complex features (3+ acceptance criteria)
- [ ] Let AI handle implementation details
- [ ] Focus on requirements definition and review

### ✅ SSOT-Driven Approach

- [ ] Define all requirements in SSOT before implementation
- [ ] Use Given-When-Then format for acceptance criteria
- [ ] Maintain traceability between FRs, NFRs, and UoWs
- [ ] Update SSOT with learned patterns

### ✅ Docker-Compose First

- [ ] Start simple with Docker-Compose
- [ ] Don't prematurely optimize to Kubernetes
- [ ] Include health checks and resource limits
- [ ] Use environment-specific compose files

### ✅ Continuous AI Verification

- [ ] Execute quality checks after each phase
- [ ] Use AI for bug detection and fixing
- [ ] Accumulate knowledge in GraphRAG
- [ ] Let AI suggest improvements

---

## 🔗 Quick Links

| Resource | Location | Purpose |
|----------|----------|---------|
| **Getting Started** | `demeter/guides/getting-started.md` | Comprehensive tutorial |
| **Phase Prompts** | `demeter/prompts/phase*.md` | Development lifecycle |
| **Tool Prompts** | `demeter/prompts/tools/*.md` | Specialized operations |
| **Hello World Demo** | `hello-world-demo/` | Complete example |
| **SSOT Template** | `demeter/core/ssot/templates/SSOT.md.template` | Requirements template |
| **Framework Docs** | `demeter/docs/LIFECYCLE.md` | Complete documentation |

---

## 🆘 Getting Help

### 1. Query AI First
```markdown
# AI can help with any question
"How do I implement user authentication using Demeter v1.3 with GraphRAG knowledge?"
"What's the best agent collaboration strategy for 5 UoWs?"
"How do I add monitoring to my Docker-Compose setup?"
```

### 2. Check Templates
```bash
# Review working examples
cat hello-world-demo/CLAUDE.md        # Development guidelines
cat hello-world-demo/docs/SSOT.md     # Requirements example
cat hello-world-demo/docker-compose.yml  # Deployment example
```

### 3. Verify Setup
```markdown
Execute: demeter/prompts/tools/quality-checks.md
"Verify that my project setup is correct and suggest any improvements"
```

### 4. Review Documentation
```bash
# Framework documentation
cat demeter/docs/LIFECYCLE.md         # Complete lifecycle guide
cat demeter/README.md                 # Framework overview
```

---

## 📊 Command Cheat Sheet

```bash
# Project Setup
cp -r demeter/ /path/to/project/       # Copy framework

# Development (in Claude Code)
# Execute: demeter/prompts/phase0-project-init.md
# Execute: demeter/prompts/phase1-2-ssot-management.md
# Execute: demeter/prompts/phase3-5-development.md
# Execute: demeter/prompts/phase6-7-verification-deployment.md

# Deployment
docker-compose up -d                   # Deploy application
docker-compose logs -f api             # View logs
docker-compose down                    # Stop services

# Monitoring
curl http://localhost:8000/health      # Health check
docker-compose ps                      # Service status
```

---

**🌾 Keep this reference handy for efficient AI-First development with Demeter WAVIS v1.3!**

> *"Zero scripts, maximum AI - the future of development is here"*