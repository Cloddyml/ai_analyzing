from openai import OpenAI, OpenAIError

from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LMStudioClient:
    def __init__(self):
        self._client = OpenAI(
            base_url=config.lm_studio_url,
            # API key обязателен для SDK, но LM Studio его не проверяет —
            # любая непустая строка подойдёт.
            api_key="lm-studio",
        )
        # Дефолты из .env. Используются только если в ask() не передали override.
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
        used_model = model or self.default_model
        used_temp = temperature if temperature is not None else self.default_temp
        used_max = max_tokens or self.default_max_tokens

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
            )

            text = response.choices[0].message.content or ""
            logger.debug(f"Ответ получен: {len(text)} символов")
            return text

        except OpenAIError as e:
            logger.error(f"Ошибка LM Studio API: {e}")
            return None

        except Exception as e:
            logger.error(f"Неожиданная ошибка при вызове LLM: {e}")
            return None
