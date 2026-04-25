from src.utils.logger import get_logger

logger = get_logger(__name__)


def calculate(results: list[dict]) -> dict:
    total = len(results)
    generated = [r for r in results if r["generated"]]
    failed = total - len(generated)

    if not generated:
        logger.warning("Нет ни одного успешно сгенерированного правила")
        return _empty_metrics(total)

    # Считаем базовые числа
    tp_count = sum(1 for r in generated if r["tp"] and not r["fp"])
    fp_count = sum(1 for r in generated if r["fp"])
    fn_count = sum(1 for r in generated if not r["tp"])
    tn_count = sum(1 for r in generated if not r["tp"] and not r["fp"])

    precision = tp_count / (tp_count + fp_count) if (tp_count + fp_count) > 0 else 0.0

    recall = tp_count / (tp_count + fn_count) if (tp_count + fn_count) > 0 else 0.0

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    generation_rate = len(generated) / total

    metrics = {
        "total": total,
        "generated": len(generated),
        "failed": failed,
        "generation_rate": round(generation_rate, 3),
        "tp": tp_count,
        "fp": fp_count,
        "fn": fn_count,
        "tn": tn_count,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
    }

    _log_summary(metrics)
    return metrics


def _empty_metrics(total: int) -> dict:
    return {
        "total": total,
        "generated": 0,
        "failed": total,
        "generation_rate": 0.0,
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "tn": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    }


def _log_summary(m: dict) -> None:
    logger.info("=== Метрики ===")
    logger.info(f"Всего багов:          {m['total']}")
    logger.info(f"Правил сгенерировано: {m['generated']} / {m['total']}")
    logger.info(f"Generation rate:      {m['generation_rate']:.1%}")
    logger.info(f"TP={m['tp']}  FP={m['fp']}  FN={m['fn']}")
    logger.info(f"Precision:  {m['precision']:.1%}")
    logger.info(f"Recall:     {m['recall']:.1%}")
    logger.info(f"F1-score:   {m['f1']:.1%}")
