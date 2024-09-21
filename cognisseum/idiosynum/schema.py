import graphene
from .ql.queries import ThroughlineQuery, PostQuery, TagCategoryQuery
from .ql.muts import ThroughlineMutation, PostMutation

class IdiosynumQuery(ThroughlineQuery, PostQuery, TagCategoryQuery, graphene.ObjectType):
    pass

class IdiosynumMutation(ThroughlineMutation, PostMutation, graphene.ObjectType):
    pass