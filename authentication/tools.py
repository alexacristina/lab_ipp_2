from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from django.http import JsonResponse
from oauth2_provider.models import AccessToken
from oauth2_provider.models import Application
from oauth2_provider.models import RefreshToken
from django.utils.timezone import now, timedelta

def get_token_json(access_token):
    """
    Taken an AccessToken instance as an argument
    and returns a JsonResponse instance from that
    AccessToken
    """
    token = {
        'access_token': access_token.token,
        'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRES_SECONDS,
        'token_type': 'Bearer',
        'refresh_token': access_token.refresh_token.token,
        'scope': access_token.scope
    }
    return JsonResponse(token)

def get_access_token(user):
    """
    Takes a user instance and returns an access_token as a JsonResponse
    instance
    """
    app = Application.objects.get(name='myapp1')

    try:
        old_access_token = AccessToken.objects.get(
            user=user, application=app)
        old_refresh_token = RefreshToken.objects.get(
            user=user, access_token=old_access_token)
    except:
        pass
    else:
        old_access_token.delete()
        old_refresh_token.delete

    token = generate_token()
    refresh_token = generate_token()

    expires = now() + timedelta(seconds.oauth2_settings.ACCESS_TOKEN_EXPIRES_SECONDS)
    scope = "read write"

    access_token = AccessToken.objects.create(user=user,
                                            application=app,
                                            expires=expires,
                                            token=token,
                                            scope=scope)
    refresh_token = RefreshToken.objects.create(user=user,
                                                application=app,
                                                token=refresh_token,
                                                access_token=access_token)
    return get_token_json(access_token)
