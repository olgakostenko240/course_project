from src.reports import spending_by_category


def test_spending_by_category(sort_date):
    result = spending_by_category(sort_date, "Супермаркеты", "03.01.2018 15:03:35")
    assert result == "Неверный формат данных"


def test_spending_by_category_1(sort_date):
    result = spending_by_category(sort_date, "Супермаркеты", "03.01.2018")
    assert result == []


def test_spending_by_category_2(sort_date):
    result = spending_by_category(sort_date, "Супермаркеты", "04.01.2018")
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
        }
    ]


def test_spending_by_category_3(sort_date):
    result = spending_by_category(sort_date, "Супермаркеты")
    assert result == []


def test_spending_by_category_4(sort_date):
    result = spending_by_category(sort_date, "Красота", "30.01.2018")
    assert result == [
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
