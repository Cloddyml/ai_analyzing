from openai import OpenAI, OpenAIError

from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def _is_qwen3_thinking_model(model_name: str) -> bool:
    """
    Эвристика: является ли модель Qwen3-семейством с включённым thinking.

    Qwen3 и Qwen3.5 по умолчанию выдают <think>...</think> блок ПЕРЕД ответом.
    Для нашей задачи (генерация XML-правил с фиксированным max_tokens=256/512)
    это критично: модель тратит все токены на размышления и не успевает
    выдать сам ответ. Решение — передать в API enable_thinking=False
    через chat_template_kwargs.

    Qwen 2.5 (включая 2.5-Coder) — НЕ thinking-модель, для неё этот флаг не нужен.
    """
    name = model_name.lower()
    # Ловим qwen3, qwen-3, qwen3.5, qwen_qwen3 и т.п. варианты именований.
    return "qwen3" in name or "qwen-3" in name


class LMStudioClient:
    """
    Клиент для LM Studio через OpenAI-совместимый API.
    Поддерживает override параметров на каждый запрос (нужно для experiment runner).
    """

    def __init__(self):
        self._client = OpenAI(
            base_url=config.lm_studio_url,
            api_key="lm-studio",
        )
        self.default_model = config.model_name
        self.default_temp = config.temperature
        self.default_max_tokens = config.max_tokens

    def ask(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str | None:
        """
        Отправляет промпт в LLM. Возвращает текст ответа или None при ошибке.
        """
        used_model = model or self.default_model
        used_temp = temperature if temperature is not None else self.default_temp
        used_max = max_tokens or self.default_max_tokens

        # Дополнительные параметры запроса. Для Qwen3 — отключаем thinking,
        # иначе модель уйдёт в reasoning и не успеет выдать XML за лимит токенов.
        extra: dict = {}
        if _is_qwen3_thinking_model(used_model):
            extra["chat_template_kwargs"] = {"enable_thinking": False}
            logger.debug(f"Для {used_model} включён режим non-thinking")

        try:
            logger.debug(
                f"Запрос: model={used_model} temp={used_temp} max_tokens={used_max}"
            )

            response = self._client.chat.completions.create(
                model=used_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You output ONLY what is requested. "
                            "No preamble, no markdown fences, no commentary."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=used_temp,
                max_tokens=used_max,
                timeout=180,
                # extra_body доезжает до бэкенда LM Studio как доп.поля JSON-запроса.
                # Для не-Qwen3 моделей extra пустой → ничего не отправляется.
                extra_body=extra if extra else None,
            )

            choice = response.choices[0]
            text = choice.message.content or ""
            finish_reason = choice.finish_reason

            # Диагностика частого случая: модель упёрлась в лимит, не выдав ничего.
            # Это бывает если thinking всё-таки прошёл (например, для не-Qwen3
            # моделей, которые тоже могут "уходить в рассуждения"), либо если
            # max_tokens слишком маленький для данного промпта.
            if not text.strip() and finish_reason == "length":
                logger.warning(
                    f"Пустой ответ при finish_reason=length — "
                    f"вероятно, max_tokens={used_max} не хватило. "
                    f"Если это Qwen3 — проверь, что enable_thinking=False прошло."
                )

            logger.debug(
                f"Ответ получен: {len(text)} символов, finish_reason={finish_reason}"
            )
            return text

        except OpenAIError as e:
            logger.error(f"Ошибка LM Studio API: {e}")
            return None

        except Exception as e:
            logger.error(f"Неожиданная ошибка при вызове LLM: {e}")
            return None
