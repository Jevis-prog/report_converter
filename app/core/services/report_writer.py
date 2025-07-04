import csv
from typing import Any

from app.utils.parser import format_number


def write_report_to_csv(report: list[dict[str, Any]], file_name: str = "unit_report.csv") -> None:
    with open(file_name, mode="w", newline='', encoding="cp1251") as file:
        writer = csv.writer(file, delimiter=';')

        writer.writerow(
            [
                "Артикул",
                "Стоимость",
                "Скидка партнеров",
                "Баллы от озона",
                "Количество",
                "Закупка",
                "Стоимость закупки",
                "Полная стоимость",
            ]
        )

        total_cost = 0.0
        total_partners = 0.0
        total_bonus = 0.0
        total_quantity = 0
        total_purchase = 0.0
        total_purchase_cost = 0.0
        total_full_cost = 0.0

        for row in report:
            total_cost += row["cost"]
            total_partners += row["partners"]
            total_bonus += row["bonus"]
            total_quantity += row["quantity"]
            total_purchase += row["purchase"]
            total_purchase_cost += row["purchase_cost"]
            total_full_cost += row["full_cost"]

            writer.writerow(
                [
                    row["unit_id"],
                    format_number(row["cost"]),
                    format_number(row["partners"]),
                    format_number(row["bonus"]),
                    row["quantity"],
                    format_number(row["purchase"]),
                    format_number(row["purchase_cost"]),
                    format_number(row["full_cost"]),
                ]
            )

        writer.writerow(
            [
                "Итого:",
                format_number(total_cost),
                format_number(total_partners),
                format_number(total_bonus),
                total_quantity,
                format_number(total_purchase),
                format_number(total_purchase_cost),
                format_number(total_full_cost),
            ]
        )
