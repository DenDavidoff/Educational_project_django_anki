from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Card, Category, Tag, CardTag



class CheckStatusFilter(SimpleListFilter):
    title = 'проведена ли проверка'  # Название фильтра, отображаемое в админ-панели
    parameter_name = 'check_status'  # Параметр в URL

    def lookups(self, request, model_admin):
        # Варианты, которые будут отображаться в интерфейсе админ-панели
        return (
            ('make_checked', 'Проверено'),
            ('make_unchecked', 'Не проверено'),
        )

    def queryset(self, request, queryset):
        # Модификация queryset в зависимости от выбранного значения фильтра
        if self.value() == 'make_checked':
            return queryset.filter(check_status=True)
        if self.value() == 'make_unchecked':
            return queryset.exclude(check_status=True)

# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'category', 'views', 'date', 'check_status')
    list_filter = (CheckStatusFilter,)
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