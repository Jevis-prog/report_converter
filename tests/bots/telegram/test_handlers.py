from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.bots.telegram.handlers import handle_file, start_handler
from app.core.exceptions import DeleteFileError, FileConversionError, ReportGenerationError


@pytest.mark.asyncio
async def test_start_handler(mock_message: AsyncMock) -> None:
    await start_handler(mock_message)
    mock_message.answer.assert_awaited_with(
        "Привет, Username! Этот бот создан для обработки отчета по реализациям"
        " с маркетплейса Ozon. Пожалуйста, пришли свой отчет."
    )


@pytest.mark.asyncio
async def test_handle_file_no_document(mock_message: AsyncMock) -> None:
    await handle_file(mock_message)
    mock_message.answer.assert_awaited_with("Пожалуйста, отправьте файл в формате .xlsx.")


@pytest.mark.asyncio
async def test_handle_file_wrong_extension(mock_message: AsyncMock) -> None:
    mock_message.document = type("Doc", (), {"file_name": "file.txt"})
    await handle_file(mock_message)
    mock_message.answer.assert_awaited_with("Пожалуйста, отправьте файл в формате .xlsx.")


@pytest.mark.asyncio
async def test_handle_file_no_bot(mock_message: AsyncMock, mock_document: type) -> None:
    mock_message.document = mock_document
    mock_message.bot = None
    await handle_file(mock_message)
    mock_message.answer.assert_awaited_with("Не удалось обработать файл, повторите попытку позже.")


@pytest.mark.asyncio
async def test_handle_file_conversion_error(
    mock_message: AsyncMock, mock_document: type, patch_convert_xlsx_to_csv: MagicMock
) -> None:
    mock_message.document = mock_document
    patch_convert_xlsx_to_csv.side_effect = FileConversionError()
    await handle_file(mock_message)
    assert any("Не удалось конвертировать файл" in call.args[0] for call in mock_message.answer.call_args_list)


@pytest.mark.asyncio
async def test_handle_file_report_generation_error(
    mock_message: AsyncMock,
    mock_document: type,
    patch_convert_xlsx_to_csv: MagicMock,
    patch_read_sell_report: MagicMock,
    patch_generate_report: MagicMock,
    patch_open: MagicMock,
) -> None:
    mock_message.document = mock_document
    patch_generate_report.side_effect = ReportGenerationError()
    patch_read_sell_report.return_value = []
    await handle_file(mock_message)
    assert any("Ошибка при создании отчёта." in call.args[0] for call in mock_message.answer.call_args_list)


@pytest.mark.asyncio
async def test_handle_file_success(
    mock_message: AsyncMock,
    mock_document: type,
    patch_convert_xlsx_to_csv: MagicMock,
    patch_read_sell_report: MagicMock,
    patch_generate_report: MagicMock,
    patch_write_report_to_csv: MagicMock,
    patch_fs_input_file: MagicMock,
    patch_open: MagicMock,
    patch_os_path_exists: MagicMock,
    patch_os_remove: MagicMock,
) -> None:
    mock_message.document = mock_document
    patch_read_sell_report.return_value = [{"good": 1}]
    patch_generate_report.return_value = [["a", "b"]]

    await handle_file(mock_message)

    mock_message.answer_document.assert_awaited_once()
    assert any("Время выполнения обработки файла:" in call.args[0] for call in mock_message.answer.call_args_list)
    patch_os_remove.assert_called()


@pytest.mark.asyncio
async def test_handle_file_remove_file_error(
    mock_message: AsyncMock,
    mock_document: type,
    patch_convert_xlsx_to_csv: MagicMock,
    patch_read_sell_report: MagicMock,
    patch_generate_report: MagicMock,
    patch_write_report_to_csv: MagicMock,
    patch_fs_input_file: MagicMock,
    patch_open: MagicMock,
    patch_os_path_exists: MagicMock,
) -> None:
    mock_message.document = mock_document

    patch_read_sell_report.return_value = [{"good": 1}]
    patch_generate_report.return_value = [["a", "b"]]

    with patch("os.remove", side_effect=DeleteFileError("Удаление не удалось")):
        await handle_file(mock_message)
