from harmonium.models import Equave, Temperament, TuningSystem, IntervalQuality, Interval, AccidentalSystem, Accidental, NoteName, Note, Clef, Enharmonic, EnharmonicClefPosition, EnharmonicEquivalence
from administrarium.models import Administrarion
from django.core.management.base import BaseCommand, CommandError


def make_model(model, acc, ip, **kwargs):
    return model(user_created=acc, user_last_updated=acc, ip_created=ip, ip_last_updated=ip, **kwargs)

def curry_model(acc, ip):
    def inner(model, **kwargs):
        return make_model(model, acc, ip, **kwargs)
    return inner



def do_seed(prime):
    _ip = "127.0.0.1"

    make = curry_model(prime, _ip)

    octave = make(Equave, name="Octave", ratio=2)
    et = make(Temperament, name="Equal Temperament" has_step_basis=True, has_ratio_basis=False)
    twelve_edo = make(TuningSystem, name="12EDO", chromaticity=12, relative_temperament=et, relative_equave=octave)
    
    perf_int = make(IntervalQuality, name="Perfect", symbol="P")
    minor_int = make(IntervalQuality, name="Minor", symbol="m")
    major_int = make(IntervalQuality, name="Major", symbol="M")

    P0 = make(Interval, step_mod=0, numerator_mod=1, denominator_mod=1, name="Perfect Unison", quality=perf_int, symbol="0")
    m2 = make(Interval, step_mod=1, numerator_mod=16, denominator_mod=15, name="Minor Second", quality=minor_int, symbol="2")
    M2 = make(Interval, step_mod=2, numerator_mod=9, denominator_mod=8, name="Major Second", quality=major_int, symbol="2")
    m3 = make(Interval, step_mod=3, numerator_mod=6, denominator_mod=5, name="Minor Third", quality=minor_int, symbol="3")
    M3 = make(Interval, step_mod=4, numerator_mod=5, denominator_mod=4, name="Major Third", quality=major_int, symbol="3")
    P4 = make(Interval, step_mod=5, numerator_mod=4, denominator_mod=3, name="Perfect Fourth", quality=perf_int, symbol="4")
    P5 = make(Interval, step_mod=7, numerator_mod=3, denominator_mod=2, name="Perfect Fifth", quality=perf_int, symbol="5")
    m6 = make(Interval, step_mod=8, numerator_mod=8, denominator_mod=5, name="Minor Sixth", quality=minor_int, symbol="6")
    M6 = make(Interval, step_mod=9, numerator_mod=5, denominator_mod=3, name="Major Sixth", quality=major_int, symbol="6")
    m7 = make(Interval, step_mod=10, numerator_mod=9, denominator_mod=5, name="Minor Seventh", quality=minor_int, symbol="7")
    M7 = make(Interval, step_mod=11, numerator_mod=15, denominator_mod=8, name="Major Seventh", quality=major_int, symbol="7")
    P8 = make(Interval, step_mod=12, numerator_mod=2, denominator_mod=1, name="Perfect Octave", quality=perf_int, symbol="8")

    


def safe_seed():
    try:
        prime = Administrarion.objects.get(username='Prime')
    except Exception as e:
        pass
    else:
        do_seed(prime)


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        safe_seed()