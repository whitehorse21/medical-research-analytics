from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Token


class TokenAuthentication(BaseAuthentication):
    """Custom token authentication"""
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Token '):
            return None
        
        token_key = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else None
        if not token_key:
            return None
        
        try:
            token = Token.objects.select_related('user').get(key=token_key)
            return (token.user, None)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
