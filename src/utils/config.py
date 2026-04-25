import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    lm_studio_url: str
    model_name: str
    temperature: float
    max_tokens: int
    max_retries: int
    dataset_path: str
    results_dir: str
    log_level: str


def _load() -> Config:
    return Config(
        lm_studio_url=os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1"),
        model_name=os.getenv("MODEL_NAME", "qwen2.5.1-coder-7b-instruct"),
        temperature=float(os.getenv("TEMPERATURE", "0.2")),
        max_tokens=int(os.getenv("MAX_TOKENS", "512")),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        dataset_path=os.getenv("DATASET_PATH", "dataset/bugs.json"),
        results_dir=os.getenv("RESULTS_DIR", "results/"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )


config = _load()
