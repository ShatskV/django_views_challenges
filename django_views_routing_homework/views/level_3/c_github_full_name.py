"""
В этом задании вам нужно реализовать ручку, которая принимает на вход ник пользователя на Github,
а возвращает полное имя этого пользователя.

- имя пользователя вы узнаёте из урла
- используя АПИ Гитхаба, получите информацию об этом пользователе (это можно сделать тут: https://api.github.com/users/USERNAME)
- из ответа Гитхаба извлеките имя и верните его в теле ответа: `{"name": "Ilya Lebedev"}`
- если пользователя на Гитхабе нет, верните ответ с пустым телом и статусом 404
- если пользователь на Гитхабе есть, но имя у него не указано, верните None вместо имени
"""

import requests
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound


def fetch_name_from_github_view(request: HttpRequest, github_username: str) -> HttpResponse:
    url = f'https://api.github.com/users/{github_username}'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.ConnectionError as e:
        return HttpResponseBadRequest('Github connection error')
    except requests.HTTPError as e:
        if response.status_code == 404:
            return HttpResponseNotFound('')
        return HttpResponseBadRequest(f'HTTP error: {e}')
    answer = response.json()
    return HttpResponse(f'{{"name": {str(answer.get("name"))}}}')   
