def parse_float(value: str) -> float:
    """Парсит строку в float, заменяя запятую на точку. Возвращает 0.0 при ошибке."""
    try:
        return float(value.strip().replace(',', '.'))
    except ValueError:
        return 0.0


def parse_int(value: str) -> int:
    """Парсит строку в int. Возвращает 0 при ошибке."""
    return int(value.strip()) if value.strip().isdigit() else 0


def format_number(number: float) -> str:
    """Форматирует число в строку с двумя знаками после запятой и заменяет точку на запятую."""
    return f"{number:.2f}".replace('.', ',')
