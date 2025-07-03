from dataclasses import dataclass


@dataclass
class SellReportOut:
    unit_id: str
    cost: float
    partners: float
    bonus: float
    quantity: int
    return_cost: float
    return_partners: float
    return_bonus: float
    return_quantity: int
