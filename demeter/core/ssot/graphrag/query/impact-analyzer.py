#!/usr/bin/env python3
"""
Impact Analysis Tool for SSOT Changes
Analyzes the impact of changes to SSOT entities across the entire system
"""

import yaml
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict, deque

@dataclass
class ImpactItem:
    """Single impact item"""
    entity_id: str
    entity_type: str
    impact_type: str
    severity: str
    description: str
    path: List[str]  # Path from source to this entity
    recommendations: List[str]

@dataclass
class ImpactReport:
    """Complete impact analysis report"""
    source_entity: str
    change_type: str
    analysis_timestamp: str
    direct_impacts: List[ImpactItem]
    indirect_impacts: List[ImpactItem]
    cascade_impacts: List[ImpactItem]
    risk_assessment: Dict[str, Any]
    mitigation_strategies: List[str]
    affected_layers: Set[str]
    testing_recommendations: List[str]

class ImpactAnalyzer:
    """Analyzes impact of changes across SSOT system"""

    def __init__(self, ssot_dir: str = "demeter/core/ssot", graphrag_dir: str = "demeter/core/ssot/graphrag"):
        self.ssot_dir = Path(ssot_dir)
        self.graphrag_dir = Path(graphrag_dir)
        self.index_dir = self.graphrag_dir / "index"

        # Load system data
        self.entities = self._load_entities()
        self.relationships = self._load_relationships()
        self.entity_index = {e['id']: e for e in self.entities}

        # Impact severity levels
        self.severity_levels = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }

        # Layer hierarchy (higher index = higher in dependency chain)
        self.layer_hierarchy = {
            "foundation": 0,
            "infrastructure": 1,
            "application": 2,
            "deployment": 3
        }

    def analyze_change_impact(self, entity_id: str, change_type: str = "modification") -> ImpactReport:
        """Perform comprehensive impact analysis for a change"""
        print(f"🔍 Analyzing impact of {change_type} to {entity_id}...")

        # Initialize report
        report = ImpactReport(
            source_entity=entity_id,
            change_type=change_type,
            analysis_timestamp=datetime.now().isoformat(),
            direct_impacts=[],
            indirect_impacts=[],
            cascade_impacts=[],
            risk_assessment={},
            mitigation_strategies=[],
            affected_layers=set(),
            testing_recommendations=[]
        )

        try:
            source_entity = self.entity_index.get(entity_id)
            if not source_entity:
                raise ValueError(f"Entity {entity_id} not found")

            # Phase 1: Direct impact analysis
            print("📊 Phase 1: Analyzing direct impacts...")
            direct_impacts = self._analyze_direct_impacts(entity_id, change_type)
            report.direct_impacts = direct_impacts

            # Phase 2: Indirect impact analysis
            print("🔄 Phase 2: Analyzing indirect impacts...")
            indirect_impacts = self._analyze_indirect_impacts(entity_id, direct_impacts)
            report.indirect_impacts = indirect_impacts

            # Phase 3: Cascade impact analysis
            print("🌊 Phase 3: Analyzing cascade impacts...")
            cascade_impacts = self._analyze_cascade_impacts(entity_id, direct_impacts + indirect_impacts)
            report.cascade_impacts = cascade_impacts

            # Phase 4: Risk assessment
            print("⚖️  Phase 4: Performing risk assessment...")
            risk_assessment = self._perform_risk_assessment(source_entity, report)
            report.risk_assessment = risk_assessment

            # Phase 5: Generate mitigation strategies
            print("🛡️  Phase 5: Generating mitigation strategies...")
            mitigation_strategies = self._generate_mitigation_strategies(report)
            report.mitigation_strategies = mitigation_strategies

            # Phase 6: Affected layers analysis
            print("🏗️  Phase 6: Analyzing affected layers...")
            affected_layers = self._analyze_affected_layers(report)
            report.affected_layers = affected_layers

            # Phase 7: Testing recommendations
            print("🧪 Phase 7: Generating testing recommendations...")
            testing_recommendations = self._generate_testing_recommendations(report)
            report.testing_recommendations = testing_recommendations

            print(f"✅ Impact analysis completed!")
            print(f"   📊 Direct impacts: {len(report.direct_impacts)}")
            print(f"   🔄 Indirect impacts: {len(report.indirect_impacts)}")
            print(f"   🌊 Cascade impacts: {len(report.cascade_impacts)}")
            print(f"   ⚖️  Risk level: {risk_assessment.get('overall_risk', 'unknown')}")

            return report

        except Exception as e:
            print(f"❌ Impact analysis failed: {e}")
            report.risk_assessment = {"error": str(e)}
            return report

    def generate_impact_matrix(self, entities: List[str]) -> Dict[str, Dict[str, str]]:
        """Generate impact matrix for multiple entities"""
        print(f"📋 Generating impact matrix for {len(entities)} entities...")

        impact_matrix = {}

        for source_entity in entities:
            impact_matrix[source_entity] = {}

            for target_entity in entities:
                if source_entity != target_entity:
                    impact_level = self._calculate_entity_impact(source_entity, target_entity)
                    impact_matrix[source_entity][target_entity] = impact_level

        print(f"✅ Impact matrix generated!")
        return impact_matrix

    def find_critical_dependencies(self) -> List[Dict[str, Any]]:
        """Find entities with critical dependencies"""
        print("🔍 Finding critical dependencies...")

        critical_deps = []

        # Analyze each entity's dependency count and importance
        for entity in self.entities:
            entity_id = entity['id']

            # Count incoming dependencies (entities that depend on this one)
            incoming_deps = [
                r for r in self.relationships
                if r.get('target') == entity_id and r.get('type') in ['depends_on', 'implements']
            ]

            # Count outgoing dependencies (entities this one depends on)
            outgoing_deps = [
                r for r in self.relationships
                if r.get('source') == entity_id and r.get('type') in ['depends_on']
            ]

            # Calculate criticality score
            criticality_score = self._calculate_criticality_score(entity, incoming_deps, outgoing_deps)

            if criticality_score >= 0.7:  # High criticality threshold
                critical_deps.append({
                    "entity": entity,
                    "criticality_score": criticality_score,
                    "incoming_dependencies": len(incoming_deps),
                    "outgoing_dependencies": len(outgoing_deps),
                    "risk_factors": self._identify_risk_factors(entity, incoming_deps, outgoing_deps)
                })

        # Sort by criticality score
        critical_deps.sort(key=lambda x: x['criticality_score'], reverse=True)

        print(f"✅ Found {len(critical_deps)} critical dependencies!")
        return critical_deps

    def simulate_entity_removal(self, entity_id: str) -> Dict[str, Any]:
        """Simulate the impact of removing an entity"""
        print(f"🎭 Simulating removal of {entity_id}...")

        simulation_result = {
            "removed_entity": entity_id,
            "broken_relationships": [],
            "orphaned_entities": [],
            "cascade_removals": [],
            "affected_contracts": [],
            "affected_bdd_scenarios": [],
            "recovery_plan": [],
            "simulation_timestamp": datetime.now().isoformat()
        }

        try:
            # Find all relationships involving this entity
            related_relationships = [
                r for r in self.relationships
                if r.get('source') == entity_id or r.get('target') == entity_id
            ]

            simulation_result["broken_relationships"] = related_relationships

            # Find entities that would become orphaned
            for rel in related_relationships:
                if rel.get('type') == 'implements' and rel.get('source') == entity_id:
                    # This entity implements something - target becomes unimplemented
                    target_entity = self.entity_index.get(rel.get('target'))
                    if target_entity:
                        simulation_result["orphaned_entities"].append(target_entity['id'])

            # Find entities that would need to be removed due to dependencies
            dependent_entities = [
                r.get('source') for r in related_relationships
                if r.get('type') == 'depends_on' and r.get('target') == entity_id
            ]

            for dep_entity_id in dependent_entities:
                # Check if this entity has alternative dependencies
                alternative_deps = [
                    r for r in self.relationships
                    if (r.get('source') == dep_entity_id and
                        r.get('type') == 'depends_on' and
                        r.get('target') != entity_id)
                ]

                if not alternative_deps:
                    # No alternative dependencies - would be cascade removal
                    simulation_result["cascade_removals"].append(dep_entity_id)

            # Find affected contracts
            for entity in self.entities:
                if entity.get('type') == 'contract':
                    applies_to = entity.get('applies_to', {})
                    if applies_to.get('entity_name') == entity_id:
                        simulation_result["affected_contracts"].append(entity['id'])

            # Generate recovery plan
            recovery_plan = self._generate_recovery_plan(simulation_result)
            simulation_result["recovery_plan"] = recovery_plan

            print(f"✅ Simulation completed!")
            print(f"   💔 Broken relationships: {len(related_relationships)}")
            print(f"   👤 Orphaned entities: {len(simulation_result['orphaned_entities'])}")
            print(f"   🌊 Cascade removals: {len(simulation_result['cascade_removals'])}")

            return simulation_result

        except Exception as e:
            simulation_result["error"] = str(e)
            return simulation_result

    # Private helper methods

    def _load_entities(self) -> List[Dict[str, Any]]:
        """Load entities from GraphRAG index"""
        entities_file = self.index_dir / "entities.json"
        if entities_file.exists():
            with open(entities_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _load_relationships(self) -> List[Dict[str, Any]]:
        """Load relationships from GraphRAG index"""
        relationships_file = self.index_dir / "relationships.json"
        if relationships_file.exists():
            with open(relationships_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _analyze_direct_impacts(self, entity_id: str, change_type: str) -> List[ImpactItem]:
        """Analyze direct impacts of a change"""
        direct_impacts = []

        # Find all direct relationships
        direct_relationships = [
            r for r in self.relationships
            if r.get('source') == entity_id or r.get('target') == entity_id
        ]

        for rel in direct_relationships:
            # Determine the affected entity
            affected_entity_id = rel.get('target') if rel.get('source') == entity_id else rel.get('source')
            affected_entity = self.entity_index.get(affected_entity_id)

            if affected_entity:
                impact_type = self._determine_impact_type(rel, change_type)
                severity = self._calculate_impact_severity(rel, affected_entity, change_type)

                impact_item = ImpactItem(
                    entity_id=affected_entity_id,
                    entity_type=affected_entity.get('type', 'unknown'),
                    impact_type=impact_type,
                    severity=severity,
                    description=self._generate_impact_description(rel, affected_entity, change_type),
                    path=[entity_id, affected_entity_id],
                    recommendations=self._generate_impact_recommendations(rel, affected_entity, change_type)
                )

                direct_impacts.append(impact_item)

        return direct_impacts

    def _analyze_indirect_impacts(self, entity_id: str, direct_impacts: List[ImpactItem]) -> List[ImpactItem]:
        """Analyze indirect impacts (second-level)"""
        indirect_impacts = []

        for direct_impact in direct_impacts:
            # Find entities that are related to the directly impacted entities
            second_level_rels = [
                r for r in self.relationships
                if (r.get('source') == direct_impact.entity_id or
                    r.get('target') == direct_impact.entity_id) and
                   r.get('source') != entity_id and r.get('target') != entity_id
            ]

            for rel in second_level_rels:
                affected_entity_id = (rel.get('target')
                                    if rel.get('source') == direct_impact.entity_id
                                    else rel.get('source'))

                # Avoid duplicates and self-references
                if (affected_entity_id != entity_id and
                    not any(impact.entity_id == affected_entity_id for impact in indirect_impacts)):

                    affected_entity = self.entity_index.get(affected_entity_id)
                    if affected_entity:
                        impact_type = f"indirect_{self._determine_impact_type(rel, 'modification')}"
                        severity = self._calculate_indirect_severity(direct_impact.severity, rel)

                        impact_item = ImpactItem(
                            entity_id=affected_entity_id,
                            entity_type=affected_entity.get('type', 'unknown'),
                            impact_type=impact_type,
                            severity=severity,
                            description=f"Indirectly affected via {direct_impact.entity_id}",
                            path=[entity_id, direct_impact.entity_id, affected_entity_id],
                            recommendations=["Review for potential side effects"]
                        )

                        indirect_impacts.append(impact_item)

        return indirect_impacts

    def _analyze_cascade_impacts(self, entity_id: str, existing_impacts: List[ImpactItem]) -> List[ImpactItem]:
        """Analyze cascade impacts (third-level and beyond)"""
        cascade_impacts = []
        visited = {entity_id}
        visited.update(impact.entity_id for impact in existing_impacts)

        # Use BFS to find cascade impacts
        queue = deque([(impact.entity_id, impact.path) for impact in existing_impacts])

        while queue and len(cascade_impacts) < 20:  # Limit cascade analysis
            current_entity_id, current_path = queue.popleft()

            if len(current_path) >= 5:  # Limit cascade depth
                continue

            # Find next level relationships
            next_level_rels = [
                r for r in self.relationships
                if r.get('source') == current_entity_id or r.get('target') == current_entity_id
            ]

            for rel in next_level_rels:
                next_entity_id = (rel.get('target')
                                if rel.get('source') == current_entity_id
                                else rel.get('source'))

                if next_entity_id not in visited:
                    visited.add(next_entity_id)
                    next_entity = self.entity_index.get(next_entity_id)

                    if next_entity:
                        severity = self._calculate_cascade_severity(len(current_path))

                        impact_item = ImpactItem(
                            entity_id=next_entity_id,
                            entity_type=next_entity.get('type', 'unknown'),
                            impact_type="cascade",
                            severity=severity,
                            description=f"Cascade impact via {' → '.join(current_path[1:])}",
                            path=current_path + [next_entity_id],
                            recommendations=["Monitor for unexpected effects"]
                        )

                        cascade_impacts.append(impact_item)
                        queue.append((next_entity_id, current_path + [next_entity_id]))

        return cascade_impacts

    def _perform_risk_assessment(self, source_entity: Dict[str, Any], report: ImpactReport) -> Dict[str, Any]:
        """Perform comprehensive risk assessment"""
        risk_factors = []
        risk_score = 0

        # Entity type risk
        entity_type = source_entity.get('type', 'unknown')
        if entity_type in ['functional_requirement', 'contract']:
            risk_factors.append("Critical entity type")
            risk_score += 3

        # Impact count risk
        total_impacts = len(report.direct_impacts) + len(report.indirect_impacts) + len(report.cascade_impacts)
        if total_impacts > 10:
            risk_factors.append("High impact count")
            risk_score += 2
        elif total_impacts > 5:
            risk_factors.append("Medium impact count")
            risk_score += 1

        # Severity risk
        critical_impacts = sum(1 for impact in (report.direct_impacts + report.indirect_impacts)
                             if impact.severity == "critical")
        if critical_impacts > 0:
            risk_factors.append("Critical severity impacts")
            risk_score += critical_impacts

        # Layer crossing risk
        affected_layers = self._analyze_affected_layers(report)
        if len(affected_layers) > 2:
            risk_factors.append("Multiple layer impact")
            risk_score += 1

        # Determine overall risk level
        if risk_score >= 8:
            overall_risk = "critical"
        elif risk_score >= 5:
            overall_risk = "high"
        elif risk_score >= 3:
            overall_risk = "medium"
        else:
            overall_risk = "low"

        return {
            "overall_risk": overall_risk,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "mitigation_required": overall_risk in ["critical", "high"]
        }

    def _generate_mitigation_strategies(self, report: ImpactReport) -> List[str]:
        """Generate mitigation strategies based on impact analysis"""
        strategies = []

        # General strategies based on risk level
        risk_level = report.risk_assessment.get('overall_risk', 'low')

        if risk_level == "critical":
            strategies.extend([
                "Implement phased rollout with rollback plan",
                "Create comprehensive test suite covering all impacts",
                "Set up monitoring for all affected entities",
                "Prepare hotfix deployment process"
            ])
        elif risk_level == "high":
            strategies.extend([
                "Perform staged deployment",
                "Enhanced testing of affected components",
                "Monitor key metrics during rollout"
            ])

        # Specific strategies based on impact types
        impact_types = set(impact.impact_type for impact in
                          report.direct_impacts + report.indirect_impacts)

        if "implementation_change" in impact_types:
            strategies.append("Update related contracts and BDD scenarios")

        if "dependency_impact" in impact_types:
            strategies.append("Verify dependency compatibility")

        if "contract_validation" in impact_types:
            strategies.append("Re-validate all affected contracts")

        # Layer-specific strategies
        if len(report.affected_layers) > 1:
            strategies.append("Coordinate changes across affected layers")

        return strategies

    def _analyze_affected_layers(self, report: ImpactReport) -> Set[str]:
        """Analyze which architectural layers are affected"""
        affected_layers = set()

        all_impacts = report.direct_impacts + report.indirect_impacts + report.cascade_impacts

        for impact in all_impacts:
            entity = self.entity_index.get(impact.entity_id)
            if entity:
                layer = entity.get('layer', 'unknown')
                if layer != 'unknown':
                    affected_layers.add(layer)

        return affected_layers

    def _generate_testing_recommendations(self, report: ImpactReport) -> List[str]:
        """Generate testing recommendations based on impact analysis"""
        recommendations = []

        # Basic recommendations
        recommendations.extend([
            "Unit tests for modified entity",
            "Integration tests for direct impacts"
        ])

        # Recommendations based on impact count
        total_impacts = len(report.direct_impacts) + len(report.indirect_impacts)

        if total_impacts > 5:
            recommendations.extend([
                "Regression test suite execution",
                "End-to-end testing of affected workflows"
            ])

        # Layer-specific recommendations
        affected_layers = report.affected_layers

        if "foundation" in affected_layers:
            recommendations.append("Infrastructure and configuration testing")

        if "application" in affected_layers:
            recommendations.append("Business logic validation testing")

        if "deployment" in affected_layers:
            recommendations.append("Deployment and operational testing")

        # Contract-specific recommendations
        contract_impacts = [impact for impact in report.direct_impacts + report.indirect_impacts
                          if impact.impact_type == "contract_validation"]

        if contract_impacts:
            recommendations.append("Contract compliance verification")

        return recommendations

    def _determine_impact_type(self, relationship: Dict[str, Any], change_type: str) -> str:
        """Determine the type of impact based on relationship and change type"""
        rel_type = relationship.get('type', 'unknown')

        if rel_type == 'implements':
            return "implementation_change"
        elif rel_type == 'depends_on':
            return "dependency_impact"
        elif rel_type == 'validates':
            return "contract_validation"
        elif rel_type == 'extends':
            return "extension_impact"
        else:
            return "general_impact"

    def _calculate_impact_severity(self, relationship: Dict[str, Any], affected_entity: Dict[str, Any], change_type: str) -> str:
        """Calculate impact severity"""
        base_severity = 1

        # Relationship type factor
        rel_type = relationship.get('type', 'unknown')
        if rel_type in ['implements', 'validates']:
            base_severity += 2
        elif rel_type == 'depends_on':
            base_severity += 1

        # Entity type factor
        entity_type = affected_entity.get('type', 'unknown')
        if entity_type in ['functional_requirement', 'contract']:
            base_severity += 2
        elif entity_type == 'unit_of_work':
            base_severity += 1

        # Change type factor
        if change_type == "removal":
            base_severity += 2
        elif change_type == "major_modification":
            base_severity += 1

        # Convert to severity level
        if base_severity >= 6:
            return "critical"
        elif base_severity >= 4:
            return "high"
        elif base_severity >= 2:
            return "medium"
        else:
            return "low"

    def _calculate_indirect_severity(self, direct_severity: str, relationship: Dict[str, Any]) -> str:
        """Calculate severity for indirect impacts"""
        direct_level = self.severity_levels.get(direct_severity, 1)

        # Reduce severity by one level for indirect impacts
        indirect_level = max(1, direct_level - 1)

        # Find corresponding severity
        for severity, level in self.severity_levels.items():
            if level == indirect_level:
                return severity

        return "low"

    def _calculate_cascade_severity(self, path_length: int) -> str:
        """Calculate severity for cascade impacts based on path length"""
        if path_length <= 3:
            return "medium"
        elif path_length <= 4:
            return "low"
        else:
            return "low"

    def _generate_impact_description(self, relationship: Dict[str, Any], affected_entity: Dict[str, Any], change_type: str) -> str:
        """Generate human-readable impact description"""
        rel_type = relationship.get('type', 'unknown')
        entity_type = affected_entity.get('type', 'unknown')
        entity_name = affected_entity.get('title', affected_entity.get('name', affected_entity.get('id', 'Unknown')))

        if rel_type == 'implements':
            return f"Implementation relationship will be affected: {entity_name}"
        elif rel_type == 'depends_on':
            return f"Dependency relationship will be affected: {entity_name}"
        elif rel_type == 'validates':
            return f"Contract validation will be affected: {entity_name}"
        else:
            return f"Related {entity_type} will be affected: {entity_name}"

    def _generate_impact_recommendations(self, relationship: Dict[str, Any], affected_entity: Dict[str, Any], change_type: str) -> List[str]:
        """Generate specific recommendations for an impact"""
        recommendations = []
        rel_type = relationship.get('type', 'unknown')

        if rel_type == 'implements':
            recommendations.extend([
                "Update implementation to match changes",
                "Verify acceptance criteria still satisfied"
            ])
        elif rel_type == 'depends_on':
            recommendations.extend([
                "Check dependency compatibility",
                "Update dependent entity if needed"
            ])
        elif rel_type == 'validates':
            recommendations.extend([
                "Re-validate contract conditions",
                "Update contract if necessary"
            ])

        return recommendations

    def _calculate_entity_impact(self, source_entity_id: str, target_entity_id: str) -> str:
        """Calculate impact level between two entities"""
        # Find shortest path between entities
        path = self._find_shortest_path(source_entity_id, target_entity_id)

        if not path:
            return "none"
        elif len(path) == 2:  # Direct relationship
            return "high"
        elif len(path) == 3:  # One hop
            return "medium"
        else:  # Multiple hops
            return "low"

    def _find_shortest_path(self, source: str, target: str) -> Optional[List[str]]:
        """Find shortest path between two entities using BFS"""
        if source == target:
            return [source]

        visited = {source}
        queue = deque([(source, [source])])

        while queue:
            current, path = queue.popleft()

            # Find connected entities
            connected = []
            for rel in self.relationships:
                if rel.get('source') == current:
                    connected.append(rel.get('target'))
                elif rel.get('target') == current:
                    connected.append(rel.get('source'))

            for next_entity in connected:
                if next_entity == target:
                    return path + [target]

                if next_entity not in visited:
                    visited.add(next_entity)
                    queue.append((next_entity, path + [next_entity]))

        return None

    def _calculate_criticality_score(self, entity: Dict[str, Any], incoming_deps: List[Dict[str, Any]], outgoing_deps: List[Dict[str, Any]]) -> float:
        """Calculate criticality score for an entity"""
        score = 0.0

        # Base score from entity type
        entity_type = entity.get('type', 'unknown')
        if entity_type == 'functional_requirement':
            score += 0.4
        elif entity_type == 'contract':
            score += 0.3
        elif entity_type == 'unit_of_work':
            score += 0.2

        # Score from incoming dependencies (entities depending on this)
        incoming_score = min(len(incoming_deps) * 0.1, 0.4)
        score += incoming_score

        # Score from outgoing dependencies (complexity)
        outgoing_score = min(len(outgoing_deps) * 0.05, 0.2)
        score += outgoing_score

        return min(score, 1.0)

    def _identify_risk_factors(self, entity: Dict[str, Any], incoming_deps: List[Dict[str, Any]], outgoing_deps: List[Dict[str, Any]]) -> List[str]:
        """Identify risk factors for a critical entity"""
        risk_factors = []

        if len(incoming_deps) > 5:
            risk_factors.append("High number of dependent entities")

        if len(outgoing_deps) > 3:
            risk_factors.append("High complexity with multiple dependencies")

        entity_type = entity.get('type', 'unknown')
        if entity_type in ['functional_requirement', 'contract']:
            risk_factors.append("Critical entity type")

        return risk_factors

    def _generate_recovery_plan(self, simulation_result: Dict[str, Any]) -> List[str]:
        """Generate recovery plan for entity removal simulation"""
        recovery_plan = []

        if simulation_result["orphaned_entities"]:
            recovery_plan.append("Create alternative implementations for orphaned requirements")

        if simulation_result["cascade_removals"]:
            recovery_plan.append("Establish alternative dependencies for cascade-affected entities")

        if simulation_result["affected_contracts"]:
            recovery_plan.append("Update or remove affected contracts")

        if simulation_result["broken_relationships"]:
            recovery_plan.append("Re-establish critical relationships with alternative entities")

        recovery_plan.append("Update documentation and traceability matrix")
        recovery_plan.append("Run full SSOT verification after changes")

        return recovery_plan

def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="SSOT Impact Analysis Tool")
    parser.add_argument("--entity", help="Entity ID to analyze")
    parser.add_argument("--change-type", choices=['modification', 'major_modification', 'removal'],
                       default='modification', help="Type of change")
    parser.add_argument("--matrix", nargs='+', help="Generate impact matrix for entity list")
    parser.add_argument("--critical-deps", action="store_true", help="Find critical dependencies")
    parser.add_argument("--simulate-removal", help="Simulate removal of entity")
    parser.add_argument("--output", help="Output file for detailed report")

    args = parser.parse_args()

    try:
        analyzer = ImpactAnalyzer()

        if args.entity:
            # Single entity impact analysis
            report = analyzer.analyze_change_impact(args.entity, args.change_type)

            print(f"\n📊 Impact Analysis Summary:")
            print(f"   Entity: {report.source_entity}")
            print(f"   Change Type: {report.change_type}")
            print(f"   Risk Level: {report.risk_assessment.get('overall_risk', 'unknown')}")
            print(f"   Direct Impacts: {len(report.direct_impacts)}")
            print(f"   Indirect Impacts: {len(report.indirect_impacts)}")
            print(f"   Cascade Impacts: {len(report.cascade_impacts)}")

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(asdict(report), f, ensure_ascii=False, indent=2, default=str)
                print(f"   📄 Detailed report saved: {args.output}")

        elif args.matrix:
            # Impact matrix generation
            matrix = analyzer.generate_impact_matrix(args.matrix)
            print(f"\n📋 Impact Matrix:")
            for source, targets in matrix.items():
                print(f"   {source}:")
                for target, impact in targets.items():
                    if impact != "none":
                        print(f"     → {target}: {impact}")

        elif args.critical_deps:
            # Critical dependencies analysis
            critical_deps = analyzer.find_critical_dependencies()
            print(f"\n🔍 Critical Dependencies ({len(critical_deps)}):")
            for dep in critical_deps[:10]:  # Show top 10
                entity = dep['entity']
                print(f"   🎯 {entity['id']}: {entity.get('title', entity.get('name', 'No title'))}")
                print(f"      Criticality: {dep['criticality_score']:.2f}")
                print(f"      Dependencies: {dep['incoming_dependencies']} in, {dep['outgoing_dependencies']} out")

        elif args.simulate_removal:
            # Entity removal simulation
            result = analyzer.simulate_entity_removal(args.simulate_removal)
            print(f"\n🎭 Removal Simulation for {args.simulate_removal}:")
            print(f"   💔 Broken relationships: {len(result['broken_relationships'])}")
            print(f"   👤 Orphaned entities: {len(result['orphaned_entities'])}")
            print(f"   🌊 Cascade removals: {len(result['cascade_removals'])}")
            print(f"   📜 Affected contracts: {len(result['affected_contracts'])}")

            if result['recovery_plan']:
                print(f"   🛠️  Recovery Plan:")
                for step in result['recovery_plan']:
                    print(f"     • {step}")

        else:
            print("Please specify an analysis option. Use --help for details.")

        sys.exit(0)

    except Exception as e:
        print(f"❌ Impact analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()