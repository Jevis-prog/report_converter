import csv
from pathlib import Path

from app.core.converters.xlsx_to_csv import convert_xlsx_to_csv


def test_convert_xlsx_to_csv(sample_xlsx: Path, tmp_path: Path) -> None:
    csv_path = tmp_path / "output.csv"
    convert_xlsx_to_csv(str(sample_xlsx), str(csv_path))

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        rows = list(reader)

    assert rows == [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
