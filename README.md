# Курсовая 5. Работа с базами данных 

## В рамках проекта осуществляется получение данных о 10 компаниях и их вакансиях с сайта hh.ru, создаются таблицы в БД PostgreSQL и полученные данные загружаются в созданные таблицы.

- Приложение запускается из файла main.py
- Перед запуском приложения нужно указать параметры подключения к БД в файле config.ini
- При запуске приложение удаляет базу данных (если она создана), создает новую базу данных, создаеттаблицы и заполняет их данными
- Взаимодействие с пользователем происходит через меню, выход из которого происходит при выборе соответствующей опции
- Для вывода данных из БД в консоль используется библиотека PrettyTable.
___

Методы получения данных из БД:
- Получить список всех компаний и количество вакансий у каждой компании
- Получить список всех вакансий с указанием названия компании названия вакансии и зарплаты и ссылки на вакансию
- Получить среднюю зарплату по вакансиям
- Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
- Получить список всех вакансий, в названии которых содержатся переданные в метод слова
