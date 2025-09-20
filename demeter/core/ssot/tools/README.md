# 🔄 SSOT Tools Migration to Prompt-Based Processing

## Migration Notice

The SSOT tools have been migrated from Python script-based processing to prompt-based processing for Claude Code execution. This migration provides better integration with the Demeter WAVIS v1.3 framework and constitutional compliance.

## 🚀 New Prompt-Based System

### Migrated Tools

| Old Python Script | New Prompt Template | Location |
|------------------|-------------------|----------|
| `merge-ssot.py` | `ssot-merge.prompt.template` | `demeter/core/prompts/templates/` |
| `nlp-to-custom-ssot.py` | `nlp-to-ssot.prompt.template` | `demeter/core/prompts/templates/` |
| `analyze-requirements.py` | `requirements-analysis.prompt.template` | `demeter/core/prompts/templates/` |
| `generate-template.py` | `ssot-generation.prompt.template` | `demeter/core/prompts/templates/` |
| `generate-analysis-prompt.py` | `ai-refinement.prompt.template` | `demeter/core/prompts/templates/` |

### Enhanced Capabilities

The new prompt-based system provides:

✅ **Constitutional Compliance Integration**: All processing includes constitutional principle validation
✅ **SDD Methodology Support**: Complete SDD workflow with [CLARIFY] markers and executable specifications
✅ **GraphRAG Optimization**: Knowledge graph preparation and context injection
✅ **AI-Enhanced Quality**: Continuous AI improvement and constitutional optimization
✅ **Domain-Specific Intelligence**: Extension-specific constitutional patterns and compliance

## 📋 How to Use New System

### 1. SSOT Merging
```bash
# Old way (deprecated)
# python merge-ssot.py --base demeter/core/ssot/base --extensions e-commerce.yaml

# New way (recommended)
# Use ssot-merge.prompt.template in Claude Code with variables:
# PROJECT_NAME, BASE_SSOT_DIR, EXTENSIONS, OUTPUT_FILE, CONSTITUTION_FILE
```

### 2. Natural Language to SSOT
```bash
# Old way (deprecated)
# python nlp-to-custom-ssot.py --input requirements.md --project-name "MyProject"

# New way (recommended)
# Use nlp-to-ssot.prompt.template in Claude Code with variables:
# PROJECT_NAME, REQUIREMENTS_FILE, PROJECT_DOMAIN, CONSTITUTION_FILE
```

### 3. Requirements Analysis
```bash
# Old way (deprecated)
# python analyze-requirements.py --input requirements.md

# New way (recommended)
# Use requirements-analysis.prompt.template in Claude Code
# Enhanced with constitutional compliance and GraphRAG integration
```

### 4. Template Generation
```bash
# Old way (deprecated)
# python generate-template.py --project-name "MyProject"

# New way (recommended)
# Use ssot-generation.prompt.template in Claude Code with variables:
# PROJECT_NAME, EXTENSIONS, CONSTITUTION_FILE
```

## 🌊 Integrated Master Workflow

For the complete end-to-end workflow, use:
```bash
# Use integrated-master-workflow.prompt.template in Claude Code
# Provides seamless: Requirements → SSOT → GraphRAG → SDD → Code Generation
```

## 🏛️ Constitutional Compliance

All new prompt templates include:
- **9 Constitutional Principles**: Library-first, CLI interface, test-first, simplicity, etc.
- **Domain-Specific Constitutional Extensions**: E-commerce, FinTech, Healthcare, IoT
- **Constitutional Validation**: Automated compliance scoring and validation
- **Constitutional Quality Gates**: Ensure constitutional adherence throughout development

## 🧠 GraphRAG Integration

Enhanced knowledge management through:
- **Constitutional Knowledge Graphs**: Constitutional principle entities and relationships
- **Context Injection**: Constitutional guidance based on development context
- **Pattern Learning**: Capture and reuse constitutional implementation patterns
- **Continuous Knowledge Evolution**: Learn from implementation experience

## 📋 SDD Methodology Support

Specification-driven development with:
- **[CLARIFY] Markers**: Explicit ambiguity identification and resolution
- **Executable Specifications**: Specifications that generate tests and implementation
- **Constitutional User Stories**: User stories with constitutional compliance integration
- **AI-Driven Refinement**: Continuous specification improvement through AI

## 🔧 Migration Path

### For Existing Projects
1. **Continue using existing Python scripts** if they meet your needs
2. **Gradually migrate to prompt-based system** for enhanced capabilities
3. **Use integrated master workflow** for new features and comprehensive development

### For New Projects
1. **Start with integrated master workflow** for complete constitutional SDD experience
2. **Use individual prompt templates** for specific SSOT processing needs
3. **Leverage constitutional compliance and GraphRAG** from the beginning

## 📚 Documentation

- **Prompt Templates**: `demeter/core/prompts/templates/`
- **Workflow Documentation**: `demeter/core/prompts/workflows/`
- **Constitutional Governance**: Use `constitution.prompt.template` to establish project constitution
- **Advanced SDD Workflow**: `demeter/core/prompts/workflows/sdd-advanced-workflow.md`

## ⚠️ Deprecation Timeline

- **Phase 1 (Current)**: Python scripts remain functional, new prompt system available
- **Phase 2 (Next Release)**: Python scripts marked deprecated, prompt system recommended
- **Phase 3 (Future Release)**: Python scripts removed, prompt system only

## 🆘 Support

For migration assistance or questions:
1. Review prompt template documentation in `demeter/core/prompts/`
2. Use GraphRAG queries for development guidance
3. Follow constitutional compliance guidelines for best results
4. Consult advanced SDD workflow documentation for complex scenarios

---

**The prompt-based system represents the future of Demeter WAVIS development with constitutional governance, GraphRAG knowledge management, and specification-driven development excellence.**