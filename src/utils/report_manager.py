import logging
import json
import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

class ReportManager:
    """
    Manages the generation of JSON and Markdown reports for evaluation runs.
    """
    def __init__(self, project_root: Path, model_name: str, run_prefix: str = "run"):
        self.model_name = model_name
        self.start_time = datetime.datetime.now()
        
        # Directory structure: reports/YYYY-MM-DD/run_ID
        date_str = self.start_time.strftime("%Y-%m-%d")
        self.base_report_dir = project_root / "reports" / date_str
        self.base_report_dir.mkdir(parents=True, exist_ok=True)
        
        # Calculate Run ID
        existing_runs = [d for d in self.base_report_dir.iterdir() if d.is_dir() and d.name.startswith(run_prefix)]
        run_id = len(existing_runs) + 1
        
        time_str = self.start_time.strftime("%H%M%S")
        self.run_dir = self.base_report_dir / f"{run_prefix}_{run_id:03d}_{time_str}"
        self.run_dir.mkdir(exist_ok=True)
        
        self.stats = {
            "meta": {
                "date": date_str, 
                "model": model_name, 
                "run_id": run_id,
                "type": run_prefix
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
        logger.info(f"Report directory initialized at: {self.run_dir}")

    def _format_bindings(self, bindings: Optional[List[Dict]]) -> List[str]:
        """Converts raw SPARQL bindings to a list of readable strings."""
        if not bindings:
            return []
        formatted = []
        for row in bindings:
            # Extract only the value (e.g., Q12345) from the full URI
            values = [v['value'].split('/')[-1] for v in row.values()] 
            formatted.append("(" + ", ".join(values) + ")")
        return formatted

    def log_entry(self, question: str, gold_sparql: str, generated_sparql: str, 
                  raw_response: str, is_valid: bool, error_info: Optional[Dict], 
                  f1_score: float, attempts: int, prompt: str, context: Any, 
                  gold_results: Optional[List], gen_results: Optional[List]):
        """
        Logs a single evaluation entry (one question).
        """
        fmt_gold = self._format_bindings(gold_results)
        fmt_gen = self._format_bindings(gen_results)

        entry = {
            "id": self.stats["metrics"]["total"] + 1,
            "question": question,
            "status": "VALID" if is_valid else "INVALID",
            "error_type": error_info.get("type") if error_info else None,
            "error_detail": error_info.get("detail") if error_info else None,
            "metrics": {"f1_score": f1_score, "attempts_needed": attempts},
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
                "context": context  # Can be string (schema) or string (ACE playbook)
            }
        }
        self.stats["results"].append(entry)
        
        # Update aggregate metrics
        m = self.stats["metrics"]
        m["total"] += 1
        if is_valid: m["valid_syntax"] += 1
        if f1_score == 1.0: m["correct_answer"] += 1
        if attempts > 1 and is_valid and f1_score > 0: m["retries_successful"] += 1
        
        if m["total"] > 0:
            total_f1 = sum(r['metrics']['f1_score'] for r in self.stats['results'])
            m["avg_f1"] = round(total_f1 / m["total"], 4)
            
        self._flush_to_disk()

    def _flush_to_disk(self):
        """Writes the current stats to JSON and Markdown."""
        try:
            with open(self.run_dir / "results.json", "w", encoding="utf-8") as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
            
            with open(self.run_dir / "report.md", "w", encoding="utf-8") as f:
                self._write_markdown(f)
        except Exception as e:
            logger.error(f"Failed to save report: {e}")

    def _write_markdown(self, f):
        """Generates the Markdown summary."""
        m = self.stats['metrics']
        total = m['total']
        syn_acc = (m['valid_syntax'] / total * 100) if total > 0 else 0
        ans_acc = (m['correct_answer'] / total * 100) if total > 0 else 0
        
        f.write(f"# Evaluation Report\n\n")
        f.write(f"**Model:** `{self.model_name}`\n")
        f.write(f"**Date:** {self.stats['meta']['date']}\n\n")
        
        f.write("## Summary Metrics\n")
        f.write(f"| Metric | Value |\n|---|---|\n")
        f.write(f"| Total Questions | {total} |\n")
        f.write(f"| Syntax Accuracy | {syn_acc:.2f}% |\n")
        f.write(f"| Answer Accuracy | {ans_acc:.2f}% |\n")
        f.write(f"| Average F1 Score | {m['avg_f1']:.4f} |\n")
        f.write(f"| Successful Repairs | {m['retries_successful']} |\n\n")
        f.write("---\n\n")
        
        f.write("## Detailed Results\n\n")
        for item in reversed(self.stats["results"]):
            status_icon = "[PASS]" if item["metrics"]["f1_score"] == 1.0 else ("[FAIL]" if item["status"] != "VALID" else "[PARTIAL]")
            
            f.write(f"### Q{item['id']}: {status_icon} {item['question']}\n\n")
            
            if item["error_type"]:
                f.write(f"**Error:** `{item['error_type']}: {item['error_detail']}`\n\n")
            
            f.write("#### SPARQL Comparison\n")
            f.write(f"**Generated:**\n```sparql\n{item['queries']['generated']}\n```\n")
            f.write(f"**Gold:**\n```sparql\n{item['queries']['gold']}\n```\n\n")

            gold_preview = ", ".join(item['execution']['gold_data'][:5])
            gen_preview = ", ".join(item['execution']['gen_data'][:5])
            if len(item['execution']['gold_data']) > 5: gold_preview += "..."
            if len(item['execution']['gen_data']) > 5: gen_preview += "..."

            f.write("#### Execution Data\n")
            f.write("| Source | Count | Data Preview |\n|---|---|---|\n")
            f.write(f"| **Gold** | {item['execution']['gold_count']} | `{gold_preview}` |\n")
            f.write(f"| **Gen** | {item['execution']['gen_count']} | `{gen_preview}` |\n\n")
            
            f.write("<details>\n<summary><b>View Prompt & Debug Info</b></summary>\n\n")
            f.write(f"**Context/Playbook:**\n```text\n{item['debug']['context']}\n```\n\n")
            f.write(f"**Full Prompt:**\n```text\n{item['debug']['prompt']}\n```\n")
            f.write("</details>\n\n")
            
            f.write(f"**F1 Score:** {item['metrics']['f1_score']:.2f} | **Attempts:** {item['metrics']['attempts_needed']}\n")
            f.write("---\n")

    def save_final_report(self):
        self._flush_to_disk()
        logger.info(f"Final report saved to {self.run_dir}")