import os
import subprocess
import tempfile

from src.utils.logger import get_logger

logger = get_logger(__name__)


def _write_temp_rule(xml: str) -> str:
    f = tempfile.NamedTemporaryFile(
        suffix=".xml", delete=False, mode="w", encoding="utf-8"
    )
    f.write(xml)
    f.close()
    return f.name


def _run_cppcheck(rule_path: str, c_file: str, rule_id: str) -> bool:
    """
    С правильным XML (<id> внутри <message>) cppcheck выводит [rule_id], не [rule].
    Проверяем оба варианта для надёжности.
    """
    if not os.path.exists(c_file):
        logger.error(f"Файл не найден: {c_file}")
        return False
    try:
        result = subprocess.run(
            ["cppcheck", f"--rule-file={rule_path}", c_file],
            capture_output=True,
            text=True,
            timeout=30,
        )
        combined = result.stdout + result.stderr
        for line in combined.strip().splitlines():
            logger.debug(f"  cppcheck: {line}")
        if "unable to load rule-file" in combined:
            logger.warning(f"Не удалось загрузить правило: {combined[:200]}")
            return False
        return (f"[{rule_id}]" in combined) or ("[rule]" in combined)
    except FileNotFoundError:
        logger.error("cppcheck не найден. Установи: sudo apt install cppcheck")
        return False
    except subprocess.TimeoutExpired:
        logger.error(f"cppcheck завис на {c_file}")
        return False


def validate(rule: dict, bug: dict) -> dict:
    rule_path = _write_temp_rule(rule["raw_xml"])
    rule_id = rule.get("id", "custom_rule")
    logger.debug(f"[{bug['id']}] XML:\n{rule['raw_xml']}")
    try:
        tp = _run_cppcheck(rule_path, bug["bad_file"], rule_id)
        fp = _run_cppcheck(rule_path, bug["good_file"], rule_id)
    finally:
        os.unlink(rule_path)
    logger.info(
        f"[{bug['id']}] валидация: TP={'да' if tp else 'нет'}  FP={'да' if fp else 'нет'}"
    )
    return {"tp": tp, "fp": fp}
