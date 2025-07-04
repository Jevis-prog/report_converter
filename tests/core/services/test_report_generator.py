from app.core.services.report_generator import generate_report
from app.domain.entities.sell_report import SellReportOut


def test_generate_report(
    sample_sold_goods: list[SellReportOut],
    sample_mc: dict[str, int],
) -> None:
    report = generate_report(sample_sold_goods, sample_mc)

    assert isinstance(report, list)
    assert all(isinstance(item, dict) for item in report)

    first = next(item for item in report if item["unit_id"] == "123")
    assert first["cost"] == 90.0
    assert first["partners"] == 5.0
    assert first["bonus"] == 2.0
    assert first["quantity"] == 9
    assert first["purchase"] == 50
    assert first["purchase_cost"] == 50 * 9
    assert first["full_cost"] == 90 + 5 + 2

    second = next(item for item in report if item["unit_id"] == "456")
    assert second["cost"] == 180.0
    assert second["partners"] == 8.0
    assert second["bonus"] == 3.0
    assert second["quantity"] == 15
    assert second["purchase"] == 100
    assert second["purchase_cost"] == 100 * 15
    assert second["full_cost"] == 180 + 8 + 3
