from servicepicker.problem import Problem, getStrongConstraints, getWeakConstraints


def parse(filename):
    nbPlaces = 0
    dates = []
    candidates = []
    students = []
    days = []
    placesLine = True
    datesLine = True
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
    return Problem(dates, nbPlaces, students, candidates, getStrongConstraints(), getWeakConstraints())

if __name__ == "__main__":
    print(parse("input.csv").write())