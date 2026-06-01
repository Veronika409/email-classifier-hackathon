"""Модуль для классификации писем"""

# Ключевые слова для каждой категории
KEYWORDS = {
    "urgent": [
        "срочно", "важно", "авария", "критично", "немедленно",
        "не работает", "поломка", "ошибка", "баг", "сбой"
    ],
    "it_issue": [
        "не работает", "ошибка", "баг", "сбой", "поломка",
        "антивирус", "excel", "word", "windows", "доступ",
        "не открывается", "зависает", "установить"
    ],
    "access_request": [
        "доступ", "права", "разрешить", "роль", "доступа"
    ],
    "meeting": [
        "созвон", "встреча", "перенос", "собрание", "совещание"
    ],
    "spam": [
        "реклама", "акция", "скидка", "партнер", "купить",
        "заработок", "казино", "лотерея"
    ]
}

# Категория по умолчанию, если ни одно правило не сработало
DEFAULT_CATEGORY = "other"

def classify(email_data: dict) -> str:
    """
    Классифицирует письмо на основе темы и тела письма.
    
    Параметры:
        email_data: dict с полями subject, from_addr, body
    
    Возвращает:
        название категории (str)
    """
    # Получаем текст для анализа
    subject = email_data.get("subject", "").lower()
    body = email_data.get("body", "").lower()
    
    # Объединяем тему и тело
    full_text = f"{subject} {body}"
    
    # Проверяем каждую категорию
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in full_text:
                return category
    
    # Если ничего не подошло
    return DEFAULT_CATEGORY
ALL_CATEGORIES = ["urgent", "it_issue", "access_request", "meeting", "spam", "other"]
UNKNOWN = "other"