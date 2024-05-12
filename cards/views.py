from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F, Q
from django.core.paginator import Paginator
from django.core.cache import cache
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Card

from .forms import CardModelForm

# Create your views here.


info = {
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
    ],
}


class MenuMixin:
    """
    Класс-миксин для добавления меню в контекст шаблона
    Добывает и кеширует cards_count, users_count, menu
    """
    timeout = 30

    # Метод, добывающий меню из контекста
    def get_menu(self):
        menu = cache.get('menu')
        if not menu:
            menu = info['menu']
            cache.set('menu', menu, timeout=self.timeout)

        return menu
    
    # Метод, добывающий информацию по количеству карточек в базе
    def get_cards_count(self):
        cards_count = cache.get('cards_count')
        if not cards_count:
            cards_count = Card.objects.count()
            cache.set('cards_count', cards_count, timeout=self.timeout)

        return cards_count
    
    # Метод, добывающий информацию по количеству пользователей в базе
    def get_users_count(self):
        users_count = cache.get('users_count')
        if not users_count:
            users_count = get_user_model().objects.count()
            cache.set('users_count', users_count, timeout=self.timeout)

        return users_count

    # Метод, который использует два предыдущих метода и собирает их в контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.get_menu()
        context['cards_count'] = self.get_cards_count()
        context['users_count'] = self.get_users_count()
        return context


class AboutView(MenuMixin, TemplateView):
    """
    Класс вьюшки для страницы "О нас"
    """
    template_name = 'about.html'


class IndexView(MenuMixin, TemplateView):
    """
    Класс вьюшки для страницы "Главная"
    """
    template_name = 'main.html'


class CatalogView(MenuMixin, ListView):
    """
    Класс вьюшки для страницы "Каталог"
    Использует методы получения параметров сортировки и добавления дополнительного контекста
    """
    model = Card
    template_name = 'cards/catalog.html'
    context_object_name = 'cards'
    paginate_by = 25

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        sort = self.request.GET.get('sort', 'date')
        order = self.request.GET.get('order', 'desc')
        search_query = self.request.GET.get('search_query', '')

        if order == 'asc':
            order_by = sort
        else:
            order_by = f'-{sort}'

        if search_query:
            queryset = Card.objects.filter(
                Q(question__iregex=search_query) |
                Q(answer__iregex=search_query) |
                Q(tags__name__iregex=search_query)
            ).select_related('category').prefetch_related('tags').order_by(order_by).distinct()
        else:
            queryset = Card.objects.select_related('category').prefetch_related('tags').order_by(order_by)
        return queryset

    # Метод для добавления дополнительного контекста
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort', 'date')
        context['order'] = self.request.GET.get('order', 'desc')
        context['search_query'] = self.request.GET.get('search_query', '')
        return context


def get_card_by_id(request, card_id):
    
    return HttpResponse(f"Карточка {card_id}")  # вернет страничку с надписью "Карточка {card_id}" на русском языке.

def get_category_by_name(request, slug):
    
    return HttpResponse(f"Категория {slug}")  # вернет страничку с надписью "Категория {slug}" на русском языке.


class CardDetailView(MenuMixin, DetailView):
    """
    Класс вьюшки для страницы "Детальная информация о карточке"
    Использует методы обновления счётчиков просмотров
    """
    model = Card
    template_name = 'cards/card_detail.html'
    context_object_name = 'card'

    # Метод для обновления счетчика просмотров при каждом отображении детальной страницы карточки
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        Card.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj


def get_cards_by_tag(request, tag_id):
    
    cards = Card.objects.filter(tags__id=tag_id)
    
    context = {
        'cards': cards,
        'menu': info['menu'],
    }
    
    return render(request, 'cards/catalog.html', context)


class AddCardCreateView(MenuMixin, LoginRequiredMixin, CreateView):
    """
    Класс вьюшки для страницы "Добавление новой карточки"
    """
    model = Card
    form_class = CardModelForm
    template_name = 'cards/add_card.html'
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного создания карточки
    redirect_field_name = 'next'
    
    def form_valid(self, form):
        # Добавляем автора к карточке перед сохранением
        form.instance.author = self.request.user
        # Логика обработки данных формы перед сохранением объекта
        return super().form_valid(form)
    

class EditCardUpdateView(MenuMixin, LoginRequiredMixin, UpdateView):
    model = Card  # Указываем модель, с которой работает представление
    form_class = CardModelForm  # Указываем класс формы для редактирования карточки
    template_name = 'cards/add_card.html'  # Указываем шаблон, который будет использоваться для отображения формы
    context_object_name = 'card'  # Имя переменной контекста для карточки
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного редактирования карточки