import collections
from collections import defaultdict

from app.domain.entities.sell_report import SellReportOut


def generate_report(sold_goods: list[SellReportOut], mc: dict[str, int]) -> list[dict[str, str | float | int]]:
    report_data: collections.defaultdict[str, dict[str, float]] = defaultdict(
        lambda: {
            "cost": 0.0,
            "partners": 0.0,
            "bonus": 0.0,
            "quantity": 0,
            "purchase": 0.0,
            "purchase_cost": 0.0,
            "full_cost": 0.0,
        }
    )

    for item in sold_goods:
        unit_id = item.unit_id
        if not unit_id:
            continue

        purchase_price = mc.get(unit_id, 0.0)

        data = report_data[unit_id]
        data["cost"] += item.cost - item.return_cost
        data["partners"] += item.partners - item.return_partners
        data["bonus"] += item.bonus - item.return_bonus
        data["quantity"] += item.quantity - item.return_quantity
        data["purchase"] = purchase_price
        data["purchase_cost"] += purchase_price * (item.quantity - item.return_quantity)

    for unit_id, data in report_data.items():
        data["full_cost"] = data["cost"] + data["partners"] + data["bonus"]

    return [{"unit_id": unit_id, **data} for unit_id, data in report_data.items()]
