class Problem(object):
    def __init__(self, Locations, Max_Places, Students, Preferences, _strongConstraints, _weakConstraints):
        self.sep = "_"
        self.L = Locations
        self.M = Max_Places
        self.S = Students
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

    def getSolutionAsStr(self):
        res = ""
        for i in range(len(self.X)):
            res += f"{self.S[i]} est de garde le "
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
                    candi.append(self.S[i])
            res += " et ".join(candi)
            res += "\n"
        return res

    def getSolutionAsCSV(self): #TODO
        res = "Students\\Dates,"
        res += ",".join(self.L)
        res += "\n"
        for i, s in enumerate(self.S):
            res += self.S[i] + ","
            for j, xij in enumerate(self.X[i]):
                if xij != 0:
                    res += "X"
                res += ","
            res = res[:-1] + "\n"
        return res
