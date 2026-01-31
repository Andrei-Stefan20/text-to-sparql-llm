import datetime
import json
import logging
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

logger = logging.getLogger(__name__)


class ReportManager:
    """
    Manages evaluation metrics, logging, and report generation.
    Supports both standard evaluation and decomposition-based evaluation.
    """

    def __init__(
        self,
        project_root: Path,
        model_name: str,
        run_prefix: str = "run",
        mode: str = "standard",
    ):
        self.model_name = model_name
        self.start_time = datetime.datetime.now()
        self.project_root = project_root
        self.mode = mode  # "standard" or "decomposition"

        date_str = self.start_time.strftime("%Y-%m-%d")
        self.base_report_dir = project_root / "reports" / date_str
        self.base_report_dir.mkdir(parents=True, exist_ok=True)

        existing_runs = [d for d in self.base_report_dir.iterdir() if d.is_dir()]
        run_id = len(existing_runs) + 1
        time_str = self.start_time.strftime("%H%M%S")

        self.folder_name = f"{run_prefix}_{model_name}_{run_id:03d}_{time_str}"
        self.run_dir = self.base_report_dir / self.folder_name
        self.run_dir.mkdir(parents=True, exist_ok=True)

        self.stats = {
            "meta": {
                "date": date_str,
                "model": model_name,
                "run_id": run_id,
                "start_time": time_str,
                "mode": mode,
            },
            "metrics": {
                "total": 0,
                "valid_syntax": 0,
                "correct_answer": 0,
                "avg_f1": 0.0,
                "retries_successful": 0,
                "successful_decompositions": 0,
            },
            "results": [],
        }
        logger.info(f"Report initialized at: {self.run_dir} (mode: {mode})")

    def _format_bindings(self, bindings: Optional[List[Dict]]) -> List[str]:
        """Converts SPARQL result bindings to human-readable format."""
        if not bindings:
            return []
        formatted = []
        for row in bindings:
            values = [v["value"].split("/")[-1] for v in row.values()]
            formatted.append(f"({', '.join(values)})")
        return formatted

    def log_entry(
        self,
        question: str,
        gold_sparql: str,
        generated_sparql: str,
        raw_response: str,
        is_valid: bool,
        error_info: Optional[Dict],
        f1_score: float,
        attempts: int,
        prompt: str,
        context: Any,
        gold_results: Optional[List],
        gen_results: Optional[List],
    ):
        """
        Records a single evaluation entry for standard mode and updates aggregate metrics.

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
            "metrics": {"f1_score": f1_score, "attempts_needed": attempts},
            "queries": {
                "gold": gold_sparql,
                "generated": generated_sparql,
                "raw_response": raw_response,
            },
            "execution": {
                "gold_count": len(fmt_gold),
                "gen_count": len(fmt_gen),
                "gold_data": fmt_gold,
                "gen_data": fmt_gen,
            },
            "debug": {"prompt": prompt, "context": context},
        }
        self.stats["results"].append(entry)

        # Update Aggregate Metrics
        m = self.stats["metrics"]
        m["total"] += 1
        if is_valid:
            m["valid_syntax"] += 1
        if f1_score == 1.0:
            m["correct_answer"] += 1
        if attempts > 1 and is_valid and f1_score > 0:
            m["retries_successful"] += 1

        if m["total"] > 0:
            total_f1 = sum(r["metrics"]["f1_score"] for r in self.stats["results"])
            m["avg_f1"] = round(total_f1 / m["total"], 4)

        self._flush_to_disk()

    def log_decomposition(
        self,
        question: str,
        decomposition_steps: List[Dict],
        execution_results: Dict,
        final_answer: str,
        execution_log: List,
    ):
        """
        Records a complete decomposition execution with all reasoning (decomposition mode).

        Args:
            question: Original natural language question
            decomposition_steps: List of decomposition steps with metadata
            execution_results: Dictionary of results from each step
            final_answer: Synthesized final answer from all steps
            execution_log: Complete execution log with all details
        """
        successful_steps = sum(
            1
            for step in decomposition_steps
            if step.get("metadata", {}).get("status") == "success"
        )

        entry = {
            "id": self.stats["metrics"]["total"] + 1,
            "timestamp": datetime.datetime.now().isoformat(),
            "question": question,
            "decomposition": {
                "total_steps": len(decomposition_steps),
                "successful_steps": successful_steps,
                "steps": decomposition_steps,
            },
            "execution": {"results": execution_results, "log": execution_log},
            "final_answer": final_answer,
            "metrics": {
                "success_rate": (
                    (successful_steps / len(decomposition_steps) * 100)
                    if decomposition_steps
                    else 0
                )
            },
        }
        self.stats["results"].append(entry)

        # Update Aggregate Metrics
        m = self.stats["metrics"]
        m["total"] += 1
        m["successful_decompositions"] += (
            1 if successful_steps == len(decomposition_steps) else 0
        )

        self._flush_to_disk()

    def log_decomposition_step(
        self,
        question_id: int,
        step_num: int,
        step_description: str,
        query_type: str,
        status: str,
        result_count: int,
        query: Optional[str] = None,
        error: Optional[str] = None,
        depends_on: Optional[int] = None,
    ):
        """
        Log individual step execution within a decomposition.
        Provides uniform, granular step-level reporting across the pipeline.

        Args:
            question_id: ID of the parent question being decomposed
            step_num: Step number (1-based)
            step_description: Human-readable step description
            query_type: Type of query (entity_search, property_search, filtering, aggregation, join)
            status: Execution status (success, failed, skipped)
            result_count: Number of results returned from this step
            query: The SPARQL/semantic query executed (optional)
            error: Error message if status is failed (optional)
            depends_on: Step number this step depends on (optional)
        """
        step_log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "question_id": question_id,
            "step_num": step_num,
            "description": step_description,
            "query_type": query_type,
            "status": status,
            "result_count": result_count,
            "query": query,
            "error": error,
            "depends_on": depends_on,
        }

        # Store in execution context for later retrieval
        if not hasattr(self, "_step_logs"):
            self._step_logs = []
        self._step_logs.append(step_log)

        logger.debug(f"Step {step_num}: {status.upper()} ({result_count} results)")

    def get_step_logs(self) -> List[Dict]:
        """Retrieve all step logs recorded in current session."""
        return getattr(self, "_step_logs", [])

    def _generate_plots(self):
        """Generates performance visualization charts for the report."""
        if not MATPLOTLIB_AVAILABLE or not self.stats["results"]:
            return

        # Skip plots for decomposition mode (no F1 scores)
        if self.mode == "decomposition":
            return

        try:
            sns.set_theme(style="whitegrid")
        except:
            plt.style.use("ggplot")

        results = self.stats["results"]
        f1_scores = [r["metrics"]["f1_score"] for r in results]
        statuses = [r["status_label"] for r in results]

        plt.figure(figsize=(10, 6))
        plt.hist(
            f1_scores,
            bins=[0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.01],
            color="#2c3e50",
            edgecolor="white",
            alpha=0.8,
        )
        plt.title("Distribution of F1 Scores", fontsize=14, pad=20)
        plt.xlabel("F1 Score", fontsize=12)
        plt.ylabel("Frequency (Questions)", fontsize=12)
        plt.axvline(
            self.stats["metrics"]["avg_f1"],
            color="#e74c3c",
            linestyle="dashed",
            linewidth=1,
            label=f"Avg F1: {self.stats['metrics']['avg_f1']:.2f}",
        )
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.run_dir / "f1_distribution.png", dpi=150)
        plt.close()

        status_counts = pd.Series(statuses).value_counts()

        plt.figure(figsize=(10, 6))
        colors = {
            "CORRECT": "#27ae60",
            "PARTIAL_MATCH": "#f39c12",
            "WRONG_ANSWER": "#c0392b",
            "SYNTAX_ERROR": "#7f8c8d",
            "EXECUTION_ERROR": "#8e44ad",
        }
        bar_colors = [colors.get(x, "#95a5a6") for x in status_counts.index]

        status_counts.plot(kind="bar", color=bar_colors, edgecolor="black", alpha=0.8)
        plt.title("Evaluation Outcomes by Type", fontsize=14, pad=20)
        plt.ylabel("Count", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(self.run_dir / "outcome_analysis.png", dpi=150)
        plt.close()

    def _write_markdown(self, f):
        """Generates comprehensive Markdown report with metrics and analysis."""
        m = self.stats["metrics"]
        total = m["total"]
        syn_acc = (m["valid_syntax"] / total * 100) if total > 0 else 0
        ans_acc = (m["correct_answer"] / total * 100) if total > 0 else 0

        f.write(f"# Text-to-SPARQL Evaluation Report\n\n")
        f.write(f"**Model Architecture:** `{self.model_name}`  \n")
        f.write(f"**Evaluation Date:** {self.stats['meta']['date']}  \n")
        f.write(f"**Mode:** `{self.mode}`  \n")
        f.write(f"**Run ID:** `{self.folder_name}`\n\n")

        if self.mode == "standard":
            self._write_markdown_standard(f, m, total, syn_acc, ans_acc)
        elif self.mode == "decomposition":
            self._write_markdown_decomposition(f, m, total)

    def _write_markdown_standard(self, f, m, total, syn_acc, ans_acc):
        """Generates markdown for standard evaluation mode."""
        f.write("## 1. Executive Summary\n\n")
        f.write("| Key Metric | Value | Definition |\n")
        f.write("| :--- | :--- | :--- |\n")
        f.write(
            f"| **Average F1 Score** | **{m['avg_f1']:.4f}** | Harmonic mean of precision and recall (0-1). |\n"
        )
        f.write(
            f"| **Exact Match Rate** | {ans_acc:.2f}% | Percentage of perfectly correct answers. |\n"
        )
        f.write(
            f"| **Syntax Validity** | {syn_acc:.2f}% | Percentage of queries that executed without errors. |\n"
        )
        f.write(
            f"| **Self-Correction** | {m['retries_successful']} | Number of times the model fixed its own errors. |\n\n"
        )

        # Visualizations
        if MATPLOTLIB_AVAILABLE:
            f.write("## 2. Visual Analysis\n\n")
            f.write("### F1 Score Distribution & Outcome Breakdown\n")
            f.write(
                "The following charts illustrate the model's performance stability and error profile.\n\n"
            )
            f.write("| F1 Score Histogram | Outcome Classification |\n")
            f.write("| :---: | :---: |\n")
            f.write(
                "| ![F1 Distribution](f1_distribution.png) | ![Outcomes](outcome_analysis.png) |\n\n"
            )

        # Detailed Results
        f.write("## 3. Detailed Question Analysis\n")
        f.write("Below is the itemized analysis for each processed question.\n\n")
        f.write("---\n")

        for item in reversed(self.stats["results"]):
            # Status Badge
            status = item["status_label"]
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
                f.write(
                    f"```text\n[{item['error_type']}] {item['error_detail']}\n```\n\n"
                )

            # Comparison Table
            f.write("**SPARQL Comparison:**\n\n")
            f.write("| Generated Query | Gold Standard (Reference) |\n")
            f.write("| :--- | :--- |\n")
            # Cleaning newlines for table formatting
            gen_q = item["queries"]["generated"].replace("\n", " ")
            gold_q = item["queries"]["gold"].replace("\n", " ")
            f.write(f"| `{gen_q}` | `{gold_q}` |\n\n")

            # Execution Results Comparison
            f.write("**Result Set Comparison:**\n\n")
            f.write(
                f"- **Gold Results ({item['execution']['gold_count']} items):** `{', '.join(item['execution']['gold_data'][:5])}`"
            )
            if item["execution"]["gold_count"] > 5:
                f.write(" ...")
            f.write("\n")
            f.write(
                f"- **Gen Results ({item['execution']['gen_count']} items):** `{', '.join(item['execution']['gen_data'][:5])}`"
            )
            if item["execution"]["gen_count"] > 5:
                f.write(" ...")
            f.write("\n\n")

            # Technical Debug Data
            f.write(
                "<details>\n<summary><b>View Full System Prompt & Raw Response</b></summary>\n\n"
            )

            f.write("**1. System Prompt Sent to LLM:**\n")
            f.write(f"```text\n{item['debug']['prompt']}\n```\n\n")

            f.write("**2. Raw LLM Response:**\n")
            f.write(f"```text\n{item['queries']['raw_response']}\n```\n\n")

            f.write("**3. Injected Context / Strategy:**\n")
            f.write(f"```text\n{item['debug']['context']}\n```\n")

            f.write("</details>\n\n")
            f.write("---\n")

    def _write_markdown_decomposition(self, f, m, total):
        """Generates markdown for decomposition evaluation mode."""
        f.write("## 1. Decomposition Summary\n\n")
        f.write("| Key Metric | Value |\n")
        f.write("| :--- | :--- |\n")
        f.write(f"| **Total Questions** | {m['total']} |\n")
        f.write(
            f"| **Fully Successful Decompositions** | {m['successful_decompositions']} |\n"
        )
        f.write(
            f"| **Success Rate** | {(m['successful_decompositions']/total*100):.1f}%"
            if total > 0
            else "N/A"
        )
        f.write(" |\n\n")

        # Detailed Results
        f.write("## 2. Decomposition Analysis\n")
        f.write("Below is the detailed breakdown of each decomposition execution.\n\n")
        f.write("---\n")

        for item in reversed(self.stats["results"]):
            f.write(f"### Question ID: {item['id']}\n\n")
            f.write(f"> **Input Question:** {item['question']}\n\n")

            # Decomposition Stats
            decomp = item["decomposition"]
            f.write(f"- **Total Steps:** {decomp['total_steps']}\n")
            f.write(f"- **Successful Steps:** {decomp['successful_steps']}\n")
            f.write(f"- **Success Rate:** {item['metrics']['success_rate']:.1f}%\n\n")

            # Steps Breakdown
            f.write("**Decomposition Steps:**\n\n")
            for step_idx, step in enumerate(decomp["steps"], 1):
                status = step.get("metadata", {}).get("status", "unknown")
                status_emoji = "✅" if status == "success" else "❌"
                description = step.get("description", "N/A")[:80]
                result_count = step.get("metadata", {}).get("result_count", 0)

                f.write(f"{status_emoji} **Step {step_idx}:** {description}\n")
                f.write(f"   - Type: `{step.get('query_type', 'N/A')}`\n")
                f.write(f"   - Status: `{status}`\n")
                f.write(f"   - Results: {result_count} items\n")

                if step.get("metadata", {}).get("query"):
                    query = step["metadata"]["query"].replace("\n", " ")
                    f.write(f"   - Query: `{query}`\n")
                f.write("\n")

            # Final Answer
            f.write("**Final Answer:**\n\n")
            f.write(f"```\n{item['final_answer']}\n```\n\n")

            # Execution Log
            f.write("<details>\n<summary><b>View Full Execution Log</b></summary>\n\n")
            f.write(f"```json\n{json.dumps(item['execution']['log'], indent=2)}\n```\n")
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

        avg_f1 = self.stats["metrics"]["avg_f1"]

        # Only rename if mode is "standard" (has F1 scores)
        if self.mode == "standard":
            new_folder_name = f"F1-{avg_f1:.2f}_{self.folder_name}"
            new_path = self.base_report_dir / new_folder_name

            try:
                if not new_path.exists() and self.run_dir.exists():
                    self.run_dir.rename(new_path)
                    logger.info(f"Report Artifacts available at: {new_path}")
                else:
                    logger.info(f"Report saved at: {self.run_dir}")
            except Exception as e:
                logger.warning(f"Could not rename report folder: {e}")
        else:
            logger.info(f"Report saved at: {self.run_dir}")
