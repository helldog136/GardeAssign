from servicepicker.problem.constraint import *

##########
# constraint:AccountPreferences
# type:weak
##########

@weakConstraint
class EquilibriumS(WeakConstraint):
    def getMinValue(self, problem):
        return 0

    def getMaxValue(self, problem):
        return 0

    def getWeight(self):
        return 50

    def computeConstraint(self, problem):
        self.addTerm(1, "s")
@weakConstraint
class EquilibriumW(WeakConstraint):
    def getMinValue(self, problem):
        return 0

    def getMaxValue(self, problem):
        return 0

    def getWeight(self):
        return 50

    def computeConstraint(self, problem):
        self.addTerm(1, "w")
@weakConstraint
class EquilibriumT(WeakConstraint):
    def getMinValue(self, problem):
        return 0

    def getMaxValue(self, problem):
        return 0

    def getWeight(self):
        return 100

    def computeConstraint(self, problem):
        self.addTerm(1, "t")
        # for i in range(len(problem.S)):
        #     for j in range(len(problem.P[i])):
        #         weight = problem.P[i][j]
        #         if weight == "":
        #             weight = str(len(problem.L))
        #         weight = len(problem.L) - int(weight)
        #         self.addTerm(-(weight), problem.prettyPrintVar("x", i, j))

