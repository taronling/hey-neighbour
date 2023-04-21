from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib.auth import login


class SignUpView(CreateView):
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

class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        print(self.request.user)
        return self.request.user
