"""
В этом задании вам нужно научиться генерировать текст заданной длинны и возвращать его в ответе в виде файла.

- ручка должна получать длину генерируемого текста из get-параметра length;
- дальше вы должны сгенерировать случайный текст заданной длины. Это можно сделать и руками
  и с помощью сторонних библиотек, например, faker или lorem;
- дальше вы должны вернуть этот текст, но не в ответе, а в виде файла;
- если параметр length не указан или слишком большой, верните пустой ответ со статусом 403

Вот пример ручки, которая возвращает csv-файл: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
С текстовым всё похоже.

Для проверки используйте браузер: когда ручка правильно работает, при попытке зайти на неё, браузер должен
скачивать сгенерированный файл.
"""

from random import choice
from string import ascii_letters, digits
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest

MAX_LENGTH = 1000


def generate_text(length):
    text = (''.join(choice(ascii_letters + digits + ' \n') for _ in range(length)))
    return text


def validate_length(length):
    try:
        length = int(length) if length is not None else None
    except ValueError:
        raise ValidationError('Field "length" is not number!')
    except TypeError:
        raise ValidationError('Field "length" is missed!')
    if length < 1 or length > MAX_LENGTH:
        raise ValidationError(f'Field "length" should be >= 1 and <= {MAX_LENGTH}!')


def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        length = request.GET.get('length')

        try:
            validate_length(length)
        except ValidationError as e:
            return HttpResponseForbidden(e)
        
        
        text = generate_text(int(length))
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=text.txt'
        response.write(text)
        return response
    return HttpResponseBadRequest('Use METHOD GET!')
