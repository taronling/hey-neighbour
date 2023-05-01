# Django Views
from django.views.generic.edit import CreateView
from django.views.generic import View, DetailView
from django.contrib.auth.views import LoginView

# Django Authentication
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login, authenticate

# Django Redirects
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class UserSignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('profile')
    template_name = 'signup.html'

    def form_valid(self, form):
        '''
        If the form is valid, save the associated model and return pass the POST request to the success_url.
        '''
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
    

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(self.success_url)
    

class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return self.request.user
