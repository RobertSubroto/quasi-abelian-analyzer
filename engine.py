# engine.py
import math
from sympy.ntheory.factor_ import multiplicity, divisors, totient
from sympy.ntheory.residue_ntheory import n_order
import itertools
import pandas as pd
from functools import reduce 

def var_nu(q, d_vec):
    orders = [n_order(q, n) if n > 1 else 1 for n in d_vec]
    return reduce(math.lcm, orders, 1)

def var_eta(q, d_vec):
    nominator = math.prod([totient(n) for n in d_vec])
    denominator = var_nu(q, d_vec)
    return int(nominator / denominator)

class GroupAlg:
    def __init__(self, p, t, param):
        self.p, self.t = p, t
        self.q = p ** t
        self.param = param
        self.dim = math.prod(param)
        self.radical_param = self.get_radical_param()
        self.localized_param = self.get_localized_param()
        self.is_local = (all(n == 1 for n in self.radical_param))
        self.is_semisimple = (all(n == 1 for n in self.localized_param))

        if self.is_local:
            self.complexity = 1
            self.components = None
        else:
            self.div_list = [list(item) for item in itertools.product(*[divisors(n) for n in self.radical_param])]
            self.complexity = sum([var_eta(self.q, n) for n in self.div_list])
            self.components = self.compute_components()

    def get_radical_param(self):
        temp = []
        for n in self.param:
            n_prime = n // (self.p ** multiplicity(self.p, n))
            if n_prime > 1: temp.append(n_prime)
        return temp if temp else [1]

    def get_localized_param(self):
        temp = []
        for n in self.param:
            m = multiplicity(self.p, n)
            if m > 0: temp.append(self.p ** m)
        return temp if temp else [1]

    def compute_components(self):
        temp_list = []
        for d_vec in self.div_list:
            nu_val = var_nu(self.q, d_vec)
            eta_val = var_eta(self.q, d_vec)
            comp = GroupAlg(self.p, self.t * nu_val, self.localized_param)
            temp_list.extend([comp] * eta_val)
        
        series = pd.Series(temp_list)
        df = series.value_counts().reset_index()
        df.columns = ['Component', 'Count']
        return df

    def __eq__(self, other):
        return isinstance(other, GroupAlg) and (self.p, self.t, tuple(self.param)) == (other.p, other.t, tuple(other.param))
    
    def __hash__(self):
        return hash((self.p, self.t, tuple(self.param)))

    def __repr__(self):
        return f"GF({self.p}^{self.t}){self.param}"