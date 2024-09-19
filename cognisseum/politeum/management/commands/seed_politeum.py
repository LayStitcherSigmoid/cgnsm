from administrarium.models import Administrarion, Ontologion
from Administrarion.utils import curry_model
from django.core.management.base import BaseCommand, CommandError
from politeum.models import (
    Country, 
    FirstLevelDivision, 
    SecondLevelDivision, 
    Person,
    CulturalArtifactType,
    CulturalArtifactTypeMetaField,
    CulturalArtifactMetaLink,
    )


def do_seed(prime):
    make = curry_model(prime, "127.0.0.1")

    mktype = lambda name: make(CulturalArtifactType, name=name)
    book_type = mktype("Book")
    poem_type = mktype("Poem")

    mkmeta = lambda name: make(CulturalArtifactTypeMetaField, name=name)
    libgen_link = mkmeta("Libgen Link")

    mklink = lambda kind, meta: make(CulturalArtifactMetaLink, kind=kind, field=meta)
    mklink(book_type, libgen_link)
    

def safe_seed():
    try:
        prime = Administrarion.objects.get(username='Prime')
    except Exception as e:
        prime = Administrarion(username='Prime')
        prime.save()
    
    do_seed(prime)


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        safe_seed()