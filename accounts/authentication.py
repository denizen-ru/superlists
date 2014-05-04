import requests
from django.conf import settings
from django.contrib.auth import get_user_model

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'

User = get_user_model()


class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        response = requests.post(PERSONA_VERIFY_URL, data={
                                 'assertion': assertion, 'audience': settings.DOMAIN})
        if response.ok and response.json()['status'] == 'okay':
            email = response.json()['email']
            try:
                return User.objects.get(email=response.json()['email'])
            except User.DoesNotExist:
                return User.objects.create(email=email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            pass
