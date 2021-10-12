from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import UserLoginForm, UserRegistrationForm, MyPasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView
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


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('register_done')
    template_name = 'accounts/register.html'

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


class RegisterDone(TemplateView):
    template_name = 'accounts/register_done.html'


class PasswordChange(SuccessMessageMixin, PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = 'blog/profile.html'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors.as_text())
        return redirect(reverse_lazy('profile', kwargs={'pk': self.request.user.pk}), self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})

