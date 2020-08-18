from servicepicker.problem.constraint import strongConstraint, StrongConstraint

##########
# constraint: AllPlacesTaken
# type: strong
##########

@strongConstraint
class AllPlacesTaken(StrongConstraint):
    def computeConstraint(self, problem):
        # sum_jk xijk = M
        res = []
        for j in range(len(problem.L)):
            res.append([])
        for j in range(len(problem.L)):
            for i in range(len(problem.S)):
                for k in range(problem.M):
                    res[j].append((1, problem.prettyPrintVar("x", i, j, k)))

        for i, resp in enumerate(res):
            self.addTerm(resp, "=", problem.M)

    def checkValidity(self, X, L, M, S, P): # not implemented, will crash
        res = True
        wrongs = []
        return (res, wrongs)


##########
# constraint: NoMoreStudentThanPlaces
# type: strong
##########

@strongConstraint
class StudentOncePerDay(StrongConstraint):
    def computeConstraint(self, problem):
        # sum_ik xijk <= 1
        res = []
        for i in range(len(problem.S)):
            res.append([])
            for j in range(len(problem.L)):
                res[i].append([])
        for i in range(len(problem.S)):
            for j in range(len(problem.L)):
                for k in range(problem.M):
                    res[i][j].append((1, problem.prettyPrintVar("x", i, j, k)))

        for i, resp in enumerate(res):
            for j, respj in enumerate(resp):
                self.addTerm(respj, "<=", 1)

    def checkValidity(self, X, L, M, S, P):
        res = True
        wrongs = []
        return (res, wrongs)

##########
# constraint: NoMoreStudentThanPlaces
# type: strong
##########

@strongConstraint
class AccountPreferences(StrongConstraint):
    def computeConstraint(self, problem):
        # for each date look at preference. if no one has put a preference, allow anyone
        # else prevent others to being assigned
        res = []
        res1 = []
        for j in range(len(problem.L)):
            res.append([])
            res1.append([])
        for j in range(len(problem.L)):
            candidates = problem.getCandidatesForDate(j)
            print("candidtes"+problem.L[j] + str(candidates))
            if len(candidates) < 2: # add vetos. Case 1 is handled in weak Account Prefs
                for i in range(len(problem.S)):
                    if problem.S[i] not in candidates:
                        for k in range(problem.M):
                            res[j].append((1, problem.prettyPrintVar("x", i, j, k)))
            if len(candidates) == 1:
                res1[j].append((1, problem.prettyPrintVar("x", problem.S.index(candidates[0]), j, 0)))
        res = filter(lambda i: len(i) > 0, res)
        res1 = filter(lambda i: len(i) > 0, res1)

        for i, resp in enumerate(res):
            self.addTerm(resp, "=", 0)
        for i, resp in enumerate(res1):
            self.addTerm(resp, "=", 1)

    def checkValidity(self, X, L, M, S, P):
        res = True
        wrongs = []
        return (res, wrongs)

@strongConstraint
class LimitS(StrongConstraint):
    def computeConstraint(self, problem):
        numberOfWeekDays = len(list(filter((lambda d: not problem.isWeekend(d)), range(len(problem.L)))))
        self.addTerm([(1, "s")], "<=", numberOfWeekDays)

    def checkValidity(self, X, L, M, S, P):
        res = True
        wrongs = []
        return (res, wrongs)

@strongConstraint
class LimitW(StrongConstraint):
    def computeConstraint(self, problem):
        numberOfWeekEndDays = len(list(filter((lambda d: problem.isWeekend(d)), range(len(problem.L)))))
        self.addTerm([(1, "w")], "<=", numberOfWeekEndDays)

    def checkValidity(self, X, L, M, S, P):
        res = True
        wrongs = []
        return (res, wrongs)

@strongConstraint
class LimitT(StrongConstraint):
    def computeConstraint(self, problem):
        self.addTerm([(1, "t")], "<=", len(problem.L))

    def checkValidity(self, X, L, M, S, P):
        res = True
        wrongs = []
        return (res, wrongs)

@strongConstraint
class EqStudents(StrongConstraint):
    def computeConstraint(self, problem):
        # sum_ik xijk <= 1
        ress = []
        resw = []
        rest = []
        for i in range(len(problem.S)):
            ress.append([])
            resw.append([])
            rest.append([])
        for i in range(len(problem.S)):
            for j in range(len(problem.L)):
                for k in range(problem.M):
                    rest[i].append((1, problem.prettyPrintVar("x", i, j, k)))
                    if problem.isWeekend(j):
                        resw[i].append((1, problem.prettyPrintVar("x", i, j, k)))
                    else:
                        ress[i].append((1, problem.prettyPrintVar("x", i, j, k)))

        for i, resp in enumerate(ress):
            self.addTerm(resp + [(-1, "s")], "<=", 0)
        for i, resp in enumerate(resw):
            self.addTerm(resp + [(-1, "w")], "<=", 0)
        for i, resp in enumerate(rest):
            self.addTerm(resp + [(-1, "t")], "<=", 0)

    def checkValidity(self, X, L, M, S, P):
        res = True
        wrongs = []
        return (res, wrongs)



@strongConstraint
class NoSuccessiveDates(StrongConstraint):
    def computeConstraint(self, problem):
        # sum_ik xijk <= 1
        res = []
        for i in range(len(problem.S)):
            res.append([])
            for j in range(len(problem.L)-2):
                res[i].append([])
        for i in range(len(problem.S)):
            for j in range(len(problem.L)-2):
                for k in range(problem.M):
                    res[i][j].append((1, problem.prettyPrintVar("x", i, j, k)))
                    res[i][j].append((1, problem.prettyPrintVar("x", i, j+1, k)))
                    res[i][j].append((1, problem.prettyPrintVar("x", i, j+2, k)))

        for i, resp in enumerate(res):
            for j, respj in enumerate(resp):
                self.addTerm(respj, "<=", 1)

    def checkValidity(self, X, L, M, S, P):
        res = True
        wrongs = []
        return (res, wrongs)
