import logging
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union
import urllib.request
import urllib.parse
import json

from omegaconf import DictConfig
from transformers import pipeline

# Configure logger
logger = logging.getLogger(__name__)


@dataclass
class LinkedEntity:
    """
    Represents a linked entity with its Wikidata QID.
    
    Attributes:
        text: The surface form/mention in the original text
        qid: The Wikidata QID (e.g., "Q76" for Obama), None if not resolved
        label: The canonical label from Wikidata (if available)
        score: Confidence score from the linker (0-1)
    """
    text: str
    qid: Optional[str] = None
    label: Optional[str] = None
    score: float = 1.0
    
    def to_sparql_format(self) -> str:
        """Returns formatted string for SPARQL prompt: 'Obama (wd:Q76)'"""
        if self.qid:
            return f"{self.text} (wd:{self.qid})"
        return self.text
    
    def __str__(self) -> str:
        return self.to_sparql_format()


class WikidataResolver:
    """
    Utility class to resolve entity text to Wikidata QIDs via the Search API.
    Used as fallback when the linker doesn't provide QIDs.
    """
    
    SEARCH_URL = "https://www.wikidata.org/w/api.php"
    
    @staticmethod
    def resolve(entity_text: str, language: str = "en") -> Optional[str]:
        """
        Resolves an entity text to a Wikidata QID using the search API.
        
        Args:
            entity_text: The entity mention to resolve
            language: Language for search (default: English)
            
        Returns:
            The QID (e.g., "Q76") or None if not found
        """
        try:
            params = {
                "action": "wbsearchentities",
                "search": entity_text,
                "language": language,
                "format": "json",
                "limit": 1,
            }
            url = f"{WikidataResolver.SEARCH_URL}?{urllib.parse.urlencode(params)}"
            
            req = urllib.request.Request(
                url, 
                headers={"User-Agent": "TextToSparqlBot/1.0"}
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                
            if data.get("search"):
                result = data["search"][0]
                qid = result.get("id")
                logger.debug(f"Resolved '{entity_text}' -> {qid}")
                return qid
                
        except Exception as e:
            logger.warning(f"Wikidata resolution failed for '{entity_text}': {e}")
        
        return None
    
    @staticmethod
    def resolve_batch(
        entities: List[str], language: str = "en"
    ) -> List[Tuple[str, Optional[str]]]:
        """
        Resolves multiple entity texts to QIDs.
        
        Returns:
            List of (entity_text, qid) tuples
        """
        results = []
        for entity in entities:
            qid = WikidataResolver.resolve(entity, language)
            results.append((entity, qid))
        return results


class BaseLinker(ABC):
    """Abstract base class for Entity Linking strategies."""

    @abstractmethod
    def extract(self, text: str) -> List[LinkedEntity]:
        """
        Extracts and links entities from the text.
        
        Args:
            text: Input text to process
            
        Returns:
            List of LinkedEntity objects with QIDs when available
        """
        pass
    
    def extract_as_strings(self, text: str) -> List[str]:
        """
        Backward-compatible method that returns formatted strings.
        Format: "EntityText (wd:QID)" or just "EntityText" if no QID.
        """
        entities = self.extract(text)
        return [e.to_sparql_format() for e in entities]


class RebelLinker(BaseLinker):
    """
    Implements relation extraction using the REBEL model.
    Note: REBEL extracts relations, not entity links. We use WikidataResolver
    as a fallback to resolve extracted entity mentions to QIDs.
    """

    def __init__(self, config: DictConfig):
        model_path = config.get("model_path", "Babelscape/rebel-large")
        device = config.get("device", 0)
        self.use_wikidata_fallback = config.get("use_wikidata_fallback", True)

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

    def extract(self, text: str) -> List[LinkedEntity]:
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

            entity_texts = self._parse_rebel_output(raw_text)
            
            # Convert to LinkedEntity with Wikidata resolution
            entities = []
            for entity_text in entity_texts:
                qid = None
                if self.use_wikidata_fallback:
                    qid = WikidataResolver.resolve(entity_text)
                
                entities.append(LinkedEntity(
                    text=entity_text,
                    qid=qid,
                    label=entity_text,  # REBEL doesn't provide canonical labels
                    score=0.8  # Fixed score since REBEL doesn't provide confidence
                ))
            
            logger.info(f"[REBEL ENTITIES]: {[str(e) for e in entities]}")
            return entities

        except Exception as e:
            logger.warning(f"REBEL generation failed: {e}")
            return []

    def _parse_rebel_output(self, text: str) -> List[str]:
        """
        Parses REBEL output to extract entity mentions.
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
    """
    Implements Entity Linking using the ReLiK model.
    ReLiK provides direct entity linking to Wikidata with QIDs.
    """
    
    def __init__(self, config: DictConfig):
        try:
            import relik
        except ImportError:
            raise ImportError("The 'relik' library is not installed.")
        
        model_path = config.get("model_path", "sapienzanlp/relik-entity-linking-large")
        self.use_wikidata_fallback = config.get("use_wikidata_fallback", True)
        
        logger.info(f"Loading ReLiK model from '{model_path}'...")
        self.model = relik.Relik.from_pretrained(model_path)

    def extract(self, text: str) -> List[LinkedEntity]:
        """
        Extracts entities with their Wikidata QIDs.
        
        ReLiK span objects contain:
        - span.text: The surface form in the text
        - span.label: The Wikidata QID (e.g., "Q76")
        - span.score: Confidence score (0-1)
        """
        if not text:
            return []
        
        try:
            response = self.model(text)
            entities = []
            
            for span in response.spans:
                # Extract QID from label (ReLiK returns full URL or just ID)
                qid = self._extract_qid(span.label) if hasattr(span, 'label') else None
                
                # Fallback to Wikidata API if no QID found
                if not qid and self.use_wikidata_fallback:
                    qid = WikidataResolver.resolve(span.text)
                
                entity = LinkedEntity(
                    text=span.text,
                    qid=qid,
                    label=getattr(span, 'label', span.text),
                    score=getattr(span, 'score', 1.0) if hasattr(span, 'score') else 1.0
                )
                entities.append(entity)
            
            logger.info(f"[RELIK ENTITIES]: {[str(e) for e in entities]}")
            return entities
            
        except Exception as e:
            logger.warning(f"ReLiK extraction failed: {e}")
            return []
    
    def _extract_qid(self, label: str) -> Optional[str]:
        """
        Extracts the QID from various label formats.
        
        Handles:
        - "Q76" -> "Q76"
        - "http://www.wikidata.org/entity/Q76" -> "Q76"
        - "Barack Obama" -> None (not a QID)
        """
        if not label:
            return None
        
        # Direct QID format
        if re.match(r'^Q\d+$', label):
            return label
        
        # URL format
        match = re.search(r'/(Q\d+)$', label)
        if match:
            return match.group(1)
        
        return None


class AllLinkersCombo(BaseLinker):
    """Runs all available linkers and merges results intelligently."""

    def __init__(self, config: DictConfig):
        logger.info("Loading all entity linkers...")
        
        rebel_config = DictConfig({
            "method": "rebel",
            "model_path": config.get("rebel_model_path", "Babelscape/rebel-large"),
            "device": config.get("device", -1),
            "use_wikidata_fallback": config.get("use_wikidata_fallback", True)
        })
        relik_config = DictConfig({
            "method": "relik",
            "model_path": config.get("relik_model_path", "sapienzanlp/relik-entity-linking-large"),
            "use_wikidata_fallback": config.get("use_wikidata_fallback", True)
        })
        
        self.rebel = RebelLinker(rebel_config)
        self.relik = RelikLinker(relik_config)

    def extract(self, text: str) -> List[LinkedEntity]:
        """
        Runs both linkers and merges results.
        Prefers entities with QIDs over those without.
        Deduplicates by QID when available, otherwise by text.
        """
        entities_rebel = self.rebel.extract(text)
        entities_relik = self.relik.extract(text)
        
        logger.info(f"[REBEL] {[str(e) for e in entities_rebel]}")
        logger.info(f"[RELIK] {[str(e) for e in entities_relik]}")
        
        # Merge with preference for entities with QIDs
        merged = {}
        
        # First add ReLiK entities (usually have QIDs)
        for entity in entities_relik:
            key = entity.qid if entity.qid else entity.text.lower()
            if key not in merged or (entity.qid and not merged[key].qid):
                merged[key] = entity
        
        # Then add REBEL entities (fill gaps)
        for entity in entities_rebel:
            key = entity.qid if entity.qid else entity.text.lower()
            if key not in merged:
                merged[key] = entity
            elif entity.qid and not merged[key].qid:
                # Upgrade existing entity with QID
                merged[key] = entity
        
        combined = list(merged.values())
        logger.info(f"[COMBINED] {[str(e) for e in combined]}")
        
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
