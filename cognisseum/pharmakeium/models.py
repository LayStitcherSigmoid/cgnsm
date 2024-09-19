from django.db import models
from administrarium.models import Pragmon

# Create your models here.

class Molecule(Pragmon):
    smiles = models.TextField(unique=True)

    def __str__(self):
        return self.smiles


class MoleculeNamingSystem(Pragmon):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class MoleculeName(Pragmon):
    relative_molecule = models.ForeignKey(Molecule, on_delete=models.RESTRICT, related_name="named_molecule")
    naming_system = models.ForeignKey(MoleculeNamingSystem, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('relative_molecule', 'naming_system')

    def __str__(self):
        return f"{self.name} ({self.naming_system.name})"


class IdentificationSystem(Pragmon):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class Identification(Pragmon):
    relative_molecule = models.ForeignKey(Molecule, on_delete=models.RESTRICT, related_name="identified_molecule")
    identification_system = models.ForeignKey(IdentificationSystem, on_delete=models.RESTRICT)
    identifier = models.CharField(max_length=255)

    class Meta:
        unique_together = ('relative_molecule', 'identification_system')

    def __str__(self):
        return f"{self.identifier} ({self.identification_system.name})"


class AnimalModel(Pragmon):
    species = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.species


class Receptor(Pragmon):
    name = models.CharField(max_length=255)
    unigene = models.CharField(max_length=50, unique=True)
    source = models.CharField(max_length=255)
    species = models.ForeignKey(AnimalModel, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class kiDbBindingAffinity(Pragmon):
    number = models.IntegerField()
    relative_receptor = models.ForeignKey(Receptor, on_delete=models.RESTRICT)
    ligand = models.ForeignKey(MoleculeName, related_name='ligand_affinities', on_delete=models.RESTRICT)
    hotligand = models.ForeignKey(MoleculeName, related_name='hotligand_affinities', on_delete=models.RESTRICT)
    ki_note = models.TextField(blank=True, null=True)
    ki_val = models.FloatField()
    reference = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.number} Binding Affinity: {self.receptor.name} - {self.ligand.name} (Ki: {self.ki_val})"