import imp
import json
import os
from unittest import mock

from solveio.config import THEIRS
from solveio.util import (get_problems, get_solutions, get_module_name)


fake_module = mock.Mock()
fake_module.generate.return_value = []
fake_module.compute.return_value = None

def _get_module(module_path):
    try:
        module = imp.load_source(get_module_name(module_path),
                                 module_path)
    except Exception as exc:
        # TODO(cmin): log this message
        print("Load: {}".format(exc))
        return fake_module
    return module


def generate_input_output():
    """Build input/output pairs for each solution."""
    for solution in get_solutions():
        # get and load solution module
        module_path = solution[0]
        module = _get_module(module_path)
        module_dir, module_name = os.path.split(module_path)
        module_name = get_module_name(module_name)
        # generate input data and obtain output
        input_fpath, output_fpath = map(
            lambda ext: os.path.join(
                module_dir,
                "{}.{}".format(module_name, ext)
            ),
            ["in", "out"]
        )
        # and write them to disk
        with open(input_fpath, "w") as input_fout, \
              open(output_fpath, "w") as output_fout:
            for data in module.generate():
                input_fout.write("{}\n".format(json.dumps(data)))
                output_fout.write("{}\n".format(
                        json.dumps(module.compute(data))
                    )
                )


def _testio(module, idata, odata):
    # test the module logic
    # TODO(cmin): do this in a safer manner
    _odata = module.compute(idata)
    return _odata == odata


def check_input_output(user, problem_name):
    """Verify if their output matches ours."""
    solutions = get_solutions()
    problems = get_problems(path=os.path.join(THEIRS, user))
    sol_match = prob_match = None
    for solution in solutions:
        if get_module_name(solution[0]) == problem_name:
            sol_match = solution
    for problem in problems:
        if get_module_name(problem) == problem_name:
            prob_match = problem
    if not all([sol_match, prob_match]):
        return None    # no solution or user problem found
    # try to compute a score
    module = _get_module(prob_match)
    tests = 0
    ok = 0
    with open(sol_match[1], "r") as input_fin, \
            open(sol_match[2], "r") as output_fin:
        while True:
            input_line = input_fin.readline().strip()
            output_line = output_fin.readline().strip()
            if not all([input_line, output_line]):
                break
            tests += 1
            if _testio(module, json.loads(input_line),
                       json.loads(output_line)):
                ok += 1
    if not tests:
        print("No tests found for {} in {}".format(user, problem_name))
        return -1
    return ok / tests * 100
