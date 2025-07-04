import csv
import io

from app.domain.entities.sell_report import SellReportOut
from app.utils.parser import parse_float, parse_int

MIN_COLUMNS = 18
UNIT_ID = 2
COST = 5
PARTNERS = 6
BONUS = 7
QUANTITY = 8
RETURN_COST = 14
RETURN_PARTNERS = 15
RETURN_BONUS = 16
RETURN_QUANTITY = 17


def read_sell_report(file: bytes) -> list[SellReportOut]:
    with io.BytesIO(file) as file_stream:
        file_content = file_stream.read().decode('utf-8')

        csv_reader = csv.reader(file_content.splitlines(), delimiter=';')
        for _ in range(15):
            next(csv_reader)

        sell_units = []

        for row in csv_reader:
            if len(row) < MIN_COLUMNS:
                continue

            sell_unit = SellReportOut(
                unit_id=str(row[UNIT_ID]),
                cost=parse_float(row[COST]),
                partners=parse_float(row[PARTNERS]),
                bonus=parse_float(row[BONUS]),
                quantity=parse_int(row[QUANTITY]),
                return_cost=parse_float(row[RETURN_COST]),
                return_partners=parse_float(row[RETURN_PARTNERS]),
                return_bonus=parse_float(row[RETURN_BONUS]),
                return_quantity=parse_int(row[RETURN_QUANTITY]),
            )

            if not sell_unit.cost:
                continue

            sell_units.append(sell_unit)

    return sell_units
