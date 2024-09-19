from .models import (
    Administrarion, 
    OntologicalRelation, 
    Ontologion, 
    OntologicalRelationType)
from .utils import curry_model
from django.core.management.base import BaseCommand, CommandError



def do_seed(prime):
    make = curry_model(prime, "127.0.0.1")

    mkont = lambda name: make(Ontologion, name=name)
    
    esotericism = mkont("Esotericism")
    religion = mkont("Religion")
    science = mkont("Science")
    technology = mkont("Technology")
    philosophy = mkont("Philosophy")
    spirituality = mkont("Spirituality")
    mysticism = mkont("Mysticism")

    

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