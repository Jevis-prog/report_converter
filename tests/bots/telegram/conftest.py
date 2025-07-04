from typing import Generator
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import pytest


@pytest.fixture
def mock_message() -> AsyncMock:
    message = AsyncMock()
    message.answer = AsyncMock()
    message.answer_document = AsyncMock()
    message.bot = AsyncMock()
    message.document = None
    message.from_user = type("User", (), {"first_name": "Username"})
    return message


@pytest.fixture
def mock_document() -> type:
    return type("Doc", (), {"file_name": "report.xlsx"})


@pytest.fixture
def patch_convert_xlsx_to_csv() -> Generator[MagicMock, None, None]:
    with patch("app.bots.telegram.handlers.convert_xlsx_to_csv") as mock_convert:
        yield mock_convert


@pytest.fixture
def patch_read_sell_report() -> Generator[MagicMock, None, None]:
    with patch("app.bots.telegram.handlers.read_sell_report") as mock_read:
        yield mock_read


@pytest.fixture
def patch_generate_report() -> Generator[MagicMock, None, None]:
    with patch("app.bots.telegram.handlers.generate_report") as mock_generate:
        yield mock_generate


@pytest.fixture
def patch_write_report_to_csv() -> Generator[MagicMock, None, None]:
    with patch("app.bots.telegram.handlers.write_report_to_csv") as mock_write:
        yield mock_write


@pytest.fixture
def patch_fs_input_file() -> Generator[MagicMock, None, None]:
    with patch("app.bots.telegram.handlers.FSInputFile") as mock_fsfile:
        yield mock_fsfile


@pytest.fixture
def patch_open() -> Generator[MagicMock, None, None]:
    with patch("builtins.open", mock_open(read_data=b"test")) as mock_file:
        yield mock_file


@pytest.fixture
def patch_os_path_exists() -> Generator[MagicMock, None, None]:
    with patch("os.path.exists", return_value=True) as mock_exists:
        yield mock_exists


@pytest.fixture
def patch_os_remove() -> Generator[MagicMock, None, None]:
    with patch("os.remove") as mock_remove:
        yield mock_remove
