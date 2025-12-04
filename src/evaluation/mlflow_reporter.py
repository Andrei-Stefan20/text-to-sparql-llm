"""
MLflow-based experiment tracking and reporting system.
Replaces custom ReportManager with professional ML tracking.
"""

import json
import mlflow
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.logging_config import get_logger

logger = get_logger(__name__)

# Configure seaborn style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class MLflowReporter:
    """
    Creates comprehensive reports with metrics, artifacts, and visualizations.
    """
    
    def __init__(
        self, 
        experiment_name: str,
        tracking_uri: Optional[str] = None,
        artifact_location: Optional[Path] = None
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
                artifact_location=str(artifact_location) if artifact_location else None
            )
        else:
            experiment_id = experiment.experiment_id
        
        mlflow.set_experiment(experiment_name)
        
        # Start run
        self.run = mlflow.start_run()
        self.run_id = self.run.info.run_id
        
        # Results storage
        self.results: List[Dict[str, Any]] = []
        
        logger.info(f"MLflow tracking started: {experiment_name} (run_id: {self.run_id})")
    
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
        metrics: Optional[Dict[str, float]] = None
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
        retry_success = sum(1 for r in self.results if r["attempts"] > 1 and r["is_valid"])
        
        avg_f1 = sum(r["f1_score"] for r in self.results) / total
        avg_attempts = sum(r["attempts"] for r in self.results) / total
        
        metrics = {
            "total_questions": total,
            "syntax_accuracy": valid_count / total,
            "answer_accuracy": correct_count / total,
            "avg_f1_score": avg_f1,
            "avg_attempts": avg_attempts,
            "retry_success_rate": retry_success / total if total > 0 else 0.0
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
        ax.set_title("F1 Score Distribution", fontsize=14, fontweight='bold')
        ax.set_xlabel("F1 Score")
        ax.set_ylabel("Count")
        plt.tight_layout()
        mlflow.log_figure(fig, "f1_distribution.png")
        plt.close()
        
        # 2. Success Rate by Attempts
        fig, ax = plt.subplots(figsize=(10, 6))
        attempt_stats = df.groupby('attempts').agg({
            'is_valid': 'mean',
            'f1_score': 'mean'
        }).reset_index()
        
        ax.bar(attempt_stats['attempts'], attempt_stats['is_valid'], 
               alpha=0.7, label='Syntax Valid Rate')
        ax.bar(attempt_stats['attempts'], attempt_stats['f1_score'], 
               alpha=0.7, label='Correct Answer Rate')
        ax.set_title("Success Rate by Number of Attempts", fontsize=14, fontweight='bold')
        ax.set_xlabel("Attempts")
        ax.set_ylabel("Success Rate")
        ax.legend()
        plt.tight_layout()
        mlflow.log_figure(fig, "attempts_success.png")
        plt.close()
        
        # 3. Error Type Distribution (if errors exist)
        errors = df[df['error_type'].notna()]
        if not errors.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            error_counts = errors['error_type'].value_counts()
            sns.barplot(x=error_counts.values, y=error_counts.index, ax=ax, palette="rocket")
            ax.set_title("Error Type Distribution", fontsize=14, fontweight='bold')
            ax.set_xlabel("Count")
            ax.set_ylabel("Error Type")
            plt.tight_layout()
            mlflow.log_figure(fig, "error_distribution.png")
            plt.close()
        
        # 4. F1 Score Over Time (question progression)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['id'], df['f1_score'], marker='o', linewidth=2, markersize=4)
        ax.axhline(y=df['f1_score'].mean(), color='r', linestyle='--', 
                   label=f'Average: {df["f1_score"].mean():.3f}')
        ax.set_title("F1 Score Progression", fontsize=14, fontweight='bold')
        ax.set_xlabel("Question ID")
        ax.set_ylabel("F1 Score")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        mlflow.log_figure(fig, "f1_progression.png")
        plt.close()
        
        logger.info("Generated 4 visualization charts")
    
    def save_detailed_results(self):
        """Save detailed results as JSON and CSV artifacts."""
        # JSON format
        results_json = {
            "run_id": self.run_id,
            "experiment": self.experiment_name,
            "timestamp": datetime.now().isoformat(),
            "summary": self.generate_summary_metrics(),
            "results": self.results
        }
        
        mlflow.log_dict(results_json, "detailed_results.json")
        
        # CSV format for easy analysis
        df = pd.DataFrame(self.results)
        csv_path = "results.csv"
        df.to_csv(csv_path, index=False)
        mlflow.log_artifact(csv_path)
        
        logger.info(f"Saved detailed results (JSON + CSV)")
    
    def generate_html_report(self):
        """Generate comprehensive HTML report."""
        summary = self.generate_summary_metrics()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SPARQL Evaluation Report - {self.experiment_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .metric {{ display: inline-block; margin: 15px; padding: 20px; background: #ecf0f1; border-radius: 5px; min-width: 200px; }}
                .metric-label {{ font-size: 12px; color: #7f8c8d; text-transform: uppercase; }}
                .metric-value {{ font-size: 32px; font-weight: bold; color: #2c3e50; }}
                .success {{ color: #27ae60; }}
                .warning {{ color: #f39c12; }}
                .error {{ color: #e74c3c; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background: #3498db; color: white; padding: 12px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ecf0f1; }}
                tr:hover {{ background: #f8f9fa; }}
                .code {{ background: #f4f4f4; padding: 10px; border-left: 3px solid #3498db; font-family: monospace; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 Text-to-SPARQL Evaluation Report</h1>
                <p><strong>Experiment:</strong> {self.experiment_name}</p>
                <p><strong>Run ID:</strong> {self.run_id}</p>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <h2>📊 Summary Metrics</h2>
                <div>
                    <div class="metric">
                        <div class="metric-label">Total Questions</div>
                        <div class="metric-value">{summary.get('total_questions', 0)}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Syntax Accuracy</div>
                        <div class="metric-value success">{summary.get('syntax_accuracy', 0)*100:.1f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Answer Accuracy</div>
                        <div class="metric-value success">{summary.get('answer_accuracy', 0)*100:.1f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Average F1 Score</div>
                        <div class="metric-value">{summary.get('avg_f1_score', 0):.3f}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Avg Attempts</div>
                        <div class="metric-value">{summary.get('avg_attempts', 0):.2f}</div>
                    </div>
                </div>
                
                <h2>📝 Detailed Results</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Question</th>
                            <th>F1</th>
                            <th>Valid</th>
                            <th>Attempts</th>
                            <th>Error</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for r in self.results[:50]:  # Show first 50
            status_class = "success" if r["f1_score"] == 1.0 else ("warning" if r["is_valid"] else "error")
            html += f"""
                        <tr>
                            <td>{r['id']}</td>
                            <td>{r['question'][:80]}...</td>
                            <td class="{status_class}">{r['f1_score']:.3f}</td>
                            <td>{'✓' if r['is_valid'] else '✗'}</td>
                            <td>{r['attempts']}</td>
                            <td>{r['error_type'] or '-'}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
                
                <p style="margin-top: 40px; color: #7f8c8d; text-align: center;">
                    Generated by MLflow Reporter | Text-to-SPARQL LLM Pipeline
                </p>
            </div>
        </body>
        </html>
        """
        
        html_path = "report.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        mlflow.log_artifact(html_path)
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
