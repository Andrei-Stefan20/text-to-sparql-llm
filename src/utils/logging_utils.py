import json
import logging
from pathlib import Path

from omegaconf import DictConfig, OmegaConf

logger = logging.getLogger(__name__)


def generate_run_name(cfg: DictConfig) -> str:
    """
    Creates a descriptive string for the experiment based on active flags.
    Example: gpt4_3shot_rebel_EntsON_ExOFF_limit10
    """
    parts = []

    # Model
    parts.append(cfg.model.name.replace("-", "").replace(" ", ""))

    # Retrieval
    parts.append(f"{cfg.retrieval.k}shot")

    # Linking
    parts.append(cfg.linking.method)

    # Prompt Flags
    if cfg.prompt.include_entities:
        parts.append("EntsON")
    else:
        parts.append("EntsOFF")

    if cfg.prompt.include_examples:
        parts.append("ExON")
    else:
        parts.append("ExOFF")

    # Data Limit
    if cfg.dataset.limit:
        parts.append(f"lim{cfg.dataset.limit}")
    else:
        parts.append("full")

    return "_".join(parts)


class ExperimentLogger:
    def __init__(self, cfg: DictConfig, output_dir: str = None):
        if output_dir is None:
            self.log_dir = Path.cwd()
        else:
            self.log_dir = Path(output_dir)
            self.log_dir.mkdir(parents=True, exist_ok=True)
        self._save_config_snapshot(cfg)

    def _save_config_snapshot(self, cfg: DictConfig):
        config_path = self.log_dir / "config_snapshot.yaml"
        with open(config_path, "w", encoding="utf-8") as f:
            OmegaConf.save(cfg, f)

    def save_results(self, results: dict):
        results_path = self.log_dir / "results_full.json"
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {results_path}")
