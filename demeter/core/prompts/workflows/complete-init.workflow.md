# 🌱 Complete Initialization Workflow

## Overview
This workflow guides you through the complete project initialization process using the minimized Demeter scripts and Claude Code prompt-based processing.

## Prerequisites
- Demeter WAVIS v1.3 template available
- Claude Code access
- Project requirements (optional)

## Workflow Steps

### Step 1: Execute Minimal Init Script
```bash
./demeter-init.sh [project-name] [extensions] [requirements-file]
```

**Examples:**
```bash
# E-commerce project
./demeter-init.sh my-shop "e-commerce" "requirements.md"

# FinTech project
./demeter-init.sh my-bank "fintech"

# Healthcare project
./demeter-init.sh my-clinic "healthcare" "patient-requirements.md"

# IoT project
./demeter-init.sh my-iot "iot"

# General project (no domain)
./demeter-init.sh my-app
```

**Script Output:**
- Creates project directory structure
- Generates `.demeter/MASTER_INIT.prompt`
- Provides next steps instructions

### Step 2: Execute Master Initialization Prompt
```bash
cd [project-name]
# Open .demeter/MASTER_INIT.prompt in Claude Code
```

**Claude Code Processing:**
1. **Project Structure Creation**
   - Creates comprehensive directory layout
   - Initializes documentation files
   - Sets up configuration files

2. **SSOT Generation**
   - Loads base requirements from template
   - Applies domain extensions
   - Merges into unified SSOT
   - Generates docs/SSOT.md and docs/merged-ssot.yaml

3. **Execution Plan Creation**
   - Builds batch/execution-plan.yaml
   - Sequences UoWs with dependencies
   - Defines quality gates

4. **Requirements Integration** (if applicable)
   - Analyzes natural language requirements
   - Creates custom SSOT extensions
   - Integrates with existing SSOT

5. **GraphRAG Knowledge Setup**
   - Initializes .demeter-dev/knowledge/
   - Creates development patterns
   - Sets up query examples

### Step 3: Validation and Review
After Claude Code execution:

1. **Review Generated Files:**
   - `docs/SSOT.md` - Complete requirements specification
   - `batch/execution-plan.yaml` - Development sequence
   - `README.md` - Project overview
   - `.demeter-dev/knowledge/` - Development knowledge base

2. **Validate Requirements:**
   - Check that all requirements are captured
   - Verify domain-specific needs are addressed
   - Confirm UoW sequences make sense

3. **Customize if Needed:**
   - Use Claude Code to adjust requirements
   - Modify execution priorities
   - Add missing requirements

### Step 4: Begin Development
```bash
./demeter-iterate.sh
# or
./demeter-uow-executor.sh
```

This starts the TDD development cycle using the generated SSOT and execution plan.

## Success Indicators

### ✅ Initialization Complete
- [ ] Project directory structure created
- [ ] SSOT.md generated with all requirements
- [ ] execution-plan.yaml ready for development
- [ ] GraphRAG knowledge base initialized
- [ ] All documentation files in place

### ✅ Ready for Development
- [ ] All requirements validated and confirmed
- [ ] UoW execution sequence approved
- [ ] Development environment configured
- [ ] Team understands the SSOT structure

## Troubleshooting

### Common Issues

**Issue: SSOT generation fails**
- **Solution**: Check extension names (use: e-commerce, fintech, healthcare, iot)
- **Alternative**: Use manual SSOT prompts in .demeter/prompts/

**Issue: Requirements not properly integrated**
- **Solution**: Review requirements file format
- **Alternative**: Use requirements-analysis.prompt.template manually

**Issue: Missing domain-specific requirements**
- **Solution**: Verify correct extension specified
- **Alternative**: Add custom requirements using Claude Code

### Recovery Steps

1. **Restart Initialization:**
   ```bash
   rm -rf [project-name]
   ./demeter-init.sh [project-name] [corrected-extensions]
   ```

2. **Manual SSOT Generation:**
   - Use individual prompt templates in demeter/core/prompts/templates/
   - Execute each phase separately in Claude Code

3. **Incremental Enhancement:**
   - Start with base SSOT
   - Add domain extensions progressively
   - Integrate custom requirements last

## Next Steps
After successful initialization:
1. Execute TDD workflow using demeter-uow-executor.sh
2. Monitor development progress in .demeter/tdd-progress.md
3. Leverage GraphRAG knowledge for development assistance