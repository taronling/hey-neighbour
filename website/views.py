from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.core import serializers
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.generic import TemplateView

# Internal Imports
from users.models import User


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class SearchUserView(ListView):
    model = User
    context_object_name = 'users'
    http_method_names = ['get']

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        print(query)
        if query:
            return User.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(full_name__icontains=query)
            )[:10]
        return User.objects.none()

    def render_to_response(self, context, **response_kwargs):
        users = context['users']
        users_serialized = serializers.serialize('json', users)
        return JsonResponse({'users': users_serialized}, safe=False)
