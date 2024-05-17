from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import logout, get_user_model
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, UserPasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from cards.views import MenuMixin
from django.views.generic import TemplateView, CreateView, ListView
from cards.models import Card
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
    

class ProfileUser(MenuMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()  # Используем модель текущего пользователя
    form_class = ProfileUserForm  # Связываем с формой профиля пользователя
    template_name = 'users/profile.html'  # Указываем путь к шаблону
    extra_context = {'title': 'Профиль пользователя','active_tab': 'profile'}  # Дополнительный контекст для передачи в шаблон

    def get_success_url(self):
        # URL, на который переадресуется пользователь после успешного обновления
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # Возвращает объект модели, который должен быть отредактирован
        return self.request.user


class PasswordChange(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Изменение пароля',
                     'active_tab': 'password_change'}
    
    def form_valid(self, form):
        return super().form_valid(form)


class PasswordChangeDone(TemplateView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Пароль изменен успешно'}
    
    
class PasswordReset(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = UserPasswordResetForm
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    subject_template_name = 'password_reset_subject.txt'
    
    def form_valid(self, form):
        return super().form_valid(form)


class PasswordResetDone(TemplateView):
    template_name = 'users/password_reset_done.html'
    extra_context = {'title': 'Инструкции отправлены'}


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_reset_complete')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    
class PasswordResetDone(TemplateView):
    template_name = 'users/password_reset_complete.html'
    extra_context = {'title': 'Пароль был успешно изменен'}


class UserCardsView(ListView):
    model = Card
    template_name = 'users/profile_cards.html'
    context_object_name = 'cards'
    extra_context = {'title': 'Мои карточки',
                     'active_tab': 'profile_cards'}

    def get_queryset(self):
        return Card.objects.filter(author=self.request.user).order_by('-upload_date')