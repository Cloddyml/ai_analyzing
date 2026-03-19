import os
import subprocess
import tempfile

from src.utils.logger import get_logger

logger = get_logger(__name__)


def _write_temp_rule(xml: str) -> str:
    """Сохраняет XML во временный файл и возвращает путь к нему."""
    f = tempfile.NamedTemporaryFile(
        suffix=".xml", delete=False, mode="w", encoding="utf-8"
    )
    f.write(xml)
    f.close()
    return f.name


def _run_cppcheck(rule_path: str, c_file: str) -> bool:
    """
    Запускает cppcheck с правилом на указанном файле.
    Возвращает True если cppcheck что-то нашёл.
    """
    if not os.path.exists(c_file):
        logger.error(f"Тестовый файл не найден: {c_file}")
        return False

    try:
        result = subprocess.run(
            ["cppcheck", f"--rule-file={rule_path}", c_file],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stderr.strip()
        found = len(output) > 0
        logger.debug(f"cppcheck на {c_file}: {'нашло' if found else 'ничего'}")
        return found

    except FileNotFoundError:
        logger.error("cppcheck не найден. Установи: apt install cppcheck")
        return False

    except subprocess.TimeoutExpired:
        logger.error(f"cppcheck завис на файле {c_file}")
        return False


def validate(rule: dict, bug: dict) -> dict:
    """
    Проверяет правило на двух файлах: с багом и без.

    Возвращает словарь:
      tp — правило нашло баг в плохом коде   (хотим True)
      fp — правило сработало на хорошем коде (хотим False)
    """
    rule_path = _write_temp_rule(rule["raw_xml"])

    try:
        tp = _run_cppcheck(rule_path, bug["bad_file"])
        fp = _run_cppcheck(rule_path, bug["good_file"])
    finally:
        os.unlink(rule_path)

    logger.info(
        f"[{bug['id']}] валидация: "
        f"TP={'да' if tp else 'нет'}  FP={'да' if fp else 'нет'}"
    )
    return {"tp": tp, "fp": fp}
