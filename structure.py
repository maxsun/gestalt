
from __future__ import annotations
from os import name
from typing import List, Callable, Dict, Set, Tuple, Optional, Union
from dataclasses import dataclass
from functools import reduce


@dataclass(frozen=True)
class Structure:
    '''Represents a context'''
    content: Set[Tuple[str, 'Relation']]

    def __getitem__(self, key: str) -> Set[Relation]:
        results = set([])
        for named_rel in self.content:
            if named_rel[0] == key:
                results.add(named_rel[1])
        return results

    def get(self, key: str, arg: Optional[Structure]=None, ctx: Optional[Structure]=None) -> Structure:
        if arg is None:
            arg = Structure(set())
        if ctx is None:
            ctx = self
        try:
            a = Structure(set())
            for f in self[key]:
                a += f(ctx, arg)
            return a
        except KeyError:
            return Structure(set())

    def take(self, keys: List[str], arg: Optional[Structure]=None) -> Structure:
        results = set([])
        for named_rel in self.content:
            if named_rel[0] in keys:
                results.add(named_rel)
        return Structure(results)

    def __add__(self, other: Structure) -> Structure:
        return Structure(self.content.union(other.content))

    def __sub__(self, other: Structure) -> Structure:
        return Structure(self.content.intersection(other.content).union(self.content))


Relation = Callable[[Structure, Structure], Structure]

