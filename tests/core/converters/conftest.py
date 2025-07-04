from pathlib import Path

import pytest
from openpyxl.workbook import Workbook


@pytest.fixture
def sample_xlsx(tmp_path: Path) -> Path:
    file_path = tmp_path / "sample.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Age"])
    ws.append(["Alice", 30])
    ws.append(["Bob", 25])
    wb.save(file_path)
    return file_path
