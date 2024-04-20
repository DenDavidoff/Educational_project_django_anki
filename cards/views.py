from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F, Q
from django.core.paginator import Paginator

from .models import Card

from .forms import CardModelForm

# Create your views here.


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
        {"title": "Добавить",
        "url": "/add/",
        "url_name": "add_card"},
    ], # Добавим в контекст шаблона информацию о карточках, чтобы все было в одном месте
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
    search_query = request.GET.get('search_query', '')
    page_number = request.GET.get('page', 1)
    
    valid_sort_fields = {'date', 'views', 'adds'}
    if sort not in valid_sort_fields:
        sort = 'date'

    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'


    if not search_query:
        cards = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)

    else:
        cards = Card.objects.filter(Q(question__icontains=search_query) | Q(answer__icontains=search_query) | Q(tags__name__icontains=search_query)).select_related('category').prefetch_related('tags').order_by(order_by).distinct()

    paginator = Paginator(cards, 25)

    page_obj = paginator.get_page(page_number)
    
    context = {
        'cards': cards,
        'cards_count': len(cards),
        'menu': info['menu'],
        'page_obj': page_obj,
        "sort": sort,
        "order": order,
    }
    
    response = render(request, 'cards/catalog.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # - кэш не используется
    response['Expires'] = '0'
    return response

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

def get_cards_by_tag(request, tag_id):
    
    cards = Card.objects.filter(tags__id=tag_id)
    
    context = {
        'cards': cards,
        'menu': info['menu'],
    }
    
    return render(request, 'cards/catalog.html', context)

def add_card(request):
    if request.method == 'POST':
        form = CardModelForm(request.POST)
        if form.is_valid():  
            card = form.save()
            # Редирект на страницу созданной карточки после успешного сохранения
            return redirect(card.get_absolute_url())
            
    else:
        form = CardModelForm()

    return render(request, 'cards/add_card.html', {'form': form, 'menu': info['menu']})