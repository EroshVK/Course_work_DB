-- SQL-команды для работы с БД

-- Удаление существующей БД
DROP DATABASE database_name

-- Создание новой БД
CREATE DATABASE database_name

-- Создание таблицы employers
CREATE TABLE employers (employer_id INT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        link VARCHAR(255),
                        open_vacancies INTEGER)

-- Создание таблицы vacancies
CREATE TABLE vacancies (vacancy_id INT PRIMARY KEY,
                        title VARCHAR(100) NOT NULL,
                        employer_id INT REFERENCES employers(employer_id),
                        salary INT,
                        experience VARCHAR(100),
                        description VARCHAR(255),
                        area VARCHAR(100),
                        link VARCHAR(255))

-- Заполнение таблицы employers данными
INSERT INTO employers (employer_id, name, link, open_vacancies)
VALUES (%s, %s, %s, %s), (employer["id"], employer["name"],
                        employer["alternate_url"], employer["open_vacancies"])

-- Заполнение таблицы vacancies данными
INSERT INTO vacancies (vacancy_id, title, employer_id,salary,
                       experience, description, area, link)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s), (vacancy["id"],
                                          vacancy["name"],
                                          vacancy["employer"]["id"],
                                          vacancy["salary"]["to"],
                                          vacancy["experience"]["name"],
                                          vacancy['snippet']['responsibility'],
                                          vacancy["area"]["name"],
                                          vacancy["alternate_url"])

-- Получение списка всех компаний и количество вакансий у каждой компании
SELECT employers.name as employer, COUNT (vacancies.vacancy_id) FROM vacancies
INNER JOIN employers ON vacancies.employer_id = employers.employer_id
GROUP BY employer ORDER BY COUNT (vacancies.vacancy_id) DESC

-- Получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT vacancies.title as vacancy, employers.name as employer, vacancies.salary, vacancies.link
FROM vacancies
INNER JOIN employers ON vacancies.employer_id = employers.employer_id

-- Получение средней зарплаты по вакансиям
SELECT ROUND(AVG(salary)) FROM vacancies

-- Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT vacancies.title as vacancy, employers.name as employer, vacancies.salary, vacancies.link
FROM vacancies
INNER JOIN employers ON vacancies.employer_id = employers.employer_id
WHERE salary > (%s)

-- Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
SELECT vacancies.title as vacancy, employers.name as employer, vacancies.salary, vacancies.link
FROM vacancies
INNER JOIN employers ON vacancies.employer_id = employers.employer_id
WHERE vacancies.title LIKE(%s)