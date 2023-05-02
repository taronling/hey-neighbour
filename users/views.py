# Django Views
from django.http import JsonResponse
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
from .models import User, FriendConnection

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

    def get_object(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_friend'] = self.request.user.friends.filter(pk=self.object.id).exists()
        return context


class AddFriendView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        friend_id = request.POST.get('friend_id')
        if friend_id:
            friend = get_object_or_404(User, pk=friend_id)
            friendship = FriendConnection(user1=request.user, user2=friend)
            friendship.save()
            return JsonResponse({'status': 'success', 'message': 'Friend added successfully'})
        return JsonResponse({'status': 'error', 'message': 'Invalid friend ID'})
