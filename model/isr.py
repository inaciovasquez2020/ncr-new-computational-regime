from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List

Var = int
Clause = List[int]

@dataclass(frozen=True)
class Node:
    var: int
    lo: int
    hi: int

class ROBDD:
    def __init__(self, nvars: int):
        self.nvars = nvars
        self.nodes: List[Node] = [Node(-1, 0, 0), Node(-1, 1, 1)]
        self.unique: Dict[Tuple[int,int,int], int] = {}
        self._count_memo: Dict[int, int] = {}

    def mk(self, var: int, lo: int, hi: int) -> int:
        if lo == hi:
            return lo
        key = (var, lo, hi)
        idx = self.unique.get(key)
        if idx is not None:
            return idx
        idx = len(self.nodes)
        self.nodes.append(Node(var, lo, hi))
        self.unique[key] = idx
        return idx

    def ite(self, f: int, g: int, h: int) -> int:
        # Shannon-style ITE for ROBDD using var order and memoization
        memo: Dict[Tuple[int,int,int], int] = {}

        def topvar(u: int) -> int:
            if u <= 1:
                return self.nvars + 1
            return self.nodes[u].var

        def cof(u: int, v: int, bit: int) -> int:
            if u <= 1:
                return u
            nu = self.nodes[u]
            if nu.var != v:
                return u
            return nu.hi if bit == 1 else nu.lo

        def rec(fu: int, gu: int, hu: int) -> int:
            key = (fu, gu, hu)
            if key in memo:
                return memo[key]
            if fu == 0:
                memo[key] = hu
                return hu
            if fu == 1:
                memo[key] = gu
                return gu
            if gu == hu:
                memo[key] = gu
                return gu

            v = min(topvar(fu), topvar(gu), topvar(hu))
            lo = rec(cof(fu, v, 0), cof(gu, v, 0), cof(hu, v, 0))
            hi = rec(cof(fu, v, 1), cof(gu, v, 1), cof(hu, v, 1))
            out = self.mk(v, lo, hi)
            memo[key] = out
            return out

        return rec(f, g, h)

    def var_bdd(self, var: int) -> int:
        return self.mk(var, 0, 1)

    def not_bdd(self, u: int) -> int:
        memo: Dict[int,int] = {}
        def rec(x: int) -> int:
            if x == 0:
                return 1
            if x == 1:
                return 0
            if x in memo:
                return memo[x]
            nx = self.nodes[x]
            lo = rec(nx.lo)
            hi = rec(nx.hi)
            out = self.mk(nx.var, lo, hi)
            memo[x] = out
            return out
        return rec(u)

    def and_bdd(self, a: int, b: int) -> int:
        return self.ite(a, b, 0)

    def or_bdd(self, a: int, b: int) -> int:
        return self.ite(a, 1, b)

    def xor_bdd(self, a: int, b: int) -> int:
        # a xor b = ite(a, not b, b)
        return self.ite(a, self.not_bdd(b), b)

    def count(self, u: int) -> int:
        # exact model count of assignments in {0,1}^nvars
        self._count_memo.clear()

        def rec(x: int, cur_var: int) -> int:
            if x == 0:
                return 0
            if x == 1:
                # remaining vars free
                return 1 << (self.nvars - cur_var)
            key = (x, cur_var)
            if key in self._count_memo:
                return self._count_memo[key]
            nx = self.nodes[x]
            # skip vars between cur_var and nx.var
            gap = nx.var - cur_var
            mul = 1 << gap
            lo = rec(nx.lo, nx.var + 1)
            hi = rec(nx.hi, nx.var + 1)
            out = mul * (lo + hi)
            self._count_memo[key] = out
            return out

        return rec(u, 0)

def clause_bdd(bdd: ROBDD, clause: Clause) -> int:
    # clause is list of ints in ±(i+1) DIMACS style
    acc = 0
    for lit in clause:
        v = abs(lit) - 1
        x = bdd.var_bdd(v)
        term = x if lit > 0 else bdd.not_bdd(x)
        acc = term if acc == 0 else bdd.or_bdd(acc, term)
    return acc

@dataclass
class ISRTraceStep:
    op: str
    detail: str
    nodes: int
    count: int

@dataclass
class ISR:
    nvars: int
    bdd: ROBDD
    state: int
    trace: List[ISRTraceStep]

    @staticmethod
    def init_universe(nvars: int) -> "ISR":
        bdd = ROBDD(nvars)
        # Universe = True
        state = 1
        trace = [ISRTraceStep(op="init", detail=f"universe n={nvars}", nodes=len(bdd.nodes), count=bdd.count(state))]
        return ISR(nvars=nvars, bdd=bdd, state=state, trace=trace)

    def apply_clause(self, clause: Clause) -> None:
        c = clause_bdd(self.bdd, clause)
        self.state = self.bdd.and_bdd(self.state, c)
        self.trace.append(ISRTraceStep(op="clause", detail=str(clause), nodes=len(self.bdd.nodes), count=self.bdd.count(self.state)))

    def apply_xor2(self, i: int, j: int, bit: int) -> None:
        xi = self.bdd.var_bdd(i)
        xj = self.bdd.var_bdd(j)
        x = self.bdd.xor_bdd(xi, xj)
        constraint = x if bit == 1 else self.bdd.not_bdd(x)
        self.state = self.bdd.and_bdd(self.state, constraint)
        self.trace.append(ISRTraceStep(op="xor2", detail=f"{i} xor {j} = {bit}", nodes=len(self.bdd.nodes), count=self.bdd.count(self.state)))

    def implicit_dimension_bits(self) -> float:
        import math
        cnt = self.bdd.count(self.state)
        if cnt <= 0:
            return float("-inf")
        return math.log2(cnt)
