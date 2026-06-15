"""Generate analysis charts for the paper (English labels).

Sources:
- outputs/exp6_agent_*  : agentic runs (n=20)
- outputs/eval394_all.csv : GERBIL-style evaluation on the full QALD-10 test set
"""
import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "outputs"
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(exist_ok=True)

MODEL_COLORS = {"GPT-4o": "#1f77b4", "GPT-4o-mini": "#ff7f0e", "Llama 3.3": "#2ca02c"}


def load_results(exp_name):
    exp_dir = OUT_ROOT / exp_name
    run_dirs = sorted(d for d in exp_dir.iterdir()
                      if d.is_dir() and (d / "results_full.json").exists())
    with open(run_dirs[-1] / "results_full.json", encoding="utf-8") as f:
        return json.load(f)["results"]


def load_eval394():
    """experiment -> f1 (%) using the latest timestamp per experiment."""
    rows = {}
    with open(OUT_ROOT / "eval394_all.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["experiment"]
            if name not in rows or row["timestamp"] > rows[name][0]:
                rows[name] = (row["timestamp"], float(row["f1"]) * 100)
    return {k: v[1] for k, v in rows.items()}


EVAL = load_eval394()

# ---- Fig 1: steps used per question, full agentic runs (budget 8) ----
runs = {
    "GPT-4o": "exp6_agent_full_gpt4_20",
    "GPT-4o-mini": "exp6_agent_full_mini_20",
    "Llama 3.3": "exp6_agent_full_llama_20",
}
fig, ax = plt.subplots(figsize=(7, 3.4))
width = 0.27
for i, (label, exp) in enumerate(runs.items()):
    counts = Counter(r["total_steps"] for r in load_results(exp))
    xs = sorted(counts)
    ax.bar([x + (i - 1) * width for x in xs], [counts[x] for x in xs],
           width=width, label=label, color=MODEL_COLORS[label])
ax.set_xlabel("Steps used per question (budget 8)")
ax.set_ylabel("Number of questions")
ax.set_xticks(range(1, 9))
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIG_DIR / "agent_steps_dist.png", dpi=200)
print("written", FIG_DIR / "agent_steps_dist.png")

# ---- Fig 2: average steps used vs. step budget ----
budget_runs = {
    "GPT-4o": {3: "exp6_agent_fast_gpt4_20", 8: "exp6_agent_full_gpt4_20"},
    "GPT-4o-mini": {5: "exp6_agent_budget5_mini_20",
                    8: "exp6_agent_full_mini_20",
                    12: "exp6_agent_marathon_mini_20"},
}
fig, ax = plt.subplots(figsize=(5.2, 3.4))
for label, series in budget_runs.items():
    xs, ys = [], []
    for budget, exp in sorted(series.items()):
        steps = [r["total_steps"] for r in load_results(exp)]
        xs.append(budget)
        ys.append(sum(steps) / len(steps))
    ax.plot(xs, ys, "o-", label=label, color=MODEL_COLORS[label])
ax.plot([3, 12], [3, 12], "--", color="gray", linewidth=1, label="full budget")
ax.set_xlabel("Step budget")
ax.set_ylabel("Average steps used")
ax.set_xticks([3, 5, 8, 12])
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIG_DIR / "agent_budget.png", dpi=200)
print("written", FIG_DIR / "agent_budget.png")

# ---- Fig 3: valid queries out of 20 across agent configurations ----
config_runs = [
    ("GPT-4o full", "exp6_agent_full_gpt4_20", MODEL_COLORS["GPT-4o"]),
    ("GPT-4o no examples", "exp6_agent_0shot_gpt4_20", MODEL_COLORS["GPT-4o"]),
    ("GPT-4o no schema hints", "exp6_agent_blind_gpt4_20", MODEL_COLORS["GPT-4o"]),
    ("GPT-4o budget 3", "exp6_agent_fast_gpt4_20", MODEL_COLORS["GPT-4o"]),
    ("mini full", "exp6_agent_full_mini_20", MODEL_COLORS["GPT-4o-mini"]),
    ("mini no schema hints", "exp6_agent_blind_mini_20", MODEL_COLORS["GPT-4o-mini"]),
    ("mini budget 5", "exp6_agent_budget5_mini_20", MODEL_COLORS["GPT-4o-mini"]),
    ("mini budget 12", "exp6_agent_marathon_mini_20", MODEL_COLORS["GPT-4o-mini"]),
    ("Llama full", "exp6_agent_full_llama_20", MODEL_COLORS["Llama 3.3"]),
]
fig, ax = plt.subplots(figsize=(7, 3.6))
labels = [c[0] for c in config_runs]
valids = [sum(1 for r in load_results(c[1]) if r["is_valid"]) for c in config_runs]
ax.barh(range(len(labels)), valids, color=[c[2] for c in config_runs])
ax.set_yticks(range(len(labels)))
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("Syntactically valid queries out of 20 questions")
ax.set_xlim(0, 21)
ax.axvline(20, color="gray", linestyle="--", linewidth=1)
for i, v in enumerate(valids):
    ax.text(v + 0.3, i, str(v), va="center", fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIG_DIR / "agent_valid.png", dpi=200)
print("written", FIG_DIR / "agent_valid.png")

# ---- Fig 4: component ablation on the full test set (GPT-4o-mini) ----
ablation = [
    ("No context", "exp7_pure_gpt4mini_394"),
    ("RAG only", "exp7_rag_only_gpt4mini_394"),
    ("Schema hints only", "exp7_schema_only_gpt4mini_394"),
    ("Linker only (REBEL)", "exp7_linker_only_gpt4mini_394"),
    ("Linker + RAG", "exp7_linker_rag_gpt4mini_394"),
    ("Linker + schema hints", "exp7_linker_schema_gpt4mini_394"),
    ("Full (linker + RAG + schema)", "exp7_full_gpt4mini_394"),
]
fig, ax = plt.subplots(figsize=(7, 3.4))
names = [a[0] for a in ablation]
f1s = [EVAL[a[1]] for a in ablation]
bars = ax.barh(range(len(names)), f1s, color="#ff7f0e")
ax.set_yticks(range(len(names)))
ax.set_yticklabels(names)
ax.invert_yaxis()
ax.set_xlabel("Macro F1 (%) on the full QALD-10 test set (GPT-4o-mini)")
for i, v in enumerate(f1s):
    ax.text(v + 0.2, i, f"{v:.1f}", va="center", fontsize=9)
ax.set_xlim(0, 24)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIG_DIR / "fullset_ablation.png", dpi=200)
print("written", FIG_DIR / "fullset_ablation.png")

# ---- Fig 5: strategies on the full test set, per model ----
strategies = [
    ("No linker", "exp2_nolink_{m}_394"),
    ("REBEL 0-shot", "exp2_rebel_{m}_394"),
    ("Standard", "exp1_standard_{m}_394"),
    ("CoT", "exp1_cot_{m}_394"),
    ("Decomposition", "exp1_decomp_{m}_394"),
    ("Self-cons. 3", "exp5_3samples_{m}_394"),
    ("Self-cons. 5", "exp5_5samples_{m}_394"),
]
models = [("GPT-4o", "gpt4"), ("GPT-4o-mini", "gpt4mini"), ("Llama 3.3", "llama")]
fig, ax = plt.subplots(figsize=(8, 3.6))
width = 0.27
for i, (label, key) in enumerate(models):
    xs, ys = [], []
    for j, (_, pattern) in enumerate(strategies):
        exp = pattern.format(m=key)
        if exp in EVAL:
            xs.append(j + (i - 1) * width)
            ys.append(EVAL[exp])
    ax.bar(xs, ys, width=width, label=label, color=MODEL_COLORS[label])
ax.set_xticks(range(len(strategies)))
ax.set_xticklabels([s[0] for s in strategies])
ax.set_ylabel("Macro F1 (%)")
ax.set_title("Full QALD-10 test set (394 questions)", fontsize=10)
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIG_DIR / "fullset_strategies.png", dpi=200)
print("written", FIG_DIR / "fullset_strategies.png")

# ---- Fig 6: few-shot examples count on the full test set ----
fig, ax = plt.subplots(figsize=(5.2, 3.4))
for label, key in models:
    xs, ys = [], []
    for k in [0, 1, 3, 5]:
        exp = f"exp4_{k}shot_{key}_394"
        if exp in EVAL:
            xs.append(k)
            ys.append(EVAL[exp])
    ax.plot(xs, ys, "o-", label=label, color=MODEL_COLORS[label])
ax.set_xlabel("Number of few-shot examples (k)")
ax.set_ylabel("Macro F1 (%)")
ax.set_xticks([0, 1, 3, 5])
ax.set_ylim(0, 25)
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(FIG_DIR / "fullset_fewshot.png", dpi=200)
print("written", FIG_DIR / "fullset_fewshot.png")
