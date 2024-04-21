from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('catalog/<int:card_id>/', views.get_card_by_id, name='card_detail'),
    path('catalog/<slug:slug>/', views.get_category_by_name, name='card_category'),
    path('catalog/<int:pk>/detail/', views.CardDetailView.as_view(), name='detail_card_by_id'),
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='cards_by_tag'),
    path('add/', views.AddCardCreateView.as_view(), name='add_card'),
]