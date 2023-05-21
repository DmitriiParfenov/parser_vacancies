import json
import os
import time
from datetime import datetime as dt

import requests

from utils.class_operations import Vacancy, Parser


class SuperJobAPI(Parser):
    """Класс для работы с API SuperJob."""
    def __init__(self):
        """Экземпляр инициализируется url, api-key, header и params для создания запроса на сервер SuperJob.
        В ответ на запрос искомые вакансии в виде экземпляров класса Vacancy будут храниться в db_vacancies."""

        self.__sj_apikey = os.getenv('SUPERJOB_API_KEY')
        self.__url = 'https://api.superjob.ru/2.0/vacancies/'
        self.__header = {'X-Api-App-Id': self.__sj_apikey}
        self.__param = {}
        self.__db_vacancies = []

    def get_vacancies(self, title_vacancy):
        """Метод в качестве аргумента принимает название вакансии в виде строки и делает запрос на сервер SuperJob.
        Вакансии, соответствующие названию, добавляются в db_vacancies. Максимальное количество вакансий в одном
        запросе составляет 500."""
        for i in range(0, 5):
            self.__param = {
                'keyword': title_vacancy,
                'count': 100,
                'not_archive': True,
                'page': i,
            }
            request = requests.get(self.__url, headers=self.__header, params=self.__param)
            if request.ok:
                response = request.content.decode()
                request.close()
                data = json.loads(response)
                if data['objects']:
                    for item in data['objects']:
                        id_ = item.get('id')
                        title = item.get('profession')
                        url = item.get('link').strip('\n')
                        if not item.get('payment_from'):
                            salary_from = None
                        else:
                            salary_from = item.get('payment_from')
                        if not item.get('payment_to'):
                            salary_to = None
                        else:
                            salary_to = item.get('payment_to')
                        name_employer = item.get('firm_name')
                        city = item.get('town').get('title')
                        description = item.get('client').get('description')
                        requirement = item.get('candidat')
                        if item.get('experience').get('title') in ('Не имеет значения', 'Без опыта'):
                            experience = 'Нет опыта'
                        elif item.get('experience').get('title') == 'От 1 года':
                            experience = 'От 1 года до 3 лет'
                        elif item.get('experience').get('title') == 'От 3 лет':
                            experience = 'От 3 до 6 лет'
                        else:
                            experience = 'Более 6 лет'
                        if item.get('date_published'):
                            date = dt.fromtimestamp(item['date_published'])
                        else:
                            date = None
                        self.__db_vacancies.append(Vacancy(id_, title, url, salary_from, salary_to, name_employer,
                                                           city, description, requirement, experience, date))
            time.sleep(0.25)
        return self.__db_vacancies

