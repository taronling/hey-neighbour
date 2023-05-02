# Django Imports
from django.urls import path
from django.contrib.admin.models import LogEntry

# View Imports
from users.views import UserSignUpView, UserLoginView, UserProfileView, AddFriendView

LogEntry.user.field.rel_to = 'users.User'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignUpView.as_view(), name='signup'),    
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='profile'),
    path('add_friend/', AddFriendView.as_view(), name='add_friend'),
    ]
