"""
MLflow-based experiment tracking and reporting system.
Replaces custom ReportManager with professional ML tracking.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import mlflow
import pandas as pd
import seaborn as sns
from src.logging_config import get_logger

logger = get_logger(__name__)

# Configure seaborn style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)


class MLflowReporter:
    """
    Creates comprehensive reports with metrics, artifacts, and visualizations.
    """

    def __init__(
        self,
        experiment_name: str,
        tracking_uri: Optional[str] = None,
        artifact_location: Optional[Path] = None,
    ):
        """
        Initialize MLflow experiment tracker.

        Args:
            experiment_name: Name of the experiment (e.g., "gemini-evaluation")
            tracking_uri: MLflow tracking URI (default: ./mlruns)
            artifact_location: Custom artifact storage location
        """
        self.experiment_name = experiment_name

        # Set tracking URI (local by default)
        if tracking_uri is None:
            tracking_uri = "file:./mlruns"
        mlflow.set_tracking_uri(tracking_uri)

        # Create or get experiment
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            experiment_id = mlflow.create_experiment(
                experiment_name,
                artifact_location=str(artifact_location) if artifact_location else None,
            )
        else:
            experiment_id = experiment.experiment_id

        mlflow.set_experiment(experiment_name)

        # Start run
        self.run = mlflow.start_run()
        self.run_id = self.run.info.run_id

        # Create timestamped output directory
        from pathlib import Path

        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("reports") / f"run_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Results storage
        self.results: List[Dict[str, Any]] = []

        logger.info(
            f"MLflow tracking started: {experiment_name} (run_id: {self.run_id})"
        )
        logger.info(f"Output directory: {self.output_dir}")

    def log_params(self, params: Dict[str, Any]):
        """Log hyperparameters and configuration."""
        mlflow.log_params(params)

    def log_question_result(
        self,
        question_id: int,
        question: str,
        gold_sparql: str,
        generated_sparql: str,
        is_valid: bool,
        f1_score: float,
        attempts: int,
        error_info: Optional[Dict] = None,
        metrics: Optional[Dict[str, float]] = None,
        prompt: Optional[str] = None,
    ):
        """
        Log individual question evaluation result.

        Args:
            question_id: Question number (1-indexed)
            question: Natural language question
            gold_sparql: Ground truth SPARQL
            generated_sparql: LLM-generated SPARQL
            is_valid: Whether query is syntactically valid
            f1_score: Answer correctness F1 score
            attempts: Number of retry attempts needed
            error_info: Error details if failed
            metrics: Additional custom metrics (syntax, execution, etc.)
            prompt: Full prompt sent to the model
        """
        result = {
            "id": question_id,
            "question": question,
            "gold_sparql": gold_sparql,
            "generated_sparql": generated_sparql,
            "is_valid": is_valid,
            "f1_score": f1_score,
            "attempts": attempts,
            "error_type": error_info.get("type") if error_info else None,
            "error_detail": error_info.get("detail") if error_info else None,
            "prompt": prompt,
        }

        # Add custom metrics
        if metrics:
            result.update(metrics)

        self.results.append(result)

        # Log metrics to MLflow (step = question_id)
        mlflow.log_metric("f1_score", f1_score, step=question_id)
        mlflow.log_metric("is_valid", 1.0 if is_valid else 0.0, step=question_id)
        mlflow.log_metric("attempts", attempts, step=question_id)

        if metrics:
            for key, value in metrics.items():
                mlflow.log_metric(key, value, step=question_id)

    def generate_summary_metrics(self) -> Dict[str, float]:
        """Calculate aggregate metrics across all questions."""
        if not self.results:
            return {}

        total = len(self.results)
        valid_count = sum(1 for r in self.results if r["is_valid"])
        correct_count = sum(1 for r in self.results if r["f1_score"] == 1.0)
        retry_success = sum(
            1 for r in self.results if r["attempts"] > 1 and r["is_valid"]
        )

        avg_f1 = sum(r["f1_score"] for r in self.results) / total
        avg_attempts = sum(r["attempts"] for r in self.results) / total

        metrics = {
            "total_questions": total,
            "syntax_accuracy": valid_count / total,
            "answer_accuracy": correct_count / total,
            "avg_f1_score": avg_f1,
            "avg_attempts": avg_attempts,
            "retry_success_rate": retry_success / total if total > 0 else 0.0,
        }

        # Log summary metrics
        for key, value in metrics.items():
            mlflow.log_metric(f"summary_{key}", value)

        return metrics

    def create_visualizations(self):
        """Generate and save visualization charts."""
        if not self.results:
            logger.warning("No results to visualize")
            return

        df = pd.DataFrame(self.results)

        # 1. F1 Score Distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=df, x="f1_score", bins=20, kde=True, ax=ax)
        ax.set_title("F1 Score Distribution", fontsize=14, fontweight="bold")
        ax.set_xlabel("F1 Score")
        ax.set_ylabel("Count")
        plt.tight_layout()
        chart_path = self.output_dir / "f1_distribution.png"
        fig.savefig(chart_path, dpi=150, bbox_inches="tight")
        mlflow.log_artifact(str(chart_path))
        plt.close()

        # 2. Success Rate by Attempts
        fig, ax = plt.subplots(figsize=(10, 6))
        attempt_stats = (
            df.groupby("attempts")
            .agg({"is_valid": "mean", "f1_score": "mean"})
            .reset_index()
        )

        ax.bar(
            attempt_stats["attempts"],
            attempt_stats["is_valid"],
            alpha=0.7,
            label="Syntax Valid Rate",
        )
        ax.bar(
            attempt_stats["attempts"],
            attempt_stats["f1_score"],
            alpha=0.7,
            label="Correct Answer Rate",
        )
        ax.set_title(
            "Success Rate by Number of Attempts", fontsize=14, fontweight="bold"
        )
        ax.set_xlabel("Attempts")
        ax.set_ylabel("Success Rate")
        ax.legend()
        plt.tight_layout()
        chart_path = self.output_dir / "attempts_success.png"
        fig.savefig(chart_path, dpi=150, bbox_inches="tight")
        mlflow.log_artifact(str(chart_path))
        plt.close()

        # 3. Error Type Distribution (if errors exist)
        errors = df[df["error_type"].notna()]
        if not errors.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            error_counts = errors["error_type"].value_counts()
            sns.barplot(
                x=error_counts.values, y=error_counts.index, ax=ax, palette="rocket"
            )
            ax.set_title("Error Type Distribution", fontsize=14, fontweight="bold")
            ax.set_xlabel("Count")
            ax.set_ylabel("Error Type")
            plt.tight_layout()
            chart_path = self.output_dir / "error_distribution.png"
            fig.savefig(chart_path, dpi=150, bbox_inches="tight")
            mlflow.log_artifact(str(chart_path))
            plt.close()

        # 4. F1 Score Over Time (question progression)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df["id"], df["f1_score"], marker="o", linewidth=2, markersize=4)
        ax.axhline(
            y=df["f1_score"].mean(),
            color="r",
            linestyle="--",
            label=f'Average: {df["f1_score"].mean():.3f}',
        )
        ax.set_title("F1 Score Progression", fontsize=14, fontweight="bold")
        ax.set_xlabel("Question ID")
        ax.set_ylabel("F1 Score")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        chart_path = self.output_dir / "f1_progression.png"
        fig.savefig(chart_path, dpi=150, bbox_inches="tight")
        mlflow.log_artifact(str(chart_path))
        plt.close()

        logger.info(f"Generated 4 visualization charts in {self.output_dir}")

    def save_detailed_results(self):
        """Save detailed results as JSON and CSV artifacts."""
        # JSON format
        results_json = {
            "run_id": self.run_id,
            "experiment": self.experiment_name,
            "timestamp": datetime.now().isoformat(),
            "summary": self.generate_summary_metrics(),
            "results": self.results,
        }

        json_path = self.output_dir / "results.json"
        with open(json_path, "w", encoding="utf-8") as f:
            import json

            json.dump(results_json, f, indent=2, ensure_ascii=False)
        mlflow.log_artifact(str(json_path))

        # CSV format for easy analysis
        df = pd.DataFrame(self.results)
        csv_path = self.output_dir / "results.csv"
        df.to_csv(csv_path, index=False)
        mlflow.log_artifact(str(csv_path))

        logger.info(f"Saved detailed results in {self.output_dir} (JSON + CSV)")

    def generate_html_report(self):
        """Generate comprehensive professional HTML report."""
        from datetime import datetime

        summary = self.generate_summary_metrics()

        # Calculate additional statistics
        syntax_valid = sum(1 for r in self.results if r["is_valid"])
        perfect_matches = sum(1 for r in self.results if r["f1_score"] == 1.0)
        avg_f1 = (
            sum(r["f1_score"] for r in self.results) / len(self.results)
            if self.results
            else 0
        )
        total_attempts = sum(r["attempts"] for r in self.results)

        # Error distribution
        error_types = {}
        for r in self.results:
            if r["error_type"]:
                error_types[r["error_type"]] = error_types.get(r["error_type"], 0) + 1

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SPARQL Generation Evaluation Report</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: #f8f9fa; 
                    color: #212529;
                    line-height: 1.6;
                }}
                .header {{
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    color: white;
                    padding: 40px 0;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header-content {{
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 0 40px;
                }}
                .header h1 {{ 
                    font-size: 32px; 
                    font-weight: 600; 
                    margin-bottom: 10px;
                }}
                .header-meta {{
                    opacity: 0.9;
                    font-size: 14px;
                    margin-top: 15px;
                }}
                .container {{ 
                    max-width: 1400px; 
                    margin: 0 auto; 
                    padding: 40px;
                }}
                
                /* Metrics Grid */
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                    gap: 20px;
                    margin: 30px 0;
                }}
                .metric-card {{
                    background: white;
                    border-radius: 8px;
                    padding: 25px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    border-left: 4px solid #1e3c72;
                }}
                .metric-label {{
                    font-size: 12px;
                    font-weight: 600;
                    text-transform: uppercase;
                    color: #6c757d;
                    letter-spacing: 0.5px;
                    margin-bottom: 10px;
                }}
                .metric-value {{
                    font-size: 36px;
                    font-weight: 700;
                    color: #1e3c72;
                }}
                .metric-sublabel {{
                    font-size: 13px;
                    color: #868e96;
                    margin-top: 8px;
                }}
                
                /* Section */
                .section {{
                    background: white;
                    border-radius: 8px;
                    padding: 30px;
                    margin: 25px 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                }}
                .section-title {{
                    font-size: 20px;
                    font-weight: 600;
                    color: #212529;
                    margin-bottom: 20px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #e9ecef;
                }}
                
                /* Table */
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 14px;
                }}
                thead {{
                    background: #f8f9fa;
                }}
                th {{
                    padding: 14px 12px;
                    text-align: left;
                    font-weight: 600;
                    color: #495057;
                    border-bottom: 2px solid #dee2e6;
                }}
                td {{
                    padding: 12px;
                    border-bottom: 1px solid #f1f3f5;
                    vertical-align: top;
                }}
                tr:hover {{
                    background: #f8f9fa;
                }}
                
                /* Code blocks */
                .code-block {{
                    background: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    padding: 12px;
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 13px;
                    overflow-x: auto;
                    margin: 8px 0;
                    white-space: pre-wrap;
                    word-break: break-word;
                }}
                
                /* Status badges */
                .badge {{
                    display: inline-block;
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                }}
                .badge-success {{ background: #d4edda; color: #155724; }}
                .badge-warning {{ background: #fff3cd; color: #856404; }}
                .badge-error {{ background: #f8d7da; color: #721c24; }}
                
                /* Expandable */
                .expandable {{
                    cursor: pointer;
                    user-select: none;
                }}
                .expandable:hover {{
                    background: #f1f3f5;
                }}
                .details {{
                    display: none;
                    margin-top: 15px;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 4px;
                }}
                .details.show {{
                    display: block;
                }}
                
                /* Footer */
                .footer {{
                    text-align: center;
                    padding: 30px;
                    color: #6c757d;
                    font-size: 13px;
                }}
                
                /* Print styles */
                @media print {{
                    .header {{ background: #1e3c72 !important; }}
                    .section {{ page-break-inside: avoid; }}
                }}
            </style>
            <script>
                function toggleDetails(id) {{
                    const details = document.getElementById('details-' + id);
                    details.classList.toggle('show');
                }}
            </script>
        </head>
        <body>
            <div class="header">
                <div class="header-content">
                    <h1>Text-to-SPARQL Generation: Evaluation Report</h1>
                    <div class="header-meta">
                        <div><strong>Experiment:</strong> {self.experiment_name}</div>
                        <div><strong>Run ID:</strong> {self.run_id}</div>
                        <div><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                    </div>
                </div>
            </div>
            
            <div class="container">
                <!-- Executive Summary -->
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Total Questions</div>
                        <div class="metric-value">{summary.get('total_questions', 0)}</div>
                        <div class="metric-sublabel">Evaluation dataset size</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Syntax Validity Rate</div>
                        <div class="metric-value">{summary.get('syntax_accuracy', 0)*100:.1f}%</div>
                        <div class="metric-sublabel">{syntax_valid}/{summary.get('total_questions', 0)} queries valid</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Answer Correctness</div>
                        <div class="metric-value">{summary.get('answer_accuracy', 0)*100:.1f}%</div>
                        <div class="metric-sublabel">{perfect_matches}/{summary.get('total_questions', 0)} perfect matches</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Mean F1 Score</div>
                        <div class="metric-value">{avg_f1:.3f}</div>
                        <div class="metric-sublabel">Result overlap with gold standard</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Average Attempts</div>
                        <div class="metric-value">{summary.get('avg_attempts', 1):.2f}</div>
                        <div class="metric-sublabel">{total_attempts} total attempts</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Retry Success Rate</div>
                        <div class="metric-value">{summary.get('retry_success_rate', 0)*100:.1f}%</div>
                        <div class="metric-sublabel">Self-correction effectiveness</div>
                    </div>
                </div>"""

        # Error distribution
        if error_types:
            html += """
                <div class="section">
                    <h2 class="section-title">Error Distribution</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Error Type</th>
                                <th>Count</th>
                                <th>Percentage</th>
                            </tr>
                        </thead>
                        <tbody>"""

            for error_type, count in sorted(
                error_types.items(), key=lambda x: x[1], reverse=True
            ):
                percentage = (count / len(self.results)) * 100
                html += f"""
                            <tr>
                                <td>{error_type}</td>
                                <td>{count}</td>
                                <td>{percentage:.1f}%</td>
                            </tr>"""

            html += """
                        </tbody>
                    </table>
                </div>"""

        # Detailed results
        html += """
                <div class="section">
                    <h2 class="section-title">Detailed Evaluation Results</h2>
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 40px;">ID</th>
                                <th>Question</th>
                                <th style="width: 80px;">F1 Score</th>
                                <th style="width: 100px;">Status</th>
                                <th style="width: 80px;">Attempts</th>
                            </tr>
                        </thead>
                        <tbody>"""

        for idx, r in enumerate(self.results, 1):
            status_badge = (
                "badge-success"
                if r["f1_score"] == 1.0
                else ("badge-warning" if r["is_valid"] else "badge-error")
            )
            status_text = (
                "Perfect"
                if r["f1_score"] == 1.0
                else ("Valid" if r["is_valid"] else "Invalid")
            )

            html += f"""
                            <tr class="expandable" onclick="toggleDetails({idx})">
                                <td><strong>{idx}</strong></td>
                                <td>{r['question']}</td>
                                <td><strong>{r['f1_score']:.3f}</strong></td>
                                <td><span class="badge {status_badge}">{status_text}</span></td>
                                <td>{r['attempts']}</td>
                            </tr>
                            <tr>
                                <td colspan="5">
                                    <div id="details-{idx}" class="details">
                                        <table style="width: 100%; margin: 0;">
                                            <tr>
                                                <td style="width: 50%; border: none; padding-right: 15px;">
                                                    <strong>Generated SPARQL:</strong>
                                                    <div class="code-block">{r.get('generated_sparql', 'N/A')}</div>
                                                </td>
                                                <td style="width: 50%; border: none;">
                                                    <strong>Gold SPARQL:</strong>
                                                    <div class="code-block">{r.get('gold_sparql', 'N/A')}</div>
                                                </td>
                                            </tr>"""

            if r.get("prompt"):
                html += f"""
                                            <tr>
                                                <td colspan="2" style="border: none; padding-top: 15px;">
                                                    <strong>Prompt Sent to Model:</strong>
                                                    <div class="code-block">{r['prompt'][:2000]}{'...' if len(r.get('prompt', '')) > 2000 else ''}</div>
                                                </td>
                                            </tr>"""

            if r.get("error_type"):
                html += f"""
                                            <tr>
                                                <td colspan="2" style="border: none; padding-top: 10px;">
                                                    <strong>Error Details:</strong> {r['error_type']}
                                                    {f" - {r.get('error_detail', '')}" if r.get('error_detail') else ''}
                                                </td>
                                            </tr>"""

            html += """
                                        </table>
                                    </div>
                                </td>
                            </tr>"""

        html += (
            """
                        </tbody>
                    </table>
                </div>
                
                <div class="footer">
                    <p>Generated by MLflow Reporter - Text-to-SPARQL Evaluation System</p>
                    <p>Report generated at: """
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + """</p>
                </div>
            </div>
        </body>
        </html>
        """
        )

        # Save to timestamped output directory
        html_path = self.output_dir / "report.html"

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Also save as latest for easy access
        from pathlib import Path

        latest_path = Path("reports") / "report.html"
        with open(latest_path, "w", encoding="utf-8") as f:
            f.write(html)

        mlflow.log_artifact(str(html_path))
        logger.info(f"Generated HTML report: {html_path}")

    def finalize(self):
        """
        Finalize experiment: generate all reports and close MLflow run.
        Call this at the end of evaluation.
        """
        logger.info("Finalizing evaluation report...")

        # Generate summary metrics
        summary = self.generate_summary_metrics()

        # Create visualizations
        self.create_visualizations()

        # Save detailed results
        self.save_detailed_results()

        # Generate HTML report
        self.generate_html_report()

        # End MLflow run
        mlflow.end_run()

        logger.info(f"✓ Evaluation complete!")
        logger.info(f"  View results: mlflow ui --port 5000")
        logger.info(f"  Run ID: {self.run_id}")
        logger.info(f"  Summary: {summary}")

        return summary
