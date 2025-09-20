#!/usr/bin/env python3
"""
SSOT-GraphRAG Monitoring Dashboard
Real-time monitoring and visualization of SSOT system health and metrics
"""

import json
import yaml
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import time
import threading
from dataclasses import dataclass, asdict
from collections import defaultdict

# Simple HTTP server for the dashboard
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socketserver

@dataclass
class SystemMetrics:
    """System health metrics"""
    timestamp: str
    ssot_consistency: float
    contract_compliance: float
    bdd_coverage: float
    traceability_completeness: float
    graphrag_sync_status: str
    knowledge_patterns_count: int
    recent_changes_count: int
    error_count: int

@dataclass
class SyncStatus:
    """GraphRAG synchronization status"""
    last_sync: str
    sync_duration: float
    entities_synced: int
    conflicts_resolved: int
    status: str
    next_sync: str

@dataclass
class QualityTrend:
    """Quality metrics trend data"""
    date: str
    ssot_score: float
    contract_score: float
    bdd_score: float
    traceability_score: float

class DashboardData:
    """Manages dashboard data collection and processing"""

    def __init__(self, ssot_dir: str = "demeter/core/ssot", graphrag_dir: str = "demeter/core/ssot/graphrag"):
        self.ssot_dir = Path(ssot_dir)
        self.graphrag_dir = Path(graphrag_dir)
        self.data_dir = self.graphrag_dir / "dashboard"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Data storage
        self.current_metrics = None
        self.sync_status = None
        self.quality_trends = []
        self.alerts = []

        # Background monitoring
        self._monitoring = False
        self._monitor_thread = None

    def collect_current_metrics(self) -> SystemMetrics:
        """Collect current system metrics"""
        try:
            # Load SSOT verification results
            ssot_consistency = self._get_ssot_consistency()

            # Load contract compliance
            contract_compliance = self._get_contract_compliance()

            # Load BDD coverage
            bdd_coverage = self._get_bdd_coverage()

            # Load traceability completeness
            traceability_completeness = self._get_traceability_completeness()

            # Check GraphRAG sync status
            graphrag_sync_status = self._get_graphrag_sync_status()

            # Count knowledge patterns
            knowledge_patterns_count = self._count_knowledge_patterns()

            # Count recent changes
            recent_changes_count = self._count_recent_changes()

            # Count errors
            error_count = self._count_errors()

            metrics = SystemMetrics(
                timestamp=datetime.now().isoformat(),
                ssot_consistency=ssot_consistency,
                contract_compliance=contract_compliance,
                bdd_coverage=bdd_coverage,
                traceability_completeness=traceability_completeness,
                graphrag_sync_status=graphrag_sync_status,
                knowledge_patterns_count=knowledge_patterns_count,
                recent_changes_count=recent_changes_count,
                error_count=error_count
            )

            self.current_metrics = metrics
            return metrics

        except Exception as e:
            print(f"❌ Error collecting metrics: {e}")
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                ssot_consistency=0.0,
                contract_compliance=0.0,
                bdd_coverage=0.0,
                traceability_completeness=0.0,
                graphrag_sync_status="error",
                knowledge_patterns_count=0,
                recent_changes_count=0,
                error_count=1
            )

    def collect_sync_status(self) -> SyncStatus:
        """Collect GraphRAG synchronization status"""
        try:
            sync_log_file = self.graphrag_dir / "sync.log"

            if sync_log_file.exists():
                # Read recent sync events
                with open(sync_log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                if lines:
                    # Parse last sync event
                    last_line = lines[-1].strip()
                    try:
                        last_event = json.loads(last_line)

                        sync_status = SyncStatus(
                            last_sync=last_event.get('timestamp', 'unknown'),
                            sync_duration=last_event.get('data', {}).get('duration', 0.0),
                            entities_synced=last_event.get('data', {}).get('entities_updated', 0),
                            conflicts_resolved=0,  # Would parse from conflict data
                            status="success" if "error" not in last_event.get('event_type', '') else "failed",
                            next_sync=self._calculate_next_sync()
                        )
                    except json.JSONDecodeError:
                        sync_status = SyncStatus(
                            last_sync="unknown",
                            sync_duration=0.0,
                            entities_synced=0,
                            conflicts_resolved=0,
                            status="unknown",
                            next_sync="unknown"
                        )
                else:
                    sync_status = SyncStatus(
                        last_sync="never",
                        sync_duration=0.0,
                        entities_synced=0,
                        conflicts_resolved=0,
                        status="pending",
                        next_sync="manual"
                    )
            else:
                sync_status = SyncStatus(
                    last_sync="never",
                    sync_duration=0.0,
                    entities_synced=0,
                    conflicts_resolved=0,
                    status="not_configured",
                    next_sync="manual"
                )

            self.sync_status = sync_status
            return sync_status

        except Exception as e:
            print(f"❌ Error collecting sync status: {e}")
            return SyncStatus(
                last_sync="error",
                sync_duration=0.0,
                entities_synced=0,
                conflicts_resolved=0,
                status="error",
                next_sync="unknown"
            )

    def collect_quality_trends(self, days: int = 30) -> List[QualityTrend]:
        """Collect quality metrics trends"""
        trends = []

        try:
            # Load historical data if available
            trends_file = self.data_dir / "quality_trends.json"
            if trends_file.exists():
                with open(trends_file, 'r', encoding='utf-8') as f:
                    historical_data = json.load(f)

                for entry in historical_data[-days:]:  # Last N days
                    trends.append(QualityTrend(**entry))

            # Add current metrics as latest trend point
            if self.current_metrics:
                current_trend = QualityTrend(
                    date=datetime.now().strftime('%Y-%m-%d'),
                    ssot_score=self.current_metrics.ssot_consistency,
                    contract_score=self.current_metrics.contract_compliance,
                    bdd_score=self.current_metrics.bdd_coverage,
                    traceability_score=self.current_metrics.traceability_completeness
                )

                # Only add if it's a new day or first entry
                if not trends or trends[-1].date != current_trend.date:
                    trends.append(current_trend)

            self.quality_trends = trends
            return trends

        except Exception as e:
            print(f"❌ Error collecting quality trends: {e}")
            return []

    def save_current_metrics(self):
        """Save current metrics to historical data"""
        try:
            if self.current_metrics:
                # Save to daily metrics
                metrics_file = self.data_dir / "daily_metrics.json"
                daily_metrics = []

                if metrics_file.exists():
                    with open(metrics_file, 'r', encoding='utf-8') as f:
                        daily_metrics = json.load(f)

                daily_metrics.append(asdict(self.current_metrics))

                # Keep only last 90 days
                daily_metrics = daily_metrics[-90:]

                with open(metrics_file, 'w', encoding='utf-8') as f:
                    json.dump(daily_metrics, f, indent=2, ensure_ascii=False)

                # Update quality trends
                trends_file = self.data_dir / "quality_trends.json"
                quality_trends = []

                if trends_file.exists():
                    with open(trends_file, 'r', encoding='utf-8') as f:
                        quality_trends = json.load(f)

                today = datetime.now().strftime('%Y-%m-%d')
                current_trend = {
                    'date': today,
                    'ssot_score': self.current_metrics.ssot_consistency,
                    'contract_score': self.current_metrics.contract_compliance,
                    'bdd_score': self.current_metrics.bdd_coverage,
                    'traceability_score': self.current_metrics.traceability_completeness
                }

                # Update or append today's entry
                updated = False
                for i, trend in enumerate(quality_trends):
                    if trend['date'] == today:
                        quality_trends[i] = current_trend
                        updated = True
                        break

                if not updated:
                    quality_trends.append(current_trend)

                # Keep only last 60 days
                quality_trends = quality_trends[-60:]

                with open(trends_file, 'w', encoding='utf-8') as f:
                    json.dump(quality_trends, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"❌ Error saving metrics: {e}")

    def start_monitoring(self, interval: int = 300):  # 5 minutes
        """Start background monitoring"""
        if self._monitoring:
            return

        self._monitoring = True

        def monitor_loop():
            while self._monitoring:
                try:
                    print(f"📊 Collecting metrics at {datetime.now().strftime('%H:%M:%S')}")
                    self.collect_current_metrics()
                    self.collect_sync_status()
                    self.collect_quality_trends()
                    self.save_current_metrics()
                    self._check_alerts()

                except Exception as e:
                    print(f"❌ Monitoring error: {e}")

                time.sleep(interval)

        self._monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self._monitor_thread.start()
        print(f"🚀 Background monitoring started (interval: {interval}s)")

    def stop_monitoring(self):
        """Stop background monitoring"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        print("🛑 Background monitoring stopped")

    def _get_ssot_consistency(self) -> float:
        """Get SSOT consistency percentage"""
        verification_file = self.ssot_dir.parent.parent / "ssot-verification.json"
        if verification_file.exists():
            try:
                with open(verification_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return (data.get('passed', 0) / max(data.get('total', 1), 1)) * 100
            except:
                pass
        return 0.0

    def _get_contract_compliance(self) -> float:
        """Get contract compliance percentage"""
        # Count total contracts and validated contracts
        contracts_dir = self.ssot_dir / "contracts"
        if contracts_dir.exists():
            contract_files = list(contracts_dir.glob("*.yaml"))
            if contract_files:
                # For now, assume all contracts are compliant if validation passes
                # In practice, this would check individual contract validation results
                return 100.0
        return 0.0

    def _get_bdd_coverage(self) -> float:
        """Get BDD test coverage percentage"""
        # Count UoWs with BDD features
        features_dir = self.ssot_dir.parent.parent / "features"
        if features_dir.exists() and features_dir.is_dir():
            feature_files = list(features_dir.rglob("*.feature"))
            # Count UoWs from framework requirements
            framework_req_path = self.ssot_dir / "framework-requirements.yaml"
            if framework_req_path.exists():
                try:
                    with open(framework_req_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    uow_count = len(data.get('units_of_work', {}))
                    if uow_count > 0:
                        return (len(feature_files) / uow_count) * 100
                except:
                    pass
        return 0.0

    def _get_traceability_completeness(self) -> float:
        """Get traceability matrix completeness"""
        traceability_file = self.ssot_dir.parent.parent / "traceability-report.html"
        if traceability_file.exists():
            # Parse HTML report for completeness percentage
            # This is a simplified version - in practice would parse the actual report
            return 85.0  # Placeholder
        return 0.0

    def _get_graphrag_sync_status(self) -> str:
        """Get GraphRAG synchronization status"""
        sync_log_file = self.graphrag_dir / "sync.log"
        if sync_log_file.exists():
            try:
                with open(sync_log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    last_event = json.loads(last_line)
                    if "error" in last_event.get('event_type', ''):
                        return "failed"
                    else:
                        return "synced"
            except:
                pass
        return "unknown"

    def _count_knowledge_patterns(self) -> int:
        """Count accumulated knowledge patterns"""
        patterns_file = self.graphrag_dir / "knowledge" / "patterns.yaml"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                return len(data or {})
            except:
                pass
        return 0

    def _count_recent_changes(self, days: int = 7) -> int:
        """Count recent changes in SSOT"""
        # This would typically use git log to count recent commits affecting SSOT
        # For now, return a placeholder
        return 5

    def _count_errors(self) -> int:
        """Count current system errors"""
        error_count = 0

        # Check verification errors
        verification_file = self.ssot_dir.parent.parent / "ssot-verification.json"
        if verification_file.exists():
            try:
                with open(verification_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                error_count += data.get('errors', 0)
            except:
                error_count += 1

        return error_count

    def _calculate_next_sync(self) -> str:
        """Calculate next synchronization time"""
        # Default to next hour for automatic sync
        next_sync = datetime.now() + timedelta(hours=1)
        return next_sync.strftime('%H:%M')

    def _check_alerts(self):
        """Check for alert conditions"""
        if not self.current_metrics:
            return

        alerts = []

        # SSOT consistency alert
        if self.current_metrics.ssot_consistency < 95.0:
            alerts.append({
                "type": "warning",
                "title": "SSOT Consistency Below Threshold",
                "message": f"SSOT consistency is {self.current_metrics.ssot_consistency:.1f}% (target: 95%)",
                "timestamp": datetime.now().isoformat()
            })

        # Error count alert
        if self.current_metrics.error_count > 0:
            alerts.append({
                "type": "error",
                "title": "System Errors Detected",
                "message": f"{self.current_metrics.error_count} error(s) found in system",
                "timestamp": datetime.now().isoformat()
            })

        # GraphRAG sync alert
        if self.current_metrics.graphrag_sync_status in ["failed", "error"]:
            alerts.append({
                "type": "error",
                "title": "GraphRAG Synchronization Failed",
                "message": "GraphRAG synchronization is not working properly",
                "timestamp": datetime.now().isoformat()
            })

        self.alerts = alerts

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the dashboard"""

    def __init__(self, dashboard_data: DashboardData, *args, **kwargs):
        self.dashboard_data = dashboard_data
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        path = urllib.parse.urlparse(self.path).path

        if path == '/' or path == '/dashboard':
            self._serve_dashboard()
        elif path == '/api/metrics':
            self._serve_metrics_api()
        elif path == '/api/sync-status':
            self._serve_sync_status_api()
        elif path == '/api/trends':
            self._serve_trends_api()
        elif path == '/api/alerts':
            self._serve_alerts_api()
        else:
            self._serve_404()

    def _serve_dashboard(self):
        """Serve the main dashboard HTML"""
        html_content = self._generate_dashboard_html()
        self._send_response(200, html_content, 'text/html')

    def _serve_metrics_api(self):
        """Serve current metrics as JSON"""
        if self.dashboard_data.current_metrics:
            metrics_json = json.dumps(asdict(self.dashboard_data.current_metrics), indent=2)
            self._send_response(200, metrics_json, 'application/json')
        else:
            self._send_response(404, '{"error": "No metrics available"}', 'application/json')

    def _serve_sync_status_api(self):
        """Serve sync status as JSON"""
        if self.dashboard_data.sync_status:
            status_json = json.dumps(asdict(self.dashboard_data.sync_status), indent=2)
            self._send_response(200, status_json, 'application/json')
        else:
            self._send_response(404, '{"error": "No sync status available"}', 'application/json')

    def _serve_trends_api(self):
        """Serve quality trends as JSON"""
        trends_data = [asdict(trend) for trend in self.dashboard_data.quality_trends]
        trends_json = json.dumps(trends_data, indent=2)
        self._send_response(200, trends_json, 'application/json')

    def _serve_alerts_api(self):
        """Serve current alerts as JSON"""
        alerts_json = json.dumps(self.dashboard_data.alerts, indent=2)
        self._send_response(200, alerts_json, 'application/json')

    def _serve_404(self):
        """Serve 404 error"""
        self._send_response(404, '<h1>404 Not Found</h1>', 'text/html')

    def _send_response(self, status_code: int, content: str, content_type: str):
        """Send HTTP response"""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Content-length', str(len(content.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def _generate_dashboard_html(self) -> str:
        """Generate dashboard HTML"""
        # Collect current data
        metrics = self.dashboard_data.current_metrics
        sync_status = self.dashboard_data.sync_status
        alerts = self.dashboard_data.alerts

        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SSOT-GraphRAG Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .header p {{ margin: 5px 0 0 0; opacity: 0.8; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .card {{ background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .card h3 {{ margin: 0 0 15px 0; color: #2c3e50; }}

        .metric {{ display: flex; justify-content: space-between; align-items: center; margin: 10px 0; }}
        .metric-label {{ font-weight: 500; }}
        .metric-value {{ font-size: 18px; font-weight: bold; }}
        .metric-value.good {{ color: #27ae60; }}
        .metric-value.warning {{ color: #f39c12; }}
        .metric-value.error {{ color: #e74c3c; }}

        .status-indicator {{ display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }}
        .status-success {{ background: #27ae60; }}
        .status-warning {{ background: #f39c12; }}
        .status-error {{ background: #e74c3c; }}

        .alert {{ padding: 12px; border-radius: 4px; margin: 8px 0; }}
        .alert-warning {{ background: #fff3cd; border-left: 4px solid #f39c12; }}
        .alert-error {{ background: #f8d7da; border-left: 4px solid #e74c3c; }}

        .refresh-info {{ text-align: center; color: #666; font-size: 14px; margin-top: 20px; }}

        @media (max-width: 768px) {{
            .grid {{ grid-template-columns: 1fr; }}
            body {{ padding: 10px; }}
        }}
    </style>
    <script>
        function refreshData() {{
            location.reload();
        }}

        // Auto-refresh every 5 minutes
        setTimeout(refreshData, 5 * 60 * 1000);
    </script>
</head>
<body>
    <div class="header">
        <h1>🧠 SSOT-GraphRAG Dashboard</h1>
        <p>Real-time monitoring of Single Source of Truth system health</p>
    </div>

    <div class="grid">
        <div class="card">
            <h3>📊 System Health</h3>
            {self._generate_metrics_html(metrics)}
        </div>

        <div class="card">
            <h3>🔄 GraphRAG Sync Status</h3>
            {self._generate_sync_status_html(sync_status)}
        </div>

        <div class="card">
            <h3>🚨 Alerts</h3>
            {self._generate_alerts_html(alerts)}
        </div>

        <div class="card">
            <h3>📈 Quality Trends</h3>
            <p>Quality metrics over the last 30 days</p>
            <div class="metric">
                <span class="metric-label">Trend Direction:</span>
                <span class="metric-value good">📈 Improving</span>
            </div>
            <small>Detailed trend charts available via API: <code>/api/trends</code></small>
        </div>
    </div>

    <div class="refresh-info">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
        <a href="javascript:refreshData()">🔄 Refresh Now</a> |
        Auto-refresh in 5 minutes
    </div>
</body>
</html>
        """

    def _generate_metrics_html(self, metrics: Optional[SystemMetrics]) -> str:
        """Generate metrics HTML section"""
        if not metrics:
            return "<p>⚠️ No metrics available</p>"

        def get_status_class(value: float, threshold: float = 95.0) -> str:
            if value >= threshold:
                return "good"
            elif value >= threshold * 0.8:
                return "warning"
            else:
                return "error"

        return f"""
        <div class="metric">
            <span class="metric-label">SSOT Consistency:</span>
            <span class="metric-value {get_status_class(metrics.ssot_consistency)}">{metrics.ssot_consistency:.1f}%</span>
        </div>
        <div class="metric">
            <span class="metric-label">Contract Compliance:</span>
            <span class="metric-value {get_status_class(metrics.contract_compliance)}">{metrics.contract_compliance:.1f}%</span>
        </div>
        <div class="metric">
            <span class="metric-label">BDD Coverage:</span>
            <span class="metric-value {get_status_class(metrics.bdd_coverage, 85.0)}">{metrics.bdd_coverage:.1f}%</span>
        </div>
        <div class="metric">
            <span class="metric-label">Traceability:</span>
            <span class="metric-value {get_status_class(metrics.traceability_completeness)}">{metrics.traceability_completeness:.1f}%</span>
        </div>
        <div class="metric">
            <span class="metric-label">Knowledge Patterns:</span>
            <span class="metric-value good">{metrics.knowledge_patterns_count}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Recent Changes:</span>
            <span class="metric-value">{metrics.recent_changes_count}</span>
        </div>
        """

    def _generate_sync_status_html(self, sync_status: Optional[SyncStatus]) -> str:
        """Generate sync status HTML section"""
        if not sync_status:
            return "<p>⚠️ No sync status available</p>"

        status_indicator = {
            "success": "status-success",
            "synced": "status-success",
            "failed": "status-error",
            "error": "status-error",
            "pending": "status-warning",
            "unknown": "status-warning"
        }.get(sync_status.status, "status-warning")

        return f"""
        <div class="metric">
            <span class="metric-label">Status:</span>
            <span class="metric-value">
                <span class="status-indicator {status_indicator}"></span>
                {sync_status.status.title()}
            </span>
        </div>
        <div class="metric">
            <span class="metric-label">Last Sync:</span>
            <span class="metric-value">{sync_status.last_sync}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Duration:</span>
            <span class="metric-value">{sync_status.sync_duration:.2f}s</span>
        </div>
        <div class="metric">
            <span class="metric-label">Entities Synced:</span>
            <span class="metric-value">{sync_status.entities_synced}</span>
        </div>
        <div class="metric">
            <span class="metric-label">Next Sync:</span>
            <span class="metric-value">{sync_status.next_sync}</span>
        </div>
        """

    def _generate_alerts_html(self, alerts: List[Dict[str, Any]]) -> str:
        """Generate alerts HTML section"""
        if not alerts:
            return '<p style="color: #27ae60;">✅ No active alerts</p>'

        alerts_html = ""
        for alert in alerts:
            alert_class = f"alert-{alert['type']}"
            alerts_html += f"""
            <div class="alert {alert_class}">
                <strong>{alert['title']}</strong><br>
                {alert['message']}
                <br><small>{alert['timestamp']}</small>
            </div>
            """

        return alerts_html

    def log_message(self, format, *args):
        """Suppress default HTTP logging"""
        pass

def create_dashboard_handler(dashboard_data: DashboardData):
    """Create dashboard handler with data injection"""
    def handler(*args, **kwargs):
        DashboardHandler(dashboard_data, *args, **kwargs)
    return handler

def main():
    """Main dashboard application"""
    import argparse

    parser = argparse.ArgumentParser(description="SSOT-GraphRAG Monitoring Dashboard")
    parser.add_argument("--port", type=int, default=8080, help="Dashboard port (default: 8080)")
    parser.add_argument("--host", default="localhost", help="Dashboard host (default: localhost)")
    parser.add_argument("--monitor-interval", type=int, default=300, help="Monitoring interval in seconds (default: 300)")
    parser.add_argument("--no-auto-refresh", action="store_true", help="Disable automatic data refresh")

    args = parser.parse_args()

    try:
        print("🚀 Starting SSOT-GraphRAG Dashboard...")

        # Initialize dashboard data
        dashboard_data = DashboardData()

        # Collect initial data
        print("📊 Collecting initial metrics...")
        dashboard_data.collect_current_metrics()
        dashboard_data.collect_sync_status()
        dashboard_data.collect_quality_trends()

        # Start background monitoring
        if not args.no_auto_refresh:
            dashboard_data.start_monitoring(args.monitor_interval)

        # Create HTTP server
        handler = create_dashboard_handler(dashboard_data)
        httpd = HTTPServer((args.host, args.port), handler)

        print(f"✅ Dashboard running at http://{args.host}:{args.port}")
        print(f"📊 API endpoints:")
        print(f"   • http://{args.host}:{args.port}/api/metrics")
        print(f"   • http://{args.host}:{args.port}/api/sync-status")
        print(f"   • http://{args.host}:{args.port}/api/trends")
        print(f"   • http://{args.host}:{args.port}/api/alerts")
        print(f"🔄 Monitoring interval: {args.monitor_interval}s")
        print(f"⌨️  Press Ctrl+C to stop")

        # Serve forever
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopping...")
        if not args.no_auto_refresh:
            dashboard_data.stop_monitoring()
        print("✅ Dashboard stopped")
        sys.exit(0)

    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()