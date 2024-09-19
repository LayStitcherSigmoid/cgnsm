import graphene
from .ql_utils.queries import ThroughlineQuery, PostQuery, TagCategoryQuery
from .ql_utils.muts import ThroughlineMutation, PostMutation

class IdiosynumQuery(ThroughlineQuery, PostQuery, TagCategoryQuery, graphene.ObjectType):
    pass

class IdiosynumMutation(ThroughlineMutation, PostMutation, graphene.ObjectType):
    pass