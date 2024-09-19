from django.db import models
from administrarium.models import Pragmon, Ontologion

# Create your models here.

class Country(Pragmon):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"],name="unique_country_name")
        ]
    name = models.CharField(max_length=200)


class FirstLevelDivision(Pragmon):
    name = models.CharField(max_length=200)
    relative_country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    abbreviation = models.CharField(max_length=10)


class SecondLevelDivision(Pragmon):
    name = models.CharField(max_length=200)
    first_div = models.ForeignKey(FirstLevelDivision, on_delete=models.RESTRICT)


class Person(Pragmon):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mononym = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)


class Biography(Pragmon):
    bio = models.TextField()
    relative_person = models.ForeignKey(Person, on_delete=models.RESTRICT)


class Book(Pragmon):
    title = models.CharField(max_length=100)
    edition = models.CharField(max_length=20, blank=True, null=True)
    isbn = models.CharField(max_length=100)


def user_directory_path(instance, filename):
        return f"user_{instance.user.id}/{filename}"


class BookFile(Pragmon):
    path = models.FileField(upload_to=user_directory_path)

    relevant_book = models.ForeignKey(Book, on_delete=models.RESTRICT)


class Authorship(Pragmon):
    author = models.ForeignKey(Person, on_delete=models.RESTRICT)
    date = models.DateField(blank=True, null=True)
    relevant_book = models.ForeignKey(Book, on_delete=models.RESTRICT)


class BookLibGenLink(Pragmon):
    link = models.URLField()


class LibGenLinkToFile(Pragmon):
    relevant_link = models.ForeignKey(BookLibGenLink, on_delete=models.RESTRICT)
    relevant_file = models.ForeignKey(BookFile, on_delete=models.RESTRICT)


