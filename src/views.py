import json
import os
from typing import Any

from config import PATH_HOME
from src.utils import (
    filtered_card,
    get_currency_rates,
    get_stock_price,
    get_user_setting,
    hello_user,
    open_excel,
    sort_operations_date,
    top_transactions_by_payment_amount,
)

# Путь до xlsx файла
path_to_file = os.path.join(PATH_HOME, "data", "operations.xlsx")

path_json = os.path.join(PATH_HOME, "user_settings.json")


def home_page(date: Any) -> str:
    """Функция, формирующая страницу главная"""
    result = open_excel(path_to_file)
    result_json = get_user_setting(path_json)
    final_list = sort_operations_date(result, date)
    greeting = hello_user()
    cards = filtered_card(final_list)
    top_trans = top_transactions_by_payment_amount(final_list)
    currency_rates = get_currency_rates(result_json)
    stocks_prices = get_stock_price(result_json)
    result = [
        {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_trans,
            "currency_rates": currency_rates,
            "stock_prices": stocks_prices,
        },
    ]
    date_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )
    return date_json


# if __name__ == "__main__":
#     result_date = home_page("2021.11.24")
#     print(result_date)
