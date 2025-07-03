import os
import time

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from app.core.converters.xlsx_to_csv import convert_xlsx_to_csv
from app.core.exceptions import FileFormatError, FileConversionError, ReportGenerationError, FileProcessingError
from app.core.services.report_generator import generate_report
from app.core.services.report_reader import read_sell_report
from app.core.services.report_writer import write_report_to_csv
from app.core.services.user_services import get_welcome_text
from logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    user_name = message.from_user.first_name
    welcome_text = await get_welcome_text(user_name)
    await message.answer(welcome_text)


@router.message(F.document)
async def handle_file(message: Message):
    start_time = time.time()
    document = message.document

    if not document.file_name.endswith(".xlsx"):
        await message.answer("Пожалуйста, отправьте файл в формате .xlsx.")
        return

    file_path = f"temp_{document.file_name}"
    await message.bot.download(document, destination=file_path)
    logger.info(f"Получен файл: {document.file_name}")

    await message.answer("Файл получен, начинается обработка. Это может занять некоторое время...")

    try:
        csv_file = f"converted_{document.file_name}.csv"
        convert_xlsx_to_csv(file_path, csv_file)

        with open(csv_file, 'rb') as f:
            file_data = f.read()

        sold_goods = await read_sell_report(file_data)
        report = generate_report(sold_goods)

        report_file = f"report_{document.file_name}.csv"
        write_report_to_csv(report, report_file)

        report_document = FSInputFile(report_file)
        await message.answer_document(report_document)

        execution_time = time.time() - start_time
        await message.answer(f"Время выполнения обработки файла: {execution_time:.2f} секунд")

        logger.info(f"Файл успешно обработан: {document.file_name}")
    except FileFormatError as e:
        logger.error(f"Формат файла неверен: {e}")
        await message.answer("Пожалуйста, отправьте файл в формате .xlsx.")
    except FileConversionError as e:
        logger.error(f"Ошибка конвертации файла: {e}")
        await message.answer("Не удалось конвертировать файл. Попробуйте другой файл.")
    except ReportGenerationError as e:
        logger.error(f"Ошибка генерации отчёта: {e}")
        await message.answer("Ошибка при создании отчёта.")
    except FileProcessingError as e:
        logger.error(f"Ошибка обработки файла: {e}")
        await message.answer("Произошла ошибка при обработке файла. Попробуйте позже.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        await message.answer("Произошла непредвиденная ошибка. Попробуйте позже.")
    finally:
        for temp_file in [file_path, csv_file, report_file]:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as e:
                    logger.warning(f"Не удалось удалить временный файл {temp_file}: {e}")
