from django.contrib import admin
from .models import Card, Category, Tag, CardTag

# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'category', 'views', 'date', 'check_status')
    list_filter = ('check_status',)
    list_per_page = 25
    list_editable = ('check_status',)
    actions = ['make_checked', 'make_unchecked']

    @admin.action(description='Отметить выбранные карточки как проверенные')
    def make_checked(self, request, queryset):
        updated_count = queryset.update(check_status=True)
        self.message_user(request, f"{updated_count} записей было помечено как проверенное")
        
    @admin.action(description='Отметить выбранные карточки как непроверенные')
    def make_unchecked(self, request, queryset):
        updated_count = queryset.update(check_status=False)
        self.message_user(request, f"{updated_count} записей было помечено как непроверенное", 'warning')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(CardTag)
class CategoryAdmin(admin.ModelAdmin):
    pass