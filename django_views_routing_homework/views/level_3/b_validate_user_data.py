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
from json.decoder import JSONDecodeError

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.forms import ValidationError
from django.core.validators import validate_email as dj_validate_email

VALID_REGISTERED_FROM = ['website', 'mobile_app']


def validate_full_name(data: dict[str, str | int]) -> None:
    full_name = data.get('full_name')

    name_length = len(full_name)
    if  name_length < 5 or name_length > 256:
        raise ValidationError('Field "full_name" should have length >5 and <256')


def validate_registered_from(data: dict[str, str | int]) -> None:
    device = data.get('registered_from')

    if device not in VALID_REGISTERED_FROM:
        raise ValidationError('Wrong field "device"!')


def validate_age(data: dict[str, str | int]) -> None:
    age = data.get('age')

    if not age:
        return None
    
    try:
        age = int(age)
    except ValueError:
        raise ValidationError('field "age" not number!')
    
    if age < 1 or age > 160:
        raise ValidationError('field "age" should be >1 and < 160!')


def validate_no_exta_fields(data: dict[str, str | int]) -> None:
    data_to_check = data.copy()
    data_to_check.pop('full_name', None)
    data_to_check.pop('email', None)
    data_to_check.pop('registered_from', None)
    data_to_check.pop('age', None)
    if data_to_check:
        raise ValidationError('There are extra fields!')
    

def validate_required_fields(data: dict[str, str | int]) -> None:
    name = data.get('full_name')
    email = data.get('email')
    device = data.get('registered_from')
    if not all([name, email, device]):
        raise ValidationError('There are not all required fields!')


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({'error': 'Use json in body!'}, status=400)
        
        try:
            validate_no_exta_fields(data)
            validate_required_fields(data)
        except ValidationError as e:
            return JsonResponse({'error': list(e)}, status=400)
        
        try:
            validate_full_name(data)
            dj_validate_email(data.get('email'))
            validate_registered_from(data) 
            validate_age(data)
        except ValidationError as e:
            return JsonResponse({"is_valid": False})
        return JsonResponse({"is_valid": True})
    return JsonResponse({'error': 'Use METHOD POST!'})
