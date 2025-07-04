from pathlib import Path
from typing import Any

import pytest

from app.domain.entities.sell_report import SellReportOut


@pytest.fixture
def sample_sold_goods() -> list[SellReportOut]:
    return [
        SellReportOut(
            unit_id="123",
            cost=100.0,
            return_cost=10.0,
            partners=5.0,
            return_partners=0.0,
            bonus=2.0,
            return_bonus=0.0,
            quantity=10,
            return_quantity=1,
        ),
        SellReportOut(
            unit_id="456",
            cost=200.0,
            return_cost=20.0,
            partners=10.0,
            return_partners=2.0,
            bonus=4.0,
            return_bonus=1.0,
            quantity=20,
            return_quantity=5,
        ),
    ]


@pytest.fixture
def sample_mc() -> dict[str, int]:
    return {
        "123": 50,
        "456": 100,
    }


@pytest.fixture
def sample_csv_bytes() -> bytes:
    csv_content = (
        "\n"
        * 15  # пропускаем 15 строк заголовков
        + "1;2;unit1;4;5;100.0;10;5;15;9;10;11;12;13;20.0;2.0;1.0;3\n"
        "1;2;unit2;4;5;;10;5;15;9;10;11;12;13;0;2.0;1.0;3\n"  # пустой cost — игнорируем
        "1;2;unit3;4;5;200.0;20;10;30;9;10;11;12;13;10.0;1.0;0.5;5\n"
        "1;2;unit4;4;5;150.0;15;7;20\n"  # меньше 18 столбцов — игнорируем
    )
    return csv_content.encode("utf-8")


@pytest.fixture
def sample_report() -> list[dict[str, Any]]:
    return [
        {
            "unit_id": "unit1",
            "cost": 100.0,
            "partners": 10.0,
            "bonus": 5.0,
            "quantity": 3,
            "purchase": 90.0,
            "purchase_cost": 270.0,
            "full_cost": 300.0,
        },
        {
            "unit_id": "unit2",
            "cost": 200.0,
            "partners": 20.0,
            "bonus": 10.0,
            "quantity": 2,
            "purchase": 180.0,
            "purchase_cost": 360.0,
            "full_cost": 400.0,
        },
    ]


@pytest.fixture
def output_file(tmp_path: Path) -> Path:
    return tmp_path / "test_report.csv"
