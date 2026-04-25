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


def _run_cppcheck(rule_path: str, c_file: str, rule_id: str) -> dict:
    if not os.path.exists(c_file):
        logger.error(f"Файл не найден: {c_file}")
        return {"loaded": False, "matched": False}

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
            logger.warning(f"Правило не загрузилось: {combined[:200]}")
            return {"loaded": False, "matched": False}

        matched = (f"[{rule_id}]" in combined) or ("[rule]" in combined)
        return {"loaded": True, "matched": matched}

    except FileNotFoundError:
        logger.error("cppcheck не найден. Установи: sudo apt install cppcheck")
        return {"loaded": False, "matched": False}
    except subprocess.TimeoutExpired:
        logger.error(f"cppcheck завис на {c_file}")
        return {"loaded": False, "matched": False}


def validate(rule: dict, bug: dict) -> dict:
    rule_path = _write_temp_rule(rule["raw_xml"])
    rule_id = rule.get("id", "custom_rule")

    logger.debug(f"[{bug['id']}] XML:\n{rule['raw_xml']}")

    try:
        bad_result = _run_cppcheck(rule_path, bug["bad_file"], rule_id)
        good_result = _run_cppcheck(rule_path, bug["good_file"], rule_id)
    finally:
        os.unlink(rule_path)

    syntactically_valid = bad_result["loaded"] and good_result["loaded"]
    tp = bad_result["matched"]
    fp = good_result["matched"]

    logger.info(
        f"[{bug['id']}] валидация: "
        f"valid={'да' if syntactically_valid else 'НЕТ'}  "
        f"TP={'да' if tp else 'нет'}  "
        f"FP={'да' if fp else 'нет'}"
    )

    return {
        "tp": tp,
        "fp": fp,
        "syntactically_valid": syntactically_valid,
    }
