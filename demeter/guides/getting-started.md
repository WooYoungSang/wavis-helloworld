# 🌾 Demeter WAVIS v1.1: AI-First Development Framework
## Complete Getting Started Guide

> **Zero Script Dependency - Everything through AI Prompts**

---

## 🎯 What is Demeter WAVIS v1.1?

Demeter WAVIS v1.1 is a revolutionary AI-First development framework that enables:

- **Zero Script Dependency**: All operations through Claude Code prompts
- **SSOT-Driven Development**: Single Source of Truth for all requirements
- **Agent Collaboration**: Multi-agent parallel and sequential execution
- **Docker-Compose First**: Simple, production-ready deployment
- **GraphRAG Integration**: Knowledge accumulation and intelligent development
- **Phase-Based Lifecycle**: Structured AI-driven development phases

## 🚀 Quick Start (5 Minutes)

### 1. Copy Framework Template

```bash
# Copy Demeter template to your project
cp -r demeter/ /path/to/your-new-project/
cd /path/to/your-new-project
```

### 2. Execute Phase 0: Project Initialization

**In Claude Code, execute this prompt:**

```markdown
# Copy and execute the entire content of:
demeter/prompts/phase0-project-init.md
```

This will:
- ✅ Create project structure automatically
- ✅ Generate CLAUDE.md development guidelines
- ✅ Initialize LEARNING.md progress tracking
- ✅ Set up GraphRAG knowledge structure
- ✅ Prepare SSOT requirements template

### 3. Start AI-Driven Development

**Your project is now ready!** Continue with:

```markdown
# Execute Phase 1-2: SSOT Management
demeter/prompts/phase1-2-ssot-management.md

# Execute Phase 3-5: Development
demeter/prompts/phase3-5-development.md

# Execute Phase 6-7: Verification & Deployment
demeter/prompts/phase6-7-verification-deployment.md
```

**That's it!** You're now developing with complete AI automation using prompt-driven workflows.

---

## 📋 Complete Workflow Example

Let's walk through implementing a complete Hello World API using Demeter v1.1.

### Phase 0: Project Initialization

**Execute in Claude Code:**
```markdown
Execute: demeter/prompts/phase0-project-init.md
```

**AI automatically performs:**
- Project structure creation
- Development environment setup
- CLAUDE.md guidelines generation
- LEARNING.md tracking initialization

### Phase 1-2: SSOT Management and UoW Design

**Execute in Claude Code:**
```markdown
Execute: demeter/prompts/phase1-2-ssot-management.md
```

**AI automatically performs:**
- Requirements definition in docs/SSOT.md
- UoW breakdown with acceptance criteria
- Dependency analysis
- Traceability matrix creation

**Example SSOT Output:**
```yaml
functional_requirements:
  FR-001:
    title: "Hello World API"
    description: "Simple greeting API with optional name parameter"
    acceptance_criteria:
      - "GET / returns welcome message"
      - "GET /hello returns Hello, World!"
      - "GET /hello?name=Alice returns Hello, Alice!"

units_of_work:
  UoW-001:
    title: "Project Foundation Setup"
    description: "FastAPI application structure"
    acceptance_criteria:
      - "FastAPI application starts on port 8000"
      - "OpenAPI documentation available at /docs"
      - "Application responds to health checks"
```

### Phase 3-5: AI-Driven Development

**Execute in Claude Code:**
```markdown
Execute: demeter/prompts/phase3-5-development.md
```

**Agent Collaboration Example:**
```markdown
"Launch 2 general-purpose agents in parallel to implement UoW-002 and UoW-003"
```

**AI automatically performs:**
- Implementation of all UoWs
- Comprehensive test suite creation
- Agent collaboration for parallel development
- GraphRAG knowledge documentation

**Generated Implementation:**
```python
# AI-generated main.py
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI(
    title="Hello World API",
    description="Demeter v1.1 Framework Verification Project",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Hello World API"}

@app.get("/hello")
async def hello(name: Optional[str] = Query(None, description="Name for personalized greeting")):
    if name is not None:
        name = name.strip()
        if not name:
            name = None

    message = f"Hello, {name}!" if name else "Hello, World!"
    return {"message": message}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Phase 6-7: Quality Verification and Deployment

**Execute in Claude Code:**
```markdown
Execute: demeter/prompts/phase6-7-verification-deployment.md
```

**AI automatically performs:**
- ✅ 100% acceptance criteria validation
- ✅ Comprehensive test execution (17 test cases)
- ✅ Docker-Compose deployment creation
- ✅ Production-ready configuration
- ✅ Performance validation (sub-1ms response times)

**Generated docker-compose.yml:**
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    deploy:
      resources:
        limits: {memory: 256M, cpus: '0.2'}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
    restart: unless-stopped
```

**Final Result:**
```bash
# Single command deployment
docker-compose up -d

# API available at http://localhost:8000
# Documentation at http://localhost:8000/docs
```

---

## 🤖 Agent Collaboration Patterns

### When to Use Agent Collaboration

**Execute this prompt for agent collaboration:**
```markdown
Execute: demeter/prompts/tools/agent-collaboration.md
```

### Parallel Agent Execution

```markdown
# For independent UoWs
"Launch 3 general-purpose agents in parallel to implement UoW-002, UoW-003, UoW-004"

# For different aspects of the same feature
"Launch 2 agents in parallel: one for implementation, one for comprehensive testing"
```

### Sequential Agent Execution

```markdown
# For dependent UoWs
"Launch general-purpose agent to implement UoW-001, then launch another agent to implement UoW-002 which depends on UoW-001"
```

### Agent Decision Matrix

| UoW Complexity | Acceptance Criteria | Agent Recommendation |
|----------------|-------------------|---------------------|
| Simple | 1-2 criteria | Direct implementation |
| Medium | 3+ criteria | Single general-purpose agent |
| Complex | 5+ criteria | Multiple agents in parallel |
| Cross-cutting | Dependencies | Sequential agent chain |

---

## 🐳 Docker-Compose First Deployment

### Why Docker-Compose First?

✅ **Simplicity**: Single configuration file
✅ **Development Parity**: Same environment for dev and prod
✅ **Monitoring Ready**: Easy to add observability
✅ **Production Ready**: Security, health checks, resource limits
✅ **Scaling Ready**: Horizontal scaling when needed

### Enhanced Production Configuration

**Execute this prompt for advanced deployment:**
```markdown
Execute: demeter/prompts/tools/deployment-prep.md
```

**Example with monitoring:**
```yaml
version: '3.8'
services:
  api:
    build: .
    ports: ["8000:8000"]
    deploy:
      resources:
        limits: {memory: 512M, cpus: '0.5'}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes: ["./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml"]

  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### When to Consider Kubernetes

- **Multiple Services**: 5+ interconnected services
- **Advanced Deployment**: Blue-green, canary deployments
- **Complex Networking**: Service mesh requirements
- **Auto-scaling**: Pod autoscaling based on metrics

---

## 📊 Quality Assurance

### AI-Driven Quality Gates

All quality assurance is automated through AI prompts:

#### Contract Validation
```markdown
Execute: demeter/prompts/tools/quality-checks.md
```

**AI automatically checks:**
- ✅ All acceptance criteria satisfied
- ✅ Performance requirements met
- ✅ Security constraints enforced
- ✅ Test coverage comprehensive

#### Validation Results Example
```
✅ Contract Verification Results

UoW-001: Project Foundation Setup
├── ✅ Acceptance Criteria (3/3 satisfied)
├── ✅ Performance: <1ms response time (Target: <100ms)
├── ✅ Test Coverage: 77% (Target: >60%)
└── ✅ Security: Input validation implemented

UoW-002: Hello World Endpoint
├── ✅ Acceptance Criteria (4/4 satisfied)
├── ✅ Edge Cases: Empty strings, unicode, whitespace
├── ✅ Parameter Validation: Optional query parameter
└── ✅ Response Format: Consistent JSON structure

🎉 All contracts validated successfully!
```

---

## 🔧 Specialized Tool Prompts

### SSOT Operations
```markdown
Execute: demeter/prompts/tools/ssot-operations.md
```
- Requirements management
- UoW dependency analysis
- Traceability matrix updates

### UoW Management
```markdown
Execute: demeter/prompts/tools/uow-management.md
```
- Implementation planning
- Progress tracking
- Completion validation

### Quality Checks
```markdown
Execute: demeter/prompts/tools/quality-checks.md
```
- Acceptance criteria validation
- Performance testing
- Security verification

### Deployment Preparation
```markdown
Execute: demeter/prompts/tools/deployment-prep.md
```
- Docker-Compose configuration
- Production environment setup
- Monitoring integration

---

## 💡 Development Best Practices

### 1. Always Start with Phase 0
```markdown
# Never skip project initialization
Execute: demeter/prompts/phase0-project-init.md
```

### 2. Use Agent Collaboration for Complex Features
```markdown
# For UoWs with 3+ acceptance criteria
"Launch general-purpose agent to implement UoW-003 which has 5 acceptance criteria"
```

### 3. Leverage GraphRAG Knowledge
```markdown
# AI accumulates and uses knowledge from previous implementations
# Knowledge automatically guides future development decisions
```

### 4. Docker-Compose First Approach
```markdown
# Start simple, scale when needed
# Don't prematurely optimize to Kubernetes
```

### 5. Continuous AI Verification
```markdown
# After each phase, verify with AI
Execute: demeter/prompts/tools/quality-checks.md
```

---

## 🏗️ Technology Stack Examples

All implementations are generated by AI based on SSOT requirements:

### Python + FastAPI (Validated)
```python
# AI-generated with 100% acceptance criteria satisfaction
# Sub-1ms response times
# Comprehensive test coverage (17 test cases)
# Production-ready Docker configuration
```

### TypeScript + Next.js (Template Available)
```typescript
// AI generates complete React components
// Type safety enforced
// Tests with React Testing Library included
// Docker-Compose configuration provided
```

### Go + Gin (Template Available)
```go
// AI generates efficient Go handlers
// Comprehensive error handling
// Performance optimized
// Docker multi-stage build
```

---

## 🚨 Troubleshooting

### AI Prompt Not Working
```markdown
# Verify prompt file exists
ls demeter/prompts/phase0-project-init.md

# Copy entire prompt content to Claude Code
# Execute as single conversation
```

### Implementation Issues
```markdown
# Use quality check prompt
Execute: demeter/prompts/tools/quality-checks.md

# AI will identify and suggest fixes for any issues
```

### Deployment Problems
```markdown
# Use deployment preparation prompt
Execute: demeter/prompts/tools/deployment-prep.md

# AI will verify Docker configuration and suggest improvements
```

### Agent Collaboration Issues
```markdown
# Refer to agent collaboration guide
Execute: demeter/prompts/tools/agent-collaboration.md

# AI will suggest optimal agent usage patterns
```

---

## 📈 Success Metrics

Track your AI-First development success:

### Framework Validation Metrics (Hello World Example)
- **Development Time**: 3 hours (vs traditional 8-12 hours)
- **Setup Time**: 15 minutes (75% reduction)
- **Test Coverage**: 77% with comprehensive edge cases
- **Performance**: <1ms response times (100x better than requirements)
- **Quality**: 0 bugs, 100% acceptance criteria satisfaction
- **Deployment**: Single command (`docker-compose up -d`)

### AI Collaboration Effectiveness
- **Agent Usage**: Optimal for UoWs with 3+ acceptance criteria
- **Parallel Execution**: 50% time savings for independent UoWs
- **Knowledge Accumulation**: Reusable patterns and insights captured

---

## 🎯 What's Next?

After mastering the basics:

### 1. Advanced Agent Patterns
```markdown
# Explore complex agent collaboration
Execute: demeter/prompts/tools/agent-collaboration.md
```

### 2. Custom Technology Stacks
```markdown
# Adapt prompts for your specific tech stack
# Modify demeter/prompts/ files for your needs
```

### 3. Production Scaling
```markdown
# When Docker-Compose isn't enough
# Consider Kubernetes migration
Execute: demeter/prompts/tools/deployment-prep.md
```

### 4. Team Collaboration
```markdown
# Multi-developer AI-First workflows
# Shared SSOT and knowledge base
```

---

## 🌟 Framework Philosophy

> **"Every operation should be a conversation with AI"**

Demeter v1.1 eliminates the cognitive overhead of learning and maintaining scripts. Instead of remembering complex command-line options and Python script parameters, you simply have conversations with Claude Code.

### Core Principles
1. **AI First**: Every operation through natural language
2. **Zero Scripts**: Complete elimination of script dependencies
3. **Knowledge Driven**: AI learns and improves with each project
4. **Agent Collaboration**: Multiple AI agents working in harmony
5. **Simple Deployment**: Docker-Compose for everything

---

**🌾 Welcome to the future of AI-First development with Demeter WAVIS v1.1!**

> *"From requirements to reality, guided by AI conversations"*