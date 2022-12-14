import logging
import os
import re
from enum import Enum
from datetime import datetime

from typing import (
    Callable,
    Iterable,
    Tuple,
    List,
    TypeVar,
    Union,
)
import itertools

T = TypeVar('T')


class Satisfiablity(str, Enum):
    SAT = "SAT"
    UNSAT = "UNSAT"
    UNKNOWN = "UNKNOWN"  # Actual result unknown
    UNSURE = "UNSURE"  # Could not find satisfiability


def satisfiability_of_output(output: str) -> Satisfiablity:
    # TODO liklely faster to do 'sat' in output.lower() or something
    if re.search('Unsat', output):
        return Satisfiablity.UNSAT
    elif re.search('Sat', output):
        return Satisfiablity.SAT
    elif re.search('Unknown', output):
        return Satisfiablity.UNKNOWN
    return Satisfiablity.UNSURE


def valid_smt(filename: Union[bytes, str]) -> bool:
    if os.fspath(filename).endswith('.smt'):
        return True
    else:
        return False


def partition(pred: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[List[T], List[T]]:
    "Use a predicate to partition entries into true entries and false entries"
    # partition(is_odd, range(10)) --> 1 3 5 7 9 and 0 2 4 6 8
    t1, t2 = itertools.tee(iterable)
    return list(filter(pred, t2)), list(itertools.filterfalse(pred, t1))


def now_string() -> str:
    """Returns the time in a %Y-%m-%d-%H-%M-%S formatted string"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d-%H-%M-%S")


def setup_logging_default():
    logging.basicConfig(filename=f'log-{now_string()}.txt', level=logging.INFO)
