#!/usr/bin/env python3
"""
⚠️  DEPRECATED: Natural Language to SSOT Prompt Generator
⚠️  This script is deprecated. Use nlp-to-ssot.prompt.template in Claude Code instead.
⚠️
⚠️  Migration Path:
⚠️  1. Use demeter/core/prompts/templates/nlp-to-ssot.prompt.template
⚠️  2. Benefits: Constitutional compliance, AI-enhanced analysis, SDD integration
⚠️  3. See demeter/core/ssot/tools/README.md for migration guide

DEPRECATED: Generates a Claude Code prompt for converting natural language requirements to SSOT

Legacy Usage:
    python nlp-to-custom-ssot.py --input requirements.md --project-name "MyProject" --domain "E-Commerce"

Recommended Usage:
    Use nlp-to-ssot.prompt.template in Claude Code with constitutional compliance and AI enhancement
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

def generate_conversion_prompt(requirements_file: Path, project_name: str, domain: str) -> str:
    """Generate Claude Code prompt for NLP to SSOT conversion"""

    # Read requirements
    try:
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements_content = f.read()
    except FileNotFoundError:
        print(f"Error: Requirements file not found: {requirements_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading requirements file: {e}")
        sys.exit(1)

    prompt = f'''# Natural Language to Custom SSOT Conversion

## Project Context
- **Project**: {project_name}
- **Domain**: {domain}
- **Input**: {requirements_file.name}

## Natural Language Requirements
```markdown
{requirements_content}
```

## Task: Convert to Custom SSOT YAML

Create `demeter/core/ssot/custom/{project_name.lower().replace(' ', '-')}.yaml` with the following structure:

```yaml
extends: "{domain.lower()}"
custom: "{project_name.lower().replace(' ', '-')}"

functional_requirements:
  FR-CUSTOM-001:
    name: "Extracted Requirement Name"
    description: "Full description from natural language"
    priority: "Critical|High|Medium|Low"  # Infer from language
    business_value: "Business value statement"
    acceptance_criteria:
      - "Specific testable criterion"
      - "Another testable criterion"
    tags: ["custom", "domain-specific"]

non_functional_requirements:
  NFR-CUSTOM-001:
    name: "Quality Attribute Name"
    category: "Performance|Security|Usability|Reliability"
    measurement_criteria:
      - "Measurable criteria"
    testing_method: "Testing approach"
    priority: "Critical|High|Medium|Low"
    tags: ["custom", "quality"]

units_of_work:
  UoW-CUSTOM-301:
    name: "Implementation Task Name"
    goal: "Clear implementation objective"
    layer: "Application|Infrastructure|Integration|Deployment"
    priority: "Critical|High|Medium|Low"
    dependencies: ["UoW-XXX"]  # Reference existing UoWs if needed
    implements: ["FR-CUSTOM-001", "NFR-CUSTOM-001"]
    estimated_effort_hours: "24"
    acceptance_criteria:
      - "Specific deliverable"
      - "Testing requirement"
    tags: ["custom", "implementation"]

metadata:
  version: "1.0.0"
  created: "{datetime.now().strftime('%Y-%m-%d')}"
  description: "Custom SSOT for {project_name}"
  generated_from: "Natural language requirements"
```

## Analysis Guidelines

### Functional Requirements Detection:
- **Action patterns**: "Users should/must/can...", "System allows/enables..."
- **User stories**: "As a [actor], I want [action] so that [benefit]"
- **Features**: Bullet points describing capabilities
- **Business rules**: Domain-specific constraints

### Priority Inference:
- **Critical**: "critical", "essential", "must", "required", "mandatory"
- **High**: "important", "should", "high priority"
- **Medium**: Default for most requirements
- **Low**: "nice to have", "could", "optional", "enhancement"

### Non-Functional Requirements Detection:
- **Performance**: Response time (ms), throughput (rps), load (users)
- **Security**: Encryption, authentication, compliance (GDPR, PCI, HIPAA)
- **Scalability**: Auto-scaling, peak traffic, concurrent users
- **Reliability**: Uptime %, error rates, recovery time

### Units of Work Grouping:
- **User Management**: Authentication, profiles, accounts
- **Data Management**: CRUD operations, storage, retrieval
- **Search/Discovery**: Search, filtering, recommendations
- **Integration**: APIs, external services, third-party
- **Business Logic**: Core domain functionality
- **Security**: Authentication, authorization, compliance

## Output Requirements:
1. **Comprehensive**: Cover all requirements from natural language
2. **Structured**: Proper YAML format with consistent IDs
3. **Traceable**: Clear mapping from natural language to structured format
4. **Testable**: Specific acceptance criteria for each requirement
5. **Prioritized**: Realistic priority assignments based on language

Create the complete YAML file following this structure.'''

    return prompt


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate Claude Code prompt for NLP to SSOT conversion')
    parser.add_argument('--input', type=str, required=True,
                       help='Input requirements markdown file')
    parser.add_argument('--project-name', type=str, required=True,
                       help='Project name')
    parser.add_argument('--domain', type=str, default='general',
                       help='Project domain (e-commerce, fintech, etc.)')

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()

    # Generate prompt
    requirements_file = Path(args.input)
    prompt = generate_conversion_prompt(requirements_file, args.project_name, args.domain)

    # Save prompt file
    prompt_file = requirements_file.parent / f"convert-{requirements_file.stem}-to-ssot.prompt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    print(f"✅ Prompt generated: {prompt_file}")
    print(f"   Execute this prompt in Claude Code to convert requirements to SSOT")
    print(f"   Output will be: demeter/core/ssot/custom/{args.project_name.lower().replace(' ', '-')}.yaml")


if __name__ == '__main__':
    main()