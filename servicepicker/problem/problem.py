class Problem(object):
    def __init__(self, Locations, Max_Places, Students, Preferences, concordances, _strongConstraints, _weakConstraints):
        self.sep = "_"
        self.L = Locations
        self.M = Max_Places
        self.S = Students
        self.concordances = concordances
        if len(self.concordances) != len(self.S):
            print(f"Not same number of students ({len(self.S)}) and concordances ({len(self.concordances)})")
            exit(-1)
        self.P = Preferences
        self.strongConstraints = _strongConstraints
        self.weakConstraints = _weakConstraints
        self.value = None
        problemMatrix = []
        for i in range(len(self.S)):
            problemMatrix.append([])
            for j in range(len(self.P)):
                problemMatrix[i].append((True, []))
        self.validity = (True, [], [], [], [], problemMatrix)

        # init matrix X for decision variables
        self.X = []
        for i in range(len(self.S)):
            line1 = []
            for j in range(len(self.L)):
                line2 = []
                for k in range(self.M):
                    line2.append(0)
                line1.append(line2)
            self.X.append(line1)

    def write(self):
        obj = ""
        binr = ""
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                for k in range(len(self.X[i][j])):
                    obj += self.prettyPrintVar("x", i, j, k) + " + "
                    binr += self.prettyPrintVar("x", i, j, k) + "\n"

        for c in self.weakConstraints.getConstraints(self):
            print("weak\n------\n" + c + "\n---")
            obj = (obj[:-3] if c[:2] == " -" else obj) + str(c) + \
                  ("" if len(c) == 0 or c[-2:] == "+ " else " + ")
        obj = obj[:-2]

        cst = ""
        for c in self.strongConstraints.getConstraints(self):
            print("strong\n------\n" + c + "\n---")
            cst += str(c) + ("" if len(c) == 0 or c[-1] == "\n" else "\n")

        res = "Minimize\n"
        res += obj
        res += "\n"
        res += "Subject To\n"
        res += cst
        res += "Binary\n"
        res += binr
        res += "End"

        print(res)
        return res

    def getCandidatesForDate(self, dateindex):
        return self.P[dateindex]

    def isWeekend(self, dayindex):
        return self.L[dayindex][:3] in ["sam", "dim"]

    def checkValidity(self):
        validity = self.strongConstraints.checkValidities(self.X, self.L, self.M, self.S, self.P)
        wrongs_L = []
        wrongs_M = []
        wrongs_S = []
        wrongs_P = []
        problemMatrix = []
        for i in range(len(self.S)):
            problemMatrix.append([])
            for j in range(len(self.P)):
                problemMatrix[i].append((True, []))
        if not validity[0]:
            for problem in validity[1]:
                if problem[0] is False:
                    for w in problem[1]:
                        if w[0] >= 0:
                            wrongs_L.append((self.L[w[0]], problem[2], w))
                        if w[1] >= 0:
                            wrongs_M.append((self.M[w[1]], problem[2], w))
                        if w[2] >= 0:
                            wrongs_S.append((self.S[w[2]], problem[2], w))
                        if w[3] >= 0:
                            wrongs_P.append((self.P[w[3]], problem[2], w))

            # TODO synthetize what's wrong
            def printList(lst):
                res = ""
                for i in lst:
                    res += str(i) + ", "
                return res

            for v, p, reason in validity[1]:
                if v is False:
                    for (i, j, k, l) in p:
                        if i >= 0 and j >= 0:
                            problemMatrix[i][j] = (False, problemMatrix[i][j][1])
                            problemMatrix[i][j][1].append(reason)

            print("Problems in wrongs_L: " + printList(wrongs_L))
            print("Problems in wrongs_M: " + printList(wrongs_M))
            print("Problems with wrongs_S: " + printList(wrongs_S))
            print("Problems with wrongs_P: " + printList(wrongs_P))
            print(problemMatrix)

        self.validity = (validity[0], wrongs_L, wrongs_M, wrongs_S, wrongs_P, problemMatrix)

    def isValid(self):
        self.checkValidity()
        return self.validity[0]

    def prettyPrintVar(self, var, i, j, k):
        return var + self.sep + str(i) + self.sep + str(j) + self.sep + str(k)

    def resetSolution(self):
        for i in range(len(self.X)):
            for j in range(len(self.X[i])):
                self.X[i][j] = 0

    def setSolution(self, sol):
        # wipe data in X
        self.resetSolution()

        print(sol)

        for t in sol["solution"]:
            self._setSol(*t)
        self.value = sol["value"]
        self.checkValidity()

    def _setSol(self, var, val):
        if var[0] == "x":
            _, i, j, k = var.split(self.sep)
            i = int(i)
            j = int(j)
            k = int(k)
            print(f"Setting {self.S[i]} to {self.L[j]} ({k} - {val})")
            self.X[i][j] = int(val)

    def displaySolution(self):
        print(self.getSolutionAsStr())

    def getName(self, stu):
        return self.concordances.get(self.S[stu])

    def getSolutionAsStr(self):
        res = ""
        for i in range(len(self.X)):
            res += f"{self.getName(i)} est de garde le "
            candi = []
            for j in range(len(self.X[i])):
                if self.X[i][j] == 1:
                    candi.append(self.L[j])
            res += " et le ".join(candi)
            res += "\n"


        for j in range(len(self.L)):
            res += f"Le {self.L[j]}, les élus sont: "
            candi = []
            for i in range(len(self.S)):
                if self.X[i][j] == 1:
                    candi.append(self.getName(i))
            res += " et ".join(candi)
            res += "\n"
        return res

    def getSolutionAsCSV(self): #TODO
        res = "Students\\Dates,"
        res += ",".join(self.L)
        res += "\n"
        for i, s in enumerate(self.S):
            res += self.getName(i) + ","
            for j, xij in enumerate(self.X[i]):
                if xij != 0:
                    res += "X"
                res += ","
            res = res[:-1] + "\n"
        return res
