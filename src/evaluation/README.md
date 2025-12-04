# Evaluation System

Experiment tracking for SPARQL query generation using **MLflow** and **DeepEval**.

## Overview

This module provides experiment tracking with:

- **MLflow**: Local tracking with interactive web UI
- **DeepEval**: Custom metrics for SPARQL validation
- **Visualizations**: 4 automatic charts (distribution, errors, progression)
- **Export**: JSON, CSV, HTML, PNG formats
- **Local hosting**: All data stored on disk, no cloud dependencies

## Quick Start

### 1. Run Evaluation

```bash
# Direct script execution
python src/evaluate_gemini.py

# Via CLI
python cli.py eval --model gemini
```

During execution:
- Metrics logged in real-time
- Artifacts saved to `./mlruns/`
- Progress tracking per question

### 2. View Results

```bash
# Launch MLflow UI
python cli.py view-results

# Or manually
mlflow ui --port 5000
```

Open **http://localhost:5000** in your browser.

### 3. Navigate Dashboard

**Experiments Tab:**
- Lists all experiments (e.g., "gemini-evaluation-2.0-flash")
- Click experiment to view runs

**Run Details Tab:**
- **Parameters**: Model configuration (temperature, k_examples, etc.)
- **Metrics**: Interactive charts (F1, syntax, attempts)
- **Artifacts**: Download reports, CSV, PNG charts

**Compare Runs:**
- Select 2+ runs
- Click "Compare"
- View side-by-side differences

## Custom Metrics

### DeepEval Metrics

**1. SPARQLSyntaxMetric** (0.0 or 1.0)
```python
from src.evaluation import SPARQLSyntaxMetric, create_test_case

metric = SPARQLSyntaxMetric(threshold=1.0)
test_case = create_test_case(question, gen_sparql, gold_sparql)
score = metric.measure(test_case)

print(f"Valid: {metric.is_successful()}")
print(f"Reason: {metric.reason}")
```

**2. SPARQLExecutionMetric** (0.0 or 1.0)
- Runs query against Wikidata
- Catches timeouts and errors
- Returns 1.0 if execution succeeds

**3. SPARQLAnswerCorrectnessMetric** (0.0 - 1.0)
- Compares results between gold and generated queries
- Calculates F1 score from precision and recall
- Default threshold: 0.8

**4. ContextRelevanceMetric** (0.0 - 1.0)
- Scores few-shot examples quality
- Measures keyword overlap with question
- Helps debug retriever issues

### Summary Metrics

Calculated at end of run:

| Metric | What it is |
|---------|----------|
| `total_questions` | How many questions processed |
| `syntax_accuracy` | Percentage of valid queries |
| `answer_accuracy` | Percentage of correct answers |
| `avg_f1_score` | Average F1 score |
| `avg_attempts` | Average retries needed |
| `retry_success_rate` | Percentage fixed by retrying |

## Visualizations

### 1. F1 Distribution
**File**: `f1_distribution.png`  
**Shows**: Score distribution with outliers

### 2. Attempts vs Success
**File**: `attempts_success.png`  
**Shows**: How many retries needed vs success

### 3. Error Distribution
**File**: `error_distribution.png`  
**Shows**: Most common errors

### 4. F1 Progression
**File**: `f1_progression.png`  
**Shows**: Performance over questions

## Output Structure

```
mlruns/
└── 1/                              # Experiment ID
    └── abc123.../                  # Run ID (UUID)
        ├── artifacts/
        │   ├── report.html                # Complete web report
        │   ├── detailed_results.json      # Raw data
        │   ├── results.csv                # Excel-compatible
        │   ├── f1_distribution.png
        │   ├── attempts_success.png
        │   ├── error_distribution.png
        │   └── f1_progression.png
        ├── metrics/
        │   ├── f1_score                   # Step-by-step values
        │   ├── is_valid
        │   ├── attempts
        │   ├── syntax_validity            # DeepEval
        │   ├── execution_success          # DeepEval
        │   ├── answer_correctness         # DeepEval
        │   └── summary_*                  # Aggregate metrics
        ├── params/
        │   ├── model
        │   ├── temperature
        │   ├── max_retries
        │   └── k_examples
        └── tags/
            └── mlflow.runName
```

## API Usage

### Create Reporter

```python
from src.evaluation import MLflowReporter

reporter = MLflowReporter(
    experiment_name="gemini-temperature-test",
    tracking_uri="file:./mlruns",  # Optional, default
    artifact_location=None          # Optional, custom path
)
```

### Log Parameters

```python
reporter.log_params({
    "model": "gemini-2.0-flash",
    "temperature": 0.1,
    "max_retries": 3,
    "k_examples": 3,
    "dataset": "QALD-10"
})
```

### Log Question Result

```python
from src.evaluation import create_test_case
from src.evaluation import SPARQLSyntaxMetric, SPARQLExecutionMetric

# Create test case
test_case = create_test_case(
    question="Who directed Inception?",
    generated_sparql="SELECT ?director WHERE { wd:Q25188 wdt:P57 ?director }",
    gold_sparql="SELECT ?director WHERE { wd:Q25188 wdt:P57 ?director }",
    examples=["Example 1...", "Example 2..."]
)

# Evaluate with DeepEval
syntax_metric = SPARQLSyntaxMetric()
exec_metric = SPARQLExecutionMetric()

custom_metrics = {
    "syntax_validity": syntax_metric.measure(test_case),
    "execution_success": exec_metric.measure(test_case)
}

# Log to MLflow
reporter.log_question_result(
    question_id=1,
    question="Who directed Inception?",
    gold_sparql="...",
    generated_sparql="...",
    is_valid=True,
    f1_score=1.0,
    attempts=1,
    error_info=None,
    metrics=custom_metrics
)
```

### Finalize Run

```python
# Generate all reports, charts, and CSV
summary = reporter.finalize()

print(summary)
# {
#   'total_questions': 100,
#   'syntax_accuracy': 0.92,
#   'answer_accuracy': 0.78,
#   'avg_f1_score': 0.843,
#   ...
# }
```

## Customization

### Modify Chart Styling

Edit `src/evaluation/mlflow_reporter.py`:

```python
# Line 14-15
sns.set_theme(style="darkgrid")      # Options: whitegrid, ticks, dark
plt.rcParams['figure.figsize'] = (14, 8)  # Chart dimensions

# Color palette
palette = "viridis"  # Options: rocket, mako, flare, crest
```

### Add Custom Charts

In the `create_visualizations()` method:

```python
def create_visualizations(self):
    df = pd.DataFrame(self.results)
    
    # ... existing charts ...
    
    # 5. Custom chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Your matplotlib/seaborn code
    sns.boxplot(data=df, x='attempts', y='f1_score', ax=ax)
    ax.set_title("F1 Score by Attempts")
    
    # Save
    mlflow.log_figure(fig, "custom_boxplot.png")
    plt.close()
```

### Create Custom Metrics

In `src/evaluation/metrics.py`:

```python
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

class QueryComplexityMetric(BaseMetric):
    """Measures query complexity (number of triple patterns)."""
    
    def __init__(self, threshold=5):
        self.threshold = threshold
    
    def measure(self, test_case: LLMTestCase) -> float:
        query = test_case.actual_output
        
        # Count triple patterns (simple heuristic)
        complexity = query.count('?s') + query.count('?p') + query.count('?o')
        
        self.score = min(complexity / 10, 1.0)  # Normalize
        self.success = self.score >= self.threshold
        self.reason = f"Complexity: {complexity} triple patterns"
        
        return self.score
    
    def is_successful(self) -> bool:
        return self.success
    
    @property
    def __name__(self):
        return "Query Complexity"
```

Usage:

```python
from src.evaluation.metrics import QueryComplexityMetric

complexity_metric = QueryComplexityMetric(threshold=0.5)
score = complexity_metric.measure(test_case)
```

## Programmatic Access

### Read Previous Runs

```python
import mlflow

# Search all runs
runs = mlflow.search_runs(
    experiment_names=["gemini-evaluation-2.0-flash"],
    filter_string="metrics.avg_f1_score > 0.8",
    order_by=["metrics.avg_f1_score DESC"]
)

print(runs[['run_id', 'metrics.avg_f1_score', 'params.temperature']])
```

### Download Artifacts

```python
# Get best run
best_run = runs.iloc[0]
run_id = best_run.run_id

# Download report
mlflow.artifacts.download_artifacts(
    run_id=run_id,
    artifact_path="report.html",
    dst_path="./downloaded_reports"
)

# Download CSV
mlflow.artifacts.download_artifacts(
    run_id=run_id,
    artifact_path="results.csv",
    dst_path="./data"
)
```

### Compare Runs

```python
# Load multiple runs
run_ids = ["abc123", "def456", "ghi789"]

for rid in run_ids:
    run = mlflow.get_run(rid)
    print(f"Run {rid[:7]}:")
    print(f"  F1: {run.data.metrics['summary_avg_f1_score']:.3f}")
    print(f"  Temp: {run.data.params['temperature']}")
    print()
```

## Troubleshooting

### MLflow UI not starting

```bash
pip install --upgrade mlflow
mlflow ui --port 5001
```

### Port 5000 already in use

```bash
mlflow ui --port 8080
```

### Charts not generated

```bash
# Install all visualization dependencies
pip install matplotlib seaborn plotly kaleido pandas

# Verify
python -c "import matplotlib, seaborn, plotly; print('OK')"
```

### DeepEval metrics fail

```python
# Test SPARQLClient
from src.utils.sparql_client import SPARQLClient

client = SPARQLClient()
result = client.validate_syntax_local("SELECT * WHERE { ?s ?p ?o }")
print(result)  # Should return {'valid': True, ...}
```

### "No experiments found"

Run an evaluation first:
```bash
python src/evaluate_gemini.py
```

## Best Practices

### Naming Experiments

Use clear, descriptive names:

```python
# Good
experiment_name = "gemini-2.0-flash-temp-0.1-k3"

# Bad
experiment_name = "test1"
```

### Tagging Runs

```python
mlflow.set_tags({
    "environment": "production",
    "version": "v2.0",
    "baseline": "true"
})
```

### Cleanup Old Runs

```bash
mlflow experiments delete --experiment-id 1
```

Or in Python:

```python
mlflow.delete_experiment("1")
```

### Backup mlruns/

```bash
tar -czf mlruns_backup_$(date +%Y%m%d).tar.gz mlruns/
```

Restore:

```bash
tar -xzf mlruns_backup_20251204.tar.gz
```

### Integration Examples

### evaluate.py (Local Model)

```python
from src.evaluation import MLflowReporter

reporter = MLflowReporter(
    experiment_name="qwen-2.5-coder-3b-evaluation"
)

reporter.log_params({
    "model": "Qwen/Qwen2.5-Coder-3B-Instruct",
    "temperature": config.model.temperature,
    "flash_attention": True
})

# ... loop evaluation ...

reporter.finalize()
```

### evaluate_ace_gemini.py (ACE Engine)

```python
from src.evaluation import MLflowReporter

reporter = MLflowReporter(
    experiment_name="ace-gemini-playbook-v2"
)

reporter.log_params({
    "ace_enabled": True,
    "playbook_size": len(ace_engine.playbook),
    "learning_rate": "dynamic"
})

mlflow.log_metric("playbook_size", len(ace_engine.playbook), step=i)
```

## Advanced Metrics

### Batch Evaluation with DeepEval

```python
from deepeval import evaluate
from src.evaluation import SPARQLSyntaxMetric, SPARQLExecutionMetric

# Create batch test cases
test_cases = [
    create_test_case(q1, gen1, gold1, ex1),
    create_test_case(q2, gen2, gold2, ex2),
    # ...
]

# Evaluate in batch
results = evaluate(
    test_cases=test_cases,
    metrics=[
        SPARQLSyntaxMetric(),
        SPARQLExecutionMetric(),
        SPARQLAnswerCorrectnessMetric(threshold=0.8)
    ]
)

# Results contains all details
print(results)
```

## Roadmap

Planned features:

- Remote MLflow server (team collaboration)
- Email alerting on low accuracy
- Auto-comparison with baseline
- Confidence intervals on metrics
- Query complexity metric
- Entity coverage analysis
- Optional export to Weights & Biases

## Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [DeepEval Documentation](https://docs.confident-ai.com/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Seaborn Examples](https://seaborn.pydata.org/examples/)

---

For implementation details, see `EVALUATION_SYSTEM.md` in the project root.
