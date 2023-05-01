# Django Views
from django.views.generic.edit import CreateView
from django.views.generic import View, DetailView
from django.contrib.auth.views import LoginView

# Django Authentication
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login, authenticate

# Django Redirects
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy

# Internal Imports
from .models import User

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

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})


class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'

    def get_object(self, user_id=None):
        print(user_id)
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        print(user.first_name, user.last_name)
        return self.request.user
