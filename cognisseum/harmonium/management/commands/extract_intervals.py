import json
from pathlib import Path
import csv
from django.core.management.base import BaseCommand, CommandError
from random import randint
from enum import Enum, auto
import re

this = Path(__file__)
here = this.parent
up_one = here.parent
data_dir = up_one / "data"
eis = data_dir / "eis.csv"

class Invertibility(Enum):
    Invertible = auto()
    Noninvertible = auto()


class CoOrd:

    def __lt__(self, other):
        return (((self[0]**2) + (self[1]**2))**1/2) < (((other[0]**2) + (other[1]**2))**1/2)

    def __invert__(self):
        return self.inverse_to_transverse()


    def __neg__(self):
        return self.determine_topleft()

    def __eq__(self, other):
        if isinstance(other, CoOrd):
            return self[0] == other[0] and self[1] == other[1]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.t1}, {self.t2})"

    def __hash__(self):
        return hash((self.t1, self.t2))

    def __getitem__(self, index):
        if index == 0:
            return self.t1
        elif index == 1:
            return self.t2

    def __init__(self, t1, t2, chunk_width=5, chunk_height=5):
        self.t1 = t1
        self.t2 = t2
        self.width = chunk_width
        self.height = chunk_height


    def relative_to_other(self, other):
        return (self[0] - other[0], self[1] - other[1])

    def relative_to_topleft(self):
        return self.relative_to_other(self.determine_topleft())

    def relative_to_transverse(self):
        if self.is_above_transverse():
            return self.relative_to_other(self.transverse_shadow())
        else:
            return self.transverse_shadow().relative_to_other(self)

    def total_inverse(self):
        return (self[1], self[0])

    def inverse_to_topleft(self):
        topleft = self.determine_topleft()
        diff = self.relative_to_topleft()
        return CoOrd(topleft[0] + diff[1], topleft[1] + diff[0])

    def determine_topleft(self):
        if (self.t1 % 5) == 0:
            t1 = self.t1 - 1
        else:
            t1 = self.t1
        return CoOrd(((t1 // self.width) * self.width) + 1, (self.t2 // self.height) * self.height)

    def is_above_transverse(self):
        return (self[0] - 1) < self[1]

    def is_on_transverse(self):
        return (self[0] - 1) == self[1]

    def is_within_transverse(self):
        return self.determine_topleft().is_on_transverse()

    def is_below_transverse(self):
        return (self[0] - 1) > self[1]

    def offset_chunk_from_transverse(self):
        return self.determine_topleft().relative_to_transverse()

    def inverse_to_transverse(self):
        topleft = self.determine_topleft()
        shadow = self.transverse_shadow()
        topleft_rel = self.relative_to_topleft()
        offset = self.offset_chunk_from_transverse()
        if self.is_below_transverse():
            inverse_topleft = CoOrd(shadow[0] - offset[1], shadow[1])
            inverse = CoOrd(inverse_topleft[0] + topleft_rel[1], inverse_topleft[1] + topleft_rel[0])
        elif self.is_above_transverse():
            inverse_topleft = CoOrd(shadow[0], shadow[1] + offset[0])
            inverse = CoOrd(inverse_topleft[0] + topleft_rel[1], inverse_topleft[1] + topleft_rel[0])
        elif self.is_within_transverse() or self.is_on_transverse():
            inverse = self.inverse_to_topleft()
        else:
            pass
        return inverse

    def transverse_shadow(self):
        if self.is_on_transverse():
            return self
        elif self != self.determine_topleft():
            return self.determine_topleft().transverse_shadow()
        elif self.is_above_transverse() and self == self.determine_topleft():
            return CoOrd(self[1] + 1, self[1] + 1).determine_topleft()
        elif self.is_below_transverse() and self == self.determine_topleft():
            return CoOrd(self[0] + 1, self[0] + 1).determine_topleft()



class MatrixEntry:

    def __invert__(self):
        return {self.coord: self.value}

    def __repr__(self):
        return f"{self.value} ({self.list_ind}, {self.elem_ind})"

    def __init__(self, value, top_ind, bot_ind):
        self.value = value
        self.list_ind = top_ind
        self.elem_ind = bot_ind
        self.coord = CoOrd(top_ind, bot_ind)


class HashMatrix:

    def __len__(self):
        return len(self.hash_xs)

    def __iter__(self):
        yield from self.hash_xs

    def __repr__(self):
        return str(self.hash_xs)

    def __getitem__(self, ind):
        if isinstance(ind, tuple):
            return self[CoOrd(*ind)]
        elif isinstance(ind, CoOrd):
            return self.hash_xs[ind]


    def __init__(self, xs, subindex):
        self.hash_xs = {}
        self.xs = xs
        for x in xs:
            self.hash_xs |= ~x



        

def flatten(xs, cond, top_ind=0, bot_ind=0):
    acc = []
    for x in xs:
        if isinstance(x, list):
            diff, diff_ind = flatten(x, cond, top_ind, bot_ind)
            acc += diff
            top_ind = diff_ind + 1
        elif cond(x):
            acc += [MatrixEntry(x, top_ind, bot_ind)]
            bot_ind += 1
    return (acc, top_ind)


def dedupe(xs):
    ys = []
    for x in xs:
        if x.value not in [y.value for y in ys]:
            ys += [x]
    return ys


class InverseMatrix:

    def __repr__(self):
        return f"{self.xs}"

    def __init__(self, xs, hash_matrix):
        self.xs = {}
        self.h = hash_matrix
        for x in xs:
            if x[0] != x[1] and not(x[0].is_within_transverse()):
                if self.has_same_chunk_qualities(x[0], x[1]) and self.is_perfect(x[0]):
                    self.xs |= {x[0]: x[1]}
                elif not(self.has_same_chunk_qualities(x[0], x[1])) and not(self.is_perfect(x[0])):
                    self.xs |= {x[0]: x[1]}
        
    def print_inverses(self):
        ys = {self.h[x]: self.h[self.xs[x]] for x in self.xs}
        acc = ""
        for y in ys:
            acc += f"\n{y} {ys[y]}"
        return acc

    def metaprogram(self):
        ys = {self.h[x]: self.h[self.xs[x]] for x in self.xs}
        zs = {}
        for y in ys:
            if y in zs or y in zs.values():
                pass
            else:
                zs |= {y:ys[y]}
        acc = ""
        i = 0
        zs |= {
                "P8": "P1", 
                "A8": "d1", 
                "AA8": "dd1", 
                "AAA8": "ddd1",
                "AAAA8": "dddd1",
                "A1": "d8",
                "AA1": "dd8",
                "AAA1": "ddd8",
                "AAAA1": "dddd8"
            }
        for z in zs:
            acc += f"\nadd_interval_inversion({z}, {zs[z]})"
            i += 1
        return acc

    def quality_of_chunk(self, n):
        return self.h[n.determine_topleft()][0]

    def has_same_chunk_qualities(self, n1, n2):
        return self.quality_of_chunk(n1) == self.quality_of_chunk(n2)
    
    def is_perfect(self, n):
        return self.quality_of_chunk(n) == "P"


def get_good_random():
    c = CoOrd(randint(least_x, max_x), randint(least_y, max_y))
    if c.flag == Invertibility.Noninvertible:
        return get_good_random()
    else:
        return c


i = re.compile("([A-Z]+|[a-z]+)([0-9])")

def parse_interval(x):
    qual_desc = {
        "P": "perf_int",
        "A": "aug_int",
        "AA": "dbl_aug_int",
        "AAA": "trpl_aug_int",
        "AAAA": "qdrpl_aug_int",
        "AAAAA": "pntpl_aug_int",
        "d": "dim_int",
        "dd": "dbl_dim_int",
        "ddd": "trpl_dim_int",
        "dddd": "qdrpl_dim_int",
        "ddddd": "pntpl_dim_int",
        "M": "major_int",
        "m": "minor_int"
    }

    step_desc = {
        "1": "First",
        "2": "Second",
        "3": "Third",
        "4": "Fourth",
        "5": "Fifth",
        "6": "Sixth",
        "7": "Seventh",
        "8": "Eighth"
    }
    qual, step = i.search(x).groups()

    return (x, qual_desc[qual], step)

def desc_to_dto(x):
    x, qual, step = parse_interval(x)
    return (f"{x} = make(Interval, quality={qual}, symbol='{step}')", step)

i = re.compile("([A-G])(b+|#+)*")

def desc_to_note(x):
    desc = {
        "##": "_dblsharp",
        "#": "_sharp",
        "b": "_flat",
        "bb": "_dblflat",
        None: "_nat"
    }

    name, acdntl = i.search(x).groups()
    return (name.lower(), desc[acdntl])


def make_eis_dto(n1, n2, i):
    n1 = "".join(desc_to_note(n1))
    n2 = "".join(desc_to_note(n2))
    return f"assign_twelve_edo_cell_intervals({n1}, {n2}, {i})"


class MetaProgrammer:

    def __init__(self, xs, names):
        self.h = HashMatrix(xs, 5)
        self.i = InverseMatrix([(x, ~x) for x in self.h], self.h)
        self.row_int = names
        self.col_int = [(x[0], x[1] - 1) for x in names]

    def intervals(self):
        uniques = [x.value for x in dedupe(self.h.xs)]
        uniques = sorted([desc_to_dto(x) for x in uniques], key=lambda x: x[1])
        return "\n".join([x[0] for x in uniques])

    def interval_inversions(self):
        return self.i.metaprogram()

    def interval_spellings(self):
        a = [x for x in self.h if x[0] - 1 > x[1]]
        acc = []
        for x in a:
            r = [y for y in self.row_int if y[1] == x[0]][0][0]
            c = [y for y in self.col_int if y[1] == x[1]][0][0]
            acc += [make_eis_dto(r, c, self.h[x])]
        return acc


class Command(BaseCommand):
    help = "ETL for enharmonic interval spellings"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open(eis, newline='') as f:
            read = csv.reader(f, delimiter=',')
            raw = [x for x in read]
        int_map = {x:raw[0].index(x) for x in raw[0]}
        i = [(x, int_map[x]) for x in int_map if x != '']
        unique_intervals, _throw = flatten(raw, lambda x: x not in int_map)
        mp = MetaProgrammer(unique_intervals, i)
        print("\n".join(mp.interval_spellings()))


        # randoms for testing
        # max_x = max([x[0] for x in hash_matrix])
        # least_x = min([x[0] for x in hash_matrix])
        # max_y = max([x[1] for x in hash_matrix])
        # least_y = min([x[1] for x in hash_matrix])
        # random = CoOrd(randint(least_x, max_x), randint(least_y, max_y))
        
