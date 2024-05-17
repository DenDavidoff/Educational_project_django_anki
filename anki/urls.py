"""
URL configuration for anki project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from anki import settings
from cards import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cards/', include('cards.urls')),
    # path('', views.main, name='index'),
    # path('about/', views.about, name='about'),
    path('', cache_page(60*15)(views.IndexView.as_view()), name='index'),
    path('about/', cache_page(60*15)(views.AboutView.as_view()), name='about'),
    path('users/', include('users.urls', namespace='users')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                      # другие URL-паттерны
                  ] + urlpatterns
    
    # Добавляем обработку медиафайлов
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)