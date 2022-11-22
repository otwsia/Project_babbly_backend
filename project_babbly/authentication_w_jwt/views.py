from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['company'] = 'GA'

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class Logout(TokenObtainPairSerializer):
    permission_classes = (IsAuthenticated,)
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['access'] = 'logout'
        token['refresh'] = 'logout'

        return token

class Logout(TokenObtainPairView):
    serializer_class = Logout