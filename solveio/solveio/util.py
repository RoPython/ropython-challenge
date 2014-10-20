import os
import re

from solveio.config import PROBLEMS, SOLUTIONS


def _check_problem(fname):
    return bool(re.match(r"^\w\.py$", fname))


def split_name_ext(fname):
    chunks = fname.split(".")
    return chunks[0], ".".join(chunks[1:])


def get_module_name(fpath):
    fname = os.path.basename(fpath)
    return split_name_ext(fname)[0]


def get_problems(path=PROBLEMS):
    """Returns a list with all the problems."""
    fpaths = []
    for fname in os.listdir(path):
        if _check_problem(fname):
            fpaths.append(os.path.join(path, fname))
    return fpaths


def get_solutions():
    """Returns a list with tuples of problem
    solution, input and output file.
    """
    solutions = []
    for problem in get_problems():
        # get file name without extension
        fname = get_module_name(problem)
        # obtain source, input and output
        results = map(
            lambda ext: os.path.join(
                SOLUTIONS,
                "{}.{}".format(fname, ext)
            ),
            ["py", "in", "out"]
        )
        # filter paths by existance
        _results = []
        for result in results:
            if os.path.isfile(result):
                _result = result
            else:
                _result = None
            _results.append(_result)
        solutions.append(tuple(_results))
    return solutions
