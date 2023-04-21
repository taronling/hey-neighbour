from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('profile')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        print(form.cleaned_data['email'])  # Print the submitted email to console
        return super().form_valid(form)


class UserProfileView(TemplateView):
    template_name = 'profile.html'
