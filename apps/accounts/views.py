from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.core import signing
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django_registration.backends.activation.views import RegistrationView, ActivationView

from .forms import UserLoginForm, UserRegistrationForm, MyPasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView
from django.utils.translation import ugettext_lazy as _


class MyLoginView(LoginView):
    form_class = UserLoginForm
    authentication_form = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):
    """
    Log out the user and display the 'You are logged out' message.
    """
    template_name = 'accounts/logout.html'


class RegisterView(RegistrationView):
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
    template_name = 'accounts/register_done.html'


class UserActivationView(ActivationView):
    success_url = reverse_lazy('activation_done')
    template_name = 'accounts/register_done.html'


class SuccessActivationView(TemplateView):
    template_name = 'accounts/activation_done.html'


class PasswordChange(SuccessMessageMixin, PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = 'blog/profile.html'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors.as_text())
        return redirect(reverse_lazy('profile', kwargs={'pk': self.request.user.pk}), self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})


class PasswordReset(PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'accounts/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_confirm.html'
    title = _('Enter new password')

