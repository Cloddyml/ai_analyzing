import json
import os

from src.metrics.calculator import calculate
from src.metrics.reporter import save_results
from src.rules.generator import generate_rule
from src.rules.validator import validate
from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def _load_dataset() -> list[dict]:
    """Загружает список багов из JSON-файла."""
    if not os.path.exists(config.dataset_path):
        logger.error(f"Датасет не найден: {config.dataset_path}")
        raise FileNotFoundError(config.dataset_path)

    with open(config.dataset_path, encoding="utf-8") as f:
        bugs = json.load(f)

    logger.info(f"Датасет загружен: {len(bugs)} багов из {config.dataset_path}")
    return bugs


def _save_rule_xml(bug_id: str, raw_xml: str) -> None:
    """Сохраняет сгенерированное XML-правило в results/rules/."""
    rules_dir = os.path.join(config.results_dir, "rules")
    os.makedirs(rules_dir, exist_ok=True)

    path = os.path.join(rules_dir, f"{bug_id}.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(raw_xml)

    logger.debug(f"Правило сохранено: {path}")


def _process_bug(bug: dict) -> dict:
    """
    Обрабатывает один баг из датасета:
      1. Генерирует правило через LLM
      2. Проверяет правило на тестовых файлах
      3. Возвращает результат для метрик

    Возвращает словарь:
      id        — идентификатор бага
      generated — удалось ли получить правило
      tp        — правило нашло баг в плохом коде
      fp        — правило сработало на хорошем коде
    """
    logger.info(f"--- [{bug['id']}] {bug['name']} ---")

    rule = generate_rule(bug)

    if rule is None:
        logger.warning(f"[{bug['id']}] правило не сгенерировано, пропускаем")
        return {
            "id": bug["id"],
            "generated": False,
            "tp": False,
            "fp": False,
        }

    _save_rule_xml(bug["id"], rule["raw_xml"])

    validation = validate(rule, bug)

    return {
        "id": bug["id"],
        "generated": True,
        "tp": validation["tp"],
        "fp": validation["fp"],
    }


def run() -> None:
    """Запускает полный пайплайн от датасета до отчёта."""
    logger.info("========================================")
    logger.info("Запуск пайплайна генерации правил")
    logger.info(f"Модель:      {config.model_name}")
    logger.info(f"Temperature: {config.temperature}")
    logger.info(f"Max retries: {config.max_retries}")
    logger.info("========================================")

    bugs = _load_dataset()
    results = []

    for i, bug in enumerate(bugs, start=1):
        logger.info(f"Прогресс: {i}/{len(bugs)}")
        result = _process_bug(bug)
        results.append(result)

    metrics = calculate(results)
    save_results(results, metrics)

    logger.info("========================================")
    logger.info("Готово. Результаты:")
    logger.info(f"  Precision:  {metrics['precision']:.1%}")
    logger.info(f"  Recall:     {metrics['recall']:.1%}")
    logger.info(f"  F1-score:   {metrics['f1']:.1%}")
    logger.info(f"  Отчёт:      {config.results_dir}report.json")
    logger.info("========================================")


if __name__ == "__main__":
    run()
