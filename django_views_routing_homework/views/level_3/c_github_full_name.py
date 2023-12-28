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
from django.http import HttpRequest, JsonResponse


def fetch_name_from_github_view(request: HttpRequest, github_username: str) -> JsonResponse:
    url = f'https://api.github.com/users/{github_username}'
    try:
        response = requests.get(url)
    except requests.ConnectionError as e:
        return JsonResponse({'error': 'github connection error'}, status=502)
    
    if response.status_code == 404:
            return JsonResponse({'error': 'username not found'}, status=404)
    
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        return JsonResponse({'error': f'HTTP error: {e}'}, status=response.status_code)
    
    answer = response.json()
    return JsonResponse({"name": answer.get("name")})
