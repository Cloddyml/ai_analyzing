import csv
import json
import os
from datetime import datetime

from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def save_results(results: list[dict], metrics: dict) -> None:
    """
    Сохраняет все результаты на диск.
    Вызывается один раз в конце pipeline.py.
    """
    os.makedirs(config.results_dir, exist_ok=True)
    _save_csv(results)
    _save_report(metrics)


def _save_csv(results: list[dict]) -> None:
    """
    Сохраняет построчные результаты в CSV.
    Одна строка = один баг из датасета.

    Пример строки:
      id,generated,tp,fp,fn
      CWE-476,True,True,False,False
    """
    path = os.path.join(config.results_dir, "raw_results.csv")

    if not results:
        logger.warning("Нечего сохранять в CSV — список результатов пуст")
        return

    fieldnames = ["id", "generated", "tp", "fp"]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    logger.info(f"CSV сохранён: {path} ({len(results)} строк)")


def _save_report(metrics: dict) -> None:
    """
    Сохраняет итоговые метрики в JSON с меткой времени.
    Это главный файл для диплома.

    Пример:
      {
        "timestamp": "2024-03-19 12:00:00",
        "model": "qwen2.5-coder:7b",
        "total": 20,
        "precision": 0.75,
        ...
      }
    """
    path = os.path.join(config.results_dir, "report.json")

    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": config.model_name,
        **metrics,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info(f"Отчёт сохранён: {path}")
