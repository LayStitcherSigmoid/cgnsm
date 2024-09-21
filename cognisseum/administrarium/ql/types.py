import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from administrarium.models import Administrarion
from django.contrib.auth import get_user_model
from graphql import GraphQLError

class UserType(DjangoObjectType):
    class Meta:
        model = Administrarion
        fields = ("id", "username", "email")

