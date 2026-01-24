# DPO Fine-Tuning Pipeline

Concise, production-focused guide (English only).

## Requirements
- Python 3.10+
- GPU recommended (≥16GB); ensure CUDA/driver installed
- Hugging Face access if the model is gated (`huggingface-cli login`)

## Install
```bash
cd /Users/andreialexandrustefan/Desktop/text-to-sparql-llm
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Data format
JSONL, one object per line with keys `id`, `question`, `gold_query`.
Example:
```json
{"id": "q_000001", "question": "Who is the author of 1984?", "gold_query": "SELECT ..."}
```

### Split train/test
```bash
cd src/dpo_finetuning
python prepare_data.py --input /path/to/raw.jsonl --output datasets --train-ratio 0.8 --seed 42
```
Outputs: `datasets/train.jsonl`, `datasets/test.jsonl`.

## Run the pipeline
```bash
cd src/dpo_finetuning
python run_pipeline.py \
  --model meta-llama/Llama-2-7b-hf \
  --train datasets/train.jsonl \
  --test datasets/test.jsonl \
  --output results
```

Flags:
- `--config path/config.json` custom hyperparameters
- `--finetuned-model /path/to/model_ft` skip training, evaluate only
- `--4bit` enable 4-bit quantization for inference

## Example config (JSON)
```json
{
  "inference": {"temperature": 0.3, "max_new_tokens": 512, "use_4bit": false},
  "finetuning": {"num_epochs": 3, "batch_size": 4, "learning_rate": 5e-5},
  "evaluation": {"use_4bit": false}
}
```
Use with `--config config.json`.

## Outputs
- `results/1_inference/results.json` base generations on train
- `results/2_dpo_dataset/dpo_pairs.json` preference pairs
- `results/3_finetuning/model/final` fine-tuned model (if trained)
- `results/4_eval_base/results.json` base model eval
- `results/4_eval_ft/results.json` fine-tuned eval
- `results/5_comparison/comparison.json` metrics comparison
- `results/summary.json` run summary

## Practical tips
- Private models: run `huggingface-cli login` first.
- Low VRAM: use `--4bit` and reduce `batch_size` in config.
- Missing TRL/Datasets: `pip install trl datasets`.

## Quick commands
- Split data: `python prepare_data.py --input raw.jsonl --output datasets`
- Run pipeline: `python run_pipeline.py --model <model> --train datasets/train.jsonl --test datasets/test.jsonl --output results`
- With config: `python run_pipeline.py ... --config config.json`
- Eval only (pretrained FT): `python run_pipeline.py ... --finetuned-model /path/to/model_ft`
