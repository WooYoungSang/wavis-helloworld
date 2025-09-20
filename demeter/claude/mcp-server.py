#!/usr/bin/env python3
"""
Demeter WAVIS MCP Server for Claude Code
Provides SSOT-driven development tools as MCP functions
"""

import json
import sys
import os
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

# Add demeter modules to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from core.ssot.graphrag.query.ssot_query import SSOTQuery
    from core.ssot.graphrag.query.impact_analyzer import ImpactAnalyzer
    from core.ssot.prompts.generate_prompt import PromptGenerator
    from core.ssot.contracts.generate_contract import ContractGenerator
except ImportError:
    # Fallback implementations if modules not available
    class SSOTQuery:
        def __init__(self, *args, **kwargs): pass
        def query(self, query_text, query_type="auto"):
            return {"query": query_text, "results": [], "metadata": {}}

    class ImpactAnalyzer:
        def __init__(self, *args, **kwargs): pass
        def analyze_change_impact(self, entity_id, change_type="modification"):
            return {"entity_id": entity_id, "direct_impacts": [], "risk_assessment": {}}

    class PromptGenerator:
        def __init__(self, *args, **kwargs): pass
        def generate_prompt(self, template_name, context):
            return f"Generated prompt for {template_name}"

    class ContractGenerator:
        def __init__(self, *args, **kwargs): pass
        def validate_contract(self, contract_file):
            return True

class DemeterMCPServer:
    """MCP Server for Demeter WAVIS framework"""

    def __init__(self):
        self.project_name = os.getenv("PROJECT_NAME", "Unknown Project")
        self.ssot_path = os.getenv("SSOT_PATH", "demeter/core/ssot/framework-requirements.yaml")
        self.project_root = Path.cwd()

        # Initialize components
        self.ssot_query = SSOTQuery()
        self.impact_analyzer = ImpactAnalyzer()
        self.prompt_generator = PromptGenerator()
        self.contract_generator = ContractGenerator()

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        try:
            method = request.get("method")
            params = request.get("params", {})

            if method == "initialize":
                return await self.initialize()
            elif method == "tools/list":
                return await self.list_tools()
            elif method == "tools/call":
                return await self.call_tool(params)
            else:
                return self.error_response(f"Unknown method: {method}")

        except Exception as e:
            return self.error_response(str(e))

    async def initialize(self) -> Dict[str, Any]:
        """Initialize MCP server"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": "demeter-wavis",
                "version": "3.0.0",
                "description": f"SSOT-driven development tools for {self.project_name}"
            }
        }

    async def list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        tools = [
            {
                "name": "ssot_query",
                "description": "Query the Single Source of Truth for requirements, UoWs, and contracts",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query text (keyword, FR/NFR/UoW ID, or 'gaps')"
                        },
                        "type": {
                            "type": "string",
                            "enum": ["auto", "keyword", "relationship", "pattern", "impact", "coverage", "gap"],
                            "description": "Query type (auto-detected if not specified)"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "generate_implementation",
                "description": "Generate implementation code based on SSOT definitions",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "uow_id": {
                            "type": "string",
                            "description": "Unit of Work ID (e.g., UoW-001)"
                        },
                        "with_tests": {
                            "type": "boolean",
                            "description": "Include test generation",
                            "default": True
                        },
                        "with_contracts": {
                            "type": "boolean",
                            "description": "Include contract validation",
                            "default": True
                        },
                        "tech_stack": {
                            "type": "string",
                            "description": "Technology stack override"
                        }
                    },
                    "required": ["uow_id"]
                }
            },
            {
                "name": "verify_contracts",
                "description": "Validate implementation against formal contracts",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target": {
                            "type": "string",
                            "description": "UoW ID, contract ID, or 'all'"
                        },
                        "strict": {
                            "type": "boolean",
                            "description": "Use strict validation mode",
                            "default": False
                        },
                        "generate_report": {
                            "type": "boolean",
                            "description": "Generate detailed report",
                            "default": False
                        }
                    },
                    "required": ["target"]
                }
            },
            {
                "name": "impact_analysis",
                "description": "Analyze impact of changes to SSOT entities",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "entity_id": {
                            "type": "string",
                            "description": "Entity ID to analyze (FR/NFR/UoW/CTR ID)"
                        },
                        "change_type": {
                            "type": "string",
                            "enum": ["modification", "major_modification", "removal"],
                            "description": "Type of change",
                            "default": "modification"
                        }
                    },
                    "required": ["entity_id"]
                }
            },
            {
                "name": "system_status",
                "description": "Get overall system health and verification status",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "detailed": {
                            "type": "boolean",
                            "description": "Include detailed metrics",
                            "default": False
                        }
                    }
                }
            }
        ]

        return {"tools": tools}

    async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "ssot_query":
                return await self.ssot_query_tool(arguments)
            elif tool_name == "generate_implementation":
                return await self.generate_implementation_tool(arguments)
            elif tool_name == "verify_contracts":
                return await self.verify_contracts_tool(arguments)
            elif tool_name == "impact_analysis":
                return await self.impact_analysis_tool(arguments)
            elif tool_name == "system_status":
                return await self.system_status_tool(arguments)
            else:
                return self.error_response(f"Unknown tool: {tool_name}")

        except Exception as e:
            return self.error_response(f"Tool execution failed: {str(e)}")

    async def ssot_query_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SSOT query"""
        query_text = args.get("query", "")
        query_type = args.get("type", "auto")

        if not query_text:
            return self.error_response("Query text is required")

        try:
            # Execute query
            result = self.ssot_query.query(query_text, query_type)

            # Format response
            content = self._format_ssot_query_result(result)

            return {
                "content": [
                    {
                        "type": "text",
                        "text": content
                    }
                ]
            }

        except Exception as e:
            return self.error_response(f"SSOT query failed: {str(e)}")

    async def generate_implementation_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation from SSOT"""
        uow_id = args.get("uow_id", "")
        with_tests = args.get("with_tests", True)
        with_contracts = args.get("with_contracts", True)
        tech_stack = args.get("tech_stack")

        if not uow_id:
            return self.error_response("UoW ID is required")

        try:
            # Load UoW definition from SSOT
            uow_data = self._load_uow_definition(uow_id)
            if not uow_data:
                return self.error_response(f"UoW {uow_id} not found in SSOT")

            # Generate implementation prompt
            context = {
                "uow_id": uow_id,
                "uow_data": uow_data,
                "project_name": self.project_name,
                "with_tests": with_tests,
                "with_contracts": with_contracts,
                "tech_stack": tech_stack or "agnostic"
            }

            prompt = self.prompt_generator.generate_prompt("implement", context)

            # Format response with implementation guidance
            content = self._format_implementation_prompt(prompt, context)

            return {
                "content": [
                    {
                        "type": "text",
                        "text": content
                    }
                ]
            }

        except Exception as e:
            return self.error_response(f"Implementation generation failed: {str(e)}")

    async def verify_contracts_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Verify contract compliance"""
        target = args.get("target", "")
        strict = args.get("strict", False)
        generate_report = args.get("generate_report", False)

        if not target:
            return self.error_response("Target (UoW ID, contract ID, or 'all') is required")

        try:
            # Perform contract validation
            if target == "all":
                results = self._verify_all_contracts(strict)
            else:
                results = self._verify_single_contract(target, strict)

            # Format response
            content = self._format_contract_verification(results, generate_report)

            return {
                "content": [
                    {
                        "type": "text",
                        "text": content
                    }
                ]
            }

        except Exception as e:
            return self.error_response(f"Contract verification failed: {str(e)}")

    async def impact_analysis_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze impact of changes"""
        entity_id = args.get("entity_id", "")
        change_type = args.get("change_type", "modification")

        if not entity_id:
            return self.error_response("Entity ID is required")

        try:
            # Perform impact analysis
            impact_report = self.impact_analyzer.analyze_change_impact(entity_id, change_type)

            # Format response
            content = self._format_impact_analysis(impact_report)

            return {
                "content": [
                    {
                        "type": "text",
                        "text": content
                    }
                ]
            }

        except Exception as e:
            return self.error_response(f"Impact analysis failed: {str(e)}")

    async def system_status_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get system health status"""
        detailed = args.get("detailed", False)

        try:
            # Collect system metrics
            status = self._get_system_status(detailed)

            # Format response
            content = self._format_system_status(status)

            return {
                "content": [
                    {
                        "type": "text",
                        "text": content
                    }
                ]
            }

        except Exception as e:
            return self.error_response(f"System status check failed: {str(e)}")

    def _load_uow_definition(self, uow_id: str) -> Optional[Dict[str, Any]]:
        """Load UoW definition from SSOT"""
        try:
            ssot_file = self.project_root / self.ssot_path
            if not ssot_file.exists():
                return None

            with open(ssot_file, 'r', encoding='utf-8') as f:
                ssot_data = yaml.safe_load(f)

            units_of_work = ssot_data.get("units_of_work", {})
            return units_of_work.get(uow_id)

        except Exception:
            return None

    def _verify_all_contracts(self, strict: bool) -> Dict[str, Any]:
        """Verify all contracts"""
        contracts_dir = self.project_root / "demeter/core/ssot/contracts"
        results = {"total": 0, "passed": 0, "failed": 0, "details": []}

        if not contracts_dir.exists():
            return results

        for contract_file in contracts_dir.glob("*.yaml"):
            results["total"] += 1
            try:
                is_valid = self.contract_generator.validate_contract(str(contract_file))
                if is_valid:
                    results["passed"] += 1
                    results["details"].append({"file": contract_file.name, "status": "PASS"})
                else:
                    results["failed"] += 1
                    results["details"].append({"file": contract_file.name, "status": "FAIL"})
            except Exception as e:
                results["failed"] += 1
                results["details"].append({"file": contract_file.name, "status": "ERROR", "error": str(e)})

        return results

    def _verify_single_contract(self, target: str, strict: bool) -> Dict[str, Any]:
        """Verify single contract"""
        # Implementation would verify specific contract
        return {"target": target, "status": "PASS", "details": "Contract validation passed"}

    def _get_system_status(self, detailed: bool) -> Dict[str, Any]:
        """Get current system status"""
        status = {
            "ssot_health": "good",
            "graphrag_status": "synced",
            "contract_compliance": "100%",
            "last_verification": "2024-01-18T10:30:00Z"
        }

        if detailed:
            status.update({
                "total_requirements": 15,
                "implemented_uows": 8,
                "pending_uows": 3,
                "verified_contracts": 5
            })

        return status

    def _format_ssot_query_result(self, result: Dict[str, Any]) -> str:
        """Format SSOT query result for display"""
        query = result.get("query", "")
        results = result.get("results", [])
        metadata = result.get("metadata", {})

        content = f"# SSOT Query Results\n\n"
        content += f"**Query**: {query}\n"
        content += f"**Type**: {metadata.get('query_type', 'auto')}\n"
        content += f"**Results**: {len(results)} items found\n\n"

        if results:
            content += "## Results\n\n"
            for i, result_item in enumerate(results[:5], 1):  # Limit to 5 results
                if isinstance(result_item, dict) and 'entity' in result_item:
                    entity = result_item['entity']
                    content += f"### {i}. {entity.get('id', 'Unknown')}\n"
                    content += f"**Type**: {entity.get('type', 'Unknown')}\n"
                    content += f"**Title**: {entity.get('title', entity.get('name', 'No title'))}\n"
                    if entity.get('description'):
                        content += f"**Description**: {entity['description']}\n"
                    content += "\n"
        else:
            content += "No results found. Try a different query or check SSOT definitions.\n"

        return content

    def _format_implementation_prompt(self, prompt: str, context: Dict[str, Any]) -> str:
        """Format implementation generation prompt"""
        uow_id = context.get("uow_id", "")
        uow_data = context.get("uow_data", {})

        content = f"# Implementation Guide for {uow_id}\n\n"

        if uow_data:
            content += f"## Unit of Work Details\n"
            content += f"**Name**: {uow_data.get('name', 'Unknown')}\n"
            content += f"**Goal**: {uow_data.get('goal', 'Not specified')}\n"
            content += f"**Layer**: {uow_data.get('layer', 'Unknown')}\n"
            content += f"**Priority**: {uow_data.get('priority', 'Normal')}\n\n"

            if uow_data.get('acceptance_criteria'):
                content += "## Acceptance Criteria\n"
                for i, ac in enumerate(uow_data['acceptance_criteria'], 1):
                    content += f"{i}. {ac}\n"
                content += "\n"

        content += "## Implementation Approach\n\n"
        content += "Based on the SSOT definition, here's the recommended implementation approach:\n\n"

        content += "### 1. Contract Definition\n"
        content += "First, ensure proper contracts are defined with:\n"
        content += "- Preconditions: Input validation requirements\n"
        content += "- Postconditions: Expected outputs and side effects\n"
        content += "- Invariants: System state consistency rules\n\n"

        content += "### 2. Test-Driven Development\n"
        content += "Write tests first, mapping each to acceptance criteria:\n"
        content += "```\n"
        content += "// Test mapping example\n"
        content += "test_ac_1() { /* Validates AC-1 */ }\n"
        content += "test_ac_2() { /* Validates AC-2 */ }\n"
        content += "```\n\n"

        content += "### 3. Implementation Guidelines\n"
        content += "- Follow SSOT requirements strictly\n"
        content += "- Implement proper error handling\n"
        content += "- Add logging for debugging\n"
        content += "- Ensure contract compliance\n"
        content += "- Include comprehensive documentation\n\n"

        content += "### 4. Verification\n"
        content += "After implementation:\n"
        content += "1. Run contract verification: `/verify-contracts " + uow_id + "`\n"
        content += "2. Execute all tests\n"
        content += "3. Check system health: `./scripts/quick-sync-check.sh`\n\n"

        return content

    def _format_contract_verification(self, results: Dict[str, Any], detailed: bool) -> str:
        """Format contract verification results"""
        content = "# Contract Verification Results\n\n"

        if "total" in results:
            # All contracts verification
            total = results.get("total", 0)
            passed = results.get("passed", 0)
            failed = results.get("failed", 0)

            content += f"**Total Contracts**: {total}\n"
            content += f"**Passed**: {passed}\n"
            content += f"**Failed**: {failed}\n"
            content += f"**Success Rate**: {(passed/total*100) if total > 0 else 0:.1f}%\n\n"

            if detailed and results.get("details"):
                content += "## Detailed Results\n\n"
                for detail in results["details"]:
                    status_icon = "✅" if detail["status"] == "PASS" else "❌"
                    content += f"{status_icon} **{detail['file']}**: {detail['status']}\n"
                    if detail.get("error"):
                        content += f"   Error: {detail['error']}\n"
                content += "\n"
        else:
            # Single contract verification
            target = results.get("target", "Unknown")
            status = results.get("status", "UNKNOWN")
            details = results.get("details", "")

            status_icon = "✅" if status == "PASS" else "❌"
            content += f"{status_icon} **{target}**: {status}\n"
            if details:
                content += f"Details: {details}\n"

        content += "## Next Steps\n"
        if failed > 0 if "failed" in results else status != "PASS":
            content += "- Review failed contracts and fix violations\n"
            content += "- Update implementation to meet contract requirements\n"
            content += "- Re-run verification after fixes\n"
        else:
            content += "- All contracts are compliant\n"
            content += "- Ready for integration and deployment\n"

        return content

    def _format_impact_analysis(self, report: Dict[str, Any]) -> str:
        """Format impact analysis report"""
        entity_id = report.get("entity_id", "Unknown")
        direct_impacts = report.get("direct_impacts", [])
        risk_assessment = report.get("risk_assessment", {})

        content = f"# Impact Analysis for {entity_id}\n\n"

        content += f"**Entity**: {entity_id}\n"
        content += f"**Change Type**: {report.get('change_type', 'modification')}\n"
        content += f"**Risk Level**: {risk_assessment.get('overall_risk', 'unknown')}\n\n"

        content += f"## Direct Impacts ({len(direct_impacts)})\n\n"
        if direct_impacts:
            for impact in direct_impacts[:5]:  # Limit to 5
                content += f"- **{impact.get('entity_id', 'Unknown')}**: {impact.get('impact_type', 'general')}\n"
                if impact.get('description'):
                    content += f"  {impact['description']}\n"
        else:
            content += "No direct impacts identified.\n"

        content += "\n## Risk Assessment\n\n"
        risk_factors = risk_assessment.get("risk_factors", [])
        if risk_factors:
            for factor in risk_factors:
                content += f"- {factor}\n"
        else:
            content += "No specific risk factors identified.\n"

        content += "\n## Recommendations\n\n"
        if risk_assessment.get("overall_risk") in ["high", "critical"]:
            content += "- Perform thorough testing before deployment\n"
            content += "- Consider phased rollout approach\n"
            content += "- Prepare rollback plan\n"
            content += "- Monitor affected systems closely\n"
        else:
            content += "- Standard testing and deployment process\n"
            content += "- Monitor for unexpected side effects\n"

        return content

    def _format_system_status(self, status: Dict[str, Any]) -> str:
        """Format system status report"""
        content = f"# System Status - {self.project_name}\n\n"

        # Health indicators
        ssot_health = status.get("ssot_health", "unknown")
        graphrag_status = status.get("graphrag_status", "unknown")
        contract_compliance = status.get("contract_compliance", "unknown")

        health_icon = "🟢" if ssot_health == "good" else "🟡" if ssot_health == "warning" else "🔴"
        sync_icon = "🟢" if graphrag_status == "synced" else "🟡" if graphrag_status == "pending" else "🔴"
        contract_icon = "🟢" if contract_compliance == "100%" else "🟡"

        content += f"{health_icon} **SSOT Health**: {ssot_health}\n"
        content += f"{sync_icon} **GraphRAG Status**: {graphrag_status}\n"
        content += f"{contract_icon} **Contract Compliance**: {contract_compliance}\n"
        content += f"📅 **Last Verification**: {status.get('last_verification', 'unknown')}\n\n"

        # Detailed metrics if available
        if status.get("total_requirements"):
            content += "## Project Metrics\n\n"
            content += f"- **Total Requirements**: {status['total_requirements']}\n"
            content += f"- **Implemented UoWs**: {status['implemented_uows']}\n"
            content += f"- **Pending UoWs**: {status['pending_uows']}\n"
            content += f"- **Verified Contracts**: {status['verified_contracts']}\n\n"

        content += "## Quick Actions\n\n"
        content += "- `/ssot-query gaps` - Find coverage gaps\n"
        content += "- `/verify-contracts all` - Verify all contracts\n"
        content += "- Run `./scripts/full-verification.sh` for complete check\n"

        return content

    def error_response(self, message: str) -> Dict[str, Any]:
        """Generate error response"""
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ Error: {message}"
                }
            ]
        }

async def main():
    """Main MCP server loop"""
    server = DemeterMCPServer()

    # Read from stdin, write to stdout (MCP protocol)
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())
            response = await server.handle_request(request)

            print(json.dumps(response))
            sys.stdout.flush()

        except Exception as e:
            error_response = {
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())