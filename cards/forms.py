from django import forms
from .models import Category, Card, Tag

class CardModelForm(forms.ModelForm):
    question = forms.CharField(label='Вопрос', max_length=100)
    answer = forms.CharField(label='Ответ', widget=forms.Textarea)
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
    
    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()
        self.instance.tags.clear() 
        
        return instance