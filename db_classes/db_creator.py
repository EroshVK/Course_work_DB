import psycopg2


def create_database(database_name, params):
    """
    Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях.
    """
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE {database_name}")
    except psycopg2.Error:
       print('База данных не существует. Создание новой базы данных.')

    cur.execute(f"CREATE DATABASE {database_name}")
    print(f'База данных {database_name} создана.')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE employers (employer_id INT PRIMARY KEY,
                                               name VARCHAR(100) NOT NULL,
                                               link VARCHAR(255),
                                               open_vacancies INTEGER)""")

    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE vacancies (vacancy_id INT PRIMARY KEY,
                                               title VARCHAR(100) NOT NULL,
                                               employer_id INT REFERENCES employers(employer_id),
                                               salary INT,
                                               experience VARCHAR(100),
                                               description VARCHAR(255),
                                               area VARCHAR(100),
                                               link VARCHAR(255))""")

    conn.commit()
    conn.close()


def save_data_to_database(data_employers, data_vacancies, database_name, params):
    """
    Сохранение данных о компаниях и вакансиях в базу данных.
    """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data_employers:
            cur.execute("""INSERT INTO employers (employer_id, name, link, open_vacancies)
                           VALUES (%s, %s, %s, %s)""",
                        (employer["id"],
                         employer["name"],
                         employer["alternate_url"],
                         employer["open_vacancies"]))
    conn.commit()

    with conn.cursor() as cur:
        for vacancy in data_vacancies:
            cur.execute("""INSERT INTO vacancies (vacancy_id, title, employer_id,salary,
                                                  experience, description, area, link)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (vacancy["id"],
                         vacancy["name"],
                         vacancy["employer"]["id"],
                         vacancy["salary"]["to"],
                         vacancy["experience"]["name"],
                         vacancy['snippet']['responsibility'],
                         vacancy["area"]["name"],
                         vacancy["alternate_url"]))
    conn.commit()

    conn.close()
    print("Данные сохранены в базу данных.")
