# 🎯 Demeter Prompt-Based Processing System

## Overview
The Demeter WAVIS v1.3 framework has been redesigned to minimize script complexity and maximize Claude Code's processing capabilities. All complex logic has been moved to structured prompts that Claude Code executes.

## Architecture

### Minimized Scripts
- **demeter-init.sh**: 50 lines - Creates project structure and master initialization prompt
- **demeter-uow-executor.sh**: 50 lines - Creates TDD execution prompt

### Prompt Templates
Located in `templates/`:

**Standard Templates:**
- `project-init.prompt.template` - Complete project initialization
- `ssot-generation.prompt.template` - SSOT creation and merging (SDD-enhanced)
- `requirements-analysis.prompt.template` - Natural language requirements integration (SDD-enhanced)
- `tdd-executor.prompt.template` - TDD cycle execution (SDD-enhanced)
- `graphrag-index.prompt.template` - GraphRAG knowledge base creation

**SDD-Specific Templates:**
- `sdd-specification.prompt.template` - GitHub SDD `/specify` command implementation
- `sdd-plan.prompt.template` - GitHub SDD `/plan` command implementation
- `sdd-tasks.prompt.template` - GitHub SDD `/tasks` command implementation

### Workflow Guides
Located in `workflows/`:
- `complete-init.workflow.md` - End-to-end initialization process
- `tdd-cycle.workflow.md` - Test-driven development workflow
- `sdd-workflow.md` - GitHub Specification-Driven Development workflow

## Quick Start

### Standard Workflow
```bash
# 1. Initialize Project
./demeter-init.sh my-project "e-commerce" "requirements.md"
cd my-project

# 2. Execute Initialization in Claude Code
# Open and execute: .demeter/MASTER_INIT.prompt

# 3. Start TDD Development
./demeter-uow-executor.sh
# Open and execute: .demeter/TDD_EXECUTOR.prompt
```

### SDD (Specification-Driven Development) Workflow
```bash
# 1. Initialize Project (same as above)
./demeter-init.sh my-project "e-commerce"

# 2. Execute SDD Workflow in Claude Code
# /specify phase: Use sdd-specification.prompt.template
# /plan phase: Use sdd-plan.prompt.template
# /tasks phase: Use sdd-tasks.prompt.template

# 3. Execute TDD with Constitutional Principles
./demeter-uow-executor.sh
# Enhanced with GitHub SDD constitutional principles
```

## Benefits

### ✅ For Developers
- **Simplified Scripts**: Easy to understand and maintain
- **Powerful Processing**: Leverage Claude Code's full capabilities
- **Flexible Customization**: Prompts can be easily modified
- **Constitutional Guidance**: GitHub SDD principles ensure consistent quality
- **Better Documentation**: Clear workflow guides

### ✅ For Projects
- **Consistent Quality**: Standardized prompt-based processing with SDD principles
- **Domain Expertise**: Built-in best practices for different domains
- **Specification-Driven**: Clear requirements traceability through SDD workflow
- **Knowledge Capture**: GraphRAG system learns from each project
- **Scalable Approach**: Works for simple to complex projects

### ✅ For Teams
- **Easy Onboarding**: Clear workflows and SDD constitutional principles
- **Reduced Maintenance**: Minimal script code to maintain
- **Enhanced Collaboration**: Shared knowledge base and constitutional compliance
- **Quality Assurance**: Built-in quality gates and SDD validation
- **Constitutional Compliance**: 9 principles ensure consistent development quality

## Template Variables

All prompt templates support variable substitution:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{PROJECT_NAME}}` | Project name | my-shop |
| `{{EXTENSIONS}}` | Domain extensions | e-commerce |
| `{{REQUIREMENTS_FILE}}` | Requirements file path | requirements.md |
| `{{FRAMEWORK_PATH}}` | Template framework path | /path/to/wavis-template |
| `{{EXECUTION_PLAN}}` | Execution plan file | batch/execution-plan.yaml |
| `{{MERGED_SSOT_FILE}}` | Merged SSOT file | docs/merged-ssot.yaml |

## Domain Extensions

Supported domain extensions:
- **e-commerce**: Product catalogs, payments, user management
- **fintech**: Compliance, security, transaction processing
- **healthcare**: HIPAA compliance, patient data, security
- **iot**: Device management, real-time data, edge computing

## File Structure

```
demeter/core/prompts/
├── README.md                    # This file
├── templates/                   # Prompt templates
│   ├── project-init.prompt.template
│   ├── ssot-generation.prompt.template
│   ├── requirements-analysis.prompt.template
│   ├── tdd-executor.prompt.template
│   └── graphrag-index.prompt.template
└── workflows/                   # Workflow documentation
    ├── complete-init.workflow.md
    └── tdd-cycle.workflow.md
```

## Integration with Existing Tools

### SSOT Tools
The existing Python tools in `demeter/core/ssot/tools/` have been simplified to generate prompts:
- `merge-ssot.py` - Creates merge prompts for Claude Code
- `generate-template.py` - Creates template generation prompts
- `analyze-requirements.py` - Creates requirements analysis prompts

### GraphRAG Integration
- Knowledge base created in `.demeter-dev/knowledge/`
- Patterns and lessons captured during development
- Query examples for ongoing development assistance

## Customization

### Creating Custom Templates
1. Copy existing template
2. Modify prompt content
3. Update variable placeholders
4. Test with sample project

### Adding New Workflows
1. Create workflow markdown file
2. Document step-by-step process
3. Include troubleshooting section
4. Provide examples and success criteria

## Support

### Common Issues
1. **Template variables not substituted**: Check variable names match exactly
2. **Prompts too long for Claude Code**: Break into smaller, focused prompts
3. **Domain extension not recognized**: Use supported extension names

### Getting Help
1. Review workflow documentation
2. Check existing prompt templates for examples
3. Use GraphRAG knowledge base for project-specific guidance
4. Consult troubleshooting sections in workflow guides

---

**Happy developing with Demeter v1.3! 🌱**