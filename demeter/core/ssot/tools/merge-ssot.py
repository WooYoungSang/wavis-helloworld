#!/usr/bin/env python3
"""
⚠️  DEPRECATED: SSOT Merge Prompt Generator
⚠️  This script is deprecated. Use ssot-merge.prompt.template in Claude Code instead.
⚠️
⚠️  Migration Path:
⚠️  1. Use demeter/core/prompts/templates/ssot-merge.prompt.template
⚠️  2. Benefits: Constitutional compliance, GraphRAG integration, SDD support
⚠️  3. See demeter/core/ssot/tools/README.md for migration guide

DEPRECATED: Generates a Claude Code prompt for merging SSOT base with extensions

Legacy Usage:
    python merge-ssot.py --base demeter/core/ssot/base --extensions domain/e-commerce.yaml --output merged-ssot.yaml --project-name "MyShop"

Recommended Usage:
    Use ssot-merge.prompt.template in Claude Code with constitutional compliance and GraphRAG integration
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import List


def generate_merge_prompt(base_dir: Path, extensions: List[str], output: str,
                         project_name: str) -> str:
    """Generate Claude Code prompt for SSOT merging"""

    # List base files
    base_files = [
        f"{base_dir}/fr-base.yaml",
        f"{base_dir}/nfr-base.yaml",
        f"{base_dir}/uow-base.yaml"
    ]

    # Extension list with proper paths
    extension_paths = []
    for ext in extensions:
        if not ext.startswith('/') and not ext.startswith('demeter/'):
            # Relative extension path
            ext_path = f"{base_dir.parent}/extensions/{ext}"
        else:
            ext_path = ext
        extension_paths.append(ext_path)

    prompt = f'''# SSOT Merge Operation

## Project Context
- **Project**: {project_name}
- **Output**: {output}
- **Timestamp**: {datetime.now().isoformat()}

## Base SSOT Files to Load
{chr(10).join(f"- `{file}`" for file in base_files)}

## Extension Files to Merge
{chr(10).join(f"- `{ext}`" for ext in extension_paths)}

## Merge Tasks

### 1. Load Base SSOT
Load and combine all base YAML files:
- Read `fr-base.yaml` → extract `functional_requirements` section
- Read `nfr-base.yaml` → extract `non_functional_requirements` section
- Read `uow-base.yaml` → extract `units_of_work` section
- Combine metadata from all files

### 2. Process Extensions
For each extension file:
- Load the YAML content
- Check for ID conflicts with existing items
- Resolve conflicts using extension prefixes:
  - e-commerce → ECOMMERC prefix
  - fintech → FINTECH prefix
  - healthcare → HEALTH prefix
  - ai-ml → AIML prefix
  - gdpr → GDPR prefix

### 3. ID Conflict Resolution
When merging, if an ID already exists:
```
Original: FR-001 (base)
Conflict: FR-001 (extension)
→ Rename to: FR-ECOMMERC-001
```

Track all ID changes for dependency updates.

### 4. Update Dependencies
After merging, update all dependency references:
- In `dependencies` arrays
- In `implements` arrays
- Replace old IDs with new IDs from conflict resolution

### 5. Validation
Verify the merged SSOT:
- All dependencies point to existing IDs
- No circular dependencies
- All implements references are valid
- UoW layers are properly structured

### 6. Generate Statistics
Calculate and include:
```yaml
metadata:
  project_name: "{project_name}"
  merge_timestamp: "{datetime.now().isoformat()}"
  extensions_merged: {extensions}
  statistics:
    total_functional_requirements: N
    total_non_functional_requirements: N
    total_units_of_work: N
    id_conflicts_resolved: N
    fr_by_priority:
      Critical: N
      High: N
      Medium: N
      Low: N
    uow_by_layer:
      Foundation: N
      Infrastructure: N
      Application: N
      Integration: N
      Deployment: N
    estimated_total_effort_hours: N
```

## Output Format
Save as `{output}` with complete merged SSOT structure:

```yaml
functional_requirements:
  FR-001: {{base FR data}}
  FR-ECOMMERC-001: {{extension FR data}}

non_functional_requirements:
  NFR-001: {{base NFR data}}
  NFR-GDPR-001: {{extension NFR data}}

units_of_work:
  UoW-001: {{base UoW data}}
  UoW-ECOMMERC-301: {{extension UoW data}}

metadata:
  {{combined metadata with statistics}}
```

## Merge Rules
1. **Base Priority**: Base requirements take precedence for ID conflicts
2. **Extension Prefixing**: Extensions get prefixed IDs to avoid conflicts
3. **Dependency Updates**: All references updated after ID changes
4. **Metadata Combination**: Merge all metadata, with statistics added
5. **Validation**: Ensure all cross-references are valid after merge

Complete the merge operation and save the result to `{output}`.'''

    return prompt


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate Claude Code prompt for SSOT merging')
    parser.add_argument('--base', type=str, required=True,
                       help='Base SSOT directory path')
    parser.add_argument('--extensions', nargs='*', default=[],
                       help='Extension YAML files to merge')
    parser.add_argument('--output', type=str, required=True,
                       help='Output merged SSOT YAML file')
    parser.add_argument('--project-name', type=str, default='Project',
                       help='Project name')

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()

    # Validate base directory
    base_dir = Path(args.base)
    if not base_dir.exists():
        print(f"Error: Base directory not found: {base_dir}")
        sys.exit(1)

    # Generate prompt
    prompt = generate_merge_prompt(
        base_dir=base_dir,
        extensions=args.extensions,
        output=args.output,
        project_name=args.project_name
    )

    # Save prompt file
    prompt_file = Path("merge-ssot.prompt")
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    print(f"✅ Prompt generated: {prompt_file}")
    print(f"   Execute this prompt in Claude Code to merge SSOT files")
    print(f"   Output will be: {args.output}")
    print(f"   Extensions: {args.extensions}")


if __name__ == '__main__':
    main()