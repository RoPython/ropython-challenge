import imp
import json
import os

from solveio.config import THEIRS
from solveio.util import (get_problems, get_solutions,
                          split_name_ext, get_module_name)


def _get_module(module_path)
    module = imp.load_source(get_module_name(module_path),
                             module_path)
    return module


def generate_input_output():
    """Build input/output pairs for each solution."""
    for solution in get_solutions():
        # get and load solution module
        module = _get_module(solution[0])
        module_name, module_dir = os.path.split(module_path)
        module_name = split_name_ext(module_name)[0]
        # generate input data and obtain output
        input_fpath, output_fpath = map(
            lambda ext: os.path.join(
                module_dir,
                "{}.{}".format(module_name, ext)
            ),
            ["in", "out"]
        )
        # and write them to disk
        with (open(input_fpath, "w") as input_fout,
              open(output_fpath, "w") as output_fout):
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
    with (open(sol_match[1], "r") as input_fin,
            open(sol_match[2], "r") as output_fin):
        input_line = input_fin.readline().strip()
        output_line = output_fin.readline().strip()
        tests += 1
        if _testio(module, json.loads(input_line),
                   json.loads(output_line)):
            ok += 1
    return ok / tests * 100
