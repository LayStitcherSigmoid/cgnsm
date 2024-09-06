import json
from pathlib import Path
import csv
from django.core.management.base import BaseCommand, CommandError
from random import randint

this = Path(__file__)
here = this.parent
up_one = here.parent
data_dir = up_one / "data"
eis = data_dir / "eis.csv"

class CoOrd:

    def __invert__(self):
        return self.inverse_to_topleft()

    def __neg__(self):
        return self.determine_topleft()

    def __eq__(self, other):
        if isinstance(other, CoOrd):
            return self[0] == other[0] and self[1] == other[1]

    def __repr__(self):
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

    def inverse_to_topleft(self):
        topleft = self.determine_topleft()
        diff = self.relative_to_topleft()
        return CoOrd(topleft[0] + diff[1], topleft[1] + diff[0])

    def determine_topleft(self):
        return CoOrd(((self.t1 // self.width) * self.width) + 1, (self.t2 // self.height) * self.height)


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
        for x in xs:
            self.hash_xs |= ~x

    def coord_to_topleft(self, coord):
        pass

        

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


class Command(BaseCommand):
    help = "ETL for enharmonic interval spellings"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open(eis, newline='') as f:
            read = csv.reader(f, delimiter=',')
            raw = [x for x in read]
        int_map = {x:raw[0].index(x) for x in raw[0]}
        unique_intervals, _throw = flatten(raw, lambda x: x not in int_map)
        hash_matrix = HashMatrix(unique_intervals, 5)
        max_x = max([x[0] for x in hash_matrix])
        least_x = min([x[0] for x in hash_matrix])
        max_y = max([x[1] for x in hash_matrix])
        least_y = min([x[1] for x in hash_matrix])
        random = CoOrd(randint(least_x, max_x), randint(least_y, max_y))
        print(random, hash_matrix[random], -random, hash_matrix[-random], ~random, hash_matrix[~random])
            