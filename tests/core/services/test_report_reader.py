from app.core.services.report_reader import read_sell_report
from app.domain.entities.sell_report import SellReportOut


async def test_read_sell_report(sample_csv_bytes: bytes) -> None:
    result: list[SellReportOut] = read_sell_report(sample_csv_bytes)

    assert len(result) == 2
    assert all(isinstance(item, SellReportOut) for item in result)
    assert result[0].unit_id == "unit1"
    assert result[0].cost == 100.0
    assert result[0].return_quantity == 3
    assert result[1].unit_id == "unit3"
    assert result[1].cost == 200.0
    assert result[1].return_bonus == 0.5
