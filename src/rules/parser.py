import re
from xml.etree import ElementTree as ET

from src.utils.logger import get_logger

logger = get_logger(__name__)


def parse_rule(llm_output: str) -> tuple[dict | None, str]:
    """
    Извлекает правило из ответа LLM.

    Возвращает кортеж (rule, reason):
      - rule   — словарь с полями правила, или None если не получилось
      - reason — причина неудачи: 'no_xml' | 'bad_xml' | 'no_pattern' | 'ok'
    """
    if not llm_output or not llm_output.strip():
        logger.warning("LLM вернула пустой ответ")
        return None, "no_xml"

    match = re.search(r"<rule>.*?</rule>", llm_output, re.DOTALL)
    if not match:
        logger.warning("В ответе LLM не найден блок <rule>...</rule>")
        return None, "no_xml"

    xml_str = match.group(0)

    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError as e:
        logger.warning(f"XML сломан: {e}")
        return None, "bad_xml"

    pattern = root.findtext("pattern", "").strip()
    if not pattern:
        logger.warning("Тег <pattern> пустой")
        return None, "no_pattern"

    rule = {
        "pattern": pattern,
        "message": root.findtext("message", "No message").strip(),
        "severity": root.findtext("severity", "warning").strip(),
        "id": root.findtext("id", "custom_rule").strip(),
        "raw_xml": xml_str,
    }

    logger.debug(f"Правило успешно распознано: id={rule['id']}")
    return rule, "ok"
