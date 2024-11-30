import datetime
import json
import logging
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from config import PATH_HOME

load_dotenv()

# Путь до xlsx файла
path_to_file = os.path.join(PATH_HOME, "data", "operations.xlsx")

# Путь до json файла
path_json = os.path.join(PATH_HOME, "user_settings.json")

# Путь до файла log
path_to_log = os.path.join(PATH_HOME, "logs", "utils.log")


logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path_to_log, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def hello_user() -> str:
    """Фунция приветствия в зависимости от текущего времени"""
    current_date_time = datetime.datetime.now()
    if 4 <= current_date_time.hour <= 10:
        return "Доброе утро!"
    elif 10 < current_date_time.hour <= 16:
        return "Добрый день!"
    elif 16 < current_date_time.hour <= 22:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def get_user_setting(path: Any) -> Any:
    """Функция перевода настроек пользователя(курс и акции) из json объекта"""
    with open(path, "r", encoding="utf-8") as f:
        user_setting = json.load(f)
    return user_setting


def open_excel(file_name: Any) -> Any:
    """Функция для считавыния финансовых операций из Excel"""
    excel_data = pd.read_excel(file_name)
    return excel_data.apply(
        lambda row: {
            "Дата операции": row["Дата операции"],
            "Дата платежа": row["Дата платежа"],
            "Номер карты": row["Номер карты"],
            "Статус": row["Статус"],
            "Сумма операции": row["Сумма операции"],
            "Сумма платежа": row["Сумма платежа"],
            "Валюта платежа": row["Валюта платежа"],
            "Категория": row["Категория"],
            "Описание": row["Описание"],
        },
        axis=1,
    ).tolist()


def sort_operations_date(operations: Any, date: Any = None) -> list:
    """Функция возвращает новый список, отсортированный по дате"""
    logger.info("Начало работы функции (sort_operations_date)")
    year, month, day = int(date[0:4]), int(date[5:7]), int(date[8:10])
    list_date = []
    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime(year, month, day)
    logger.info("Перебор транзакций")
    for operation in operations:
        if str(operation["Дата платежа"]) == "nan":
            continue
        elif (
            date
            >= datetime.datetime.strptime(str(operation["Дата платежа"]), "%d.%m.%Y")
            >= date - datetime.timedelta(days=day)
        ):
            list_date.append(operation)
    logger.info("Вывод результата")
    return list_date


def filtered_card(card_number: Any) -> list:
    """Функция возвращает список по каждой карте"""
    logger.info("Начало работы функции")
    card = {}
    cards = []
    logger.info("Перебор транзакций")
    for i in card_number:
        if i["Номер карты"] == "nan" or type(i["Номер карты"]) is float:
            continue
        elif i["Сумма платежа"] == "nan":
            continue
        else:
            if i["Номер карты"][1:] in card:
                card[i["Номер карты"][1:]] += float(str(i["Сумма платежа"])[1:])
            else:
                card[i["Номер карты"][1:]] = float(str(i["Сумма платежа"])[1:])
    for k, v in card.items():
        cards.append({"last_digit": k, "total_spend": round(v, 2), "cashback": round(v / 100, 2)})
    logger.info("Вывод результата")
    return cards


def top_transactions_by_payment_amount(transactions: Any) -> list:
    """Функция возвращает топ-5 транзакций"""
    logger.info("Начало работы функции")
    sorted_transactions = sorted(transactions, key=lambda x: x["Сумма платежа"], reverse=True)
    top_transactions = sorted_transactions[:5]
    result_top = []
    for transaction in top_transactions:
        top = {
            "date": transaction["Дата платежа"],
            "amount": transaction["Сумма платежа"],
            "category": transaction["Категория"],
            "description": transaction["Описание"],
        }
        result_top.append(top)
    logger.info("Вывод результата")
    return result_top


def get_stock_price(stocks: Any) -> list:
    """Функция, возвращающая курсы акций"""
    logger.info("Начало работы функции")
    apikey = os.environ.get("API_KEY_STOCK")
    stock_price = []
    for stock in stocks["user_stocks"]:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={apikey}"
        response = requests.get(url)
        if response.status_code != 200:
            print("Запрос не был успешным.")

        else:
            data_ = response.json()
            stock_price.append({"stock": stock, "price": round(float(data_["Global Quote"]["05. price"]), 2)})
    logger.info("Вывод результата")
    return stock_price


def get_currency_rates(currencies: Any) -> list:
    """функция, возвращает курсы"""
    logger.info("Начало работы функции")
    API_KEY = os.environ.get("API_KEY")
    symbols = ",".join(currencies["user_currencies"])
    url = f"https://api.apilayer.com/currency_data/live?symbols={symbols}"

    headers = {"apikey": API_KEY}
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    if status_code != 200:
        print("Запрос не был успешным.")

    else:
        data = response.json()
        quotes = data.get("quotes", {})
        usd = quotes.get("USDRUB")
        eur_usd = quotes.get("USDEUR")
        eur = usd / eur_usd
        return [
            {"currency": "USD", "rate": round(usd, 2)},
            {"currency": "EUR", "rate": round(eur, 2)},
        ]


# if __name__ == "__main__":
#     result_hello = hello_user()
#     result = open_excel(path_to_file)
#     result_json = get_user_setting(path_json)
#     result_date = sort_operations_date(result)
#     result_trans = top_transactions_by_payment_amount(result_date)
#     result_card = filtered_card(result_date)
#     result_api_stock = get_stock_price(result_json)
#     result_api = get_currency_rates(result_json)
#     print(result_date)
