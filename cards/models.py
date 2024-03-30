from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=75, unique=True)

    class Meta:
        verbose_name = 'Тег'  # имя модели в единственном числе
        verbose_name_plural = 'Теги'  # имя модели во множественном числе

    def __str__(self):
        return f'Тег {self.name}'

class Card(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    adds = models.IntegerField(default=0)
    tags = models.JSONField(default=list)

    class Meta:
        db_table = 'Cards' # имя таблицы в базе данных
        verbose_name = 'Карточка' # имя модели в единственном числе
        verbose_name_plural = 'Карточки' # имя модели во множественном числе

    def __str__(self):
        return f'Карточка {self.question} - {self.answer[:50]}'

"""
### CRUD Операции с этой моделью
1. Создание записи
card = Card(question='Пайтон или Питон?!', answer='Пайтон')
card.save()

2. Чтение записи
card = Card.objects.get(pk=1)
Мы можем добыть любые данные из записи, просто обратившись к атрибутам модели:
card.question
card.answer
card.upload_date

3. Обновление записи
card = Card.objects.get(pk=1)
card.question = 'Питон или Пайтон?!!'

4. Удаление записи
card = Card.objects.get(pk=1)
card.delete()
"""