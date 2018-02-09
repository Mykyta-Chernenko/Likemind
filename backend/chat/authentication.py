from urllib.parse import parse_qs, parse_qsl

import jwt
from channels.auth import AuthMiddlewareStack
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.contrib import auth
from django.utils.functional import SimpleLazyObject
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import Person

from rest_framework_jwt.settings import api_settings

jwt_authentication = JSONWebTokenAuthentication()
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def get_user(scope):
    print('GET Here')
    if "_cached_user" not in scope:
        fake_request = type("FakeRequest", (object,), {"session": scope["session"]})
        scope["_cached_user"] = auth.get_user(fake_request)
    return scope["_cached_user"]


class JWTAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        # Look up user from query string (you should also do things like
        qs = dict(parse_qsl(scope["query_string"].decode('utf-8')))
        jwt_token = qs.pop('token')
        if not jwt_token:
            raise ValueError(
                "No JWT token provided"
            )
        try:
            payload = jwt_decode_handler(jwt_token)
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise AuthenticationFailed()
        user = jwt_authentication.authenticate_credentials(payload)
        if not user:
            raise AuthenticationFailed()
        scope["user"] = user
        for key, value in qs.items():
            scope[key] = value
        return self.inner(scope)


JWTAuthMiddlewareStack = lambda inner: CookieMiddleware(SessionMiddleware(JWTAuthMiddleware(inner)))
