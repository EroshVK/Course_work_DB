import psycopg2


class DBManager:
    def get_companies_and_vacancies_count(self, database_name, params):
        """
        Данный метод получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT employers.name as employer, COUNT (vacancies.vacancy_id) FROM vacancies
                               INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                               GROUP BY employer ORDER BY COUNT (vacancies.vacancy_id) DESC""")
                data = cur.fetchall()
                return data
        finally:
            conn.close()

    def get_all_vacancies(self, database_name, params):
        """
        Данный метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT vacancies.title as vacancy, employers.name as employer, vacancies.salary, vacancies.link
                               FROM vacancies
                               INNER JOIN employers ON vacancies.employer_id = employers.employer_id""")
                data = cur.fetchall()
                return data
        finally:
            conn.close()

    def get_avg_salary(self, database_name, params):
        """
        Данный метод получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT ROUND(AVG(salary)) FROM vacancies""")
                data = cur.fetchall()
                return data
        finally:
            conn.close()

    def get_vacancies_with_higher_salary(self, database_name, params):
        """
        Данный метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT vacancies.title as vacancy, employers.name as employer, vacancies.salary, vacancies.link
                               FROM vacancies
                               INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                               WHERE salary > (%s)""",
                               (self.get_avg_salary(database_name, params)))
                data = cur.fetchall()
                return data
        finally:
            conn.close()

    def get_vacancies_with_keyword(self, database_name, params, keyword):
        """
        Данный метод получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например “python”.
        """
        conn = psycopg2.connect(dbname=database_name, **params)
        try:
            with conn.cursor() as cur:
                query = """SELECT vacancies.title as vacancy, employers.name as employer, vacancies.salary, vacancies.link
                               FROM vacancies
                               INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                               WHERE vacancies.title LIKE(%s)"""
                param_format = '%{}%'.format(keyword)
                cur.execute(query, (param_format,))
                data = cur.fetchall()
                return data
        finally:
            conn.close()
