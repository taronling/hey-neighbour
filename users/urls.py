from django.urls import path
from users.views import UserSignUpView, UserLoginView, UserProfileView
from django.contrib.admin.models import LogEntry

LogEntry.user.field.rel_to = 'users.User'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignUpView.as_view(), name='signup'),    
    path('profile/', UserProfileView.as_view(), name='profile'),
]
