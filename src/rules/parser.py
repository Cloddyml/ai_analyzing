import re
from xml.etree import ElementTree as ET

from src.utils.logger import get_logger

logger = get_logger(__name__)
_THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def parse_rule(llm_output: str) -> tuple[dict | None, str]:
    if not llm_output or not llm_output.strip():
        logger.warning("LLM вернула пустой ответ")
        return None, "no_xml"
    cleaned = _THINK_BLOCK.sub("", llm_output)
    matches = list(re.finditer(r"<rule[^>]*>.*?</rule>", cleaned, re.DOTALL))
    if not matches:
        logger.warning("В ответе LLM не найден блок <rule>...</rule>")
        return None, "no_xml"

    xml_str = matches[-1].group(0)

    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError as e:
        logger.warning(f"XML сломан: {e}")
        return None, "bad_xml"

    pattern = root.findtext("pattern", "").strip()
    if not pattern:
        logger.warning("Тег <pattern> пустой")
        return None, "no_pattern"

    message_elem = root.find("message")

    if message_elem is not None and message_elem.find("id") is not None:
        rule_id = (message_elem.findtext("id") or "custom_rule").strip()
        severity = (message_elem.findtext("severity") or "warning").strip()
        summary = (
            message_elem.findtext("summary") or "Rule violation detected"
        ).strip()
    else:
        rule_id = (root.findtext("id") or "custom_rule").strip()
        severity = (root.findtext("severity") or "warning").strip()
        summary = ""
        if message_elem is not None:
            summary = (message_elem.text or "").strip()
        if not summary:
            summary = "Rule violation detected"

    correct_xml = (
        f'<?xml version="1.0"?>\n'
        f'<rule version="1">\n'
        f"  <pattern>{_escape_xml(pattern)}</pattern>\n"
        f"  <message>\n"
        f"    <id>{_escape_xml(rule_id)}</id>\n"
        f"    <severity>{_escape_xml(severity)}</severity>\n"
        f"    <summary>{_escape_xml(summary)}</summary>\n"
        f"  </message>\n"
        f"</rule>"
    )

    rule = {
        "pattern": pattern,
        "message": summary,
        "severity": severity,
        "id": rule_id,
        "raw_xml": correct_xml,
    }

    logger.debug(f"Правило успешно распознано: id={rule['id']}, pattern={pattern!r}")
    return rule, "ok"


def _escape_xml(text: str) -> str:
    """Экранирует спецсимволы XML в тексте."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
