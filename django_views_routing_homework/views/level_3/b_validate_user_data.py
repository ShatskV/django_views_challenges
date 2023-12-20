"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

- получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
- если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
- если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
- если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
- есть поле full_name, в нём хранится строка от 5 до 256 символов
- есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
- поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
- других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""
import json

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest

VALID_REGISTERED_FROM = ['website', 'mobile_app']


def check_full_name(full_name: str) -> bool:
    name_length = len(full_name)
    if name_length < 5 or name_length > 256:
        return False
    return True


def check_email(email: str) -> bool:
    if '@' in email and '.' in email:
        return True
    return False


def check_registered_from(device: str) -> bool:
    if device in VALID_REGISTERED_FROM:
        return True
    return False


def check_age(age: str | int) -> bool:
    try:
        age = int(age)
    except ValueError:
        return False
    if age < 1 or age > 160:
        return False
    return True


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.pop('full_name', None)
        email = data.pop('email', None)
        device = data.pop('registered_from', None)
        age = data.pop('age', None)
        if data:
            return HttpResponseBadRequest('There are extra fields!')
        if not all([name, email, device]):
            return HttpResponseBadRequest('There are not all required fields!')
        if not all([check_full_name(name), check_email(email), check_registered_from(device), 
                    check_age(age) if age else 1]):
            return HttpResponse('{"is_valid": false}')
        else:
            return HttpResponse('{"is_valid": true}')
    return HttpResponseBadRequest('Use METHOD POST!')
