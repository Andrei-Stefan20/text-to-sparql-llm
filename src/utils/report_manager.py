import logging
import json
import datetime
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Any

try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

logger = logging.getLogger(__name__)

class ReportManager:
    """Manages evaluation metrics, logging, and report generation."""
    
    def __init__(self, project_root: Path, model_name: str, run_prefix: str = "run"):
        self.model_name = model_name
        self.start_time = datetime.datetime.now()
        self.project_root = project_root
        
        date_str = self.start_time.strftime("%Y-%m-%d")
        self.base_report_dir = project_root / "reports" / date_str
        self.base_report_dir.mkdir(parents=True, exist_ok=True)
        
        existing_runs = [d for d in self.base_report_dir.iterdir() if d.is_dir()]
        run_id = len(existing_runs) + 1
        time_str = self.start_time.strftime("%H%M%S")
        
        self.folder_name = f"{run_prefix}_{model_name}_{run_id:03d}_{time_str}"
        self.run_dir = self.base_report_dir / self.folder_name
        self.run_dir.mkdir(exist_ok=True)
        
        self.stats = {
            "meta": {
                "date": date_str, 
                "model": model_name, 
                "run_id": run_id,
                "start_time": time_str
            },
            "metrics": {
                "total": 0, 
                "valid_syntax": 0, 
                "correct_answer": 0, 
                "avg_f1": 0.0, 
                "retries_successful": 0
            },
            "results": []
        }
        logger.info(f"Report initialized at: {self.run_dir}")

    def _format_bindings(self, bindings: Optional[List[Dict]]) -> List[str]:
        """Converts SPARQL result bindings to human-readable format."""
        if not bindings:
            return []
        formatted = []
        for row in bindings:
            values = [v['value'].split('/')[-1] for v in row.values()] 
            formatted.append(f"({', '.join(values)})")
        return formatted

    def log_entry(self, question: str, gold_sparql: str, generated_sparql: str, 
                  raw_response: str, is_valid: bool, error_info: Optional[Dict], 
                  f1_score: float, attempts: int, prompt: str, context: Any, 
                  gold_results: Optional[List], gen_results: Optional[List]):
        """
        Records a single evaluation entry and updates aggregate metrics.
        
        Args:
            question: Natural language input question
            gold_sparql: Reference SPARQL query
            generated_sparql: Model-generated SPARQL query
            raw_response: Unprocessed model output
            is_valid: Whether the query passed syntax validation
            error_info: Dictionary containing error type and details
            f1_score: Result similarity score
            attempts: Number of generation attempts needed
            prompt: Full prompt sent to the model
            context: Schema context used in generation
            gold_results: Reference query execution results
            gen_results: Generated query execution results
        """
        fmt_gold = self._format_bindings(gold_results)
        fmt_gen = self._format_bindings(gen_results)

        status_label = "UNKNOWN"
        if not is_valid:
            status_label = "SYNTAX_ERROR"
            if error_info and error_info.get("type") == "Execution Error":
                status_label = "EXECUTION_ERROR"
        else:
            if f1_score == 1.0:
                status_label = "CORRECT"
            elif f1_score > 0:
                status_label = "PARTIAL_MATCH"
            else:
                status_label = "WRONG_ANSWER"

        entry = {
            "id": self.stats["metrics"]["total"] + 1,
            "question": question,
            "status_label": status_label,
            "is_valid": is_valid,
            "error_type": error_info.get("type") if error_info else None,
            "error_detail": error_info.get("detail") if error_info else None,
            "metrics": {
                "f1_score": f1_score, 
                "attempts_needed": attempts
            },
            "queries": {
                "gold": gold_sparql, 
                "generated": generated_sparql,
                "raw_response": raw_response 
            },
            "execution": {
                "gold_count": len(fmt_gold),
                "gen_count": len(fmt_gen),
                "gold_data": fmt_gold,
                "gen_data": fmt_gen
            },
            "debug": {
                "prompt": prompt, 
                "context": context 
            }
        }
        self.stats["results"].append(entry)
        
        # Update Aggregate Metrics
        m = self.stats["metrics"]
        m["total"] += 1
        if is_valid: m["valid_syntax"] += 1
        if f1_score == 1.0: m["correct_answer"] += 1
        if attempts > 1 and is_valid and f1_score > 0: m["retries_successful"] += 1
        
        if m["total"] > 0:
            total_f1 = sum(r['metrics']['f1_score'] for r in self.stats['results'])
            m["avg_f1"] = round(total_f1 / m["total"], 4)
            
        self._flush_to_disk()

    def _generate_plots(self):
        """Generates performance visualization charts for the report."""
        if not MATPLOTLIB_AVAILABLE or not self.stats["results"]:
            return

        try:
            sns.set_theme(style="whitegrid")
        except:
            plt.style.use('ggplot')

        results = self.stats['results']
        f1_scores = [r['metrics']['f1_score'] for r in results]
        statuses = [r['status_label'] for r in results]
        
        plt.figure(figsize=(10, 6))
        plt.hist(f1_scores, bins=[0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.01], color='#2c3e50', edgecolor='white', alpha=0.8)
        plt.title('Distribution of F1 Scores', fontsize=14, pad=20)
        plt.xlabel('F1 Score', fontsize=12)
        plt.ylabel('Frequency (Questions)', fontsize=12)
        plt.axvline(self.stats['metrics']['avg_f1'], color='#e74c3c', linestyle='dashed', linewidth=1, label=f"Avg F1: {self.stats['metrics']['avg_f1']:.2f}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.run_dir / "f1_distribution.png", dpi=150)
        plt.close()

        status_counts = pd.Series(statuses).value_counts()
        
        plt.figure(figsize=(10, 6))
        colors = {'CORRECT': '#27ae60', 'PARTIAL_MATCH': '#f39c12', 'WRONG_ANSWER': '#c0392b', 'SYNTAX_ERROR': '#7f8c8d', 'EXECUTION_ERROR': '#8e44ad'}
        bar_colors = [colors.get(x, '#95a5a6') for x in status_counts.index]
        
        status_counts.plot(kind='bar', color=bar_colors, edgecolor='black', alpha=0.8)
        plt.title('Evaluation Outcomes by Type', fontsize=14, pad=20)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.run_dir / "outcome_analysis.png", dpi=150)
        plt.close()

    def _write_markdown(self, f):
        """Generates comprehensive Markdown report with metrics and analysis."""
        m = self.stats['metrics']
        total = m['total']
        syn_acc = (m['valid_syntax'] / total * 100) if total > 0 else 0
        ans_acc = (m['correct_answer'] / total * 100) if total > 0 else 0
        
        f.write(f"# Text-to-SPARQL Evaluation Report\n\n")
        f.write(f"**Model Architecture:** `{self.model_name}`  \n")
        f.write(f"**Evaluation Date:** {self.stats['meta']['date']}  \n")
        f.write(f"**Run ID:** `{self.folder_name}`\n\n")
        
        f.write("## 1. Executive Summary\n\n")
        f.write("| Key Metric | Value | Definition |\n")
        f.write("| :--- | :--- | :--- |\n")
        f.write(f"| **Average F1 Score** | **{m['avg_f1']:.4f}** | Harmonic mean of precision and recall (0-1). |\n")
        f.write(f"| **Exact Match Rate** | {ans_acc:.2f}% | Percentage of perfectly correct answers. |\n")
        f.write(f"| **Syntax Validity** | {syn_acc:.2f}% | Percentage of queries that executed without errors. |\n")
        f.write(f"| **Self-Correction** | {m['retries_successful']} | Number of times the model fixed its own errors. |\n\n"))

        # Visualizations
        if MATPLOTLIB_AVAILABLE:
            f.write("## 2. Visual Analysis\n\n")
            f.write("### F1 Score Distribution & Outcome Breakdown\n")
            f.write("The following charts illustrate the model's performance stability and error profile.\n\n")
            f.write("| F1 Score Histogram | Outcome Classification |\n")
            f.write("| :---: | :---: |\n")
            f.write("| ![F1 Distribution](f1_distribution.png) | ![Outcomes](outcome_analysis.png) |\n\n")
        
        # Detailed Results
        f.write("## 3. Detailed Question Analysis\n")
        f.write("Below is the itemized analysis for each processed question.\n\n")
        f.write("---\n")
        
        for item in reversed(self.stats["results"]):
            # Status Badge
            status = item['status_label']
            badge = f"**[{status}]**"
            
            f.write(f"### Question ID: {item['id']}\n\n")
            f.write(f"> **Input Question:** {item['question']}\n\n")
            
            # Status Line
            f.write(f"- **Status:** {badge}\n")
            f.write(f"- **F1 Score:** {item['metrics']['f1_score']:.4f}\n")
            f.write(f"- **Attempts:** {item['metrics']['attempts_needed']}\n\n")
            
            # Error Details (if any)
            if item["error_type"]:
                f.write(f"**Error Log:**\n")
                f.write(f"```text\n[{item['error_type']}] {item['error_detail']}\n```\n\n")
            
            # Comparison Table
            f.write("**SPARQL Comparison:**\n\n")
            f.write("| Generated Query | Gold Standard (Reference) |\n")
            f.write("| :--- | :--- |\n")
            # Cleaning newlines for table formatting
            gen_q = item['queries']['generated'].replace('\n', ' ')
            gold_q = item['queries']['gold'].replace('\n', ' ')
            f.write(f"| `{gen_q}` | `{gold_q}` |\n\n")
            
            # Execution Results Comparison
            f.write("**Result Set Comparison:**\n\n")
            f.write(f"- **Gold Results ({item['execution']['gold_count']} items):** `{', '.join(item['execution']['gold_data'][:5])}`")
            if item['execution']['gold_count'] > 5: f.write(" ...")
            f.write("\n")
            f.write(f"- **Gen Results ({item['execution']['gen_count']} items):** `{', '.join(item['execution']['gen_data'][:5])}`")
            if item['execution']['gen_count'] > 5: f.write(" ...")
            f.write("\n\n")

            # Technical Debug Data
            f.write("<details>\n<summary><b>View Full System Prompt & Raw Response</b></summary>\n\n")
            
            f.write("**1. System Prompt Sent to LLM:**\n")
            f.write(f"```text\n{item['debug']['prompt']}\n```\n\n")
            
            f.write("**2. Raw LLM Response:**\n")
            f.write(f"```text\n{item['queries']['raw_response']}\n```\n\n")
            
            f.write("**3. Injected Context / Strategy:**\n")
            f.write(f"```text\n{item['debug']['context']}\n```\n")
            
            f.write("</details>\n\n")
            f.write("---\n")

    def _flush_to_disk(self):
        """Persists current evaluation state to JSON and Markdown files."""
        try:
            self._generate_plots()
            
            json_path = self.run_dir / "results.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, indent=4, ensure_ascii=False)
            
            md_path = self.run_dir / "report.md"
            with open(md_path, "w", encoding="utf-8") as f:
                self._write_markdown(f)
        except Exception as e:
            logger.error(f"Failed to save report artifacts: {e}")

    def save_final_report(self):
        """Finalizes and archives the evaluation report with F1 score in filename."""
        self._flush_to_disk()
        
        avg_f1 = self.stats['metrics']['avg_f1']
        new_folder_name = f"F1-{avg_f1:.2f}_{self.folder_name}"
        new_path = self.base_report_dir / new_folder_name
        
        try:
            if not new_path.exists():
                self.run_dir.rename(new_path)
                logger.info(f"Report Artifacts available at: {new_path}")
            else:
                logger.info(f"Report saved at: {self.run_dir}")
        except Exception as e:
            logger.warning(f"Could not rename report folder : {e}")