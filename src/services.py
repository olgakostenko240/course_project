import datetime
import logging
import os
from typing import Any

from config import PATH_HOME

# Путь до файла log
path_to_log = os.path.join(PATH_HOME, "logs", "services.log")


logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path_to_log, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float:
    """Функция, возвращающая сумму, которую можно было бы отложить в Инвесткопилку
    в заданном месяце года при заданном округлении"""
    logger.info("Начало работы функции")
    operations = []
    for transaction in transactions:
        date_excel = transaction["Дата операции"]
        operation_data = datetime.datetime.strptime(date_excel, "%d.%m.%Y %H:%M:%S")
        format_date = operation_data.strftime("%Y-%m-%d %H:%M:%S")
        transaction["Дата_операции"] = format_date
        if month in transaction["Дата_операции"]:
            operations.append(transaction)
    # print(operations)

    total_investment = 0
    for operation in operations:
        amount = operation["Сумма операции"]
        ceshback = abs(amount) * -1 // limit * -1 * limit
        investment = ceshback - abs(amount)
        operation["Кэшбэк"] = investment
        total_investment += investment
        total_investment = round(total_investment, 2)

    print(f"Итого за {month} в инвесткопилку была бы отложена сумма {total_investment} руб.")
    logger.info("Вывод результата")
    return total_investment


# if __name__ == "__main__":
#     result = investment_bank("2021-12", open_excel(path_to_file), 50)
#     print(result)
