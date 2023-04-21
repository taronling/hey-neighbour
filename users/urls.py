from django.urls import path
from users.views import SignUpView, UserProfileView
from django.contrib.admin.models import LogEntry

LogEntry.user.field.rel_to = 'users.User'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
