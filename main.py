#!/usr/bin/env python3
import sys
import servicepicker.problem.constraint as constraint
import os


def importMods():
    #clear old imports
    constraint.clearConstraints()
    # Import mods
    for module in os.listdir("mods"):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        __import__("mods", locals(), globals(), [module[:-3]])
    del module


def check_args(args): #TODO
    return args


if __name__ == "__main__":
    from optimizer import scip
    from servicepicker import reader
    importMods()
    args = sys.argv
    if(len(args) > 1):
        # console mode
        print("Starting in console mode...")
        args = check_args(args)
        ext = "." + args[1].split(".")[-1]

        problem = reader.parse(args[2], args[1])

        if problem is None:
            print("Unknown file format:", args[1].split(".")[-1])
            sys.exit(-1)

        res = scip.solve(problem)
        problem.displaySolution()
        with open(f"{args[1].split('.')[0]}_out.txt", 'w', encoding='utf-8') as outfile:
            outfile.write(problem.getSolutionAsStr())
        with open(f"{args[1].split('.')[0]}_out.csv", 'w', encoding='utf-8') as outfile:
            outfile.write(problem.getSolutionAsCSV())

