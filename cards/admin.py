from django.contrib import admin
from .models import Card, Category, Tag

# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass