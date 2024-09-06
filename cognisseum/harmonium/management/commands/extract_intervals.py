import json
from pathlib import Path
import csv
from django.core.management.base import BaseCommand, CommandError

this = Path(__file__)
here = this.parent
up_one = here.parent
data_dir = up_one / "data"
eis = data_dir / "eis.csv"


class MatrixEntry:

    def __repr__(self):
        return f"{self.value} ({self.list_ind}, {self.elem_ind})"

    def __init__(self, value, top_ind, bot_ind):
        self.value = value
        self.list_ind = top_ind
        self.elem_ind = bot_ind


def flatten(xs, cond, top_ind=0, bot_ind=0):
    acc = []
    print(top_ind)
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
        if x.value not in ys:
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
        print(dedupe(unique_intervals))
        intervals_minus_unison = unique_intervals[1:]
            