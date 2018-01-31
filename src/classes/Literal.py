class Literal:
    def __init__(self, var, neg):
        self.var = var
        self.neg = neg

    def __str__(self):
        print_literal = ""

        if self.neg == 0:
            print_literal = print_literal + self.var
        else:
            print_literal = print_literal + "-" + self.var

        return print_literal

    def variable(self):
        return self.var

    def evaluation(self, intp):
        if self.var not in intp.map.keys():
            return False
        return intp.map[self.var] != self.neg

    def __key(self):
        return self.var, self.neg

    def __eq__(self, other):
        if self.var == other.var and self.neg == other.neg:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__key())
