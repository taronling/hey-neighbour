# Django Views
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.views.generic import View, DetailView
from django.contrib.auth.views import LoginView
from django.db.models import Q

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
        context['is_friend'] = FriendConnection.objects.filter(
            Q(user1=self.request.user, user2=self.object) | 
            Q(user1=self.object, user2=self.request.user)
        ).exists()
        return context


class AddRemoveFriendView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        friend_id = request.POST.get('friend_id')
        action = request.POST.get('action')

        if friend_id and action in ['add', 'remove']:
            friend = get_object_or_404(User, pk=friend_id)

            if action == 'add':
                request.user.friends.add(friend)
                return JsonResponse({'status': 'ok', 'message': 'Friend added successfully', 'action': 'added'})
            else:
                request.user.friends.remove(friend)
                return JsonResponse({'status': 'ok', 'message': 'Friend removed successfully', 'action': 'removed'})
        return JsonResponse({'status': 'error', 'message': 'Invalid friend ID or action'})