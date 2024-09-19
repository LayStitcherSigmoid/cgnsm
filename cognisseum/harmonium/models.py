from django.db import models
from administrarium.models import Pragmon

# Create your models here.

class Equave(Pragmon):
    name = models.CharField(max_length=20)


class Temperament(Pragmon):
    name = models.CharField(max_length=20)


class TuningSystem(Pragmon):
    name = models.CharField(max_length=20)
    chromaticity = models.IntegerField()
    relative_temperament = models.ForeignKey(Temperament, on_delete=models.RESTRICT)
    relative_equave = models.ForeignKey(Equave, on_delete=models.RESTRICT)


class IntervalQuality(Pragmon):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=5)
    

class Interval(Pragmon):
    quality = models.ForeignKey(IntervalQuality, on_delete=models.RESTRICT)
    symbol = models.CharField(max_length=5)


class AccidentalSystem(Pragmon):
    name = models.CharField(max_length=50)


class AccidentalDirection(Pragmon):
    name = models.CharField(max_length=20)


class Accidental(Pragmon):
    accidental_system = models.ForeignKey(AccidentalSystem, on_delete=models.RESTRICT)
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=5)
    interval_mod = models.ForeignKey(Interval, on_delete=models.RESTRICT)
    direction = models.ForeignKey(AccidentalDirection, on_delete=models.RESTRICT)


class NoteName(Pragmon):
    name = models.CharField(max_length=20)


class Note(Pragmon):
    note_name = models.ForeignKey(NoteName, on_delete=models.RESTRICT)
    relative_accidental = models.ForeignKey(Accidental, on_delete=models.RESTRICT)
    tuning_system = models.ForeignKey(TuningSystem, on_delete=models.RESTRICT)


class Clef(Pragmon):
    name = models.CharField(max_length=20)
    bottom_note = models.ForeignKey(NoteName, on_delete=models.RESTRICT)


class Enharmonic(Pragmon):
    chromatic_number = models.IntegerField()
    tuning_system = models.ForeignKey(TuningSystem, on_delete=models.RESTRICT)


class EnharmonicClefPosition(Pragmon):
    relative_clef = models.ForeignKey(Clef, on_delete=models.RESTRICT)
    relative_enharmonic = models.ForeignKey(Enharmonic, on_delete=models.RESTRICT)
    position = models.IntegerField()


class EnharmonicEquivalence(Pragmon):
    cell = models.ForeignKey(Enharmonic, on_delete=models.RESTRICT)
    element = models.ForeignKey(Note, on_delete=models.RESTRICT)


class IntervalInverse(Pragmon):
    first_interval = models.ForeignKey(Interval, on_delete=models.RESTRICT, related_name="first_interval")
    second_interval = models.ForeignKey(Interval, on_delete=models.RESTRICT, related_name="second_interval")


class EnharmonicIntervalAssignment(Pragmon):
    relative_tuning = models.ForeignKey(TuningSystem, on_delete=models.RESTRICT)
    first_note = models.ForeignKey(Note, on_delete=models.RESTRICT, related_name="first_note")
    second_note = models.ForeignKey(Note, on_delete=models.RESTRICT, related_name="second_note")
    relative_interval = models.ForeignKey(Interval, on_delete=models.RESTRICT)


class ScaleFamily(Pragmon):
    name = models.CharField(max_length=30)


class ScaleStep(Pragmon):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30)
    relative_interval = models.ForeignKey(Interval, on_delete=models.RESTRICT)


class ScaleDegree(Pragmon):
    mode_name = models.CharField(max_length=20)
    order = models.IntegerField()
    relative_step = models.ForeignKey(ScaleStep, on_delete=models.RESTRICT)


class ScaleStepIntervalRelation(Pragmon):
    first_interval = models.ForeignKey(Interval, on_delete=models.RESTRICT, related_name="source_interval")
    relative_step = models.ForeignKey(ScaleStep, on_delete=models.RESTRICT)
    second_interval = models.ForeignKey(Interval, on_delete=models.RESTRICT, related_name="target_interval")


class EquivarationalRelation(Pragmon):
    name = models.CharField(max_length=100)
    relative_tuning = models.ForeignKey(TuningSystem, on_delete=models.RESTRICT)

