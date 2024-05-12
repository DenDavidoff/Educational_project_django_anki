from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import logout
from .forms import LoginUserForm, RegisterUserForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from cards.views import MenuMixin
from django.views.generic import TemplateView

# Create your views here.

class LoginUser(MenuMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.POST.get('next', '').strip():
            return self.request.POST.get('next')
        return reverse_lazy('catalog')

class LogoutUser(LogoutView):
    next_page = reverse_lazy('users:login')


def SignUpUser(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Устанавливаем пароль
            user.save()
            return redirect(reverse('users:thanks')) # После успешной регистрации перенаправляем на страницу авторизации
    else:
        form = RegisterUserForm()  # Пустая форма для GET-запроса
    return render(request, 'users/register.html', {'form': form})


class ThanksForRegister(MenuMixin, TemplateView):
    template_name = 'users/thanks.html'
    extra_context = {'title': 'Регистрация завершена'}