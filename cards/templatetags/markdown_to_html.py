from django import template
import markdown
from django.utils.safestring import mark_safe


# в Django это регистрация библиотеки шаблонов, которая позволяет использовать пользовательские теги 
# и фильтры в шаблонах Django.
register = template.Library()

# @register это декоратор, который используется в Django для создания простых пользовательских тегов шаблонов.
# simple_tag - это декоратор, который используется для создания простых пользовательских тегов шаблонов.
@register.simple_tag(name='markdown_to_html')
def markdown_to_html(markdown_text: str) -> str:
    
    md_extensions = ['extra', 'fenced_code', 'tables']
    
    html_content = markdown.markdown(markdown_text, extensions=md_extensions)
    
    return mark_safe(html_content)