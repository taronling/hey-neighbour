# Internal Imports
from .utils import get_user_location

class UpdateUserLocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            user = request.user
            # city, country = get_user_location(request)
            city = 'TestCity'
            country = 'TestCountry'
            if city and city != user.city and country and country != user.country:
                user.city = city
                user.country = country
                user.save(update_fields=['city', 'country'])

        return response
