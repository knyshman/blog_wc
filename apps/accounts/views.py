from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django_registration.backends.activation.views import RegistrationView, ActivationView
from .forms import UserLoginForm, UserRegistrationForm, MyPasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.utils.translation import ugettext_lazy as _


class MyLoginView(LoginView):
    """Аутентификация пользователя"""
    form_class = UserLoginForm
    authentication_form = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):
    """
    Log out the user and display the 'You are logged out' message.
    """
    template_name = 'accounts/logout.html'
    def get_success_url(self, user=None):
        return redirect(reverse_lazy('home'))


class RegisterView(RegistrationView):
    """Регистрация пользователя"""
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register_done')
    template_name = 'accounts/register.html'
    email_body_template = 'accounts/email/activation_email_body.txt'
    email_subject_template = 'accounts/email/activation_email_subject.txt'

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data["password"]
        user.password = make_password(password)
        return super().form_valid(form)

    def get_success_url(self, user=None):
        return reverse_lazy('register_done')


class RegisterDone(TemplateView):
    """Успешная регистрация"""
    template_name = 'accounts/register_done.html'


class UserActivationView(ActivationView):
    """Активация пользователя, подтверджение электроннной почты"""
    success_url = reverse_lazy('activation_done')
    template_name = 'accounts/register_done.html'


class SuccessActivationView(TemplateView):
    """Странница успешной активации пользователя"""
    template_name = 'accounts/activation_done.html'


class PasswordChange(SuccessMessageMixin, PasswordChangeView):
    """Изменение пароля"""
    form_class = MyPasswordChangeForm
    template_name = 'blog/profile.html'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors.as_text().replace('old_password', 'текущий пароль').replace('new_password2', 'новый пароль'))
        return redirect(reverse_lazy('profile'))

    def get_success_url(self):
        return reverse_lazy('profile')

