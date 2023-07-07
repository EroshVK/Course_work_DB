import requests

from api_classes.abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """
    Класс для работы с API HeadHunter
    """
    def __init__(self):
        self.url = 'https://api.hh.ru/'
        self.header = {'User-Agent': 'user_agent_hh'}

    def get_vacancies(self):
        """
        Метод для получения вакансий из 10 выбранных компаний
        """
        endpoint = 'vacancies'
        url = f'{self.url}{endpoint}'
        params = {"per_page": 100,
                  "page": 0,
                  "only_with_salary": True,
                  "area": 1,
                  "employer_id": ["3529",
                                  "1740",
                                  "80",
                                  "15478",
                                  "78638",
                                  "1057",
                                  "64174",
                                  "84585",
                                  "1429999",
                                  "1122462"]}
        response_for_pages = requests.get(url, params=params, headers=self.header)
        pages = response_for_pages.json()["pages"]
        response_vacancies = []
        for page in range(pages):
            params.update({'page': page})
            data = requests.get(url, params=params, headers=self.header)
            response_vacancies += data.json()['items']

        for vacancy in response_vacancies:
            if vacancy["salary"]["from"] is None:
                vacancy["salary"]["from"] = vacancy["salary"]["to"]
            else:
                vacancy["salary"]["from"] = vacancy["salary"]["from"]

            if vacancy["salary"]["to"] is None:
                vacancy["salary"]["to"] = vacancy["salary"]["from"]
            else:
                vacancy["salary"]["to"] = vacancy["salary"]["to"]

        return response_vacancies

    def get_employers(self):
        """
        Метод для получения данных о 10 выбранных компаниях
        """
        endpoint = 'employers/'
        employers_id = ["3529",
                        "1740",
                        "80",
                        "15478",
                        "78638",
                        "1057",
                        "64174",
                        "84585",
                        "1429999",
                        "1122462"]
        response_employers = []
        for employer in employers_id:
            url = f'{self.url}{endpoint}{employer}'
            response_employer = requests.get(url, headers=self.header)
            response_employers.append({"id": employer,
                                       "name": response_employer.json()["name"],
                                       "alternate_url": response_employer.json()["alternate_url"],
                                       "open_vacancies": response_employer.json()["open_vacancies"]})
        return response_employers
