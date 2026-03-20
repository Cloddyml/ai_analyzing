import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    ollama_url: str
    model_name: str
    temperature: float
    num_ctx: int
    max_retries: int
    dataset_path: str
    results_dir: str
    log_level: str


def _load() -> Config:
    return Config(
        ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        model_name=os.getenv("MODEL_NAME", "qwen2.5-coder:7b"),
        temperature=float(os.getenv("TEMPERATURE", "0.2")),
        num_ctx=int(os.getenv("NUM_CTX", "2048")),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        dataset_path=os.getenv("DATASET_PATH", "dataset/bugs.json"),
        results_dir=os.getenv("RESULTS_DIR", "results/"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )


config = _load()
