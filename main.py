from scr.hh_parser import HeadHunterAPI
from scr.superjob_parser import SuperJobAPI
from utils.db_operation import CSVSaver


def user_interaction():
    """
    Функция для взаимодействия с пользователем, запрашивающая следующие данные:
    1) Интересующая должность, 2) Поиск в названии или в ключевых словах: 1 — только в названии, 2 — по всей вакансии,
    3) Поиск с указанием дохода: 1 — да, 2 — нет, если да, то программа предложит ввести желаемую сумму, 4) Поиск
    по конкретному городу: 1 — да, 2 — нет, если да, то программа предложит ввести желаемый город, 5) Поиск по опыту
    работу: 1 — да, 2 — нет, если да, то программа предложит выбрать из четырех возможных вариантов, 6) Сортировать
    ли вакансии по дате публикации: 1 — да, 2 — нет.
    """
    user_search_request = input("Введите интересующую должность для поиска вакансий: ").lower()
    if not user_search_request.isalpha():
        user_search_request = input("Введите существующую должность: ").title()

    print('Искать только в названии вакансии?')
    print('----------------------------------\n1. Да\n2. Нет')
    user_answer_keywords = input("Введите выбранный пункт: ")
    if not user_answer_keywords.isdigit():
        user_answer_keywords = input("Повторно введите выбранный пункт, который должен быть числом: ")
    if int(user_answer_keywords) not in (1, 2):
        user_answer_keywords = input("Повторно введите выбранный пункт [1 или 2]: ")

    print('Искать вакансии с указанием уровня дохода?')
    print('------------------------------------------\n1. Да\n2. Нет')
    user_answer_salary = input("Введите выбранный пункт: ")
    if not user_answer_salary.isdigit():
        user_answer_salary = input("Повторно введите выбранный пункт, который должен быть числом: ")
    if int(user_answer_salary) not in (1, 2):
        user_answer_salary = input("Повторно введите выбранный пункт [1 или 2]: ")
    if user_answer_salary == '1':
        user_answer_salary_amount = input('Введите сумму, в диапазоне которой хотите отфильтровать вакансии: ')
        if not user_answer_salary_amount.isdigit():
            user_answer_salary_amount = input("Повторно введите выбранный пункт, который должен быть числом: ")
    else:
        user_answer_salary_amount = None
    if user_answer_salary_amount:
        user_answer_salary_amount = int(user_answer_salary_amount)

    print('Искать вакансии в конкретном городе?')
    print('------------------------------------\n1. Да\n2. Нет')
    user_answer_city = input("Введите выбранный пункт: ")
    if not user_answer_city.isdigit():
        user_answer_city = input("Повторно введите выбранный пункт, который должен быть числом: ")
    if int(user_answer_city) not in (1, 2):
        user_answer_city = input("Повторно введите выбранный пункт [1 или 2]: ")
    if user_answer_city == '1':
        user_answer_current_city = input('Введите конкретный город для фильтрации: ').title()
        if user_answer_current_city.isdigit():
            user_answer_current_city = input("Введите существующий город в России на русском языке: ")
    else:
        user_answer_current_city = None

    print('Фильтровать вакансии по опыту работы?')
    print('--------------------------------\n1. Да\n2. Нет')
    user_answer_experience = input("Введите выбранный пункт: ")
    if not user_answer_experience.isdigit():
        user_answer_experience = input("Повторно введите выбранный пункт, который должен быть числом: ")
    if int(user_answer_experience) not in (1, 2):
        user_answer_experience = input("Повторно введите выбранный пункт [1, 2]: ")
    if user_answer_experience == '1':
        print('Выберете релевантный опыт работы')
        print('--------------------------------\n1. Нет опыта\n2. От 1 года до 3 лет\n3. От 3 до 6 лет\n4. Более 6 лет')
        user_answer_current_experience = input("Введите выбранный пункт: ")
        if not user_answer_current_experience.isdigit():
            user_answer_current_experience = input("Повторно введите выбранный пункт [1, 2, 3, 4]: ")
        if int(user_answer_current_experience) not in (1, 2, 3, 4):
            user_answer_current_experience = input("Повторно введите выбранный пункт [1, 2, 3, 4]: ")
    else:
        user_answer_current_experience = None

    user_vacancy_amount = input("Введите количество вакансий для вывода в топ N: ")
    if not user_vacancy_amount.isdigit():
        user_vacancy_amount = input("N должен быть числом. Повторите ввод: ")

    print('Сортировать вакансии по дате публикации?')
    print('----------------------------------------\n1. Да\n2. Нет')
    user_answer_data = input("Введите выбранный пункт: ")
    if not user_answer_data.isdigit():
        user_answer_data = input("Повторно введите выбранный пункт, который должен быть числом: ")
    if int(user_answer_data) not in (1, 2):
        user_answer_data = input("Повторно введите выбранный пункт [1 или 2]: ")

    experience_data = {'1': 'Нет опыта', '2': 'От 1 года до 3 лет', '3': 'От 3 до 6 лет', '4': 'Более 6 лет'}
    salary_data = {'1': user_answer_salary_amount, '2': None}
    city_data = {'1': user_answer_current_city, '2': None}
    sorting_by_date = {'1': True, '2': None}

    top_vacancies = int(user_vacancy_amount)

    hh_api = HeadHunterAPI()
    super_job_api = SuperJobAPI()
    hh_vacancies = hh_api.get_vacancies(user_search_request)
    super_job_vacancies = super_job_api.get_vacancies(user_search_request)
    saver = CSVSaver()
    for hh_vac in hh_vacancies:
        saver.add_vacancy(hh_vac)
    for sp_vac in super_job_vacancies:
        saver.add_vacancy(sp_vac)

    if user_answer_keywords == '1':
        if user_answer_experience == '1':
            return saver.get_vacancy_by_keyword_in_title(keyword=user_search_request.lower(),
                                                         salary=salary_data.get(user_answer_salary),
                                                         experience=experience_data.get(user_answer_current_experience),
                                                         city=city_data.get(user_answer_city),
                                                         date=sorting_by_date.get(user_answer_data)
                                                         )[:top_vacancies]
        elif user_answer_experience == '2':
            return saver.get_vacancy_by_keyword_in_title(keyword=user_search_request.lower(),
                                                         salary=salary_data.get(user_answer_salary),
                                                         experience=None,
                                                         city=city_data.get(user_answer_city),
                                                         date=sorting_by_date.get(user_answer_data)
                                                         )[:top_vacancies]
    else:
        if user_answer_experience == '1':
            return saver.get_vacancy_by_filtered_words_not_in_title(salary=salary_data.get(user_answer_salary),
                                                                    experience=experience_data.get(
                                                                        user_answer_current_experience),
                                                                    city=city_data.get(user_answer_city),
                                                                    date=sorting_by_date.get(user_answer_data)
                                                                    )[:top_vacancies]
        elif user_answer_experience == '2':
            return saver.get_vacancy_by_filtered_words_not_in_title(salary=salary_data.get(user_answer_salary),
                                                                    experience=None,
                                                                    city=city_data.get(user_answer_city),
                                                                    date=sorting_by_date.get(user_answer_data)
                                                                    )[:top_vacancies]


# Вывод отфильтрованных вакансий в консоль
vacancies = user_interaction()
if not vacancies:
    print("Нет вакансий, соответствующих заданным критериям.")
else:
    for vacancy in vacancies:
        for key in vacancy:
            print(key, '—', vacancy[key])
        print()