# 🤖 Demeter v1.2 AI Prompt Library

**Zero Script Dependency - Complete AI-Driven Development**

## 🎯 Overview

This directory contains all AI prompts for the Demeter v1.2 framework. Every operation is performed through Claude Code prompts rather than scripts, enabling true AI-First development.

## 📁 Prompt Structure

### 🔄 Phase-Based Development Prompts
Execute in sequential order for complete project lifecycle:

| Phase | Prompt File | Purpose | Duration |
|-------|-------------|---------|----------|
| **Phase 0** | [`phase0-project-init.md`](phase0-project-init.md) | Project initialization | 5 min |
| **Phase 1-2** | [`phase1-2-ssot-management.md`](phase1-2-ssot-management.md) | SSOT & UoW design | 15 min |
| **Phase 3-5** | [`phase3-5-development.md`](phase3-5-development.md) | Implementation | 60+ min |
| **Phase 6** | [`phase6-quality-verification.md`](phase6-quality-verification.md) | Quality verification | 15 min |
| **Phase 7** | [`phase7-deployment.md`](phase7-deployment.md) | Production deployment | 15 min |

### 🔧 Tool-Specific Operation Prompts
Use for specialized operations during development:

| Tool | Prompt File | Use Case |
|------|-------------|----------|
| **SSOT Operations** | [`tools/ssot-operations.md`](tools/ssot-operations.md) | Requirements management |
| **UoW Management** | [`tools/uow-management.md`](tools/uow-management.md) | Task breakdown & tracking |
| **Agent Collaboration** | [`tools/agent-collaboration.md`](tools/agent-collaboration.md) | Multi-agent workflows |
| **Quality Checks** | [`tools/quality-checks.md`](tools/quality-checks.md) | Validation & testing |
| **Docker-Compose Deployment** | [`tools/docker-compose-deployment.md`](tools/docker-compose-deployment.md) | Primary deployment method |
| **Kubernetes Deployment** | [`tools/kubernetes-deployment.md`](tools/kubernetes-deployment.md) | Advanced orchestration |
| **Deployment Security** | [`tools/deployment-security.md`](tools/deployment-security.md) | Security hardening |

---

## 🚀 Quick Start Guide

### 1. New Project Development
```markdown
# Execute these prompts sequentially in Claude Code:

1. Execute: demeter/prompts/phase0-project-init.md
2. Execute: demeter/prompts/phase1-2-ssot-management.md
3. Execute: demeter/prompts/phase3-5-development.md
4. Execute: demeter/prompts/phase6-quality-verification.md
5. Execute: demeter/prompts/phase7-deployment.md
```

### 2. Agent Collaboration Development
```markdown
# For complex projects with multiple UoWs:
"Launch 3 general-purpose agents in parallel to implement UoW-002, UoW-003, UoW-004"

# For sequential dependencies:
"Launch agent for UoW-001, then launch agent for UoW-002 which depends on UoW-001"
```

### 3. Specialized Operations
```markdown
# SSOT and UoW management:
Execute: demeter/prompts/tools/ssot-operations.md
Execute: demeter/prompts/tools/uow-management.md

# Quality and deployment:
Execute: demeter/prompts/tools/quality-checks.md
Execute: demeter/prompts/tools/docker-compose-deployment.md
```

---

## 🤖 Agent Collaboration Quick Reference

### When to Use Agents
| UoW Complexity | Acceptance Criteria | Strategy |
|----------------|-------------------|----------|
| **Simple** | 1-2 criteria | Direct implementation |
| **Medium** | 3-4 criteria | Single general-purpose agent |
| **Complex** | 5+ criteria | Multiple agents in parallel |
| **Dependent** | Sequential UoWs | Agent chain execution |

### Agent Commands
```markdown
# Single Agent
"Launch general-purpose agent to implement UoW-XXX"

# Parallel Agents
"Launch 3 general-purpose agents in parallel to implement UoW-A, UoW-B, UoW-C"

# Sequential Agents
"Launch agent for UoW-A, then launch agent for UoW-B which depends on UoW-A"

# Complex Agent (many criteria)
"Launch general-purpose agent to implement UoW-XXX which has 7 acceptance criteria"
```

---

## 🐳 Deployment Strategy

### Docker-Compose First (Recommended)
```markdown
# Primary deployment method for most projects
Execute: demeter/prompts/tools/docker-compose-deployment.md

# With security hardening
Execute: demeter/prompts/tools/deployment-security.md
```

### Kubernetes (Advanced)
```markdown
# Only when Docker-Compose isn't sufficient
Execute: demeter/prompts/tools/kubernetes-deployment.md

# Use cases: 5+ services, auto-scaling, service mesh
```

---

## ✅ Quality Assurance

### Development Quality
```markdown
# Comprehensive quality verification
Execute: demeter/prompts/tools/quality-checks.md

# Specific validations
"Validate all acceptance criteria for implemented UoWs"
"Analyze test coverage and identify gaps"
"Execute performance tests and validate NFR compliance"
```

### Security Validation
```markdown
# Production security hardening
Execute: demeter/prompts/tools/deployment-security.md

# Compliance configurations
"Configure deployment for GDPR compliance requirements"
"Apply security best practices to Docker-Compose deployment"
```

---

## 📈 Success Metrics

### Framework Validation Results (Hello World Demo)
- **Development Time**: 2.5 hours (vs traditional 8-12 hours) ✅
- **Setup Time**: 10 minutes (85% reduction) ✅
- **Test Coverage**: 77% with comprehensive edge cases ✅
- **Performance**: <1ms response times (100x better) ✅
- **Quality**: 0 bugs, 100% AC satisfaction ✅
- **Deployment**: Single command (`docker-compose up -d`) ✅

### AI Collaboration Benefits
- **Agent Usage**: 50% faster for complex UoWs (3+ criteria)
- **Parallel Execution**: 50% time savings for independent UoWs
- **Knowledge Accumulation**: Reusable patterns captured
- **Quality**: Near-zero bugs through AI validation

---

## 🔍 Troubleshooting

### Prompt Issues
```bash
# Verify prompt file exists
ls demeter/prompts/phase0-project-init.md

# Copy entire content to Claude Code
# Execute as single conversation
# Don't break up prompts into pieces
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

### Deployment Problems
```markdown
# Use deployment troubleshooting
Execute: demeter/prompts/tools/docker-compose-deployment.md

# Common issues: port conflicts, resource limits, health checks
```

---

## 🎯 Best Practices

### ✅ AI-First Development
- Always start with prompts, never scripts
- Use agent collaboration for complex features (3+ AC)
- Let AI handle implementation details
- Focus on requirements definition and review

### ✅ Prompt Execution
- Execute complete prompts in single conversations
- Don't break prompts into multiple parts
- Use agent collaboration for parallel work
- Accumulate knowledge in GraphRAG

### ✅ Quality First
- Execute quality checks after each phase
- Use AI for bug detection and fixing
- Validate all acceptance criteria
- Apply security best practices from day one

---

## 🔗 Related Resources

### Framework Documentation
- **[Complete Lifecycle Guide](../docs/LIFECYCLE.md)**: Full development lifecycle
- **[Getting Started Guide](../guides/getting-started.md)**: Comprehensive tutorial
- **[Quick Reference Guide](../guides/quick-reference.md)**: Essential commands

### Examples
- **[Hello World Demo](../../hello-world-demo/)**: Complete working example
- **[Framework Templates](../templates/)**: Project scaffolding
- **[Core Components](../core/)**: Framework utilities

---

**🤖 AI-First Development - The Future is Here**

> *"Every operation is a conversation with AI - no scripts, just intelligence"*