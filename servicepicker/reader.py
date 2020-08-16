from servicepicker.problem import Problem, getStrongConstraints, getWeakConstraints


def parse(concordances, filename):
    nbPlaces = 0
    dates = []
    candidates = []
    students = []
    days = []
    concordance = {}
    placesLine = True
    datesLine = True
    with open(concordances) as cf:
        for line in cf:
            splittedLine = line.strip().split(',')
            concordance[splittedLine[0]] = splittedLine[1]
    with open(filename) as f:
        for line in f:
            splittedLine = line.strip().split(',')
            if placesLine:
                placesLine = False
                nbPlaces = int(splittedLine[1])
            elif datesLine:
                datesLine = False
                dates = splittedLine[1:]
                for i in dates:
                    candidates.append([])
            else:
                student = splittedLine[0]
                students.append(student)
                for i, v in enumerate(splittedLine[1:]):
                    if v != "":
                        candidates[i].append(student)
    return Problem(dates, nbPlaces, students, candidates, concordance, getStrongConstraints(), getWeakConstraints())

if __name__ == "__main__":
    print(parse("input.csv").write())