# Проект — parser vacancies

Parser vacancies — это проект, который с помощью API обращается к серверам HeadHunters и SuperJob, получает
вакансии по желаемой должности и записывает их в csv-файл. Данный скрипт включает в себя взаимодействие с пользователем,
от которого мы получаем желаемую должность, также в зависимости от выбора пользователя все полученные вакансии возможно
отфильтровать по зарплатным ожиданиям, по месторасположению работодателя, по опыту работы и отсортировать по дате 
публикации. Отфильтрованные вакансии выводятся в терминал. </br>
В коде используются библиотеки: `time`, `requests`, `datetime`, `os`, `re`, `csv`.

# Дополнительная информация

- Формат предоставления результатов: </br>
  - <Идентификатор> — <*значение*> </br>
  - <Название вакансии> — <*значение*> </br>
  - <Ссылка> — <*значение*> </br>
  - <Зарплата_от> — <*значение*> </br>
  - <Зарплата_до> — <*значение*> </br>
  - <Имя_нанимателя> — <*значение*> </br>
  - <Город> — <*значение*> </br>
  - <Описание_вакансии> — <*значение*> </br>
  - <Требование> — <*значение*> </br>
  - <Опыт> — <*значение*> </br>
  - <Дата_публикации> — <*значение*> </br>
- Файл с полученными от API вакансиями находится в директории:
   - `parser_vacancies/db_vacancies.csv` </br>
- Для просмотра покрытия кода тестами введите в консоли:
   ```
    cd tests
    pytest --cov --cov-report term-missing
    ```

# Клонирование репозитория

В проекте для управления зависимостями используется [poetry](https://python-poetry.org/). </br>
Выполните в консоли: </br>

Для Windows: </br>
```
git clone git@github.com:DmitriiParfenov/parser_vacancies.git
python -m venv venv
venv\Scripts\activate
pip install poetry
poetry install
poetry run python main.py
```

Для Linux: </br>
```
git clone git@github.com:DmitriiParfenov/parser_vacancies.git
cd parser_vacancies
python3 -m venv venv
source venv/bin/activate
curl -sSL https://install.python-poetry.org | python3
poetry install
poetry run python3 main.py
```

# Получение ключей API

- Получите ключ API для поиска вакансий на сайте [dev.hh.ru](https://dev.hh.ru/admin).
- Установите ключ API в переменную окружения: `HH_API_KEY`.
- Получите ключ API для поиска вакансий на сайте [api.superjob.ru](https://api.superjob.ru/).
- Установите ключ API в переменную окружения: `SUPERJOB_API_KEY`.

# Запуск
- Зайдите в директорию `parser_vacancies/main.py` и запустите скрипт.
- Следуйте инструкциям, которые выводятся в терминале.
- Все найденные вакансии будут сохранены в `parser_vacancies/db_vacancies.csv`, а отфильтрованные согласно вашему выбору будут выведены в терминале.