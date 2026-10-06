import requests

from config_data.config import OPENROUTER_API_KEY


REQUESTY_URL = "https://router.requesty.ai/v1/chat/completions"
REQUESTY_MODEL = "google/gemma-4-31b-it"
REQUEST_TIMEOUT = 30


SYSTEM_PROMPT = (
    "Ты — виртуальный гид по Петергофу "
    "Отвечай на вопросы пользователя о Петергофе, его истории, "
    "дворцах, фонтанах, Нижнем парке и других достопримечательностях "
    "Отвечай на русском языке "
    "Ответ должен быть понятным, интересным и не слишком длинным "
    "Если вопрос не связан с Петергофом, вежливо сообщи, "
    "что ты специализируешься на вопросах о Петергофе"
)


class AINotConfiguredError(Exception):
    """API-ключ не настроен."""


class AIRequestError(Exception):
    """Ошибка при запросе к AI."""


def ask_about_peterhof(question: str) -> str:
    """
    Отправляет вопрос пользователя в Requesty
    и возвращает ответ AI.
    """
    question = question.replace('.', ' ')
    if not OPENROUTER_API_KEY:
        raise AINotConfiguredError(
            "API-ключ AI не настроен. "
            "Добавьте OPENROUTER_API_KEY в файл .env."
        )

    payload = {
        "model": REQUESTY_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"Ответь на вопрос по Петергофу:\n\n{question}",
            },
        ],
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            REQUESTY_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

    except requests.Timeout as exc:
        raise AIRequestError(
            "Время ожидания ответа от AI истекло."
        ) from exc

    except requests.RequestException as exc:
        raise AIRequestError(
            f"Ошибка соединения с AI: {exc}"
        ) from exc

    if not response.ok:
        print("REQUESTY STATUS:", response.status_code)
        print("REQUESTY RESPONSE:", response.text)

        raise AIRequestError(
            f"Requesty вернул ошибку HTTP {response.status_code}."
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise AIRequestError(
            "AI вернул некорректный JSON-ответ."
        ) from exc

    try:
        answer = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        print("REQUESTY JSON:", data)

        raise AIRequestError(
            "Не удалось получить текст ответа от AI."
        ) from exc

    if not answer or not answer.strip():
        raise AIRequestError(
            "AI вернул пустой ответ."
        )

    return answer.strip()