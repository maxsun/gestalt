''' Some kind of information parser '''
from __future__ import annotations
from pprint import pformat
from dataclasses import dataclass
from typing import List, Callable, Dict, FrozenSet, Tuple, Optional, Union
import re
import hashlib


@dataclass(frozen=True)
class Context:
    '''Represents a context'''
    transforms: Dict[str, Callable[['Context', 'Context' ], 'Context']]

    def __getitem__(self, key: str) -> Callable[['Context', 'Context' ], 'Context']:
        return self.transforms[key]

    def __repr__(self):
        return pformat(self.transforms)

    def get(self, key: str, arg: Optional[Context]=None) -> Context:
        if arg is None:
            arg = Context({})
        return self.transforms[key](self, arg)

    def take(self, keys: List[str]) -> Context:
        result = {}
        for key in keys:
            if key in self.transforms:
                result[key] = self.transforms[key]
        return Context(result)


def _id(ctx: Context, arg: Context) -> Context:
    return arg


def t(ctx: Context, arg: Context) -> Context:
    return Context({})


def f(ctx: Context, arg: Context) -> Context:
    return Context({})


def _and(ctx: Context, arg: Context) -> Context:
    fst = arg['fst'] == ctx['true']
    snd = arg['snd'] == ctx['true']
    # print(arg.take(['fst']), arg.take(['snd']))
    return ctx.take(['true']) if fst and snd else ctx.take(['false'])


def _or(ctx: Context, arg: Context) -> Context:
    fst = arg['fst'] == ctx['true']
    snd = arg['snd'] == ctx['true']
    # print(arg.take(['fst']), arg.take(['snd']))
    return ctx.take(['true']) if fst or snd else ctx.take(['false'])


c = Context({
    'id': _id,
    'true': t,
    'false': f,
    'and': _and,
    'or': _or,
})

x = Context({
    'fst': c['true'],
    'snd': c['false']
})

print(c.get('and', x))
print(c.get('or', x))
