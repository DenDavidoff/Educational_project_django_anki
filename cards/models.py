from django.db import models

# Create your models here.

class Card(models.Model):
    id = models.AutoField(primary_key=True, db_column='CardID')
    question = models.CharField(max_length=255, db_column='Question')
    answer = models.TextField(max_length=5000, db_column='Answer')
    date = models.DateTimeField(auto_now_add=True, db_column='Date')
    views = models.IntegerField(default=0, db_column='Views')
    adds = models.IntegerField(default=0, db_column='Favorites')
    tags = models.ManyToManyField('Tag', through='CardTag', related_name='cards')

    class Meta:
        db_table = 'Cards' # имя таблицы в базе данных
        verbose_name = 'Карточка' # имя модели в единственном числе
        verbose_name_plural = 'Карточки' # имя модели во множественном числе

    def __str__(self):
        return f'Карточка {self.question} - {self.answer[:50]}'
    
class Tag(models.Model):
    id = models.AutoField(primary_key=True, db_column='TagID')
    name = models.CharField(max_length=75, db_column='Name')

    class Meta:
        db_table = 'Tags'
        verbose_name = 'Тег'  # имя модели в единственном числе
        verbose_name_plural = 'Теги'  # имя модели во множественном числе

    def __str__(self):
        return f'Тег {self.name}'

class CardTag(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, db_column='CardID')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='TagID')
    
    class Meta:
        db_table = 'CardTags'
        verbose_name = 'Тег карточки'  # имя модели в единственном числе
        verbose_name_plural = 'Теги карточек'  # имя модели во множественном числе
        
        unique_together = ('card', 'tag')

    def __str__(self):
        return f'Тег {self.tag.name} к карточке {self.card.question}'
    
    
class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='CategoryID')
    name = models.CharField(max_length=120, db_column='Name')

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Категория'  # имя модели в единственном числе
        verbose_name_plural = 'Категории'  # имя модели во множественном числе

    def __str__(self):
        return f'Категория {self.name}'