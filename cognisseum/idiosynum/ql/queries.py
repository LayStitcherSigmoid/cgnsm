import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import graphene
from idiosynum.models import Throughline
from .types import ThroughlineType


class ThroughlineQuery(graphene.ObjectType):
    throughline = graphene.Field(ThroughlineType, id=graphene.UUID(required=True))
    all_throughlines = graphene.List(ThroughlineType)

    def resolve_throughline(self, info, id):
        return Throughline.objects.get(pk=id)

    def resolve_all_throughlines(self, info):
        return Throughline.objects.all()

from idiosynum.models import PostCategory, Tag
from .types import PostCategoryType, TagType

class TagCategoryQuery(graphene.ObjectType):
    post_category = graphene.Field(PostCategoryType, id=graphene.UUID(required=True))
    all_post_categories = graphene.List(PostCategoryType)
    tag = graphene.Field(TagType, id=graphene.UUID(required=True))
    all_tags = graphene.List(TagType)

    def resolve_post_category(self, info, id):
        return PostCategory.objects.get(pk=id)

    def resolve_all_post_categories(self, info):
        return PostCategory.objects.all()

    def resolve_tag(self, info, id):
        return Tag.objects.get(pk=id)

    def resolve_all_tags(self, info):
        return Tag.objects.all()

from idiosynum.models import Post
from .types import PostType

class PostQuery(graphene.ObjectType):
    post = graphene.Field(PostType, id=graphene.UUID(required=True))
    all_posts = graphene.List(PostType)

    def resolve_post(self, info, id):
        return Post.objects.get(pk=id)

    def resolve_all_posts(self, info):
        return Post.objects.all()
