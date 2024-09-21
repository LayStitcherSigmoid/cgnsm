import graphene
from graphene_django import DjangoObjectType
from politeum.schema import PoliteumMutation, PoliteumQuery
from idiosynum.schema import IdiosynumMutation, IdiosynumQuery
from administrarium.schema import AdministrariumMutation


class Query(PoliteumQuery, IdiosynumQuery, graphene.ObjectType):
    pass


class Mutation(AdministrariumMutation, PoliteumMutation, IdiosynumMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)