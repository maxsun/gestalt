'''The Perspective Model'''
from __future__ import annotations
from re import sub
from typing import DefaultDict, Iterable, FrozenSet, NamedTuple, Optional, Sequence, Set
from functools import reduce
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Stance:
    topic: str
    view: 'Perspective'

Perspective = FrozenSet[Stance]
# A Perspective is a set of Stance's, and Stances are perspectives towards topics.

def persp(stances: Iterable[Stance]) -> Perspective:
    '''Helper function; returns a Perspective from an iterable of Stances'''
    per = set()
    for stance in stances:
        per.add(stance)
    return frozenset(per)


def persp_topics(per: Perspective) -> Set[str]:
    topics = set()
    for stance in per:
        topics.add(stance.topic)
    return topics


def persp_get(per: Perspective, topic: str) -> Perspective:
    '''Returns the sub-structure(s) with name = <name>'''
    return persp(filter(
        lambda s: s.topic == topic,
        per
    ))


def persp_sum(base: Perspective, addition: Perspective) -> Perspective:
    '''Returns the sum of two Perspectives'''
    content_groups: DefaultDict[str, Set[Perspective]] = defaultdict(set)
    for r in base.union(addition):
        content_groups[r.topic].add(r.view)
    results = set()
    for topic in persp_topics(base).union(persp_topics(addition)):
        results.add(
            Stance(topic, reduce(persp_sum, content_groups[topic], frozenset()))
            )
    return persp(results)

def persp_diff(base: Perspective, subtraction: Perspective) -> Perspective:
    '''Returns the difference between two Perspectives'''
    if base == subtraction:
        return persp([])
    content_groups: DefaultDict[str, Set[Perspective]] = defaultdict(set)
    for r in base.union(subtraction):
        content_groups[r.topic].add(r.view)
    results = set()
    for topic in persp_topics(base):
        if len(persp_get(subtraction, topic)) == 0:
            # results[topic] = content_groups[topic]
            results = results.union(persp_get(base, topic))
        else: # topic is in subtract first-level
            print('topic')
            a = []
            for x in persp_get(base, topic):
                a += x.view
            a = persp(a)

            b = []
            for x in persp_get(subtraction, topic):
                b += x.view
            b = persp(b)

            diff = persp_diff(a, b)
            if len(diff) > 0 and topic not in persp_topics(subtraction):
                results.add(Stance(topic, diff))
            print('***', topic)
            print('**', b)
            print('*', a)
            print('>>', diff)

    return persp(results)


def pformat(per: Perspective, indent: int = 0) -> str:
    indent_str = '  ' * indent
    output = ''
    for stance in per:
        output += indent_str + stance.topic + '\n'
        output += pformat(stance.view, indent + 1)

    return output


def pprint(per: Perspective) -> None:
    print(pformat(per))

a = Stance('a', frozenset())
b = Stance('b', frozenset())
c = Stance('c', frozenset([b, Stance('Whoa', frozenset([a]))]))
d = Stance('d', frozenset())

x = persp([a, b])
y = persp([c, d])
fake_c = Stance('c', frozenset([Stance('Whoa', frozenset())]))
pprint(persp_diff(persp_sum(x, y), persp([fake_c])))

# RepSet = FrozenSet['Rep']


# @dataclass(frozen=True)
# class Rep:
#     '''The Representation dataclass'''
#     name: str
#     content: RepSet = frozenset()


# def repset(items: Optional[Iterable[Rep]] = None) -> RepSet:
#     '''Helper function to build a RepSet from an iterable of Reps, <items>'''
#     if items is None:
#         return frozenset()
#     contents = set()
#     for item in items:
#         contents.add(Rep(item.name, repset(item.content)))
#     return frozenset(contents)


# def is_atomic(r: Rep) -> bool:
#     '''Returns whether or not <rep> has content'''
#     return len(r.content) == 0


# def repset_get(rset: RepSet, name: str) -> RepSet:
#     '''Returns the sub-structure(s) with name = <name>'''
#     return repset(filter(
#         lambda r: r.name == name,
#         rset
#     ))

# def repset_names(rset: RepSet) -> Set[str]:
#     '''Returns names of the first-children of <rset>'''
#     return set([r.name for r in rset])


# def repset_sum(set_a: RepSet, set_b: RepSet) -> RepSet:
#     '''Returns the sum of two RepSets'''
#     content_groups: DefaultDict[str, Set[RepSet]] = defaultdict(set)
#     for r in set_a.union(set_b):
#         content_groups[r.name].add(r.content)

#     results = set()
#     for name in repset_names(set_a).union(repset_names(set_b)):
#         results.add(
#             Rep(name, reduce(repset_sum, content_groups[name], repset()))
#             )
#     return repset(results)


# def repset_sub(set_a: RepSet, set_b: RepSet) -> RepSet:
#     '''Returns the difference between two RepSets'''
#     results = set()
#     for rep1 in set_a:
#         if not is_atomic(rep1):
#             for rep2 in repset_get(set_b, rep1.name):
#                 results.add(Rep(rep1.name, repset_sub(rep1.content, rep2.content)))
#         elif len(repset_get(set_b, rep1.name)) == 0:
#             results.add(rep1)
#     return repset(results)


# x1 = repset([
#     Rep('x', repset([
#                 Rep('1', repset()),
#                 Rep('2', repset()),
#                 ])),
#     Rep('y', repset([
#                 Rep('a'),
#                 Rep('b'),
#                 ]))
#         ,])

# x2 = repset([
#     Rep('x', repset([
#                 Rep('3', repset()),
#                 ])),
#     Rep('y', repset([
#                 Rep('c'),
#                 ]))
#         ,])

# diff = repset_sub(repset_sum(x1, x2), x2)
# print(diff)
