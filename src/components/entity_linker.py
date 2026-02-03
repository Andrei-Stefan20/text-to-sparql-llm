import logging
import os
import re
from abc import ABC, abstractmethod
from typing import List, Tuple

from omegaconf import DictConfig
from transformers import pipeline

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
    Implements Entity Linking using the REBEL model.
    """

    def __init__(self, config: DictConfig):
        model_path = config.get("model_path", "Babelscape/rebel-large")
        device = config.get("device", 0)

        logger.info(f"Loading REBEL model from '{model_path}' on device {device}...")
        try:
            self.pipe = pipeline(
                "text2text-generation",
                model=model_path,
                tokenizer=model_path,
                device=device,
            )
        except Exception as e:
            logger.error(f"Failed to load REBEL model: {e}")
            raise

    def extract(self, text: str) -> List[str]:
        if not text:
            return []

        try:
            model_inputs = self.pipe.tokenizer(text, return_tensors="pt").to(
                self.pipe.device
            )

            generated_ids = self.pipe.model.generate(
                **model_inputs, max_length=256, num_beams=3, num_return_sequences=1
            )

            raw_text = self.pipe.tokenizer.decode(
                generated_ids[0], skip_special_tokens=False
            )

            logger.info(f"[REBEL RAW]: {raw_text}")

            return self._parse_rebel_output(raw_text)

        except Exception as e:
            logger.warning(f"REBEL generation failed: {e}")
            return []

    def _parse_rebel_output(self, text: str) -> List[str]:
        """
        Parses REBEL output.
        """
        text = text.replace("</s>", "").replace("<s>", "")
        entities = set()

        relations = text.split("<triplet>")

        for relation in relations:
            if "<subj>" in relation:
                parts = relation.split("<subj>")
                subject = parts[0].strip()
                if subject:
                    entities.add(subject)

                if len(parts) > 1 and "<obj>" in parts[1]:
                    obj_parts = parts[1].split("<obj>")

                    rel_text = obj_parts[0].strip()
                    if rel_text:
                        entities.add(rel_text)

                    if len(obj_parts) > 1:
                        obj = obj_parts[1].strip()
                        if obj and obj.lower() != "instance of":
                            entities.add(obj)

        return list(entities)


class RelikLinker(BaseLinker):
    def __init__(self, config: DictConfig):
        try:
            import relik
        except ImportError:
            raise ImportError("The 'relik' library is not installed.")
        logger.info(f"Loading ReLiK model from '{config.model_path}'...")
        self.model = relik.Relik.from_pretrained(config.model_path)

    def extract(self, text: str) -> List[str]:
        response = self.model(text)
        return [span.text for span in response.spans]


class AllLinkersCombo(BaseLinker):
    """Runs all available linkers and concatenates results."""

    def __init__(self, config: DictConfig):
        logger.info("Loading all entity linkers...")
        
        rebel_config = DictConfig({
            "method": "rebel",
            "model_path": config.get("rebel_model_path", "Babelscape/rebel-large"),
            "device": config.get("device", -1)
        })
        relik_config = DictConfig({
            "method": "relik",
            "model_path": config.get("relik_model_path", "sapienzanlp/relik-entity-linking-large"),
            "window_size": config.get("window_size", 32)
        })
        
        self.rebel = RebelLinker(rebel_config)
        self.relik = RelikLinker(relik_config)

    def extract(self, text: str) -> List[str]:
        entities_rebel = self.rebel.extract(text)
        entities_relik = self.relik.extract(text)
        
        logger.info(f"[REBEL] {entities_rebel}")
        logger.info(f"[RELIK] {entities_relik}")
        
        # Merge and deduplicate
        combined = list(dict.fromkeys(entities_rebel + entities_relik))
        logger.info(f"[COMBINED] {combined}")
        
        return combined


def get_linker(config: DictConfig, cache_dir: str = None) -> BaseLinker:
    # Set HuggingFace cache directory if provided
    if cache_dir:
        os.environ['HF_HOME'] = os.path.expanduser(cache_dir)
        logger.info(f"Using HuggingFace cache: {cache_dir}")
    
    method = config.method.lower()
    if method == "rebel":
        return RebelLinker(config)
    elif method == "relik":
        return RelikLinker(config)
    elif method == "all":
        return AllLinkersCombo(config)
    else:
        raise ValueError(f"Unknown entity linking method: {method}")
