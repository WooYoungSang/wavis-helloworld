#!/usr/bin/env python3
"""
Knowledge Accumulation and Learning Engine
Analyzes code changes and runtime behavior to feed knowledge back to SSOT
"""

import yaml
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib
import re
import ast
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Pattern:
    """Represents a discovered pattern"""
    id: str
    name: str
    category: str
    description: str
    examples: List[str]
    frequency: int
    confidence: float
    metadata: Dict[str, Any]

@dataclass
class Decision:
    """Represents an architecture decision"""
    id: str
    title: str
    context: str
    decision: str
    rationale: str
    consequences: List[str]
    alternatives: List[str]
    status: str  # proposed, accepted, superseded
    date: str

@dataclass
class Lesson:
    """Represents a lesson learned"""
    id: str
    category: str
    situation: str
    problem: str
    solution: str
    outcome: str
    tags: List[str]
    impact: str  # high, medium, low

class LearningEngine:
    """Learns from code changes and runtime behavior"""

    def __init__(self, ssot_dir: str = "demeter/core/ssot", knowledge_dir: str = "demeter/core/ssot/graphrag/knowledge"):
        self.ssot_dir = Path(ssot_dir)
        self.knowledge_dir = Path(knowledge_dir)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)

        # Knowledge storage files
        self.patterns_file = self.knowledge_dir / "patterns.yaml"
        self.decisions_file = self.knowledge_dir / "decisions.yaml"
        self.lessons_file = self.knowledge_dir / "lessons.yaml"
        self.insights_file = self.knowledge_dir / "insights.yaml"

        # Pattern detection rules
        self.pattern_detectors = {
            "error_handling": self._detect_error_handling_patterns,
            "data_validation": self._detect_validation_patterns,
            "configuration": self._detect_config_patterns,
            "testing": self._detect_testing_patterns,
            "performance": self._detect_performance_patterns
        }

    def analyze_recent_changes(self, git_log_days: int = 7) -> Dict[str, Any]:
        """Analyze recent code changes to extract patterns and lessons"""
        print(f"🔍 Analyzing code changes from last {git_log_days} days...")

        analysis_result = {
            "patterns_discovered": [],
            "decisions_extracted": [],
            "lessons_learned": [],
            "analysis_timestamp": datetime.now().isoformat()
        }

        try:
            # Analyze git changes
            git_changes = self._get_git_changes(git_log_days)

            # Extract patterns from code changes
            patterns = self._extract_patterns_from_changes(git_changes)
            analysis_result["patterns_discovered"] = patterns

            # Extract architecture decisions from commit messages and code
            decisions = self._extract_decisions_from_changes(git_changes)
            analysis_result["decisions_extracted"] = decisions

            # Learn from error patterns and fixes
            lessons = self._extract_lessons_from_changes(git_changes)
            analysis_result["lessons_learned"] = lessons

            # Save discovered knowledge
            self._save_patterns(patterns)
            self._save_decisions(decisions)
            self._save_lessons(lessons)

            print(f"✅ Analysis completed:")
            print(f"   🧩 Patterns discovered: {len(patterns)}")
            print(f"   🏗️  Decisions extracted: {len(decisions)}")
            print(f"   📚 Lessons learned: {len(lessons)}")

            return analysis_result

        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return analysis_result

    def analyze_runtime_metrics(self, metrics_file: Optional[str] = None) -> Dict[str, Any]:
        """Analyze runtime performance metrics to extract insights"""
        print("📊 Analyzing runtime metrics...")

        insights = {
            "performance_patterns": [],
            "bottlenecks": [],
            "optimization_opportunities": [],
            "analysis_timestamp": datetime.now().isoformat()
        }

        try:
            # Load runtime metrics (from logs, monitoring, etc.)
            metrics_data = self._load_runtime_metrics(metrics_file)

            if metrics_data:
                # Detect performance patterns
                perf_patterns = self._analyze_performance_patterns(metrics_data)
                insights["performance_patterns"] = perf_patterns

                # Identify bottlenecks
                bottlenecks = self._identify_bottlenecks(metrics_data)
                insights["bottlenecks"] = bottlenecks

                # Find optimization opportunities
                optimizations = self._find_optimization_opportunities(metrics_data)
                insights["optimization_opportunities"] = optimizations

                # Save insights
                self._save_insights(insights)

            print(f"✅ Runtime analysis completed:")
            print(f"   🚀 Performance patterns: {len(insights['performance_patterns'])}")
            print(f"   🚨 Bottlenecks found: {len(insights['bottlenecks'])}")
            print(f"   💡 Optimization opportunities: {len(insights['optimization_opportunities'])}")

            return insights

        except Exception as e:
            print(f"❌ Runtime analysis failed: {e}")
            return insights

    def record_lesson(self, category: str, situation: str, problem: str, solution: str, outcome: str, tags: List[str] = None) -> str:
        """Manually record a lesson learned"""
        lesson_id = f"LESSON-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        lesson = Lesson(
            id=lesson_id,
            category=category,
            situation=situation,
            problem=problem,
            solution=solution,
            outcome=outcome,
            tags=tags or [],
            impact="medium"  # Default impact level
        )

        # Load existing lessons
        existing_lessons = self._load_lessons()
        existing_lessons[lesson_id] = {
            "category": lesson.category,
            "situation": lesson.situation,
            "problem": lesson.problem,
            "solution": lesson.solution,
            "outcome": lesson.outcome,
            "tags": lesson.tags,
            "impact": lesson.impact,
            "recorded_at": datetime.now().isoformat()
        }

        # Save updated lessons
        with open(self.lessons_file, 'w', encoding='utf-8') as f:
            yaml.dump(existing_lessons, f, allow_unicode=True, default_flow_style=False)

        print(f"✅ Lesson recorded: {lesson_id}")
        return lesson_id

    def generate_ssot_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations for SSOT improvements based on accumulated knowledge"""
        print("💡 Generating SSOT recommendations...")

        recommendations = {
            "new_requirements": [],
            "uow_improvements": [],
            "contract_updates": [],
            "bdd_enhancements": [],
            "generation_timestamp": datetime.now().isoformat()
        }

        try:
            # Load accumulated knowledge
            patterns = self._load_patterns()
            decisions = self._load_decisions()
            lessons = self._load_lessons()

            # Analyze patterns for new requirements
            new_reqs = self._recommend_new_requirements(patterns, lessons)
            recommendations["new_requirements"] = new_reqs

            # Suggest UoW improvements
            uow_improvements = self._recommend_uow_improvements(patterns, decisions)
            recommendations["uow_improvements"] = uow_improvements

            # Suggest contract updates
            contract_updates = self._recommend_contract_updates(lessons, decisions)
            recommendations["contract_updates"] = contract_updates

            # Suggest BDD enhancements
            bdd_enhancements = self._recommend_bdd_enhancements(patterns, lessons)
            recommendations["bdd_enhancements"] = bdd_enhancements

            # Save recommendations
            recommendations_file = self.knowledge_dir / "ssot-recommendations.yaml"
            with open(recommendations_file, 'w', encoding='utf-8') as f:
                yaml.dump(recommendations, f, allow_unicode=True, default_flow_style=False)

            print(f"✅ SSOT recommendations generated:")
            print(f"   📋 New requirements: {len(new_reqs)}")
            print(f"   ⚙️  UoW improvements: {len(uow_improvements)}")
            print(f"   📜 Contract updates: {len(contract_updates)}")
            print(f"   🥒 BDD enhancements: {len(bdd_enhancements)}")

            return recommendations

        except Exception as e:
            print(f"❌ Recommendation generation failed: {e}")
            return recommendations

    def _get_git_changes(self, days: int) -> List[Dict[str, Any]]:
        """Get git changes from the last N days"""
        changes = []
        try:
            import subprocess

            # Get git log for the last N days
            cmd = [
                "git", "log",
                f"--since={days} days ago",
                "--pretty=format:%H|%s|%an|%ad",
                "--date=iso",
                "--name-status"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.ssot_dir.parent.parent))

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                current_commit = None

                for line in lines:
                    if '|' in line:  # Commit info line
                        parts = line.split('|')
                        current_commit = {
                            "hash": parts[0],
                            "message": parts[1],
                            "author": parts[2],
                            "date": parts[3],
                            "files": []
                        }
                        changes.append(current_commit)
                    elif current_commit and line.strip():  # File change line
                        current_commit["files"].append(line.strip())

        except Exception as e:
            print(f"⚠️  Could not get git changes: {e}")

        return changes

    def _extract_patterns_from_changes(self, git_changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract patterns from code changes"""
        patterns = []

        # Analyze commit messages for patterns
        message_patterns = self._analyze_commit_message_patterns(git_changes)
        patterns.extend(message_patterns)

        # Analyze file change patterns
        file_patterns = self._analyze_file_change_patterns(git_changes)
        patterns.extend(file_patterns)

        return patterns

    def _analyze_commit_message_patterns(self, git_changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze commit messages for patterns"""
        patterns = []
        message_keywords = defaultdict(int)

        for change in git_changes:
            message = change["message"].lower()

            # Common patterns
            if "fix" in message or "bug" in message:
                message_keywords["bug_fix"] += 1
            if "refactor" in message:
                message_keywords["refactoring"] += 1
            if "test" in message:
                message_keywords["testing"] += 1
            if "performance" in message or "optimize" in message:
                message_keywords["performance"] += 1
            if "security" in message:
                message_keywords["security"] += 1

        # Convert to patterns
        for keyword, count in message_keywords.items():
            if count >= 2:  # Pattern threshold
                patterns.append({
                    "id": f"COMMIT-PATTERN-{keyword.upper()}",
                    "name": f"Frequent {keyword.replace('_', ' ').title()}",
                    "category": "development_practice",
                    "description": f"Frequent commits related to {keyword.replace('_', ' ')}",
                    "frequency": count,
                    "confidence": min(count / 10.0, 1.0),
                    "examples": [change["message"] for change in git_changes if keyword in change["message"].lower()][:3]
                })

        return patterns

    def _analyze_file_change_patterns(self, git_changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze file change patterns"""
        patterns = []
        file_types = defaultdict(int)
        directories = defaultdict(int)

        for change in git_changes:
            for file_info in change["files"]:
                if '\t' in file_info:
                    status, filepath = file_info.split('\t', 1)

                    # Analyze file extensions
                    if '.' in filepath:
                        ext = filepath.split('.')[-1]
                        file_types[ext] += 1

                    # Analyze directories
                    if '/' in filepath:
                        directory = filepath.split('/')[0]
                        directories[directory] += 1

        # Convert to patterns
        for file_type, count in file_types.items():
            if count >= 3:
                patterns.append({
                    "id": f"FILE-PATTERN-{file_type.upper()}",
                    "name": f"Frequent {file_type} Changes",
                    "category": "file_modification",
                    "description": f"Frequent changes to {file_type} files",
                    "frequency": count,
                    "confidence": min(count / 15.0, 1.0),
                    "examples": []
                })

        return patterns

    def _extract_decisions_from_changes(self, git_changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract architecture decisions from changes"""
        decisions = []

        for change in git_changes:
            message = change["message"]

            # Look for decision keywords
            decision_keywords = ["architecture", "design", "approach", "strategy", "framework", "library"]

            if any(keyword in message.lower() for keyword in decision_keywords):
                decision_id = f"DEC-{change['hash'][:8]}"
                decisions.append({
                    "id": decision_id,
                    "title": message,
                    "context": f"Commit: {change['hash']}",
                    "decision": message,
                    "rationale": "Extracted from commit message",
                    "consequences": [],
                    "alternatives": [],
                    "status": "accepted",
                    "date": change["date"]
                })

        return decisions

    def _extract_lessons_from_changes(self, git_changes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract lessons from changes (especially bug fixes)"""
        lessons = []

        for change in git_changes:
            message = change["message"].lower()

            # Look for bug fix patterns
            if "fix" in message or "bug" in message or "error" in message:
                lesson_id = f"LESSON-{change['hash'][:8]}"
                lessons.append({
                    "id": lesson_id,
                    "category": "bug_fix",
                    "situation": f"Code change in commit {change['hash'][:8]}",
                    "problem": f"Issue requiring fix: {change['message']}",
                    "solution": "Code changes applied",
                    "outcome": "Issue resolved",
                    "tags": ["bug_fix", "code_change"],
                    "impact": "medium",
                    "recorded_at": change["date"]
                })

        return lessons

    def _load_runtime_metrics(self, metrics_file: Optional[str]) -> Optional[Dict[str, Any]]:
        """Load runtime metrics from file or monitoring system"""
        # Placeholder implementation
        # In real implementation, this would connect to monitoring systems
        return None

    def _analyze_performance_patterns(self, metrics_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze performance patterns from metrics"""
        return []

    def _identify_bottlenecks(self, metrics_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks"""
        return []

    def _find_optimization_opportunities(self, metrics_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find optimization opportunities"""
        return []

    def _recommend_new_requirements(self, patterns: Dict[str, Any], lessons: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend new requirements based on patterns and lessons"""
        recommendations = []

        # Analyze patterns for missing requirements
        if patterns:
            for pattern_id, pattern in patterns.items():
                if pattern.get("category") == "security" and pattern.get("frequency", 0) > 5:
                    recommendations.append({
                        "type": "functional_requirement",
                        "title": f"Enhanced Security Requirement",
                        "description": f"Based on frequent security-related changes: {pattern.get('description')}",
                        "priority": "High",
                        "source": f"Pattern: {pattern_id}"
                    })

        return recommendations

    def _recommend_uow_improvements(self, patterns: Dict[str, Any], decisions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend UoW improvements"""
        return []

    def _recommend_contract_updates(self, lessons: Dict[str, Any], decisions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend contract updates"""
        return []

    def _recommend_bdd_enhancements(self, patterns: Dict[str, Any], lessons: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend BDD enhancements"""
        return []

    def _save_patterns(self, patterns: List[Dict[str, Any]]):
        """Save discovered patterns"""
        if not patterns:
            return

        existing_patterns = self._load_patterns()

        for pattern in patterns:
            existing_patterns[pattern["id"]] = pattern

        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            yaml.dump(existing_patterns, f, allow_unicode=True, default_flow_style=False)

    def _save_decisions(self, decisions: List[Dict[str, Any]]):
        """Save extracted decisions"""
        if not decisions:
            return

        existing_decisions = self._load_decisions()

        for decision in decisions:
            existing_decisions[decision["id"]] = decision

        with open(self.decisions_file, 'w', encoding='utf-8') as f:
            yaml.dump(existing_decisions, f, allow_unicode=True, default_flow_style=False)

    def _save_lessons(self, lessons: List[Dict[str, Any]]):
        """Save learned lessons"""
        if not lessons:
            return

        existing_lessons = self._load_lessons()

        for lesson in lessons:
            existing_lessons[lesson["id"]] = lesson

        with open(self.lessons_file, 'w', encoding='utf-8') as f:
            yaml.dump(existing_lessons, f, allow_unicode=True, default_flow_style=False)

    def _save_insights(self, insights: Dict[str, Any]):
        """Save runtime insights"""
        with open(self.insights_file, 'w', encoding='utf-8') as f:
            yaml.dump(insights, f, allow_unicode=True, default_flow_style=False)

    def _load_patterns(self) -> Dict[str, Any]:
        """Load existing patterns"""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _load_decisions(self) -> Dict[str, Any]:
        """Load existing decisions"""
        if self.decisions_file.exists():
            with open(self.decisions_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _load_lessons(self) -> Dict[str, Any]:
        """Load existing lessons"""
        if self.lessons_file.exists():
            with open(self.lessons_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    # Pattern detection methods (placeholders for specific detectors)
    def _detect_error_handling_patterns(self, code: str) -> List[Pattern]:
        return []

    def _detect_validation_patterns(self, code: str) -> List[Pattern]:
        return []

    def _detect_config_patterns(self, code: str) -> List[Pattern]:
        return []

    def _detect_testing_patterns(self, code: str) -> List[Pattern]:
        return []

    def _detect_performance_patterns(self, code: str) -> List[Pattern]:
        return []

def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Knowledge Accumulation and Learning Engine")
    parser.add_argument("--analyze-recent", action="store_true", help="Analyze recent code changes")
    parser.add_argument("--analyze-runtime", action="store_true", help="Analyze runtime metrics")
    parser.add_argument("--record-lesson", nargs=5, metavar=('CATEGORY', 'SITUATION', 'PROBLEM', 'SOLUTION', 'OUTCOME'),
                       help="Record a lesson learned")
    parser.add_argument("--generate-recommendations", action="store_true", help="Generate SSOT recommendations")
    parser.add_argument("--days", type=int, default=7, help="Number of days to analyze (default: 7)")
    parser.add_argument("--metrics-file", help="Runtime metrics file path")

    args = parser.parse_args()

    try:
        learning_engine = LearningEngine()

        if args.analyze_recent:
            result = learning_engine.analyze_recent_changes(args.days)
            print(f"\n✅ Analysis completed: {json.dumps(result, indent=2, ensure_ascii=False)}")

        elif args.analyze_runtime:
            result = learning_engine.analyze_runtime_metrics(args.metrics_file)
            print(f"\n✅ Runtime analysis completed: {json.dumps(result, indent=2, ensure_ascii=False)}")

        elif args.record_lesson:
            category, situation, problem, solution, outcome = args.record_lesson
            lesson_id = learning_engine.record_lesson(category, situation, problem, solution, outcome)
            print(f"\n✅ Lesson recorded: {lesson_id}")

        elif args.generate_recommendations:
            recommendations = learning_engine.generate_ssot_recommendations()
            print(f"\n✅ Recommendations generated: {json.dumps(recommendations, indent=2, ensure_ascii=False)}")

        else:
            # Default: analyze recent changes
            result = learning_engine.analyze_recent_changes(args.days)
            print(f"\n✅ Default analysis completed: {json.dumps(result, indent=2, ensure_ascii=False)}")

        sys.exit(0)

    except Exception as e:
        print(f"❌ Learning engine error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()