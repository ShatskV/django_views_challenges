from django.http import HttpResponse, HttpResponseNotFound
from typing import Union

"""
Вьюха get_month_title_view возвращает название месяца по его номеру. 
Вся логика работы должна происходить в функции get_month_title_by_number.

Задания:
    1. Напишите логику получения названия месяца по его номеру в функции get_month_title_by_number
    2. Если месяца по номеру нет, то должен возвращаться ответ типа HttpResponseNotFound c любым сообщением об ошибке
    3. Добавьте путь в файле urls.py, чтобы при открытии http://127.0.0.1:8000/month-title/тут номер месяца/ 
       вызывалась вьюха get_month_title_view. Например http://127.0.0.1:8000/month-title/3/ 
"""


MONTH_NAMES = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь',
               'октябрь', 'ноябрь', 'декабрь']


def get_month_title_by_number(month_number: int) -> str | None:
    amount = len(MONTH_NAMES)
    if month_number < 1 or month_number > amount:
        return None
    return MONTH_NAMES[month_number - 1]


def get_month_title_view(request, month_number: int):
    month_name = get_month_title_by_number(month_number)
    if not month_name:
        return HttpResponseNotFound('Месяца с таким номером не существует')
    return HttpResponse(month_name)
