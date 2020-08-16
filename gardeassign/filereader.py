
def readChoices(choicesfilename):
    nbPlaces = 0
    dates = []
    candidates = []
    students = []
    placesLine = True
    datesLine = True
    with open(choicesfilename) as f:
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

    return nbPlaces, dates, candidates, students
