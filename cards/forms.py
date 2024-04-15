from django import forms
from .models import Category, Card, Tag

class CardModelForm(forms.ModelForm):
    question = forms.CharField(label='Вопрос', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    answer = forms.CharField(label='Ответ', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label='Категория', widget=forms.Select(attrs={'class': 'form-control'}))
    tags = forms.CharField(label='Теги', required=False, help_text='Перечислите теги через запятую', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Card
        fields = ['question', 'answer', 'category', 'tags']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40}),
        }
        
        labels = {
            'question': 'Вопрос',
            'answer': 'Ответ',
        }
    
    def clean_tags(self):
        tags_str = self.cleaned_data['tags'].lower()
        tag_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return tag_list
    
    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()
        
        for tag_name in self.cleaned_data['tags']:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)
        
        # self.instance.tags.clear() 
        # Закоментил, чтобы теги сохранялись
        
        return instance