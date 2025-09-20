#!/usr/bin/env python3
"""
SSOT → GraphRAG Indexer
Converts SSOT YAML data into GraphRAG-compatible format for indexing
"""

import yaml
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

class SSOTIndexer:
    """Indexes SSOT data into GraphRAG format"""

    def __init__(self, ssot_dir: str = "demeter/core/ssot", output_dir: str = "demeter/core/ssot/graphrag/index"):
        self.ssot_dir = Path(ssot_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # GraphRAG entity types
        self.entity_types = {
            "FUNCTIONAL_REQUIREMENT": "functional_requirement",
            "NON_FUNCTIONAL_REQUIREMENT": "non_functional_requirement",
            "UNIT_OF_WORK": "unit_of_work",
            "CONTRACT": "contract",
            "BDD_SCENARIO": "bdd_scenario",
            "EXTENSION": "extension",
            "DEPENDENCY": "dependency"
        }

        # Relationship types
        self.relationship_types = {
            "IMPLEMENTS": "implements",
            "DEPENDS_ON": "depends_on",
            "EXTENDS": "extends",
            "VALIDATES": "validates",
            "COVERS": "covers",
            "CONFLICTS_WITH": "conflicts_with"
        }

    def load_ssot_data(self) -> Dict[str, Any]:
        """Load all SSOT YAML files"""
        ssot_data = {}

        # Load main framework requirements
        framework_req_path = self.ssot_dir / "framework-requirements.yaml"
        if framework_req_path.exists():
            with open(framework_req_path, 'r', encoding='utf-8') as f:
                ssot_data['framework_requirements'] = yaml.safe_load(f)

        # Load extensions
        extensions_dir = self.ssot_dir / "extensions"
        if extensions_dir.exists():
            ssot_data['extensions'] = {}
            for category_dir in extensions_dir.iterdir():
                if category_dir.is_dir():
                    ssot_data['extensions'][category_dir.name] = {}
                    for ext_file in category_dir.glob("*.yaml"):
                        with open(ext_file, 'r', encoding='utf-8') as f:
                            ssot_data['extensions'][category_dir.name][ext_file.stem] = yaml.safe_load(f)

        # Load contracts
        contracts_dir = self.ssot_dir / "contracts"
        if contracts_dir.exists():
            ssot_data['contracts'] = {}
            for contract_file in contracts_dir.glob("*.yaml"):
                with open(contract_file, 'r', encoding='utf-8') as f:
                    ssot_data['contracts'][contract_file.stem] = yaml.safe_load(f)

        # Load base definitions
        base_dir = self.ssot_dir / "base"
        if base_dir.exists():
            ssot_data['base'] = {}
            for base_file in base_dir.glob("*.yaml"):
                with open(base_file, 'r', encoding='utf-8') as f:
                    ssot_data['base'][base_file.stem] = yaml.safe_load(f)

        return ssot_data

    def extract_entities(self, ssot_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract entities from SSOT data"""
        entities = []

        # Extract Functional Requirements
        if 'framework_requirements' in ssot_data:
            fr_data = ssot_data['framework_requirements']
            if 'functional_requirements' in fr_data:
                for fr_id, fr_spec in fr_data['functional_requirements'].items():
                    entity = {
                        "id": fr_id,
                        "type": self.entity_types["FUNCTIONAL_REQUIREMENT"],
                        "title": fr_spec.get('title', ''),
                        "description": fr_spec.get('description', ''),
                        "category": fr_spec.get('category', ''),
                        "priority": fr_spec.get('priority', ''),
                        "acceptance_criteria": fr_spec.get('acceptance_criteria', []),
                        "metadata": {
                            "source": "framework_requirements",
                            "last_updated": datetime.now().isoformat(),
                            "hash": self._generate_hash(fr_spec)
                        }
                    }
                    entities.append(entity)

            # Extract Non-Functional Requirements
            if 'non_functional_requirements' in fr_data:
                for nfr_id, nfr_spec in fr_data['non_functional_requirements'].items():
                    entity = {
                        "id": nfr_id,
                        "type": self.entity_types["NON_FUNCTIONAL_REQUIREMENT"],
                        "title": nfr_spec.get('title', ''),
                        "description": nfr_spec.get('description', ''),
                        "category": nfr_spec.get('category', ''),
                        "priority": nfr_spec.get('priority', ''),
                        "requirements": nfr_spec.get('requirements', []),
                        "measurement": nfr_spec.get('measurement', ''),
                        "metadata": {
                            "source": "framework_requirements",
                            "last_updated": datetime.now().isoformat(),
                            "hash": self._generate_hash(nfr_spec)
                        }
                    }
                    entities.append(entity)

            # Extract Units of Work
            if 'units_of_work' in fr_data:
                for uow_id, uow_spec in fr_data['units_of_work'].items():
                    entity = {
                        "id": uow_id,
                        "type": self.entity_types["UNIT_OF_WORK"],
                        "name": uow_spec.get('name', ''),
                        "goal": uow_spec.get('goal', ''),
                        "layer": uow_spec.get('layer', ''),
                        "priority": uow_spec.get('priority', ''),
                        "effort": uow_spec.get('effort', ''),
                        "implements": uow_spec.get('implements', []),
                        "dependencies": uow_spec.get('dependencies', []),
                        "acceptance_criteria": uow_spec.get('acceptance_criteria', []),
                        "metadata": {
                            "source": "framework_requirements",
                            "last_updated": datetime.now().isoformat(),
                            "hash": self._generate_hash(uow_spec)
                        }
                    }
                    entities.append(entity)

        # Extract Contracts
        if 'contracts' in ssot_data:
            for contract_id, contract_spec in ssot_data['contracts'].items():
                entity = {
                    "id": contract_spec.get('contract_id', contract_id),
                    "type": self.entity_types["CONTRACT"],
                    "title": contract_spec.get('title', ''),
                    "applies_to": contract_spec.get('applies_to', {}),
                    "preconditions": contract_spec.get('preconditions', []),
                    "postconditions": contract_spec.get('postconditions', []),
                    "invariants": contract_spec.get('invariants', []),
                    "performance": contract_spec.get('performance', {}),
                    "security": contract_spec.get('security', {}),
                    "metadata": {
                        "source": f"contracts/{contract_id}",
                        "last_updated": datetime.now().isoformat(),
                        "hash": self._generate_hash(contract_spec)
                    }
                }
                entities.append(entity)

        # Extract Extensions
        if 'extensions' in ssot_data:
            for category, extensions in ssot_data['extensions'].items():
                for ext_name, ext_spec in extensions.items():
                    entity = {
                        "id": f"{category}_{ext_name}",
                        "type": self.entity_types["EXTENSION"],
                        "name": ext_spec.get('name', ext_name),
                        "category": category,
                        "description": ext_spec.get('description', ''),
                        "functional_requirements": ext_spec.get('functional_requirements', {}),
                        "non_functional_requirements": ext_spec.get('non_functional_requirements', {}),
                        "units_of_work": ext_spec.get('units_of_work', {}),
                        "metadata": {
                            "source": f"extensions/{category}/{ext_name}",
                            "last_updated": datetime.now().isoformat(),
                            "hash": self._generate_hash(ext_spec)
                        }
                    }
                    entities.append(entity)

        return entities

    def extract_relationships(self, ssot_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract relationships from SSOT data"""
        relationships = []

        # Extract UoW → FR/NFR relationships
        if 'framework_requirements' in ssot_data:
            fr_data = ssot_data['framework_requirements']
            if 'units_of_work' in fr_data:
                for uow_id, uow_spec in fr_data['units_of_work'].items():
                    implements = uow_spec.get('implements', [])
                    for req_id in implements:
                        relationship = {
                            "source": uow_id,
                            "target": req_id,
                            "type": self.relationship_types["IMPLEMENTS"],
                            "metadata": {
                                "created": datetime.now().isoformat(),
                                "source_file": "framework_requirements"
                            }
                        }
                        relationships.append(relationship)

                    # Extract dependencies
                    dependencies = uow_spec.get('dependencies', [])
                    for dep_id in dependencies:
                        relationship = {
                            "source": uow_id,
                            "target": dep_id,
                            "type": self.relationship_types["DEPENDS_ON"],
                            "metadata": {
                                "created": datetime.now().isoformat(),
                                "source_file": "framework_requirements"
                            }
                        }
                        relationships.append(relationship)

        # Extract Contract → UoW relationships
        if 'contracts' in ssot_data:
            for contract_id, contract_spec in ssot_data['contracts'].items():
                applies_to = contract_spec.get('applies_to', {})
                if applies_to.get('entity_type') == 'uow':
                    entity_name = applies_to.get('entity_name')
                    if entity_name:
                        relationship = {
                            "source": contract_spec.get('contract_id', contract_id),
                            "target": entity_name,
                            "type": self.relationship_types["VALIDATES"],
                            "metadata": {
                                "created": datetime.now().isoformat(),
                                "source_file": f"contracts/{contract_id}"
                            }
                        }
                        relationships.append(relationship)

        return relationships

    def _generate_hash(self, data: Any) -> str:
        """Generate hash for change detection"""
        content = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

    def save_graphrag_data(self, entities: List[Dict[str, Any]], relationships: List[Dict[str, Any]]):
        """Save data in GraphRAG format"""

        # Save entities
        entities_file = self.output_dir / "entities.json"
        with open(entities_file, 'w', encoding='utf-8') as f:
            json.dump(entities, f, ensure_ascii=False, indent=2)

        # Save relationships
        relationships_file = self.output_dir / "relationships.json"
        with open(relationships_file, 'w', encoding='utf-8') as f:
            json.dump(relationships, f, ensure_ascii=False, indent=2)

        # Save metadata
        metadata = {
            "indexed_at": datetime.now().isoformat(),
            "total_entities": len(entities),
            "total_relationships": len(relationships),
            "entity_types": {entity_type: len([e for e in entities if e['type'] == entity_type])
                           for entity_type in self.entity_types.values()},
            "relationship_types": {rel_type: len([r for r in relationships if r['type'] == rel_type])
                                 for rel_type in self.relationship_types.values()}
        }

        metadata_file = self.output_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"✅ GraphRAG data saved:")
        print(f"   📄 Entities: {len(entities)} ({entities_file})")
        print(f"   🔗 Relationships: {len(relationships)} ({relationships_file})")
        print(f"   📊 Metadata: {metadata_file}")

    def index_ssot(self, incremental: bool = False):
        """Main indexing function"""
        print("🚀 Starting SSOT → GraphRAG indexing...")

        # Load SSOT data
        print("📖 Loading SSOT data...")
        ssot_data = self.load_ssot_data()

        # Extract entities and relationships
        print("🔍 Extracting entities...")
        entities = self.extract_entities(ssot_data)

        print("🔗 Extracting relationships...")
        relationships = self.extract_relationships(ssot_data)

        # Save to GraphRAG format
        print("💾 Saving GraphRAG data...")
        self.save_graphrag_data(entities, relationships)

        print("🎉 SSOT indexing completed successfully!")

        return {
            "entities_count": len(entities),
            "relationships_count": len(relationships),
            "status": "success"
        }

def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Index SSOT data into GraphRAG format")
    parser.add_argument("--ssot-dir", default="demeter/core/ssot", help="SSOT directory path")
    parser.add_argument("--output-dir", default="demeter/core/ssot/graphrag/index", help="Output directory")
    parser.add_argument("--incremental", action="store_true", help="Incremental indexing (only changed items)")

    args = parser.parse_args()

    try:
        indexer = SSOTIndexer(args.ssot_dir, args.output_dir)
        result = indexer.index_ssot(incremental=args.incremental)
        print(f"\n✅ Indexing completed: {result}")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Indexing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()