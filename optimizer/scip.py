import subprocess, tempfile, os


outfile = tempfile.gettempdir() + os.sep + "servicepicker_output"


def _runCommand(cmd):
    print("Running command")
    subprocess.getoutput(cmd)
    file = open(outfile, "r")
    res = ""
    for line in file:
        res += line
    print(res)
    return res


def _createBatch(filePath):
    text  = "read "+filePath+"\n"
    text += "optimize\n"
    text += "write solution "+outfile+"\n"
    text += "quit"

    file = open(outfile, "w")
    file.write(text)
    file.flush()
    file.close()
    return outfile


def _getSolverOutput(filePath):
    batchPath = _createBatch(filePath)
    return _runCommand("scip -b " + batchPath)


class InfeasibleError(ValueError):
    pass


def _extractSolution(output):
    print("_extractSolution\n\n"+output+"\n\nEND")
    lines = output.split("\n")
    res = {}
    res["status"] = lines[0].split(":")[1].strip()
    if res["status"] == "infeasible":
        raise InfeasibleError()
    res["value"] = float(lines[1].split(":")[1].strip())
    res["solution"] = []
    for i in range(2,len(lines)-1):
        ln = lines[i].split("\t")[0].split(" ")
        res["solution"].append((ln[0], float(ln[-2])))
    print("-"*80)
    return res


def solve(problem, filePath = tempfile.gettempdir() + os.sep + "pb.lp"):
    with open(filePath, "w") as f:
        toWrite = problem.write()
        f.write(toWrite)

    sol = _extractSolution(_getSolverOutput(filePath))
    problem.setSolution(sol)

    return sol