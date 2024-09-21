import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import graphene
from graphene_django.types import DjangoObjectType
from idiosynum.models import Post, Throughline, DirectedPostRelation, SymmetricPostRelation

class ThroughlineType(DjangoObjectType):
    class Meta:
        model = Throughline
        fields = ('id', 'name', 'related_to')
    
    related_to = graphene.List(lambda: ThroughlineType)
    
    def resolve_related_to(self, info):
        return self.related_to.all()

from idiosynum.models import PostCategory, Tag

class PostCategoryType(DjangoObjectType):
    class Meta:
        model = PostCategory
        fields = ('id', 'name', 'parent')

    parent = graphene.Field(lambda: PostCategoryType)

    def resolve_parent(self, info):
        return self.parent

class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'related_tags')

    related_tags = graphene.List(lambda: TagType)

    def resolve_related_tags(self, info):
        return self.related_tags.all()

from idiosynum.models import DirectedPostRelation, SymmetricPostRelation

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'tags', 'throughlines', 'asymmetrically_related_posts', 'symmetrically_related_posts', 'body')

    tags = graphene.List(lambda: TagType)
    throughlines = graphene.List(lambda: ThroughlineType)
    asymmetrically_related_posts = graphene.List(lambda: PostType)
    symmetrically_related_posts = graphene.List(lambda: PostType)

    def resolve_tags(self, info):
        return self.tags.all()

    def resolve_throughlines(self, info):
        return self.throughlines.all()

    def resolve_asymmetrically_related_posts(self, info):
        return self.asymmetrically_related_posts.all()

    def resolve_symmetrically_related_posts(self, info):
        return self.symmetrically_related_posts.all()
