'''The Representation Model'''
from typing import DefaultDict, Iterable, FrozenSet, NamedTuple, Optional, Set
from functools import reduce
from collections import defaultdict

RepSet = FrozenSet['Rep']

class Rep(NamedTuple):
    '''The Representation dataclass'''
    name: str
    content: RepSet = frozenset()


def repset(items: Optional[Iterable[Rep]] = None) -> RepSet:
    '''Helper function to build a RepSet from an iterable of Reps, <items>'''
    if items is None:
        return frozenset()
    contents = set()
    for rep in items:
        contents.add(Rep(rep.name, repset(rep.content)))
    return frozenset(contents)


def is_atomic(rep: Rep) -> bool:
    '''Returns whether or not <rep> has content'''
    return len(rep.content) == 0


def repset_get(rset: RepSet, name: str, recursive: bool = True) -> RepSet:
    '''Returns the sub-structure(s) with name = <name>'''
    results = set()
    for rep in rset:
        if recursive:
            results = results.union(repset_get(rep.content, name, recursive))
        if rep.name == name:
            results.add(rep)
    return repset(results)


def repset_sum(set_a: RepSet, set_b: RepSet) -> RepSet:
    '''Returns the sum of two RepSets'''
    content_groups: DefaultDict[str, Set[Rep]] = defaultdict(set)
    for rep in set_a.union(set_b):
        content_groups[rep.name].add(rep)

    results = set()
    for name in content_groups:
        all_content = [x.content for x in content_groups[name]]
        accum_content = reduce(repset_sum, all_content, repset())
        results.add(Rep(name, accum_content))
    return repset(results)


def repset_difference(set_a: RepSet, set_b: RepSet) -> RepSet:
    '''Returns the difference between two RepSets'''
    results = set()
    for rep in set_a:
        if not is_atomic(rep):
            for rep2 in repset_get(set_b, rep.name):
                results.add(Rep(rep.name, repset_difference(rep.content, rep2.content)))
        elif rep.name not in [x.name for x in set_b]:
            results.add(rep)

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

diff = repset_difference(repset_sum(x1, x2), x2)
print(diff)
# print(repset_get(diff, 'x'))
