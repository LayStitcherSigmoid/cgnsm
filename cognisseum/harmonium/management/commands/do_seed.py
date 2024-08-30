from harmonium.models import Equave, Temperament, TuningSystem, IntervalQuality, Interval, AccidentalSystem, Accidental, AccidentalDirection, NoteName, Note, Clef, Enharmonic, EnharmonicClefPosition, EnharmonicEquivalence, IntervalInverse, EnharmonicIntervalAssignment
from administrarium.models import Administrarion
from django.core.management.base import BaseCommand, CommandError


def make_model(model, acc, ip, **kwargs):
    return model(user_created=acc, user_last_updated=acc, ip_created=ip, ip_last_updated=ip, **kwargs)

def curry_model(acc, ip):
    def inner(model, **kwargs):
        model = make_model(model, acc, ip, **kwargs)
        model.save()
        return model
    return inner

def enh_curry(make_f):
    def inner(cell, elem):
        return make_f(EnharmonicEquivalence, cell=cell, elem=elem)
    return inner

def interval_inverse_curry(make_f):
    def inner(interval_1, interval_2):
        first_relation = make_f(IntervalInverse, first_interval=interval_1, second_interval=interval_2)
        second_relation = make_f(IntervalInverse, first_interval=interval_2, second_interval=interval_1)
        return (first_relation, second_relation)
    return inner

def assign_interval_curry(make_f, tuning):
    def inner(note_1, note_2, interval):
        inverse_interval = IntervalInverse.objects.get(first_interval=interval).second_interval
        first_relation = make_f(EnharmonicIntervalAssignment, relative_tuning=tuning, first_note=note_1, second_note=note_2, relative_interval=interval)
        inverse_relation = make_f(EnharmonicIntervalAssignment, relative_tuning=tuning, first_note=note_2, second_note=note_1, relative_interval=inverse_interval)
        return (first_relation, inverse_relation)
    return inner

def do_seed(prime):
    _ip = "127.0.0.1"

    make = curry_model(prime, _ip)
    enh = enh_curry(make)

    octave = make(Equave, name="Octave", ratio=2)
    et = make(Temperament, name="Equal Temperament" has_step_basis=True, has_ratio_basis=False)
    twelve_edo = make(TuningSystem, name="12EDO", chromaticity=12, relative_temperament=et, relative_equave=octave)

    add_interval_inversion = interval_inverse_curry(make)
    assign_twelve_edo_cell_intervals = assign_interval_curry(make, twelve_edo)

    perf_int = make(IntervalQuality, name="Perfect", symbol="P")
    minor_int = make(IntervalQuality, name="Minor", symbol="m")
    major_int = make(IntervalQuality, name="Major", symbol="M")

    P1 = make(Interval, step_mod=0, numerator_mod=1, denominator_mod=1, name="Perfect Unison", quality=perf_int, symbol="1")
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

    add_interval_inversion(P1, P8)
    add_interval_inversion(m2, M7)
    add_interval_inversion(M2, m7)
    add_interval_inversion(m3, M6)
    add_interval_inversion(M3, m6)
    add_interval_inversion(P5, P4)

    comprac = make(AccidentalSystem, name="Common Practice")
    upward = make(AccidentalDirection, name="Upward")
    downward = make(AccidentalDirection, name="Downward")

    nat = make(Accidental, name="Natural", symbol="♮", interval_mod=P1, direction=upward, accidental_system=comprac)
    sharp = make(Accidental, name="Sharp", symbol="#", interval_mod=m2, direction=upward, accidental_system=comprac)
    double_sharp = make(Accidental, name="Double Sharp", symbol="##", interval_mod=M2, direction=upward, accidental_system=comprac)
    flat = make(Accidental, name="Flat", symbol="b", interval_mod=m2, direction=downward, accidental_system=comprac)
    double_flat = make(Accidental, name="Double Flat", symbol="bb", interval_mod=M2, direction=downward, accidental_system=comprac)

    a = make(NoteName, name="A")
    b = make(NoteName, name="B")
    c = make(NoteName, name="C")
    d = make(NoteName, name="D")
    e = make(NoteName, name="E")
    f = make(NoteName, name="F")
    g = make(NoteName, name="G")

    a_nat = make(Note, note_name=a, relative_accidental=nat, tuning_system=twelve_edo)
    a_sharp = make(Note, note_name=a, relative_accidental=sharp, tuning_system=twelve_edo)
    a_flat = make(Note, note_name=a, relative_accidental=flat, tuning_system=twelve_edo)
    a_dblsharp = make(Note, note_name=a, relative_accidental=double_sharp, tuning_system=twelve_edo)
    a_dblflat = make(Note, note_name=a, relative_accidental=double_flat, tuning_system=twelve_edo)

    b_nat = make(Note, note_name=b, relative_accidental=nat, tuning_system=twelve_edo)
    b_sharp = make(Note, note_name=b, relative_accidental=sharp, tuning_system=twelve_edo)
    b_flat = make(Note, note_name=b, relative_accidental=flat, tuning_system=twelve_edo)
    b_dblsharp = make(Note, note_name=b, relative_accidental=double_sharp, tuning_system=twelve_edo)
    b_dblflat = make(Note, note_name=b, relative_accidental=double_flat, tuning_system=twelve_edo)

    c_nat = make(Note, note_name=c, relative_accidental=nat, tuning_system=twelve_edo)
    c_sharp = make(Note, note_name=c, relative_accidental=sharp, tuning_system=twelve_edo)
    c_flat = make(Note, note_name=c, relative_accidental=flat, tuning_system=twelve_edo)
    c_dblsharp = make(Note, note_name=c, relative_accidental=double_sharp, tuning_system=twelve_edo)
    c_dblflat = make(Note, note_name=c, relative_accidental=double_flat, tuning_system=twelve_edo)

    d_nat = make(Note, note_name=d, relative_accidental=nat, tuning_system=twelve_edo)
    d_sharp = make(Note, note_name=d, relative_accidental=sharp, tuning_system=twelve_edo)
    d_flat = make(Note, note_name=d, relative_accidental=flat, tuning_system=twelve_edo)
    d_dblsharp = make(Note, note_name=d, relative_accidental=double_sharp, tuning_system=twelve_edo)
    d_dblflat = make(Note, note_name=d, relative_accidental=double_flat, tuning_system=twelve_edo)

    e_nat = make(Note, note_name=e, relative_accidental=nat, tuning_system=twelve_edo)
    e_sharp = make(Note, note_name=e, relative_accidental=sharp, tuning_system=twelve_edo)
    e_flat = make(Note, note_name=e, relative_accidental=flat, tuning_system=twelve_edo)
    e_dblsharp = make(Note, note_name=e, relative_accidental=double_sharp, tuning_system=twelve_edo)
    e_dblflat = make(Note, note_name=e, relative_accidental=double_flat, tuning_system=twelve_edo)

    f_nat = make(Note, notf_name=f, relativf_accidental=nat, tuning_system=twelvf_edo)
    f_sharp = make(Note, notf_name=f, relativf_accidental=sharp, tuning_system=twelvf_edo)
    f_flat = make(Note, notf_name=f, relativf_accidental=flat, tuning_system=twelvf_edo)
    f_dblsharp = make(Note, notf_name=f, relativf_accidental=doublf_sharp, tuning_system=twelvf_edo)
    f_dblflat = make(Note, notf_name=f, relativf_accidental=doublf_flat, tuning_system=twelvf_edo)

    g_nat = make(Note, notg_name=g, relativg_accidental=nat, tuning_system=twelvg_edo)
    g_sharp = make(Note, notg_name=g, relativg_accidental=sharp, tuning_system=twelvg_edo)
    g_flat = make(Note, notg_name=g, relativg_accidental=flat, tuning_system=twelvg_edo)
    g_dblsharp = make(Note, notg_name=g, relativg_accidental=doublg_sharp, tuning_system=twelvg_edo)
    g_dblflat = make(Note, notg_name=g, relativg_accidental=doublg_flat, tuning_system=twelvg_edo)

    assign_twelve_edo_cell_intervals(a_nat, a_sharp, m2)

    cell_1 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=1)
    cell_2 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=2)
    cell_3 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=3)
    cell_4 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=4)
    cell_5 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=5)
    cell_6 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=6)
    cell_7 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=7)
    cell_8 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=8)
    cell_9 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=9)
    cell_10 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=10)
    cell_11 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=11)
    cell_12 = make(Enharmonic, tuning_system=twelve_edo, chromatic_number=12)

    # cell_1: A Cell
    enh(1, a_nat)
    enh(1, b_dblflat)
    enh(1, g_dblsharp)

    # cell_2: A# Cell
    enh(2, b_flat)
    enh(2, a_sharp)
    enh(2, c_dblflat)

    # cell_3: B Cell
    enh(3, c_flat)
    enh(3, b_nat)
    enh(3, a_dblsharp)

    # cell_4: C Cell
    enh(4, d_dblflat)
    enh(4, c_nat)
    enh(4, b_sharp)

    # cell_5: C# Cell
    enh(5, d_flat)
    enh(5, c_sharp)
    enh(5, b_dblsharp)

    # cell_6: D Cell
    enh(6, e_dblflat)
    enh(6, d_nat)
    enh(6, c_dblsharp)

    # cell_7: D# Cell
    enh(7, f_dblflat)
    enh(7, e_flat)
    enh(7, d_sharp)

    # cell_8: E Cell
    enh(8, f_flat)
    enh(8, e_nat)
    enh(8, d_dblsharp)

    # cell_9: F Cell
    enh(9, g_dblflat)
    enh(9, f_nat)
    enh(9, e_sharp)

    # cell_10: F# Cell
    enh(10, g_flat)
    enh(10, f_sharp)
    enh(10, e_dblsharp)

    # cell_11: G Cell
    enh(11, a_dblflat)
    enh(11, g_nat)
    enh(11, f_dblsharp)

    # cell_12: G# Cell
    enh(12, g_sharp)
    enh(12, a_flat)




def safe_seed():
    try:
        prime = Administrarion.objects.get(username='Prime')
    except Exception as e:
        prime = make(Administrarion, username="Prime")
    
    do_seed(prime)


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        safe_seed()