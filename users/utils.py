import ipapi
from ipware import get_client_ip

def get_user_location(request):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        return None

    location_data = ipapi.location(client_ip)
    city = location_data.get('city', None)
    country = location_data.get('country', None)
    return city, country
