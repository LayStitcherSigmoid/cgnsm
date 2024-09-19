import graphene
from graphene_django.types import DjangoObjectType
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from idiosynum.models import Throughline, ThroughlineRelation
from .types import ThroughlineType

class CreateThroughline(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        related_to_ids = graphene.List(graphene.UUID, required=False)

    throughline = graphene.Field(ThroughlineType)

    def mutate(self, info, name, related_to_ids=None):
        throughline = Throughline(name=name)
        throughline.save()

        if related_to_ids:
            related_to_objects = Throughline.objects.filter(id__in=related_to_ids)
            throughline.related_to.set(related_to_objects)
        
        return CreateThroughline(throughline=throughline)


class UpdateThroughline(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        name = graphene.String(required=False)
        related_to_ids = graphene.List(graphene.UUID, required=False)

    throughline = graphene.Field(ThroughlineType)

    def mutate(self, info, id, name=None, related_to_ids=None):
        throughline = Throughline.objects.get(pk=id)
        
        if name:
            throughline.name = name
        if related_to_ids:
            related_to_objects = Throughline.objects.filter(id__in=related_to_ids)
            throughline.related_to.set(related_to_objects)
        
        throughline.save()
        return UpdateThroughline(throughline=throughline)


class DeleteThroughline(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            throughline = Throughline.objects.get(pk=id)
            throughline.delete()
            return DeleteThroughline(success=True)
        except Throughline.DoesNotExist:
            return DeleteThroughline(success=False)


class ThroughlineMutation(graphene.ObjectType):
    create_throughline = CreateThroughline.Field()
    update_throughline = UpdateThroughline.Field()
    delete_throughline = DeleteThroughline.Field()

from idiosynum.models import Post, PostCategory, Tag, Throughline, DirectedPostRelation, SymmetricPostRelation
from .types import PostType, TagType, ThroughlineType, PostCategoryType

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        category_id = graphene.UUID(required=True)
        tag_ids = graphene.List(graphene.UUID, required=False)
        throughline_ids = graphene.List(graphene.UUID, required=False)
        asymmetrically_related_post_ids = graphene.List(graphene.UUID, required=False)
        symmetrically_related_post_ids = graphene.List(graphene.UUID, required=False)
        body = graphene.String(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, title, category_id, tag_ids=None, throughline_ids=None, asymmetrically_related_post_ids=None, symmetrically_related_post_ids=None, body=None):
        category = PostCategory.objects.get(pk=category_id)
        tags = Tag.objects.filter(id__in=tag_ids) if tag_ids else []
        throughlines = Throughline.objects.filter(id__in=throughline_ids) if throughline_ids else []
        asymmetrically_related_posts = Post.objects.filter(id__in=asymmetrically_related_post_ids) if asymmetrically_related_post_ids else []
        symmetrically_related_posts = Post.objects.filter(id__in=symmetrically_related_post_ids) if symmetrically_related_post_ids else []

        post = Post(
            title=title,
            category=category,
            body=body
        )
        post.save()
        post.tags.set(tags)
        post.throughlines.set(throughlines)
        post.asymmetrically_related_posts.set(asymmetrically_related_posts)
        post.symmetrically_related_posts.set(symmetrically_related_posts)

        return CreatePost(post=post)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)
        title = graphene.String(required=False)
        category_id = graphene.UUID(required=False)
        tag_ids = graphene.List(graphene.UUID, required=False)
        throughline_ids = graphene.List(graphene.UUID, required=False)
        asymmetrically_related_post_ids = graphene.List(graphene.UUID, required=False)
        symmetrically_related_post_ids = graphene.List(graphene.UUID, required=False)
        body = graphene.String(required=False)

    post = graphene.Field(PostType)

    def mutate(self, info, id, title=None, category_id=None, tag_ids=None, throughline_ids=None, asymmetrically_related_post_ids=None, symmetrically_related_post_ids=None, body=None):
        post = Post.objects.get(pk=id)

        if title:
            post.title = title
        if category_id:
            post.category = PostCategory.objects.get(pk=category_id)
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            post.tags.set(tags)
        if throughline_ids:
            throughlines = Throughline.objects.filter(id__in=throughline_ids)
            post.throughlines.set(throughlines)
        if asymmetrically_related_post_ids:
            asymmetrically_related_posts = Post.objects.filter(id__in=asymmetrically_related_post_ids)
            post.asymmetrically_related_posts.set(asymmetrically_related_posts)
        if symmetrically_related_post_ids:
            symmetrically_related_posts = Post.objects.filter(id__in=symmetrically_related_post_ids)
            post.symmetrically_related_posts.set(symmetrically_related_posts)
        if body:
            post.body = body
        
        post.save()
        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            return DeletePost(success=True)
        except Post.DoesNotExist:
            return DeletePost(success=False)

class PostMutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()