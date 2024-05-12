from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('signup/', views.SignUpUser, name='signup'),
    path('thanks/', views.ThanksForRegister.as_view(), name='thanks'),
]