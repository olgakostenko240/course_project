from src.services import investment_bank


def test_investment_bank(sort_date):
    result = investment_bank("2018.01", sort_date, 50)
    assert result == 0
