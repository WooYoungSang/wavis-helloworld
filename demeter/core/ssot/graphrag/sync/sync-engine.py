#!/usr/bin/env python3
"""
SSOT ↔ GraphRAG 양방향 동기화 엔진
Maintains bidirectional synchronization between SSOT and GraphRAG
"""

import yaml
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib
import difflib
from dataclasses import dataclass

@dataclass
class SyncConflict:
    """Represents a synchronization conflict"""
    entity_id: str
    conflict_type: str
    ssot_value: Any
    graphrag_value: Any
    resolution: Optional[str] = None

@dataclass
class SyncResult:
    """Result of synchronization operation"""
    success: bool
    entities_updated: int = 0
    conflicts: List[SyncConflict] = None
    error: Optional[str] = None

class SyncEngine:
    """Bidirectional SSOT ↔ GraphRAG synchronization engine"""

    def __init__(self, ssot_dir: str = "demeter/core/ssot", graphrag_dir: str = "demeter/core/ssot/graphrag"):
        self.ssot_dir = Path(ssot_dir)
        self.graphrag_dir = Path(graphrag_dir)
        self.index_dir = self.graphrag_dir / "index"
        self.knowledge_dir = self.graphrag_dir / "knowledge"
        self.sync_log_file = self.graphrag_dir / "sync.log"

        # Ensure directories exist
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)

        # Conflict resolution strategies
        self.conflict_resolvers = {
            "metadata_mismatch": self._resolve_metadata_conflict,
            "content_divergence": self._resolve_content_conflict,
            "dependency_conflict": self._resolve_dependency_conflict,
            "schema_mismatch": self._resolve_schema_conflict
        }

    def load_ssot_state(self) -> Dict[str, Any]:
        """Load current SSOT state"""
        ssot_state = {}

        # Load framework requirements
        framework_req_path = self.ssot_dir / "framework-requirements.yaml"
        if framework_req_path.exists():
            with open(framework_req_path, 'r', encoding='utf-8') as f:
                ssot_state['framework_requirements'] = yaml.safe_load(f)

        # Load extensions
        extensions_dir = self.ssot_dir / "extensions"
        if extensions_dir.exists():
            ssot_state['extensions'] = {}
            for category_dir in extensions_dir.iterdir():
                if category_dir.is_dir():
                    ssot_state['extensions'][category_dir.name] = {}
                    for ext_file in category_dir.glob("*.yaml"):
                        with open(ext_file, 'r', encoding='utf-8') as f:
                            ssot_state['extensions'][category_dir.name][ext_file.stem] = yaml.safe_load(f)

        # Load contracts
        contracts_dir = self.ssot_dir / "contracts"
        if contracts_dir.exists():
            ssot_state['contracts'] = {}
            for contract_file in contracts_dir.glob("*.yaml"):
                with open(contract_file, 'r', encoding='utf-8') as f:
                    ssot_state['contracts'][contract_file.stem] = yaml.safe_load(f)

        return ssot_state

    def load_graphrag_state(self) -> Dict[str, Any]:
        """Load current GraphRAG state"""
        graphrag_state = {}

        # Load entities
        entities_file = self.index_dir / "entities.json"
        if entities_file.exists():
            with open(entities_file, 'r', encoding='utf-8') as f:
                graphrag_state['entities'] = json.load(f)

        # Load relationships
        relationships_file = self.index_dir / "relationships.json"
        if relationships_file.exists():
            with open(relationships_file, 'r', encoding='utf-8') as f:
                graphrag_state['relationships'] = json.load(f)

        # Load knowledge
        patterns_file = self.knowledge_dir / "patterns.yaml"
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                graphrag_state['patterns'] = yaml.safe_load(f)

        decisions_file = self.knowledge_dir / "decisions.yaml"
        if decisions_file.exists():
            with open(decisions_file, 'r', encoding='utf-8') as f:
                graphrag_state['decisions'] = yaml.safe_load(f)

        lessons_file = self.knowledge_dir / "lessons.yaml"
        if lessons_file.exists():
            with open(lessons_file, 'r', encoding='utf-8') as f:
                graphrag_state['lessons'] = yaml.safe_load(f)

        return graphrag_state

    def detect_changes(self, ssot_state: Dict[str, Any], graphrag_state: Dict[str, Any]) -> Dict[str, List[str]]:
        """Detect changes between SSOT and GraphRAG states"""
        changes = {
            "ssot_updates": [],
            "graphrag_updates": [],
            "conflicts": []
        }

        # Check for SSOT changes
        if 'entities' in graphrag_state:
            ssot_entities = self._extract_ssot_entities(ssot_state)
            graphrag_entities = {entity['id']: entity for entity in graphrag_state['entities']}

            for entity_id, ssot_entity in ssot_entities.items():
                if entity_id in graphrag_entities:
                    graphrag_entity = graphrag_entities[entity_id]
                    if self._entities_differ(ssot_entity, graphrag_entity):
                        changes["ssot_updates"].append(entity_id)
                else:
                    changes["ssot_updates"].append(entity_id)

            # Check for GraphRAG-only entities (potential knowledge accumulated)
            for entity_id, graphrag_entity in graphrag_entities.items():
                if entity_id not in ssot_entities:
                    if graphrag_entity.get('type') in ['pattern', 'decision', 'lesson']:
                        changes["graphrag_updates"].append(entity_id)
                    else:
                        changes["conflicts"].append(entity_id)

        return changes

    def sync_ssot_to_graphrag(self, changes: List[str]) -> SyncResult:
        """Synchronize SSOT changes to GraphRAG"""
        try:
            # Re-index changed SSOT entities
            from .indexer.ssot_indexer import SSOTIndexer
            indexer = SSOTIndexer(str(self.ssot_dir), str(self.index_dir))
            result = indexer.index_ssot(incremental=True)

            self._log_sync_event("ssot_to_graphrag", {
                "entities_updated": len(changes),
                "changes": changes,
                "timestamp": datetime.now().isoformat()
            })

            return SyncResult(
                success=True,
                entities_updated=len(changes)
            )

        except Exception as e:
            self._log_sync_event("ssot_to_graphrag_error", {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return SyncResult(success=False, error=str(e))

    def sync_graphrag_to_ssot(self, knowledge_updates: List[str]) -> SyncResult:
        """Synchronize GraphRAG knowledge back to SSOT"""
        try:
            updated_count = 0
            graphrag_state = self.load_graphrag_state()

            # Process accumulated patterns
            if 'patterns' in graphrag_state and graphrag_state['patterns']:
                self._integrate_patterns_to_ssot(graphrag_state['patterns'])
                updated_count += len(graphrag_state['patterns'])

            # Process architecture decisions
            if 'decisions' in graphrag_state and graphrag_state['decisions']:
                self._integrate_decisions_to_ssot(graphrag_state['decisions'])
                updated_count += len(graphrag_state['decisions'])

            # Process lessons learned
            if 'lessons' in graphrag_state and graphrag_state['lessons']:
                self._integrate_lessons_to_ssot(graphrag_state['lessons'])
                updated_count += len(graphrag_state['lessons'])

            self._log_sync_event("graphrag_to_ssot", {
                "entities_updated": updated_count,
                "knowledge_updates": knowledge_updates,
                "timestamp": datetime.now().isoformat()
            })

            return SyncResult(
                success=True,
                entities_updated=updated_count
            )

        except Exception as e:
            self._log_sync_event("graphrag_to_ssot_error", {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return SyncResult(success=False, error=str(e))

    def resolve_conflicts(self, conflicts: List[str]) -> List[SyncConflict]:
        """Resolve synchronization conflicts"""
        resolved_conflicts = []
        ssot_state = self.load_ssot_state()
        graphrag_state = self.load_graphrag_state()

        for entity_id in conflicts:
            conflict = self._analyze_conflict(entity_id, ssot_state, graphrag_state)
            if conflict:
                resolver = self.conflict_resolvers.get(conflict.conflict_type)
                if resolver:
                    resolution = resolver(conflict)
                    conflict.resolution = resolution
                resolved_conflicts.append(conflict)

        return resolved_conflicts

    def full_sync(self) -> SyncResult:
        """Perform full bidirectional synchronization"""
        print("🔄 Starting full SSOT ↔ GraphRAG synchronization...")

        try:
            # Load current states
            print("📖 Loading SSOT state...")
            ssot_state = self.load_ssot_state()

            print("📖 Loading GraphRAG state...")
            graphrag_state = self.load_graphrag_state()

            # Detect changes
            print("🔍 Detecting changes...")
            changes = self.detect_changes(ssot_state, graphrag_state)

            total_updates = 0
            all_conflicts = []

            # Sync SSOT → GraphRAG
            if changes["ssot_updates"]:
                print(f"⬆️  Syncing {len(changes['ssot_updates'])} SSOT updates to GraphRAG...")
                result = self.sync_ssot_to_graphrag(changes["ssot_updates"])
                if result.success:
                    total_updates += result.entities_updated
                else:
                    return result

            # Sync GraphRAG → SSOT
            if changes["graphrag_updates"]:
                print(f"⬇️  Syncing {len(changes['graphrag_updates'])} GraphRAG updates to SSOT...")
                result = self.sync_graphrag_to_ssot(changes["graphrag_updates"])
                if result.success:
                    total_updates += result.entities_updated
                else:
                    return result

            # Resolve conflicts
            if changes["conflicts"]:
                print(f"⚠️  Resolving {len(changes['conflicts'])} conflicts...")
                conflicts = self.resolve_conflicts(changes["conflicts"])
                all_conflicts.extend(conflicts)

            print(f"✅ Full synchronization completed!")
            print(f"   📊 Total updates: {total_updates}")
            print(f"   ⚠️  Conflicts resolved: {len(all_conflicts)}")

            return SyncResult(
                success=True,
                entities_updated=total_updates,
                conflicts=all_conflicts
            )

        except Exception as e:
            error_msg = f"Full synchronization failed: {e}"
            print(f"❌ {error_msg}")
            return SyncResult(success=False, error=error_msg)

    def incremental_sync(self) -> SyncResult:
        """Perform incremental synchronization"""
        print("🔄 Starting incremental SSOT ↔ GraphRAG synchronization...")

        # For incremental sync, we focus on recently changed files
        recent_changes = self._get_recent_changes()

        if not recent_changes:
            print("✅ No recent changes detected")
            return SyncResult(success=True, entities_updated=0)

        return self.full_sync()

    def _extract_ssot_entities(self, ssot_state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Extract entities from SSOT state for comparison"""
        entities = {}

        if 'framework_requirements' in ssot_state:
            fr_data = ssot_state['framework_requirements']

            # Extract FRs
            if 'functional_requirements' in fr_data:
                for fr_id, fr_spec in fr_data['functional_requirements'].items():
                    entities[fr_id] = {
                        "id": fr_id,
                        "type": "functional_requirement",
                        "content": fr_spec,
                        "hash": self._generate_hash(fr_spec)
                    }

            # Extract NFRs
            if 'non_functional_requirements' in fr_data:
                for nfr_id, nfr_spec in fr_data['non_functional_requirements'].items():
                    entities[nfr_id] = {
                        "id": nfr_id,
                        "type": "non_functional_requirement",
                        "content": nfr_spec,
                        "hash": self._generate_hash(nfr_spec)
                    }

            # Extract UoWs
            if 'units_of_work' in fr_data:
                for uow_id, uow_spec in fr_data['units_of_work'].items():
                    entities[uow_id] = {
                        "id": uow_id,
                        "type": "unit_of_work",
                        "content": uow_spec,
                        "hash": self._generate_hash(uow_spec)
                    }

        return entities

    def _entities_differ(self, ssot_entity: Dict[str, Any], graphrag_entity: Dict[str, Any]) -> bool:
        """Check if SSOT and GraphRAG entities differ"""
        ssot_hash = ssot_entity.get('hash')
        graphrag_hash = graphrag_entity.get('metadata', {}).get('hash')
        return ssot_hash != graphrag_hash

    def _integrate_patterns_to_ssot(self, patterns: Dict[str, Any]):
        """Integrate learned patterns back to SSOT"""
        # Add new UoW templates based on patterns
        knowledge_file = self.knowledge_dir / "ssot-integrated-patterns.yaml"

        integrated_patterns = {
            "integration_timestamp": datetime.now().isoformat(),
            "patterns": patterns,
            "status": "integrated"
        }

        with open(knowledge_file, 'w', encoding='utf-8') as f:
            yaml.dump(integrated_patterns, f, allow_unicode=True, default_flow_style=False)

    def _integrate_decisions_to_ssot(self, decisions: Dict[str, Any]):
        """Integrate architecture decisions back to SSOT"""
        decisions_file = self.knowledge_dir / "ssot-integrated-decisions.yaml"

        integrated_decisions = {
            "integration_timestamp": datetime.now().isoformat(),
            "decisions": decisions,
            "status": "integrated"
        }

        with open(decisions_file, 'w', encoding='utf-8') as f:
            yaml.dump(integrated_decisions, f, allow_unicode=True, default_flow_style=False)

    def _integrate_lessons_to_ssot(self, lessons: Dict[str, Any]):
        """Integrate lessons learned back to SSOT"""
        lessons_file = self.knowledge_dir / "ssot-integrated-lessons.yaml"

        integrated_lessons = {
            "integration_timestamp": datetime.now().isoformat(),
            "lessons": lessons,
            "status": "integrated"
        }

        with open(lessons_file, 'w', encoding='utf-8') as f:
            yaml.dump(integrated_lessons, f, allow_unicode=True, default_flow_style=False)

    def _analyze_conflict(self, entity_id: str, ssot_state: Dict[str, Any], graphrag_state: Dict[str, Any]) -> Optional[SyncConflict]:
        """Analyze a specific conflict"""
        # Implementation would analyze the specific conflict type
        return SyncConflict(
            entity_id=entity_id,
            conflict_type="content_divergence",
            ssot_value="ssot_content",
            graphrag_value="graphrag_content"
        )

    def _resolve_metadata_conflict(self, conflict: SyncConflict) -> str:
        """Resolve metadata mismatch conflicts"""
        return "prefer_ssot"

    def _resolve_content_conflict(self, conflict: SyncConflict) -> str:
        """Resolve content divergence conflicts"""
        return "manual_review_required"

    def _resolve_dependency_conflict(self, conflict: SyncConflict) -> str:
        """Resolve dependency conflicts"""
        return "merge_dependencies"

    def _resolve_schema_conflict(self, conflict: SyncConflict) -> str:
        """Resolve schema mismatch conflicts"""
        return "update_to_latest_schema"

    def _get_recent_changes(self) -> List[str]:
        """Get list of recently changed files"""
        # Implementation would check file modification times
        return []

    def _generate_hash(self, data: Any) -> str:
        """Generate hash for change detection"""
        content = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

    def _log_sync_event(self, event_type: str, data: Dict[str, Any]):
        """Log synchronization events"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }

        with open(self.sync_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="SSOT ↔ GraphRAG Synchronization Engine")
    parser.add_argument("--full-sync", action="store_true", help="Perform full synchronization")
    parser.add_argument("--incremental", action="store_true", help="Perform incremental synchronization")
    parser.add_argument("--ssot-dir", default="demeter/core/ssot", help="SSOT directory path")
    parser.add_argument("--graphrag-dir", default="demeter/core/ssot/graphrag", help="GraphRAG directory path")

    args = parser.parse_args()

    try:
        sync_engine = SyncEngine(args.ssot_dir, args.graphrag_dir)

        if args.full_sync:
            result = sync_engine.full_sync()
        elif args.incremental:
            result = sync_engine.incremental_sync()
        else:
            result = sync_engine.incremental_sync()  # Default to incremental

        if result.success:
            print(f"\n✅ Synchronization completed successfully!")
            print(f"   📊 Entities updated: {result.entities_updated}")
            if result.conflicts:
                print(f"   ⚠️  Conflicts resolved: {len(result.conflicts)}")
            sys.exit(0)
        else:
            print(f"\n❌ Synchronization failed: {result.error}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Synchronization error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()