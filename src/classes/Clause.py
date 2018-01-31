class Clause:
    def __init__(self, literals):
        self.literals = literals

    def __str__(self):
        print_clause = "("

        for lit in self.literals[: -1]:
            print_clause = print_clause + lit.__str__() + " or "

        print_clause = print_clause + str(self.literals[-1]) + ")"

        return print_clause

    def get_variables(self):
        data_variables = []

        for var in self.literals:
            data_variables.append(var.variable())

        return set(data_variables)

    def evaluation(self, intp):
        for lit in self.literals:
            if lit.evaluation(intp):
                return True
        return False

    def get_number_of_unsigned_literals(self, intp):
        return set(self.get_variables()) - set(intp.definition())
