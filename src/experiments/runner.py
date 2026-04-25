import csv
import json
import os
from itertools import product

from src.rules.generator import generate_rule
from src.rules.validator import validate
from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

MODELS = [
    "meta-llama-3.1-8b-instruct",
    "qwen2.5.1-coder-7b-instruct",
    "qwen_qwen3.5-9b",
]

TEMPERATURES = [0.0, 0.3, 0.7]

MAX_TOKENS_VALUES = [256, 512]

CSV_FIELDS = [
    "model",
    "temperature",
    "max_tokens",
    "bug_id",
    "bug_name",
    "generated",
    "syntactically_valid",
    "tp",
    "fp",
    "raw_xml",
]


def _load_bugs() -> list[dict]:
    if not os.path.exists(config.dataset_path):
        raise FileNotFoundError(
            f"Датасет не найден: {config.dataset_path}. Проверь DATASET_PATH в .env"
        )
    with open(config.dataset_path, encoding="utf-8") as f:
        bugs = json.load(f)
    logger.info(f"Датасет загружен: {len(bugs)} багов")
    return bugs


def _load_existing_results(csv_path: str) -> set[tuple]:
    if not os.path.exists(csv_path):
        return set()

    done = set()
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            done.add(
                (
                    row["model"],
                    float(row["temperature"]),
                    int(row["max_tokens"]),
                    row["bug_id"],
                )
            )
    return done


def _ensure_csv(csv_path: str) -> None:
    if os.path.exists(csv_path):
        return
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
    logger.info(f"Создан новый CSV: {csv_path}")


def _append_row(csv_path: str, row: dict) -> None:
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writerow(row)


def _process_one(bug: dict, model: str, temperature: float, max_tokens: int) -> dict:
    rule = generate_rule(
        bug,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    base = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "bug_id": bug["id"],
        "bug_name": bug["name"],
    }

    if rule is None:
        return {
            **base,
            "generated": False,
            "syntactically_valid": False,
            "tp": False,
            "fp": False,
            "raw_xml": "",
        }

    val = validate(rule, bug)

    return {
        **base,
        "generated": True,
        "syntactically_valid": val["syntactically_valid"],
        "tp": val["tp"],
        "fp": val["fp"],
        "raw_xml": rule["raw_xml"].replace("\n", " "),
    }


def run() -> None:
    csv_path = os.path.join(config.results_dir, "experiments.csv")
    _ensure_csv(csv_path)

    bugs = _load_bugs()
    done = _load_existing_results(csv_path)
    configs = list(product(MODELS, TEMPERATURES, MAX_TOKENS_VALUES))
    total_cells = len(configs) * len(bugs)

    logger.info("=" * 60)
    logger.info("Запуск эксперимента")
    logger.info(f"  Моделей:        {len(MODELS)}")
    logger.info(f"  Температур:     {len(TEMPERATURES)}")
    logger.info(f"  Max_tokens:     {len(MAX_TOKENS_VALUES)}")
    logger.info(f"  Багов:          {len(bugs)}")
    logger.info(f"  Конфигураций:   {len(configs)}")
    logger.info(f"  Итого ячеек:    {total_cells}")
    if done:
        logger.info(f"  Уже посчитано:  {len(done)} (пропустим)")
    logger.info("=" * 60)

    current_model = None
    completed = 0
    skipped = 0

    for model, temp, max_tok in configs:
        if model != current_model:
            logger.info("")
            logger.info("#" * 60)
            logger.info(f"# Переключение на модель: {model}")
            logger.info(f"# (LM Studio JIT загрузит её при первом запросе)")
            logger.info("#" * 60)
            current_model = model

        logger.info("")
        logger.info(f"--- Конфиг: model={model} temp={temp} max_tokens={max_tok} ---")

        for bug in bugs:
            completed += 1
            key = (model, temp, max_tok, bug["id"])

            if key in done:
                skipped += 1
                logger.debug(
                    f"[{completed}/{total_cells}] {bug['id']} — уже посчитано, пропуск"
                )
                continue

            logger.info(f"[{completed}/{total_cells}] {bug['id']} ({bug['name']})")
            row = _process_one(bug, model, temp, max_tok)
            _append_row(csv_path, row)

    logger.info("")
    logger.info("=" * 60)
    logger.info("Эксперимент завершён")
    logger.info(f"  Всего ячеек:        {total_cells}")
    logger.info(f"  Пропущено (resume): {skipped}")
    logger.info(f"  Обработано сейчас:  {total_cells - skipped}")
    logger.info(f"  CSV:                {csv_path}")
    logger.info("=" * 60)


if __name__ == "__main__":
    run()
