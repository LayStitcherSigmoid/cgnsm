from . import models
from cognisseum.utils import ip_from_info, ip_is_home, user_from_info
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .forms import NewCountryForm
from ipware import get_client_ip
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import uuid

# Country CRUD

class CountryType(DjangoObjectType):
    class Meta:
        model = models.Country
        fields = ("id", "name")


class CountryQuery(graphene.ObjectType):
    countries = graphene.List(CountryType)
    country_by_name = graphene.Field(CountryType, name=graphene.String(required=True))
    country_by_id = graphene.Field(CountryType, name=graphene.String(required=True))

    def resolve_countries(root, info, **kwargs):
        return models.Country.objects.all()

    def resolve_country_by_name(root, info, name):
        return models.Country.objects.get(name=name)

    def resolve_country_by_id(root, info, id):
        return models.Country.objects.get(id=id)


class CreateCountry(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    country = graphene.Field(CountryType)
    ok = graphene.Boolean()

    def mutate(self, info, name):
        ip = ip_from_info(info)
        user = user_from_info(info, True)
        try:
            country = models.Country.objects.get(name=name)
        except ObjectDoesNotExist:
            country = models.Country.objects.create(
                name = name,
                ip_last_updated = ip,
                ip_created = ip,
                time_created = datetime.datetime.now(),
                time_last_updated = datetime.datetime.now(),
                user_created_id = user,
                user_last_updated_id = user,
            )
            
        return CreateCountry(country=country, ok=True)


class UpdateCountry(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        id = graphene.String(required=True)

    country = graphene.Field(CountryType)
    ok = graphene.Boolean()

    def mutate(self, info, id, name):
        ip = ip_from_info(info)
        user = user_from_info(info, True)
        try:
            country = models.Country.objects.get(id=uuid.UUID(id))
            country.name = name
            country.save()
            return UpdateCountry(country=country, ok=True)
        except Exception as e:
            return GraphQLError(f"No such Country object with ID {uuid.UUID(id)} {e}")


class CountryMutation(CreateCountry, UpdateCountry, graphene.Mutation):
    pass


# FLD CRUD



# SLD CRUD

# Person CRUD

# Biography CRUD

# Book CRUD

class BookType(DjangoObjectType):
    class Meta:
        model = models.Book
        fields = ("id", "title", "isbn", "edition")
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'isbn': ['exact'],
            'libgenlink': ['exact'],
        }


class BookQuery(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book_by_name = graphene.Field(BookType, name=graphene.String(required=True))
    book_by_isbn = graphene.Field(BookType, isbn=graphene.String(required=True))
    book_by_author = graphene.Field(BookType, mononym=graphene.String(required=False), first_name=graphene.String(required=False), middle_name=graphene.String(required=False), last_name=graphene.String(required=False))

    def resolve_book_by_author(self, info, mononym, first_name, last_name, middle_name):
        try:
            author_role = models.BookEventInvolvement.objects.get(name="Author")
        except ObjectDoesNotExist:
            return GraphQLError("No 'Author' involvement role!")

        if not mononym and not first_name and not last_name:
            return GraphQLError("Provide at least a mononym, a first name, or a last name!")

        
        filters = {}
        if mononym:
            filters['mononym__iexact'] = mononym
        if first_name:
            filters['first_name__iexact'] = first_name
        if middle_name:
            filters['middle_name__iexact'] = middle_name
        if last_name:
            filters['last_name__iexact'] = last_name

        matching_authors = models.Person.objects.filter(**filters)

        if not(matching_authors.exists()):
            return GraphQLError("No authors found with that combination of names!") 

        books = Book.objects.filter(
            bookeventdate__bookeventpersoninvolved__event__involvement=author_role,
            bookeventdate__bookeventpersoninvolved__relevant_person__in=matching_authors
        ).distinct()

        return books

class AuthorInput(graphene.InputObjectType):
    first_name = graphene.String(required=False)
    middle_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    mononym = graphene.String(required=False)
    create_when_absent = graphene.Boolean(required=True)


class PersonType(DjangoObjectType):
    class Meta:
        model = models.Person
        fields = ("id", "first_name", "last_name", "middle_name", "mononym", "birth_date", "death_date")


class AuthorshipType(DjangoObjectType):
    class Meta:
        model = models.Authorship  # Replace with your actual Authorship model
        fields = ("id", "author", "date", "relevant_book")  # Specify the fields you want to expose


class CreateBook(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        isbn = graphene.String(required=False)
        edition = graphene.String(required=True)
        author = AuthorInput(required=True)
        date_published = graphene.Date(required=False)

    book = graphene.Field(BookType)
    authorship = graphene.Field(AuthorshipType)
    ok = graphene.Boolean()

    def mutate(self, info, name, isbn, edition, author, date_published):
        author_filters = {k: v for k, v in author.items() if v}
        if author.create_when_absent:
            try:
                author_instance, created = models.Person.objects.get_or_create(**author_filters)
            except MultipleObjectsReturned:
                return GraphQLError("Multiple 'Person' models with supplied author input!")
        else:
            try:
                author_instance = models.Person.objects.get(**author_filters)
            except ObjectDoesNotExist:
                return GraphQLError("No 'Person' model with supplied author input!")
            except MultipleObjectsReturned:
                return GraphQLError("Multiple 'Person' models with supplied author input!")


        book = models.Book(title=name, isbn=isbn, edition=edition)
        book.save()

        models.Authorship(author=author_instance, date=date_published, relevant_book=book).save()
        
        return CreateBook(book=book, ok=True)


class BookMutation(CreateBook, graphene.Mutation):
    pass


class PoliteumQuery(CountryQuery, BookQuery, graphene.ObjectType):
    pass


class PoliteumMutation(BookMutation, CountryMutation, graphene.ObjectType):
    pass
