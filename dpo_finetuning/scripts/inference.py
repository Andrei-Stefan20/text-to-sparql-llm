"""
Inference wrapper for DPO fine-tuned model.

This script provides a simple interface to generate SPARQL from natural language
using the fine-tuned model.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import logging

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DPOSPARQLGenerator:
    """Generate SPARQL using DPO fine-tuned model."""
    
    def __init__(
        self,
        model_path: Path,
        device: str = "cuda",
        dtype: str = "bfloat16",
    ):
        """Initialize generator with fine-tuned model."""
        
        self.device = device
        self.model_path = model_path
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model with appropriate dtype
        torch_dtype = torch.bfloat16 if dtype == "bfloat16" else torch.float32
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch_dtype,
            device_map="auto" if device == "cuda" else device,
        )
        self.model.eval()
        
        logger.info(f"Loaded model from {model_path}")
        logger.info(f"Model dtype: {self.model.dtype}")
        logger.info(f"Device: {self.device}")
    
    def generate(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        num_beams: int = 1,
        num_return_sequences: int = 1,
    ) -> List[str]:
        """Generate SPARQL queries from natural language prompt."""
        
        # Format prompt
        formatted_prompt = f"{prompt}\n"
        
        # Tokenize
        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_beams=num_beams,
                num_return_sequences=num_return_sequences,
                do_sample=(num_beams == 1),
                pad_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode
        generated_texts = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        
        # Extract SPARQL (remove prompt)
        sparql_queries = []
        for text in generated_texts:
            if formatted_prompt in text:
                sparql = text.split(formatted_prompt)[-1].strip()
            else:
                sparql = text.strip()
            sparql_queries.append(sparql)
        
        return sparql_queries
    
    def generate_batch(
        self,
        prompts: List[str],
        batch_size: int = 4,
        **kwargs
    ) -> List[List[str]]:
        """Generate SPARQL for multiple prompts."""
        
        results = []
        for i in range(0, len(prompts), batch_size):
            batch = prompts[i:i+batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(prompts)-1)//batch_size + 1}")
            
            for prompt in batch:
                sparql = self.generate(prompt, **kwargs)
                results.append(sparql)
        
        return results


def load_questions(filepath: Path) -> List[Dict]:
    """Load questions from JSONL file."""
    questions = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    return questions


def save_predictions(
    filepath: Path,
    predictions: List[Dict],
    mode: str = 'w'
):
    """Save predictions to JSONL file."""
    with open(filepath, mode) as f:
        for pred in predictions:
            f.write(json.dumps(pred) + '\n')
    logger.info(f"Saved {len(predictions)} predictions to {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate SPARQL using DPO fine-tuned model"
    )
    parser.add_argument(
        "--model",
        type=Path,
        required=True,
        help="Path to fine-tuned model"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input file with questions (JSONL or txt)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output file for predictions (default: input_predictions.jsonl)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="Batch size for processing"
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=512,
        help="Maximum length for generated SPARQL"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature"
    )
    parser.add_argument(
        "--top-p",
        type=float,
        default=0.9,
        help="Top-p sampling parameter"
    )
    parser.add_argument(
        "--num-beams",
        type=int,
        default=1,
        help="Number of beams for beam search (1 = sampling)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="Device to use (cuda or cpu)"
    )
    parser.add_argument(
        "--dtype",
        type=str,
        default="bfloat16",
        choices=["bfloat16", "float32"],
        help="Model dtype"
    )
    
    args = parser.parse_args()
    
    # Set output path
    if args.output is None:
        args.output = args.input.parent / f"{args.input.stem}_predictions.jsonl"
    
    try:
        # Initialize generator
        generator = DPOSPARQLGenerator(
            args.model,
            device=args.device,
            dtype=args.dtype,
        )
        
        # Load questions
        logger.info(f"Loading questions from {args.input}")
        if args.input.suffix == '.jsonl':
            questions = load_questions(args.input)
            prompts = [q['prompt'] for q in questions]
        else:
            with open(args.input, 'r') as f:
                prompts = [line.strip() for line in f if line.strip()]
            questions = [{'prompt': p} for p in prompts]
        
        logger.info(f"Loaded {len(questions)} questions")
        
        # Generate SPARQL
        logger.info(f"Generating SPARQL queries...")
        predictions = []
        
        for i, question in enumerate(questions):
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1}/{len(questions)} questions")
            
            sparql = generator.generate(
                question['prompt'],
                max_length=args.max_length,
                temperature=args.temperature,
                top_p=args.top_p,
                num_beams=args.num_beams,
            )[0]
            
            prediction = {
                'question_id': question.get('question_id', i),
                'prompt': question['prompt'],
                'sparql': sparql,
                'gold': question.get('gold', None),
            }
            predictions.append(prediction)
        
        # Save predictions
        save_predictions(args.output, predictions)
        logger.info(f"Saved predictions to {args.output}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Inference failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit(main())
