from . import models

class EquaveType(DjangoObjectType):
    class Meta:
        model = models.Equave
        fields = ("id", "name")


class TemperamentType(DjangoObjectType):
    class Meta:
        model = models.Temperament
        fields = ("id", "name")


class TuningSystemType(DjangoObjectType):
    class Meta:
        model = models.TuningSystem
        fields = ("id", "name", "relative_temperament", "relative_equave")


class IntervalQualityType(DjangoObjectType):
    class Meta:
        model = models.IntervalQuality
        fields = ("id", "name", "symbol")


class IntervalType(DjangoObjectType):
    class Meta:
        model = models.Interval
        fields = ("id", "quality", "symbol")


class AccidentalType(DjangoObjectType):
    class Meta:
        model = models.Accidental
        fields = ("id", "name", "symbol", "interval_mod", "direction")


class NoteType(DjangoObjectType):
    class Meta:
        model = models.Note
        fields = ("id", "note_name", "tuning_system", "relative_accidental")