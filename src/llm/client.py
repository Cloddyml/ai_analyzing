import requests

from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    """Клиент для общения с локально запущенным Ollama."""

    def __init__(self):
        self.url = config.ollama_url + "/api/generate"
        self.model = config.model_name
        self.temp = config.temperature

    def ask(self, prompt: str) -> str | None:
        """
        Отправляет промпт в LLM и возвращает текст ответа.
        Возвращает None если запрос не удался.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temp,
                "num_ctx": 2048,
                "top_p": 0.9,
            },
        }

        try:
            logger.debug(f"Отправляем запрос к {self.model}...")
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            text = response.json()["response"]
            logger.debug(f"Ответ получен, длина: {len(text)} символов")
            return text

        except requests.exceptions.ConnectionError:
            logger.error("Ollama недоступен. Проверь: docker compose up -d")
            return None

        except requests.exceptions.Timeout:
            logger.error("Ollama не ответил за 120 секунд")
            return None

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP ошибка от Ollama: {e}")
            return None

        except (KeyError, ValueError) as e:
            logger.error(f"Неожиданный формат ответа от Ollama: {e}")
            return None
