import os

from config import PATH_HOME
from src.reports import spending_by_category
from src.services import investment_bank
from src.utils import open_excel
from src.views import home_page

# Путь до xlsx файла
path_to_file = os.path.join(PATH_HOME, "data", "operations.xlsx")


if __name__ == "__main__":
    result = open_excel(path_to_file)

    result_invest = investment_bank("2021-12", result, 50)
    print(result_invest)

    result_category = spending_by_category(result, "Супермаркеты", "05.10.2018")
    print(result_category)

    result_home = home_page("2021.11.24")
    print(result_home)
