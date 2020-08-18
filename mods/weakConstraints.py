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


@weakConstraint
class AccountPreferences(WeakConstraint):
    def getMinValue(self, problem):
        return 0

    def getMaxValue(self, problem):
        return 0

    def getWeight(self):
        return 100

    def computeConstraint(self, problem):
        for i in range(len(problem.S)):
            for j in range(len(problem.L)):
                if (problem.S[i] in problem.getCandidatesForDate(j)):
                    for k in range(problem.M):
                        self.addTerm(-1, problem.prettyPrintVar("x",i,j,k))
