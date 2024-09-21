import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import graphene
from django.contrib.auth import authenticate, login
from graphene_django.types import DjangoObjectType

from administrarium.models import Administrarion
from .types import UserType

class LoginMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(info.context, user)
                return LoginMutation(user=user, success=True, errors=[])
            else:
                return LoginMutation(success=False, errors=["Account is disabled."])
        else:
            return LoginMutation(success=False, errors=["Invalid credentials."])


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    user = graphene.Field(lambda: UserType)

    def mutate(self, info, username, email, password):
        if Administrarion.objects.filter(username=username).exists():
            raise GraphQLError('Username already taken.')
        if Administrarion.objects.filter(email=email).exists():
            raise GraphQLError('Email already registered.')

        # Create the user
        user = Administrarion(username=username, email=email)
        user.set_password(password)
        user.save()

        return CreateUser(success=True, user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        username = graphene.String(required=False)
        email = graphene.String(required=False)

    success = graphene.Boolean()
    user = graphene.Field(lambda: UserType)

    def mutate(self, info, user_id, username=None, email=None):
        user = Administrarion.objects.get(id=user_id)

        # Check if new username is provided and is available
        if username and username != user.username:
            if Administrarion.objects.filter(username=username).exists():
                raise GraphQLError('Username already taken.')
            user.username = username

        # Check if new email is provided and is available
        if email and email != user.email:
            if Administrarion.objects.filter(email=email).exists():
                raise GraphQLError('Email already registered.')
            user.email = email

        user.save()
        return UpdateUser(success=True, user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, user_id):
        try:
            user = Administrarion.objects.get(id=user_id)
            user.delete()
            return DeleteUser(success=True)
        except UserModel.DoesNotExist:
            raise GraphQLError('User not found.')

class UserMutation(graphene.ObjectType):
    login = LoginMutation.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
