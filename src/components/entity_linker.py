from abc import ABC, abstractmethod
from typing import List, Tuple
from omegaconf import DictConfig
from transformers import pipeline
import re
import logging

# Configure logger
logger = logging.getLogger(__name__)

class BaseLinker(ABC):
    """Abstract base class for Entity Linking strategies."""
    @abstractmethod
    def extract(self, text: str) -> List[str]:
        """Extracts a list of entity mentions from the text."""
        pass

class RebelLinker(BaseLinker):
    """
    Implements Entity Linking using the REBEL model (Relation Extraction By End-to-end Language generation).
    It parses the generated triplets to identify salient entities in the question.
    """
    
    def __init__(self, config: DictConfig):
        model_path = config.get("model_path", "Babelscape/rebel-large")
        device = config.get("device", 0) # -1 for CPU, 0 for GPU
        
        logger.info(f"Loading REBEL model from '{model_path}' on device {device}...")
        try:
            self.pipe = pipeline("text2text-generation", model=model_path, tokenizer=model_path, device=device)
        except Exception as e:
            logger.error(f"Failed to load REBEL model: {e}")
            raise

    def extract(self, text: str) -> List[str]:
        """
        Generates triplets and extracts the subject/object entities.
        """
        if not text:
            return []

        try:
            model_inputs = self.pipe.tokenizer(text, return_tensors="pt").to(self.pipe.device)
            
            generated_ids = self.pipe.model.generate(
                **model_inputs,
                max_length=256,
                num_beams=3,
                num_return_sequences=1
            )
            
            raw_text = self.pipe.tokenizer.decode(generated_ids[0], skip_special_tokens=False)
            
            print(f"\n[REBEL RAW]: {raw_text}") 
            
            #Clean string (es. <pad>, </s>)
            return self._parse_rebel_output(raw_text)
            
        except Exception as e:
            logger.warning(f"REBEL generation failed for text '{text[:30]}...': {e}")
            return []

    def _parse_rebel_output(self, text: str) -> List[str]:
        """
        Parses REBEL output format: <triplet> Subject <subj> Relation <obj> Object
        Returns a list of unique entity names found.
        """
        text = text.replace("</s>", "").replace("<s>", "")
        entities = set()
        
        # Split by the triplet token to isolate relations
        relations = text.split("<triplet>")
        
        for relation in relations:
            # Each relation should contain <subj> and <obj> tokens
            # We extract the text before <subj> (Subject) and after <obj> (Object)
            
            # Extract Subject
            if "<subj>" in relation:
                parts = relation.split("<subj>")
                subject = parts[0].strip()
                if subject:
                    entities.add(subject)
                
                # Extract Object
                if len(parts) > 1 and "<obj>" in parts[1]:
                    obj_parts = parts[1].split("<obj>")
                    if len(obj_parts) > 1:
                        obj = obj_parts[1].strip()
                        if obj:
                            entities.add(obj)
                            
        return list(entities)

class RelikLinker(BaseLinker):
    """Wrapper for the ReLiK entity linking system."""
    
    def __init__(self, config: DictConfig):
        try:
            import relik
        except ImportError:
            raise ImportError("The 'relik' library is not installed. Please install it to use RelikLinker.")
            
        logger.info(f"Loading ReLiK model from '{config.model_path}'...")
        self.model = relik.Relik.from_pretrained(config.model_path)

    def extract(self, text: str) -> List[str]:
        response = self.model(text)
        # ReLiK returns spans; we extract the text of the identified entities
        return [span.text for span in response.spans]

def get_linker(config: DictConfig) -> BaseLinker:
    """Factory function to instantiate the correct linker based on configuration."""
    method = config.method.lower()
    if method == "rebel":
        return RebelLinker(config)
    elif method == "relik":
        return RelikLinker(config)
    else:
        raise ValueError(f"Unknown entity linking method: {method}")