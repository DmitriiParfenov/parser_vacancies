import datetime
from abc import ABC, abstractmethod


class Parser(ABC):
    """Абстрактный класс для работы с API сервераов с вакансиями."""

    @abstractmethod
    def get_vacancies(self, title_vacancy):
        """Абстрактный метод, который должен быть переопределен в дочерных классах родительского класса Parser."""
        pass


class Vacancy:
    """Класс для представления вакансий."""

    def __init__(self, vacancy_id: int, title: str, url: str, salary_from: int | None, salary_to: int | None,
                 name_employer: str | None, city: str | None, description: str | None, requirement: str | None,
                 experience: str | None, date: datetime.datetime):
        """
        Экземпляр инициализируется id, title, url, salary_from, salary_to, name_employer, city, description,
        requirement, experience и date для хранения информации об вакансии. При инициализации экземпляров
        класса Vacancy происходит валидация данных при помощи метода validate date.
        """

        self.__validate_data(vacancy_id, title, url, salary_from, salary_to, name_employer,
                             city, description, requirement, experience, date)
        self.__id = vacancy_id
        self.title = title
        self.__url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.name_employer = name_employer
        self.city = city
        self.description = description
        self.requirement = requirement
        self.experience = experience
        self.date = date

    @staticmethod
    def __validate_data(vacancy_id: int, title: str, url: str, salary_from: int | None, salary_to: int | None,
                        name_employer: str | None, city: str | None, description: str | None, requirement: str | None,
                        experience: str | None, date: datetime.datetime) -> None:
        """Метод проверяет корректность входных данных при инициализации экземпляров класса Vacancy."""

        if not isinstance(vacancy_id, int):
            raise TypeError('id вакансии должен быть целым числом')
        if not isinstance(title, str):
            raise TypeError('Название вакансии должно быть строкой')
        if not isinstance(url, str):
            raise TypeError('Ссылка на вакансию должна быть строкой')
        if not url.startswith('http'):
            raise TypeError('Ссылка на вакансию должна быть в виде существующей ссылки на нее')
        if not isinstance(salary_from, int | None):
            raise TypeError('Зарплата должна быть целым числом или None')
        if not isinstance(salary_to, int | None):
            raise TypeError('Зарплата должна быть целым числом или None')
        if not isinstance(name_employer, str | None):
            raise TypeError('Имя нанимателя должно быть строкой или None')
        if not isinstance(city, str | None):
            raise TypeError('Город должен быть строкой или None')
        if not isinstance(description, str | None):
            raise TypeError('Описание вакансии должно быть строкой или None')
        if not isinstance(requirement, str | None):
            raise TypeError('Обязанности должны быть строкой или None')
        if not isinstance(experience, str | None):
            raise TypeError('Опыт должен быть строкой или None')
        if not isinstance(date, datetime.datetime):
            raise TypeError('Дата публикация должна быть преобразована в <datetime.datetime>')

    @property
    def id(self):
        """Getter возвращает идентификатор вакансии."""
        return self.__id

    @property
    def url(self):
        """Getter возвращает ссылку на вакансию."""
        return self.__url

    def __str__(self):
        """Возвращает строку с атрибутами экземпляров в дружественном формате."""
        result = ''
        for elem in self.__dict__:
            if elem == '_Vacancy__id':
                result += f'Идентификатор вакансии — {self.__dict__[elem]}\n'
            elif elem == '_Vacancy__url':
                result += f'Ссылка на вакансию — {self.__dict__[elem]}\n'
            else:
                result += f'{elem} — {self.__dict__[elem]}\n'
        return result

    def __repr__(self):
        """Возвращает строку с названием классов и атрибутами при инициализации экземпляров класса."""
        return f"{self.__class__.__name__}({self.id}, '{self.title}', '{self.url}', {self.salary_from}, " \
               f"{self.salary_to}, '{self.name_employer}', '{self.city}', '{self.description}', '{self.requirement}'," \
               f"'{self.experience}', {self.date})"

    def __eq__(self, other):
        """
        Метод проверяет, равны ли экземпляры классов Vacancy между собой по среднему значению атрибутов <salary_from>
        и <salary_to>.
        """
        if not issubclass(other.__class__, self.__class__):
            raise ValueError('Должны сравниваться объекты унаследованных классов')
        if not self.salary_from:
            self.salary_from = 0
        if not self.salary_to:
            self.salary_to = 0
        if not other.salary_from:
            other.salary_from = 0
        if not other.salary_to:
            other.salary_to = 0
        average_salary_1 = (self.salary_from + self.salary_to) // 2
        average_salary_2 = (other.salary_to + other.salary_from) // 2
        return average_salary_2 == average_salary_1

    def __gt__(self, other):
        """
        Метод проверяет, больше ли экземпляр класса Vacancy, находящийся слева в аргументах функции, чем экземпляр
        класса Vacancy, находящийся справа, по среднему значению атрибутов <salary_from> и <salary_to>.
        """
        if not issubclass(other.__class__, self.__class__):
            raise ValueError('Должны сравниваться объекты унаследованных классов')
        if not self.salary_from:
            self.salary_from = 0
        if not self.salary_to:
            self.salary_to = 0
        if not other.salary_from:
            other.salary_from = 0
        if not other.salary_to:
            other.salary_to = 0
        average_salary_1 = (self.salary_from + self.salary_to) // 2
        average_salary_2 = (other.salary_to + other.salary_from) // 2
        return average_salary_1 > average_salary_2

    def __ge__(self, other):
        """
        Метод проверяет, больше или равен экземпляр класса Vacancy, находящийся слева в аргументах функции, чем
        экземпляр класса Vacancy, находящийся справа, по среднему значению атрибутов <salary_from> и <salary_to>.
        """
        if not issubclass(other.__class__, self.__class__):
            raise ValueError('Должны сравниваться объекты унаследованных классов')
        if not self.salary_from:
            self.salary_from = 0
        if not self.salary_to:
            self.salary_to = 0
        if not other.salary_from:
            other.salary_from = 0
        if not other.salary_to:
            other.salary_to = 0
        average_salary_1 = (self.salary_from + self.salary_to) // 2
        average_salary_2 = (other.salary_to + other.salary_from) // 2
        return average_salary_1 >= average_salary_2