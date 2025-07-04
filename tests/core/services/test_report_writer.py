import csv
from typing import Any

from app.core.services.report_writer import write_report_to_csv
from app.utils.parser import format_number


def test_write_report_to_csv(sample_report: list[dict[str, Any]], output_file: str) -> None:
    write_report_to_csv(sample_report, str(output_file))

    with open(output_file, encoding="cp1251", newline="") as f:
        reader = csv.reader(f, delimiter=';')
        rows = list(reader)

    # Проверим заголовок
    assert rows[0] == [
        "Артикул",
        "Стоимость",
        "Скидка партнеров",
        "Баллы от озона",
        "Количество",
        "Закупка",
        "Стоимость закупки",
        "Полная стоимость",
    ]

    # Проверим строки с данными (первые две записи)
    assert rows[1] == [
        "unit1",
        format_number(100.0),
        format_number(10.0),
        format_number(5.0),
        "3",
        format_number(90.0),
        format_number(270.0),
        format_number(300.0),
    ]
    assert rows[2] == [
        "unit2",
        format_number(200.0),
        format_number(20.0),
        format_number(10.0),
        "2",
        format_number(180.0),
        format_number(360.0),
        format_number(400.0),
    ]

    # Проверим итоговую строку
    assert rows[3] == [
        "Итого:",
        format_number(300.0),  # 100 + 200
        format_number(30.0),  # 10 + 20
        format_number(15.0),  # 5 + 10
        "5",  # 3 + 2
        format_number(270.0),  # 90 + 180
        format_number(630.0),  # 270 + 360
        format_number(700.0),  # 300 + 400
    ]
