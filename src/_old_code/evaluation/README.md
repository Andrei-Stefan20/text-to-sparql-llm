# Evaluation System



## Overview

This module provides experiment tracking with:

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



## Troubleshooting



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



### Backup mlruns/

```bash
tar -czf mlruns_backup_$(date +%Y%m%d).tar.gz mlruns/
```

Restore:

```bash
tar -xzf mlruns_backup_20251204.tar.gz
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


- Email alerting on low accuracy
- Auto-comparison with baseline
- Confidence intervals on metrics
- Query complexity metric
- Entity coverage analysis
- Optional export to Weights & Biases

## Resources


- [DeepEval Documentation](https://docs.confident-ai.com/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Seaborn Examples](https://seaborn.pydata.org/examples/)

---

For implementation details, see `EVALUATION_SYSTEM.md` in the project root.
