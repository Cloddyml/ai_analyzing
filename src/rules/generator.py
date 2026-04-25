import os
import subprocess

from src.llm.client import LMStudioClient
from src.llm.prompts import make_retry_hint, make_rule_prompt
from src.rules.parser import parse_rule
from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

_client = LMStudioClient()


def _get_token_stream(c_file: str) -> str:
    if not c_file or not os.path.exists(c_file):
        return ""
    try:
        result = subprocess.run(
            ["cppcheck", "--rule=.+", c_file],
            capture_output=True,
            text=True,
            timeout=15,
        )
        for line in (result.stdout + result.stderr).splitlines():
            if "[rule]" in line and "found '" in line:
                start = line.find("found '") + len("found '")
                end = line.rfind("' [rule]")
                if start > 0 and end > start:
                    return line[start:end].strip()
    except Exception as e:
        logger.warning(f"Не удалось получить токен-стрим из {c_file}: {e}")
    return ""


def generate_rule(
    bug: dict,
    *,
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> dict | None:
    bad_stream = _get_token_stream(bug.get("bad_file", ""))
    good_stream = _get_token_stream(bug.get("good_file", ""))

    if bad_stream:
        logger.debug(f"[{bug['id']}] bad stream: {bad_stream[:80]}...")
    else:
        logger.warning(f"[{bug['id']}] токен-стрим bad_file недоступен")

    hint = ""
    for attempt in range(config.max_retries):
        logger.info(f"[{bug['id']}] попытка {attempt + 1}/{config.max_retries}")

        prompt = make_rule_prompt(
            bug, bad_stream=bad_stream, good_stream=good_stream, retry_hint=hint
        )
        response = _client.ask(
            prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        if response is None:
            logger.error(f"[{bug['id']}] LM Studio не ответил, прерываем")
            return None

        rule, reason = parse_rule(response)
        if rule is not None:
            logger.info(f"[{bug['id']}] правило получено с попытки {attempt + 1}")
            return rule

        hint = make_retry_hint(attempt, reason)
        logger.warning(f"[{bug['id']}] попытка {attempt + 1} неудачна: {reason}")

    logger.error(f"[{bug['id']}] не удалось за {config.max_retries} попыток")
    return None
