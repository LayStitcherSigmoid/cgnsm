from django.db import models
from administrarium import Pragmon

# Create your models here.

class Equave(Pragmon):
    name = models.CharField(max_length=20)
    ratio = models.IntegerField()


class Temperament(Pragmon):
    name = models.CharField(max_length=20)
    has_step_basis = models.BooleanField()
    has_ratio_basis = models.BooleanField()


class TuningSystem(Pragmon):
    name = models.CharField(max_length=20)
    chromaticity = models.IntegerField()
    temperament = models.ForeignKey(Temperament, on_delete=models.RESTRICT)
    equave = models.ForeignKey(Equave, on_delete=models.RESTRICT)


class IntervalQuality(Pragmon):
    name = models.CharField(max_length=20)
    

class Interval(Pragmon):
    step_mod = models.IntegerField(blank=True)
    numerator_mod = models.IntegerField(blank=True)
    denominator_mod = models.IntegerField(blank=True)
    name = models.CharField(max_length=10)
    quality = models.ForeignKey(IntervalQuality, on_delete=models.RESTRICT)


class Enharmonic(Pragmon):
    chromatic_number = models.IntegerField()
    tuning_system = models.ForeignKey(TuningSystem, on_delete=models.RESTRICT)


class Clef(Pragmon):
    name = models.CharField(max_length=20)


class EnharmonicClefPosition(Pragmon):
    relative_staff = models.ForeignKey(Enharmonic, on_delete=models.RESTRICT)
    relative_enharmonic = models.ForeignKey(Enharmonic, on_delete=models.RESTRICT)


class AccidentalSystem(Pragmon):
    name = models.CharField(max_length=50)


class Accidental(Pragmon):
    accidental_system = models.ForeignKey(AccidentalSystem, on_delete=models.RESTRICT)
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=5)
    interval_mod = 


class Note(Pragmon):
    name = models.CharField(max_length=20)
    accidental = models.ForeignKey(Accidental, on_delete=models.RESTRICT)


class EnharmonicEquivalence(Pragmon):
    cell = models.ForeignKey(Enharmonic, on_delete=models.RESTRICT)
    element = models.ForeignKey(Note, on_delete=models.RESTRICT)