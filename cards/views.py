from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Card
from django.db.models import F

# Create your views here.

cards_dataset = [
    { "question": "Что такое PEP 8?",
    "answer": "PEP 8 — стандарт написания кода на Python.",
    "category": "Стандарты кода",
    "tags": ["PEP 8", "стиль", "форматирование"],
    "id_author": 1,
    "id_card": 1,
    "upload_date": "2023-01-15",
    "views_count": 100,
    "favorites_count": 25
    },
    { "question": "Как объявить список в Python?",
    "answer": "С помощью квадратных скобок: lst = []",
    "category": "Основы",
    "tags": ["списки", "основы"],
    "id_author": 2,
    "id_card": 2,
    "upload_date": "2023-01-20",
    "views_count": 150,
    "favorites_count": 30
    },
    { "question": "Что делает метод .append()?",
    "answer": "Добавляет элемент в конец списка.",
    "category": "Списки",
    "tags": ["списки", "методы"],
    "id_author": 2,
    "id_card": 3,
    "upload_date": "2023-02-05",
    "views_count": 75,
    "favorites_count": 20
    },
    { "question": "Какие типы данных в Python иммутабельные?",
    "answer": "Строки, числа, кортежи.",
    "category": "Типы данных",
    "tags": ["типы данных", "иммутабельность"],
    "id_author": 1,
    "id_card": 4,
    "upload_date": "2023-02-10",
    "views_count": 90,
    "favorites_count": 22
    },
    { "question": "Как создать виртуальное окружение в Python?",
    "answer": "С помощью команды: python -m venv myenv",
    "category": "Виртуальные окружения",
    "tags": ["venv", "окружение"],
    "id_author": 2,
    "id_card": 5,
    "upload_date": "2023-03-01",
    "views_count": 120,
    "favorites_count": 40
    }
]

info = {
    "users_count": 100500,
    "cards_count": 200600,
    # "menu": ['Главная', 'О проекте', 'Каталог']
    "menu": [
        {"title": "Главная",
        "url": "/",
        "url_name": "index"},
        {"title": "О проекте",
        "url": "/about/",
        "url_name": "about"},
        {"title": "Каталог",
        "url": "/cards/catalog/",
        "url_name": "catalog"},
    ],
    "cards": cards_dataset # Добавим в контекст шаблона информацию о карточках, чтобы все было в одном месте
}


def main(request):
    """Представление рендерит шаблон base.html"""
    return render(request, 'main.html', info)  # рендер главной странички

def about(request):
    """Представление рендерит шаблон about.html"""
    return render(request, 'about.html', info)  # рендер странички о нас

def catalog(request):
    
    sort = request.GET.get('sort', 'date')
    order = request.GET.get('order', 'desc')

    valid_sort_fields = {'date', 'views', 'adds'}
    if sort not in valid_sort_fields:
        sort = 'date'

    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    cards = Card.objects.all().order_by(order_by)
    
    context = {
        'cards': cards,
        'cards_count': cards.count(),
        'menu': info['menu'],
    }
    
    return render(request, 'cards/catalog.html', context)  # рендер странички каталога карточек

def get_card_by_id(request, card_id):
    return HttpResponse(f"Карточка {card_id}")  # вернет страничку с надписью "Карточка {card_id}" на русском языке.

def get_category_by_name(request, slug):
    return HttpResponse(f"Категория {slug}")  # вернет страничку с надписью "Категория {slug}" на русском языке.

def get_detail_card_by_id(request, card_id):
    """
    Возвращает детальную информацию по карточке для представления
    """
    # Ищем карточку по id в нашем наборе данных
    card = get_object_or_404(Card, pk=card_id)
    
    card.views = F('views') + 1
    card.save()

    card.refresh_from_db() 
    
    context = {
        'card': card,
        'menu': info['menu'],
    }

    return render(request, 'cards/card_detail.html', context)