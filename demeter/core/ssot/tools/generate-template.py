#!/usr/bin/env python3
"""
⚠️  DEPRECATED: SSOT Template Generation Prompt Creator
⚠️  This script is deprecated. Use ssot-generation.prompt.template in Claude Code instead.
⚠️
⚠️  Migration Path:
⚠️  1. Use demeter/core/prompts/templates/ssot-generation.prompt.template
⚠️  2. Benefits: Constitutional compliance, GraphRAG integration, SDD methodology
⚠️  3. See demeter/core/ssot/tools/README.md for migration guide

DEPRECATED: Generates a Claude Code prompt for converting SSOT YAML to Markdown documentation

Legacy Usage:
    python generate-template.py --input merged-ssot.yaml --output SSOT.md --project-name "MyShop"

Recommended Usage:
    Use ssot-generation.prompt.template in Claude Code with constitutional compliance
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def generate_template_prompt(input_yaml: str, output_md: str, project_name: str,
                           project_description: str = "") -> str:
    """Generate Claude Code prompt for SSOT template generation"""

    prompt = f'''# Generate SSOT Documentation

## Task Overview
Convert the merged SSOT YAML file into comprehensive Markdown documentation.

## Input/Output
- **Input**: `{input_yaml}` (Merged SSOT YAML)
- **Output**: `{output_md}` (Final SSOT Documentation)
- **Project**: {project_name}
- **Description**: {project_description or f"{project_name} project requirements"}

## Documentation Structure

Generate `{output_md}` with the following structure:

```markdown
# Single Source of Truth (SSOT) - {project_name}

## Project Overview
{project_description or f"{project_name} application"}

**Technology Stack**: [Technology] [Version]+
**Architecture**: Clean Architecture with SSOT-driven development
**Knowledge Management**: GraphRAG integration for context-aware development

## Functional Requirements (FR)

### FR-001: Configuration Management
**Description**: System must support structured configuration with schema validation
**Priority**: Critical
**Dependencies**: [if any]
**Business Value**: Secure, maintainable configuration management
**Acceptance Criteria**:
- Load configuration from structured files with schema validation
- Support environment-specific configurations (dev, test, prod)
- Hot-reload capability without service restart
- No environment variables for configuration (security requirement)

[... continue for all FRs from YAML]

## Non-Functional Requirements (NFR)

### NFR-001: Performance
**Description**: System must handle specified load with acceptable latency
**Category**: Performance
**Measurement Criteria**:
- Response time: < 200ms (95th percentile) for API calls
- Throughput: > [N] requests/second
- Memory usage: < [N]MB baseline

[... continue for all NFRs from YAML]

## Units of Work (UoW) - Implementation Roadmap

### UoW-000: Project Structure Setup
**Goal**: Establish architecture foundation
**Layer**: Foundation
**Priority**: Critical
**Dependencies**: []
**Implements**: [NFR-005]
**Estimated Effort**: [N] hours
**Acceptance Criteria**:
- Standard project layout with clear directory structure
- Architecture layers clearly defined and documented

[... continue for all UoWs from YAML]

## Cross-Reference Matrix

### FR to UoW Mapping
| Functional Requirement | Primary UoWs | Validation Method |
|------------------------|--------------|-------------------|
| FR-001 (Configuration Management) | UoW-101, UoW-102 | Unit + Integration tests |
| FR-002 (HTTP API Server) | UoW-103, UoW-104 | Unit + Integration tests |

[... generate complete mapping table]

### NFR to UoW Mapping
| Non-Functional Requirement | Related UoWs | Measurement Method | Target Value |
|-----------------------------|--------------|-------------------|--------------|
| NFR-001 (Performance) | UoW-201, UoW-301 | Load testing | < 200ms response |

[... generate complete mapping table]

### UoW Dependency Matrix
**Foundation**: UoW-000 → UoW-101 → UoW-102
**Infrastructure**: UoW-201 → UoW-202 → UoW-203
**Application**: UoW-301 → UoW-302 → UoW-303
**Integration**: UoW-401 → UoW-402
**Deployment**: UoW-501 → UoW-502

## Implementation Guidelines

### Development Sequence
1. **Prerequisites First**: Complete foundation layer before implementation
2. **Layer by Layer**: Complete each layer before proceeding
3. **Dependency Respect**: Never implement a UoW before its dependencies
4. **Testing Priority**: Write tests first (TDD approach)
5. **Documentation**: Update documentation with each UoW

### Quality Gates
- **Foundation UoWs**: 80%+ test coverage, architectural review required
- **Infrastructure UoWs**: Integration testing, security review required
- **Business UoWs**: 60%+ test coverage, business logic validation required
- **Deployment UoWs**: End-to-end testing, security scanning required

---

**Template Version**: [from metadata.version]
**Framework**: SSOT-Driven Development with GraphRAG
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Statistics**: [N] FRs, [N] NFRs, [N] UoWs
```

## Generation Instructions

### 1. Load YAML Data
- Read and parse `{input_yaml}`
- Extract sections: functional_requirements, non_functional_requirements, units_of_work, metadata

### 2. Generate Documentation Sections

#### Functional Requirements
For each FR in the YAML:
- Format as `### FR-ID: Name`
- Include all properties: description, priority, dependencies, business_value, acceptance_criteria
- Convert YAML arrays to bullet lists

#### Non-Functional Requirements
For each NFR in the YAML:
- Format as `### NFR-ID: Name`
- Include: description, category, measurement_criteria, testing_method, priority

#### Units of Work
For each UoW in the YAML:
- Format as `### UoW-ID: Name`
- Include: goal, layer, priority, dependencies, implements, estimated_effort_hours, acceptance_criteria

### 3. Generate Cross-Reference Matrices

#### FR to UoW Mapping
Create table showing:
- Which UoWs implement each FR (from UoW.implements arrays)
- Validation method (default: "Unit + Integration tests")

#### NFR to UoW Mapping
Create table showing:
- Which UoWs relate to each NFR (from UoW.implements arrays)
- Measurement method (from NFR.testing_method)
- Target value (from NFR.measurement_criteria)

#### UoW Dependency Matrix
Group UoWs by layer and show dependency chains:
- Foundation → Infrastructure → Application → Integration → Deployment
- Use UoW.dependencies to show flow within layers

### 4. Calculate Statistics
From the loaded YAML data:
- Total FRs: count of functional_requirements
- Total NFRs: count of non_functional_requirements
- Total UoWs: count of units_of_work
- Priority distribution (Critical/High/Medium/Low counts)
- Layer distribution (Foundation/Infrastructure/Application counts)
- Total estimated effort (sum of all UoW estimated_effort_hours)

### 5. Quality Requirements
- **Complete**: Include all items from YAML
- **Accurate**: Maintain exact IDs and references
- **Formatted**: Clean markdown with proper tables
- **Linked**: Ensure cross-references work
- **Statistics**: Include metadata from YAML

Generate the complete documentation following this structure.'''

    return prompt


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate Claude Code prompt for SSOT template generation')
    parser.add_argument('--input', type=str, required=True,
                       help='Input merged SSOT YAML file')
    parser.add_argument('--output', type=str, required=True,
                       help='Output SSOT markdown file')
    parser.add_argument('--project-name', type=str, default='Project',
                       help='Project name')
    parser.add_argument('--project-description', type=str, default='',
                       help='Project description')

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # Generate prompt
    prompt = generate_template_prompt(
        input_yaml=args.input,
        output_md=args.output,
        project_name=args.project_name,
        project_description=args.project_description
    )

    # Save prompt file
    prompt_file = Path("generate-ssot-template.prompt")
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    print(f"✅ Prompt generated: {prompt_file}")
    print(f"   Execute this prompt in Claude Code to generate SSOT documentation")
    print(f"   Input: {args.input}")
    print(f"   Output: {args.output}")


if __name__ == '__main__':
    main()