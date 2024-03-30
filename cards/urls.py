from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:card_id>/', views.get_card_by_id, name='card_detail'),
    path('catalog/<slug:slug>/', views.get_category_by_name, name='card_category'),
    path('catalog/<int:card_id>/detail/', views.get_detail_card_by_id, name='detail_card_by_id'),
]