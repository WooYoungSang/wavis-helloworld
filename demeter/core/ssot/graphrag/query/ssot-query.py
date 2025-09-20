#!/usr/bin/env python3
"""
SSOT GraphRAG Query Interface
Provides intelligent querying capabilities for SSOT data through GraphRAG
"""

import yaml
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import re
from dataclasses import dataclass

@dataclass
class QueryResult:
    """Result of a GraphRAG query"""
    query: str
    results: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    execution_time: float

@dataclass
class Entity:
    """GraphRAG entity representation"""
    id: str
    type: str
    properties: Dict[str, Any]
    relationships: List[Dict[str, Any]]

class SSOTQuery:
    """GraphRAG-powered SSOT query interface"""

    def __init__(self, ssot_dir: str = "demeter/core/ssot", graphrag_dir: str = "demeter/core/ssot/graphrag"):
        self.ssot_dir = Path(ssot_dir)
        self.graphrag_dir = Path(graphrag_dir)
        self.index_dir = self.graphrag_dir / "index"
        self.knowledge_dir = self.graphrag_dir / "knowledge"

        # Load indexed data
        self.entities = self._load_entities()
        self.relationships = self._load_relationships()
        self.knowledge = self._load_knowledge()

        # Query processors
        self.query_processors = {
            "keyword": self._process_keyword_query,
            "relationship": self._process_relationship_query,
            "pattern": self._process_pattern_query,
            "impact": self._process_impact_query,
            "coverage": self._process_coverage_query,
            "gap": self._process_gap_query
        }

    def query(self, query_text: str, query_type: str = "auto") -> QueryResult:
        """Execute a GraphRAG query"""
        start_time = datetime.now()

        try:
            # Auto-detect query type if not specified
            if query_type == "auto":
                query_type = self._detect_query_type(query_text)

            # Process query based on type
            processor = self.query_processors.get(query_type, self._process_keyword_query)
            results = processor(query_text)

            # Calculate execution time
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            return QueryResult(
                query=query_text,
                results=results,
                metadata={
                    "query_type": query_type,
                    "timestamp": end_time.isoformat(),
                    "results_count": len(results)
                },
                execution_time=execution_time
            )

        except Exception as e:
            return QueryResult(
                query=query_text,
                results=[],
                metadata={
                    "error": str(e),
                    "query_type": query_type,
                    "timestamp": datetime.now().isoformat()
                },
                execution_time=0.0
            )

    def find_requirements_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Find requirements containing specific keywords"""
        results = []

        for entity in self.entities:
            if entity.get('type') in ['functional_requirement', 'non_functional_requirement']:
                # Search in title, description, and acceptance criteria
                searchable_text = ' '.join([
                    entity.get('title', ''),
                    entity.get('description', ''),
                    ' '.join(entity.get('acceptance_criteria', []))
                ]).lower()

                if keyword.lower() in searchable_text:
                    results.append({
                        "entity": entity,
                        "relevance": self._calculate_relevance(keyword, searchable_text),
                        "matches": self._find_keyword_matches(keyword, entity)
                    })

        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results

    def find_implementing_uows(self, requirement_id: str) -> List[Dict[str, Any]]:
        """Find UoWs that implement a specific requirement"""
        implementing_uows = []

        # Find direct implementation relationships
        for rel in self.relationships:
            if (rel.get('type') == 'implements' and
                rel.get('target') == requirement_id):

                uow_entity = self._get_entity_by_id(rel.get('source'))
                if uow_entity:
                    implementing_uows.append({
                        "uow": uow_entity,
                        "relationship": rel,
                        "direct": True
                    })

        # Find indirect relationships through dependencies
        for uow in implementing_uows:
            indirect_uows = self._find_dependent_uows(uow['uow']['id'])
            for indirect_uow in indirect_uows:
                implementing_uows.append({
                    "uow": indirect_uow,
                    "relationship": {"type": "indirect"},
                    "direct": False
                })

        return implementing_uows

    def find_related_contracts(self, entity_id: str) -> List[Dict[str, Any]]:
        """Find contracts related to a specific entity"""
        related_contracts = []

        for entity in self.entities:
            if entity.get('type') == 'contract':
                applies_to = entity.get('applies_to', {})
                if applies_to.get('entity_name') == entity_id:
                    related_contracts.append({
                        "contract": entity,
                        "relationship_type": "validates",
                        "applies_to": applies_to
                    })

        return related_contracts

    def find_bdd_scenarios(self, uow_id: str) -> List[Dict[str, Any]]:
        """Find BDD scenarios for a specific UoW"""
        # This would integrate with the BDD feature files
        bdd_scenarios = []

        # Load BDD features for the UoW
        features_dir = self.ssot_dir.parent.parent / "features"
        if features_dir.exists():
            for layer_dir in features_dir.iterdir():
                if layer_dir.is_dir():
                    feature_file = layer_dir / f"{uow_id.lower().replace('-', '_')}.feature"
                    if feature_file.exists():
                        scenarios = self._parse_gherkin_file(feature_file)
                        bdd_scenarios.extend(scenarios)

        return bdd_scenarios

    def analyze_coverage_gaps(self) -> Dict[str, Any]:
        """Analyze coverage gaps in SSOT"""
        gaps = {
            "requirements_without_uows": [],
            "uows_without_contracts": [],
            "uows_without_bdd": [],
            "orphaned_contracts": [],
            "analysis_timestamp": datetime.now().isoformat()
        }

        # Find requirements without implementing UoWs
        requirement_ids = [e['id'] for e in self.entities if e.get('type') in ['functional_requirement', 'non_functional_requirement']]
        implemented_reqs = [r['target'] for r in self.relationships if r.get('type') == 'implements']

        gaps["requirements_without_uows"] = [
            req_id for req_id in requirement_ids if req_id not in implemented_reqs
        ]

        # Find UoWs without contracts
        uow_ids = [e['id'] for e in self.entities if e.get('type') == 'unit_of_work']
        contracted_uows = []

        for entity in self.entities:
            if entity.get('type') == 'contract':
                applies_to = entity.get('applies_to', {})
                if applies_to.get('entity_type') == 'uow':
                    contracted_uows.append(applies_to.get('entity_name'))

        gaps["uows_without_contracts"] = [
            uow_id for uow_id in uow_ids if uow_id not in contracted_uows
        ]

        # Find UoWs without BDD scenarios
        uows_with_bdd = []
        features_dir = self.ssot_dir.parent.parent / "features"
        if features_dir.exists():
            for layer_dir in features_dir.iterdir():
                if layer_dir.is_dir():
                    for feature_file in layer_dir.glob("*.feature"):
                        # Extract UoW ID from filename
                        uow_match = re.search(r'uow[_-](\d+)', feature_file.stem)
                        if uow_match:
                            uow_num = uow_match.group(1)
                            uows_with_bdd.append(f"UoW-{uow_num}")

        gaps["uows_without_bdd"] = [
            uow_id for uow_id in uow_ids if uow_id not in uows_with_bdd
        ]

        # Find orphaned contracts (contracts without valid entity references)
        valid_entity_ids = [e['id'] for e in self.entities]
        for entity in self.entities:
            if entity.get('type') == 'contract':
                applies_to = entity.get('applies_to', {})
                target_entity = applies_to.get('entity_name')
                if target_entity and target_entity not in valid_entity_ids:
                    gaps["orphaned_contracts"].append(entity['id'])

        return gaps

    def analyze_impact(self, entity_id: str, change_type: str = "modification") -> Dict[str, Any]:
        """Analyze the impact of changes to a specific entity"""
        impact_analysis = {
            "entity_id": entity_id,
            "change_type": change_type,
            "direct_impacts": [],
            "indirect_impacts": [],
            "risk_level": "low",
            "recommendations": [],
            "analysis_timestamp": datetime.now().isoformat()
        }

        try:
            entity = self._get_entity_by_id(entity_id)
            if not entity:
                impact_analysis["error"] = f"Entity {entity_id} not found"
                return impact_analysis

            # Find direct relationships
            direct_relationships = [
                r for r in self.relationships
                if r.get('source') == entity_id or r.get('target') == entity_id
            ]

            # Analyze direct impacts
            for rel in direct_relationships:
                related_entity_id = rel.get('target') if rel.get('source') == entity_id else rel.get('source')
                related_entity = self._get_entity_by_id(related_entity_id)

                if related_entity:
                    impact_analysis["direct_impacts"].append({
                        "entity": related_entity,
                        "relationship": rel,
                        "impact_type": self._determine_impact_type(rel, entity, related_entity)
                    })

            # Find indirect impacts (second-level relationships)
            for direct_impact in impact_analysis["direct_impacts"]:
                indirect_rels = [
                    r for r in self.relationships
                    if (r.get('source') == direct_impact['entity']['id'] or
                        r.get('target') == direct_impact['entity']['id']) and
                       r not in direct_relationships
                ]

                for indirect_rel in indirect_rels:
                    related_entity_id = (indirect_rel.get('target')
                                       if indirect_rel.get('source') == direct_impact['entity']['id']
                                       else indirect_rel.get('source'))
                    related_entity = self._get_entity_by_id(related_entity_id)

                    if related_entity and related_entity['id'] != entity_id:
                        impact_analysis["indirect_impacts"].append({
                            "entity": related_entity,
                            "relationship": indirect_rel,
                            "via": direct_impact['entity']['id'],
                            "impact_type": "indirect"
                        })

            # Calculate risk level
            impact_analysis["risk_level"] = self._calculate_risk_level(
                len(impact_analysis["direct_impacts"]),
                len(impact_analysis["indirect_impacts"]),
                entity.get('type')
            )

            # Generate recommendations
            impact_analysis["recommendations"] = self._generate_impact_recommendations(
                entity, impact_analysis["direct_impacts"], impact_analysis["indirect_impacts"]
            )

        except Exception as e:
            impact_analysis["error"] = str(e)

        return impact_analysis

    def search_patterns(self, pattern_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for learned patterns"""
        patterns = []

        if 'patterns' in self.knowledge:
            for pattern_id, pattern_data in self.knowledge['patterns'].items():
                if pattern_type is None or pattern_data.get('category') == pattern_type:
                    patterns.append({
                        "id": pattern_id,
                        "pattern": pattern_data,
                        "relevance": pattern_data.get('frequency', 0)
                    })

        # Sort by relevance (frequency)
        patterns.sort(key=lambda x: x['relevance'], reverse=True)
        return patterns

    def get_recommendations(self, context: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get AI recommendations based on accumulated knowledge"""
        recommendations = []

        # Load existing recommendations
        recommendations_file = self.knowledge_dir / "ssot-recommendations.yaml"
        if recommendations_file.exists():
            with open(recommendations_file, 'r', encoding='utf-8') as f:
                recs_data = yaml.safe_load(f)

                if recs_data:
                    for rec_type, rec_list in recs_data.items():
                        if rec_type != "generation_timestamp" and isinstance(rec_list, list):
                            for rec in rec_list:
                                if context is None or context.lower() in str(rec).lower():
                                    recommendations.append({
                                        "type": rec_type,
                                        "recommendation": rec,
                                        "priority": rec.get("priority", "medium")
                                    })

        return recommendations

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

    def _load_knowledge(self) -> Dict[str, Any]:
        """Load accumulated knowledge"""
        knowledge = {}

        # Load patterns
        patterns_file = self.knowledge_dir / "patterns.yaml"
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                knowledge['patterns'] = yaml.safe_load(f) or {}

        # Load decisions
        decisions_file = self.knowledge_dir / "decisions.yaml"
        if decisions_file.exists():
            with open(decisions_file, 'r', encoding='utf-8') as f:
                knowledge['decisions'] = yaml.safe_load(f) or {}

        # Load lessons
        lessons_file = self.knowledge_dir / "lessons.yaml"
        if lessons_file.exists():
            with open(lessons_file, 'r', encoding='utf-8') as f:
                knowledge['lessons'] = yaml.safe_load(f) or {}

        return knowledge

    def _detect_query_type(self, query_text: str) -> str:
        """Auto-detect query type from query text"""
        query_lower = query_text.lower()

        if any(word in query_lower for word in ['impact', 'affect', 'change']):
            return "impact"
        elif any(word in query_lower for word in ['implement', 'cover', 'relate']):
            return "relationship"
        elif any(word in query_lower for word in ['pattern', 'frequent', 'common']):
            return "pattern"
        elif any(word in query_lower for word in ['gap', 'missing', 'without']):
            return "gap"
        elif any(word in query_lower for word in ['coverage', 'complete']):
            return "coverage"
        else:
            return "keyword"

    def _process_keyword_query(self, query_text: str) -> List[Dict[str, Any]]:
        """Process keyword-based queries"""
        keywords = query_text.split()
        results = []

        for keyword in keywords:
            keyword_results = self.find_requirements_by_keyword(keyword)
            results.extend(keyword_results)

        # Remove duplicates and sort by relevance
        seen_ids = set()
        unique_results = []
        for result in results:
            entity_id = result['entity']['id']
            if entity_id not in seen_ids:
                seen_ids.add(entity_id)
                unique_results.append(result)

        return unique_results

    def _process_relationship_query(self, query_text: str) -> List[Dict[str, Any]]:
        """Process relationship-based queries"""
        # Extract entity IDs from query
        entity_patterns = [r'FR-\d+', r'NFR-\d+', r'UoW-\d+', r'CTR-\d+']
        found_entities = []

        for pattern in entity_patterns:
            matches = re.findall(pattern, query_text, re.IGNORECASE)
            found_entities.extend(matches)

        results = []
        for entity_id in found_entities:
            # Find implementing UoWs
            if entity_id.startswith(('FR-', 'NFR-')):
                implementing_uows = self.find_implementing_uows(entity_id)
                results.extend(implementing_uows)

            # Find related contracts
            contracts = self.find_related_contracts(entity_id)
            results.extend(contracts)

        return results

    def _process_pattern_query(self, query_text: str) -> List[Dict[str, Any]]:
        """Process pattern-based queries"""
        # Extract pattern type from query
        pattern_type = None
        pattern_keywords = {
            'error': 'error_handling',
            'validation': 'data_validation',
            'config': 'configuration',
            'test': 'testing',
            'performance': 'performance'
        }

        for keyword, p_type in pattern_keywords.items():
            if keyword in query_text.lower():
                pattern_type = p_type
                break

        return self.search_patterns(pattern_type)

    def _process_impact_query(self, query_text: str) -> List[Dict[str, Any]]:
        """Process impact analysis queries"""
        # Extract entity ID from query
        entity_patterns = [r'FR-\d+', r'NFR-\d+', r'UoW-\d+', r'CTR-\d+']
        found_entities = []

        for pattern in entity_patterns:
            matches = re.findall(pattern, query_text, re.IGNORECASE)
            found_entities.extend(matches)

        results = []
        for entity_id in found_entities:
            impact_analysis = self.analyze_impact(entity_id)
            results.append({
                "entity_id": entity_id,
                "impact_analysis": impact_analysis
            })

        return results

    def _process_coverage_query(self, query_text: str) -> List[Dict[str, Any]]:
        """Process coverage analysis queries"""
        coverage_gaps = self.analyze_coverage_gaps()
        return [{"coverage_analysis": coverage_gaps}]

    def _process_gap_query(self, query_text: str) -> List[Dict[str, Any]]:
        """Process gap analysis queries"""
        return self._process_coverage_query(query_text)

    def _get_entity_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity by ID"""
        for entity in self.entities:
            if entity.get('id') == entity_id:
                return entity
        return None

    def _calculate_relevance(self, keyword: str, text: str) -> float:
        """Calculate relevance score for keyword match"""
        keyword_count = text.lower().count(keyword.lower())
        text_length = len(text.split())
        return keyword_count / max(text_length, 1)

    def _find_keyword_matches(self, keyword: str, entity: Dict[str, Any]) -> List[str]:
        """Find specific keyword matches in entity"""
        matches = []
        keyword_lower = keyword.lower()

        # Check title
        title = entity.get('title', '')
        if keyword_lower in title.lower():
            matches.append(f"title: {title}")

        # Check description
        description = entity.get('description', '')
        if keyword_lower in description.lower():
            matches.append(f"description: {description}")

        return matches

    def _find_dependent_uows(self, uow_id: str) -> List[Dict[str, Any]]:
        """Find UoWs that depend on the given UoW"""
        dependent_uows = []

        for rel in self.relationships:
            if (rel.get('type') == 'depends_on' and
                rel.get('target') == uow_id):

                dependent_entity = self._get_entity_by_id(rel.get('source'))
                if dependent_entity:
                    dependent_uows.append(dependent_entity)

        return dependent_uows

    def _parse_gherkin_file(self, feature_file: Path) -> List[Dict[str, Any]]:
        """Parse Gherkin feature file for scenarios"""
        scenarios = []

        try:
            with open(feature_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple Gherkin parsing (would use proper parser in production)
            scenario_blocks = re.split(r'\n\s*Scenario:', content)[1:]

            for i, block in enumerate(scenario_blocks):
                lines = block.strip().split('\n')
                if lines:
                    scenario_name = lines[0].strip()
                    scenarios.append({
                        "name": scenario_name,
                        "file": str(feature_file),
                        "scenario_index": i + 1
                    })

        except Exception as e:
            print(f"⚠️  Could not parse Gherkin file {feature_file}: {e}")

        return scenarios

    def _determine_impact_type(self, relationship: Dict[str, Any], source_entity: Dict[str, Any], target_entity: Dict[str, Any]) -> str:
        """Determine the type of impact based on relationship and entities"""
        rel_type = relationship.get('type')

        if rel_type == 'implements':
            return "implementation_change"
        elif rel_type == 'depends_on':
            return "dependency_impact"
        elif rel_type == 'validates':
            return "contract_validation"
        else:
            return "general_impact"

    def _calculate_risk_level(self, direct_count: int, indirect_count: int, entity_type: str) -> str:
        """Calculate risk level based on impact scope"""
        total_impacts = direct_count + indirect_count

        # Higher risk for critical entity types
        risk_multiplier = 1.0
        if entity_type in ['functional_requirement', 'contract']:
            risk_multiplier = 1.5

        adjusted_impact = total_impacts * risk_multiplier

        if adjusted_impact >= 10:
            return "high"
        elif adjusted_impact >= 5:
            return "medium"
        else:
            return "low"

    def _generate_impact_recommendations(self, entity: Dict[str, Any], direct_impacts: List[Dict[str, Any]], indirect_impacts: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on impact analysis"""
        recommendations = []

        if len(direct_impacts) > 5:
            recommendations.append("Consider breaking down this entity due to high coupling")

        if len(indirect_impacts) > 10:
            recommendations.append("Review architecture to reduce indirect dependencies")

        if entity.get('type') == 'functional_requirement' and len(direct_impacts) == 0:
            recommendations.append("This requirement has no implementing UoWs - consider adding implementation")

        return recommendations

def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="SSOT GraphRAG Query Interface")
    parser.add_argument("--query", required=True, help="Query text")
    parser.add_argument("--type", choices=['auto', 'keyword', 'relationship', 'pattern', 'impact', 'coverage', 'gap'],
                       default='auto', help="Query type")
    parser.add_argument("--keyword", help="Find requirements by keyword")
    parser.add_argument("--implements", help="Find UoWs implementing a requirement")
    parser.add_argument("--contracts", help="Find contracts for an entity")
    parser.add_argument("--impact", help="Analyze impact of changes to entity")
    parser.add_argument("--gaps", action="store_true", help="Analyze coverage gaps")
    parser.add_argument("--patterns", help="Search patterns by type")
    parser.add_argument("--recommendations", action="store_true", help="Get AI recommendations")

    args = parser.parse_args()

    try:
        query_engine = SSOTQuery()

        if args.keyword:
            results = query_engine.find_requirements_by_keyword(args.keyword)
            print(f"✅ Found {len(results)} requirements matching '{args.keyword}':")
            for result in results:
                entity = result['entity']
                print(f"   📋 {entity['id']}: {entity.get('title', 'No title')}")

        elif args.implements:
            results = query_engine.find_implementing_uows(args.implements)
            print(f"✅ Found {len(results)} UoWs implementing {args.implements}:")
            for result in results:
                uow = result['uow']
                print(f"   ⚙️  {uow['id']}: {uow.get('name', 'No name')}")

        elif args.contracts:
            results = query_engine.find_related_contracts(args.contracts)
            print(f"✅ Found {len(results)} contracts for {args.contracts}:")
            for result in results:
                contract = result['contract']
                print(f"   📜 {contract['id']}: {contract.get('title', 'No title')}")

        elif args.impact:
            result = query_engine.analyze_impact(args.impact)
            print(f"✅ Impact analysis for {args.impact}:")
            print(f"   🎯 Risk Level: {result['risk_level']}")
            print(f"   📊 Direct impacts: {len(result['direct_impacts'])}")
            print(f"   🔄 Indirect impacts: {len(result['indirect_impacts'])}")

        elif args.gaps:
            result = query_engine.analyze_coverage_gaps()
            print("✅ Coverage gap analysis:")
            print(f"   📋 Requirements without UoWs: {len(result['requirements_without_uows'])}")
            print(f"   📜 UoWs without contracts: {len(result['uows_without_contracts'])}")
            print(f"   🥒 UoWs without BDD: {len(result['uows_without_bdd'])}")

        elif args.patterns:
            results = query_engine.search_patterns(args.patterns)
            print(f"✅ Found {len(results)} patterns:")
            for result in results:
                pattern = result['pattern']
                print(f"   🧩 {result['id']}: {pattern.get('name', 'No name')}")

        elif args.recommendations:
            results = query_engine.get_recommendations()
            print(f"✅ Found {len(results)} recommendations:")
            for result in results:
                print(f"   💡 {result['type']}: {result['recommendation']}")

        else:
            # General query
            result = query_engine.query(args.query, args.type)
            print(f"✅ Query executed in {result.execution_time:.3f}s:")
            print(f"   📊 Results: {len(result.results)}")
            print(f"   🔍 Query type: {result.metadata.get('query_type')}")

            for i, res in enumerate(result.results[:5]):  # Show top 5 results
                if 'entity' in res:
                    entity = res['entity']
                    print(f"   {i+1}. {entity['id']}: {entity.get('title', entity.get('name', 'No title'))}")

        sys.exit(0)

    except Exception as e:
        print(f"❌ Query failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()