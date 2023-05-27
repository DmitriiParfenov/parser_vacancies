import json
import os
import time

import isodate
import requests

from utils.class_operations import Vacancy, Parser


class HeadHunterAPI(Parser):
    """Класс для работы с API HeadHunter."""
    def __init__(self):
        """
        Экземпляр инициализируется url, api-key, header и params для создания запроса на сервер HeadHunter.
        В ответ на запрос искомые вакансии в виде экземпляров класса Vacancy будут храниться в db_vacancies.
        """

        self.__url = 'https://api.hh.ru/vacancies'
        self.__hh_apikey = os.getenv('HH_API_KEY')
        self.__header = {'client_id': self.__hh_apikey}
        self.__params = {}
        self.__db_vacancies = []

    def get_vacancies(self, title_vacancy: str) -> list:
        """Метод в качестве аргумента принимает название вакансии в виде строки и делает запрос на сервер HeadHunter.
        Вакансии, соответствующие названию, добавляются в db_vacancies. Максимальное количество вакансий в одном
        запросе составляет 2000."""

        for i in range(0, 20):
            self.__params = {
                'text': title_vacancy,
                'area': 113,
                'per_page': 100,
                'page': i,
            }
            request = requests.get(self.__url, headers=self.__header, params=self.__params)
            if request.ok:
                response = request.content.decode()
                request.close()
                data = json.loads(response)
                if data['items']:
                    for item in data['items']:
                        id_ = int(item.get('id'))
                        title = item.get('name')
                        url = item.get('alternate_url')
                        if item.get('salary'):
                            salary_from = item.get('salary').get('from')
                        else:
                            salary_from = item.get('salary')
                        if item.get('salary'):
                            salary_to = item.get('salary').get('to')
                        else:
                            salary_to = item.get('salary')
                        name_employer = item.get('employer').get('name')
                        city = item.get('area').get('name')
                        description = item.get('snippet').get('responsibility')
                        requirement = item.get('snippet').get('requirement')
                        experience = item.get('experience').get('name')
                        if item.get('published_at'):
                            date = isodate.parse_datetime(item.get('published_at'))
                        else:
                            date = None
                        self.__db_vacancies.append(Vacancy(id_, title, url, salary_from, salary_to, name_employer,
                                                           city, description, requirement, experience, date))
                else:
                    continue
            time.sleep(0.25)
        return self.__db_vacancies
