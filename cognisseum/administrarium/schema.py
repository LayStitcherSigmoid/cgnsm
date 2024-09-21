from .ql.muts import UserMutation
import graphene

class AdministrariumMutation(UserMutation, graphene.ObjectType):
    pass