import datetime
import logging
import os
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import PATH_HOME

# Путь до файла log
path_to_log = os.path.join(PATH_HOME, "logs", "reports.log")


logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path_to_log, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def log(filename: Any = None) -> Callable:
    """декоратор,который логирует вызов функции и ее результат в файл или в консоль"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = "my_function ok\n"
            except Exception as e:
                result = None
                log_message = f"my_function error: {e}. Inputs: {args}, {kwargs} \n"
            if filename:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(log_message)
            else:
                print(log_message)
            return result

        return wrapper

    return decorator


@log("reports.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list | str:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""
    logger.info("Начало работы функции")
    if date is None:
        return []

    try:
        end_date = datetime.datetime.strptime(date, "%d.%m.%Y")
        start_date = end_date - relativedelta(months=3)
    except ValueError:
        logger.error("Неверный формат данных")
        return "Неверный формат данных"

    current_transactions = []
    for transaction in transactions:
        if not isinstance(transaction["Дата платежа"], str):
            continue
        transaction_date = datetime.datetime.strptime(transaction["Дата платежа"], "%d.%m.%Y")
        if transaction["Категория"] == category and start_date <= transaction_date <= end_date:
            current_transactions.append(transaction)
    logger.info("Вывод результата")
    return current_transactions


# if __name__ == "__main__":
#     results = open_excel(path_to_file)
#     result_category = spending_by_category(results, "Супермаркеты", "05.10.2018")
#     result_log = log(result_category)
#     print(result_category)
