'''The Representation Model'''
from typing import DefaultDict, Iterable, FrozenSet, Optional, Set
from functools import reduce
from collections import defaultdict
from dataclasses import dataclass


RepSet = FrozenSet['Rep']


@dataclass(frozen=True)
class Rep:
    '''The Representation dataclass'''
    name: str
    content: RepSet = frozenset()


def repset(items: Optional[Iterable[Rep]] = None) -> RepSet:
    '''Helper function to build a RepSet from an iterable of Reps, <items>'''
    if items is None:
        return frozenset()
    contents = set()
    for item in items:
        contents.add(Rep(item.name, repset(item.content)))
    return frozenset(contents)


def is_atomic(r: Rep) -> bool:
    '''Returns whether or not <rep> has content'''
    return len(r.content) == 0


def repset_get(rset: RepSet, name: str) -> RepSet:
    '''Returns the sub-structure(s) with name = <name>'''
    return repset(filter(
        lambda r: r.name == name,
        rset
    ))

def repset_names(rset: RepSet) -> Set[str]:
    '''Returns names of the first-children of <rset>'''
    return set([r.name for r in rset])


def repset_sum(set_a: RepSet, set_b: RepSet) -> RepSet:
    '''Returns the sum of two RepSets'''
    content_groups: DefaultDict[str, Set[RepSet]] = defaultdict(set)
    for r in set_a.union(set_b):
        content_groups[r.name].add(r.content)

    results = set()
    for name in repset_names(set_a).union(repset_names(set_b)):
        results.add(
            Rep(name, reduce(repset_sum, content_groups[name], repset()))
            )
    return repset(results)


def repset_sub(set_a: RepSet, set_b: RepSet) -> RepSet:
    '''Returns the difference between two RepSets'''
    results = set()
    for rep1 in set_a:
        if not is_atomic(rep1):
            for rep2 in repset_get(set_b, rep1.name):
                results.add(Rep(rep1.name, repset_sub(rep1.content, rep2.content)))
        elif len(repset_get(set_b, rep1.name)) == 0:
            results.add(rep1)
    return repset(results)


x1 = repset([
    Rep('x', repset([
                Rep('1', repset()),
                Rep('2', repset()),
                ])),
    Rep('y', repset([
                Rep('a'),
                Rep('b'),
                ]))
        ,])

x2 = repset([
    Rep('x', repset([
                Rep('3', repset()),
                ])),
    Rep('y', repset([
                Rep('c'),
                ]))
        ,])

diff = repset_sub(repset_sum(x1, x2), x2)
print(diff)
