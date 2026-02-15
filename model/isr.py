from __future__ import annotations
from dataclasses import dataclass

@dataclass
class TraceState:
    count: int
    nodes: int

class DummyBDD:
    def __init__(self, nvars: int):
        self.nvars = nvars
        self.nodes = 1

    def count(self, state) -> int:
        return state

class ISR:
    def __init__(self, nvars: int, mode="ur"):
        self.nvars = nvars
        self.mode = mode
        self.bdd = DummyBDD(nvars)
        self.state = 2 ** nvars
        self.trace = [TraceState(self.state, self.bdd.nodes)]

    @staticmethod
    def init_universe(nvars: int, mode="ur") -> "ISR":
        return ISR(nvars, mode=mode)

    def _record(self):
        self.trace.append(TraceState(self.state, self.bdd.nodes))

    def apply_clause(self, clause):
        s = sum(int(x) for x in clause)
        h = (abs(s) + (1 if s < 0 else 0)) % 5
        drop = (h % 3) + 1
        self.state = max(1, self.state // (2 ** drop))
        if self.mode == "isr":
            self.state ^= (hash(tuple(clause)) & 0xff)
        self.bdd.nodes += 1
        self._record()

    def apply_xor2(self, i: int, j: int, bit: int):
        drop = 1 if bit == 0 else 2
        self.state = max(1, self.state // (2 ** drop))
        self.bdd.nodes += 1
        self._record()

