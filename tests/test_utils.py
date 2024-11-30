from unittest.mock import Mock, patch

from src.utils import (
    filtered_card,
    get_currency_rates,
    get_stock_price,
    sort_operations_date,
    top_transactions_by_payment_amount,
)


def test_get_user_setting(user_settings_json):
    assert user_settings_json == {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }


def test_open_excel(open_file_xlsx):
    assert open_file_xlsx == [
        {
            "Дата операции": "03.01.2018 14:55:21",
            "Дата платежа": "05.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -21.0,
            "Сумма платежа": -21.0,
            "Валюта платежа": "RUB",
            "Категория": "Красота",
            "Описание": "OOO Balid",
        }
    ]


def test_sort_operations_date(sort_date):
    result = sort_operations_date(sort_date, "2018.01.05")
    assert result == [
        {
            "Дата операции": "03.01.2018 15:03:35",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -73.06,
            "Сумма платежа": -73.06,
            "Валюта платежа": "RUB",
            "Категория": "Супермаркеты",
            "Описание": "Magazin 25",
        },
        {
            "Дата операции": "03.01.2018 14:55:21",
            "Дата платежа": "05.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -21.0,
            "Сумма платежа": -21.0,
            "Валюта платежа": "RUB",
            "Категория": "Красота",
            "Описание": "OOO Balid",
        },
        {
            "Дата операции": "01.01.2018 20:27:51",
            "Дата платежа": "04.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -316.0,
            "Сумма платежа": -316.0,
            "Валюта платежа": "RUB",
            "Категория": "Красота",
            "Описание": "OOO Balid",
        },
    ]


def test_sort_operations_date_1(sort_date_3):
    result = sort_operations_date(sort_date_3, "2018.01.05")
    assert result == []


def test_filtered_card(sort_date):
    results = filtered_card(sort_date)
    assert results == [{"last_digit": "7197", "total_spend": 410.06, "cashback": 4.1}]


def test_filtered_card_1(sort_date_1):
    result_card = filtered_card(sort_date_1)
    assert result_card == []


def test_filtered_card_2(sort_date_2):
    result_card = filtered_card(sort_date_2)
    assert result_card == []


def test_top_transactions_by_payment_amount(sort_date):
    result_top = top_transactions_by_payment_amount(sort_date)
    assert result_top == [
        {"date": "05.01.2018", "amount": -21.0, "category": "Красота", "description": "OOO Balid"},
        {"date": "04.01.2018", "amount": -73.06, "category": "Супермаркеты", "description": "Magazin 25"},
        {"date": "04.01.2018", "amount": -316.0, "category": "Красота", "description": "OOO Balid"},
    ]


def test_get_currency_rates():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"quotes": {"USDRUB": 108.24, "USDEUR": 0.95}}
    with patch("requests.get", return_value=mock_response):
        result = get_currency_rates(
            {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
        )
        assert result == [{"currency": "USD", "rate": 108.24}, {"currency": "EUR", "rate": 113.94}]


def test_get_stock_price():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"Global Quote": {"05. price": "228.8300"}}

    with patch("requests.get", return_value=mock_response):
        result = get_stock_price(
            {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
        )
        assert result == [
            {"stock": "AAPL", "price": 228.83},
            {"stock": "AMZN", "price": 228.83},
            {"stock": "GOOGL", "price": 228.83},
            {"stock": "MSFT", "price": 228.83},
            {"stock": "TSLA", "price": 228.83},
        ]


@patch("requests.get")
def test_get_stock_price_invalid(mocked_get):
    mocked_get.return_value.status_code = 404
    mocked_get.return_value.json.return_value = {"message": "Not Found"}
    result = get_stock_price({"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL"]})
    assert result == []


@patch("requests.get")
def test_get_currency_rates_invalid(mocked_get):
    mocked_get.return_value.status_code = 404
    mocked_get.return_value.json.return_value = {"message": "Not Found"}
    result = get_currency_rates({"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL"]})
    assert result is None
