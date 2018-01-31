"""
    DPLL Algorithm: (See: https://en.wikipedia.org/wiki/DPLL_algorithm)
"""
from src.dpll import is_cnf_satisfiable

print str(is_cnf_satisfiable("(-a || -b || c || d) && (c || d || -b) && (-c || -d || -f || d) && "
                             "(-d || c || -f) && (c) && (-c || -d || -e || b) && (-c || d || d || e)"))
