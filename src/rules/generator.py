from src.llm.client import OllamaClient
from src.llm.prompts import make_retry_hint, make_rule_prompt
from src.rules.parser import parse_rule
from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

_client = OllamaClient()


def generate_rule(bug: dict) -> dict | None:
    """
    Генерирует cppcheck-правило для одного бага.
    При неудаче повторяет попытку до MAX_RETRIES раз.
    Возвращает словарь правила или None если все попытки провалились.
    """
    hint = ""

    for attempt in range(config.max_retries):
        logger.info(f"[{bug['id']}] попытка {attempt + 1}/{config.max_retries}")

        prompt = make_rule_prompt(bug, retry_hint=hint)
        response = _client.ask(prompt)

        if response is None:
            logger.error(f"[{bug['id']}] Ollama не ответил, прерываем")
            return None

        rule, reason = parse_rule(response)

        if rule is not None:
            logger.info(f"[{bug['id']}] правило получено с попытки {attempt + 1}")
            return rule

        hint = make_retry_hint(attempt, reason)
        logger.warning(f"[{bug['id']}] попытка {attempt + 1} неудачна: {reason}")

    logger.error(f"[{bug['id']}] не удалось за {config.max_retries} попыток")
    return None
