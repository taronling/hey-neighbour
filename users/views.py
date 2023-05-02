# Django Views
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.views.generic import View, DetailView
from django.contrib.auth.views import LoginView
from django.db.models import Q

# Django Authentication
from .forms import SignUpForm, LoginForm, CustomUserChangeForm
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
        context['form'] = CustomUserChangeForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(request.path_info)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class AddRemoveFriendView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        friend_id = request.POST.get('friend_id')
        action = request.POST.get('action')
        print(action)

        if friend_id and action in ['add', 'remove']:
            friend = get_object_or_404(User, pk=friend_id)

            if action == 'add':
                # Check if the connection already exists
                connection_exists = FriendConnection.objects.filter(
                    Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user)
                ).exists()

                if not connection_exists:
                    friendship = FriendConnection(user1=request.user, user2=friend)
                    friendship.save()
                    return JsonResponse({'status': 'ok', 'message': 'Friend added successfully', 'action': 'added'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Friend connection already exists'})
            else:
                # Remove the connection from the FriendConnection table
                connection = FriendConnection.objects.filter(
                    Q(user1=request.user, user2=friend) | Q(user1=friend, user2=request.user)
                )
                if connection.exists():
                    connection.delete()
                    return JsonResponse({'status': 'ok', 'message': 'Friend removed successfully', 'action': 'removed'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Friend connection not found'})
        return JsonResponse({'status': 'error', 'message': 'Invalid friend ID or action'})
