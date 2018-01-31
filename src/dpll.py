from classes.Clause import Clause
from classes.Interpretation import Interpretation
from classes.Literal import Literal


def is_cnf_satisfiable(cnf):
    print 'We decide if the CNF is satisfiable'

    clauses_list = cnf.split(' && ')
    clauses = []
    symbols = []

    for cl in clauses_list:
        literals_list = cl[1:-1].split(' || ')
        literals = []

        for lit in literals_list:
            if '-' in lit:
                literals.append(Literal(lit.split('-')[1], True))
                symbols.append(lit.split('-')[1])
            else:
                literals.append(Literal(lit, False))
                symbols.append(lit)

        clauses.append(Clause(literals))

    return dpll(clauses, set(symbols), Interpretation({}))


def dpll(clauses, symbols, interpretation):
    print str(len(clauses)) + '\n'

    if not symbols or not clauses:
        if are_true_clauses(clauses, interpretation):
            print 'Found correct interpretation:'
            print str(interpretation)
            print '-------------------'

            return True
        else:
            return False

    lit = get_pure_symbols(clauses, symbols)
    if lit is not None:
        # Reduction
        symbols.remove(lit.var)
        new_clauses = list(clauses)

        # Elimination
        remove_satisfied_clause(new_clauses, lit)
        print 'Pure symbol ' + lit.var + ' eliminated, ' + lit.var \
              + ':' + str(not lit.neg)

        return dpll(new_clauses, symbols,
                    interpretation.union(Interpretation({lit.var: not lit.neg})))

    # Unit clause
    lit = get_unit_clause(clauses, symbols, interpretation)
    if lit is not None:
        # Reduction
        symbols.remove(lit.var)
        new_clauses = list(clauses)

        # Elimination
        remove_satisfied_clause(new_clauses, lit)
        print 'Unit clause ' + lit.var + ' eliminated, ' + lit.var \
              + ':' + str(not lit.neg)
        return dpll(new_clauses, symbols,
                    interpretation.union(Interpretation({lit.var: not lit.neg})))

    p = next(iter(symbols))
    print 'Variable ' + p + ' branching...'

    # Reduction

    symbols.remove(p)
    new_clauses1 = list(clauses)
    new_clauses2 = list(clauses)

    # Elimination

    remove_satisfied_clause(new_clauses1, Literal(p, False))
    remove_satisfied_clause(new_clauses2, Literal(p, True))

    # Split

    return dpll(new_clauses1,
                symbols,
                interpretation.union(Interpretation({p: True}))
                ) \
           or \
           dpll(
               new_clauses2,
               symbols,
               interpretation.union(Interpretation({p: False}))
           )


def get_pure_symbols(clauses, symbols):
    lst = []

    for cl in clauses:
        lst = lst + cl.literals

    short = set(lst)

    for s in symbols:
        if Literal(s, True) in short:
            if Literal(s, False) not in short:
                return Literal(s, True)

        elif Literal(s, False) in short:
            return Literal(s, False)

    return None


def get_unit_clause(clauses, symbols, interpretation):
    for cl in clauses:
        difference = cl.get_number_of_unsigned_literals(interpretation)

        if len(difference) == 1 and difference.issubset(symbols):
            var = next(iter(difference))

            for lit in cl.literals:
                if lit.var == var:
                    return lit

    return None


def are_true_clauses(clauses, interpretation):
    for cl in clauses:
        if not cl.evaluation(interpretation):
            return False

    return True


def remove_satisfied_clause(clauses, lit):
    odds = []

    for cl in clauses:
        for l in cl.literals:
            if lit == l:
                odds.append(cl)
                break

    for cl in odds:
        print 'Removing: ' + str(cl) + '\n'
        clauses.remove(cl)
