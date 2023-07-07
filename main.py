from prettytable import PrettyTable

from config import config
from api_classes.hh_cls import HeadHunterAPI
from db_classes.db_creator import *
from db_classes.db_manager import DBManager


def interact_with_user():
    """
    Метод для работы с пользователем
    """
    dbmanager = DBManager()

    print("Выберете метод получения данных из БД")
    print("1. Получить список всех компаний и количество вакансий у каждой компании")
    print("2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
    print("3. Получить среднюю зарплату по вакансиям")
    print("4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям")
    print("5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”")
    print("Для выхода нажмите 6")

    while True:
        table = PrettyTable()

        choice = input("Выберите действие: ")

        if choice == "1":
            print("Cписок всех компаний и количество вакансий у каждой компании")
            data = dbmanager.get_companies_and_vacancies_count('headhunter', params)
            table.field_names = ["Компания", "Кол-во вакансий"]
            for item in data:
                table.add_row([item[0], item[1]])
            print(table)

        elif choice == "2":
            print("Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
            data = dbmanager.get_all_vacancies('headhunter', params)
            table.field_names = ["Вакансия", "Компания", "Зарплата", "Ссылка"]
            for item in data:
                table.add_row([item[0], item[1], item[2], item[3]])
            print(table)

        elif choice == "3":
            print("Cредняя зарплата по вакансиям")
            data = dbmanager.get_avg_salary('headhunter', params)
            table.header = False
            table.add_row(data[0])
            print(table)

        elif choice == "4":
            print("Cписок всех вакансий, у которых зарплата выше средней по всем вакансиям")
            data = dbmanager.get_vacancies_with_higher_salary('headhunter', params)
            table.field_names = ["Вакансия", "Компания", "Зарплата", "Ссылка"]
            for item in data:
                table.add_row([item[0], item[1], item[2], item[3]])
            print(table)

        elif choice == "5":
            keyword = input("Ведите слово для поиска. Внимание поиск чувствителен к регистру    ")
            print(f"Cписок всех вакансий, в названии которых содержится слово {keyword}")
            data = dbmanager.get_vacancies_with_keyword('headhunter', params, keyword)
            table.field_names = ["Вакансия", "Компания", "Зарплата", "Ссылка"]
            for item in data:
                table.add_row([item[0], item[1], item[2], item[3]])
            print(table)

        elif choice == "6":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    hh = HeadHunterAPI()
    params = config()
    create_database('headhunter', params)
    data_employers = hh.get_employers()
    data_vacancies = hh.get_vacancies()
    save_data_to_database(data_employers, data_vacancies, 'headhunter', params)
    interact_with_user()
