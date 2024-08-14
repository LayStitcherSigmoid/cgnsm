from django.db import models
from administrarium.models import Pragmon

# Create your models here.

class Country(Pragmon):
    name = models.CharField(max_length=200)


class FirstLevelDivision(Pragmon):
    name = models.CharField(max_length=200)
    relative_country = models.ForeignKey(Country, on_delete=models.RESTRICT)


class SecondLevelDivision(Pragmon):
    name = models.CharField(max_length=200)
    first_div = models.ForeignKey(FirstLevelDivision, on_delete=models.RESTRICT)


class Person(Pragmon):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField()


class Biography(Pragmon):
    bio = models.TextField()
    relative_person = models.ForeignKey(Person, on_delete=models.RESTRICT)


class CulturalArtifactType(Pragmon):
    name = models.CharField(max_length=100)


class CulturalArtifactMetaType(Pragmon):
    meta_kind = models.ForeignKey(CulturalArtifactType, on_delete=models.RESTRICT)
    field_name = models.CharField(max_length=100)


class CulturalArtifact(Pragmon):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True)
    kind = models.ForeignKey(CulturalArtifactType, on_delete=models.RESTRICT)


class CulturalArtifactMeta(Pragmon):
    cultural_artifact = models.ForeignKey(CulturalArtifact, on_delete=models.RESTRICT)
    meta = models.ForeignKey(CulturalArtifactMetaType, on_delete=models.RESTRICT)


class CulturalArtifactReview(Pragmon):
    artifact = models.ForeignKey(CulturalArtifact, on_delete=models.RESTRICT)
    review = models.TextField()
    decimal_rating = models.IntegerField()