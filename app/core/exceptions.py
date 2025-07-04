class FileProcessingError(Exception):
    """Общее исключение для ошибок обработки файлов."""

    pass


class FileFormatError(FileProcessingError):
    """Ошибка неправильного формата файла."""

    pass


class FileConversionError(FileProcessingError):
    """Ошибка при конвертации файла."""

    pass


class ReportGenerationError(FileProcessingError):
    """Ошибка при генерации отчёта."""

    pass


class TemporaryFileError(FileProcessingError):
    """Ошибка работы с временными файлами."""

    pass


class DeleteFileError(FileProcessingError):
    """Неожиданная ошибка"""

    pass
