from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from stations.models import Station

class StationAPIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication class that handles Bearer token in the form:
    Authorization: Bearer <API_KEY>
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            # Raise an AuthenticationFailed exception if the token is missing
            raise AuthenticationFailed('Authorization header is missing.')

        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Invalid token header. No Bearer token.')

        api_key = auth_header.split(' ')[1]

        try:
            station = Station.objects.get(api_key=api_key)
        except Station.DoesNotExist:
            raise AuthenticationFailed('Invalid API key.')

        # Return the station object as the authenticated user
        return (station, None)
    