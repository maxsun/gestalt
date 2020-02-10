# from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import List, Callable, Dict, FrozenSet, Tuple, Optional, Union
import re
import hashlib


@dataclass(frozen=True)
class Token:
    type: str
    value: str


@dataclass(frozen=True)
class Expression:
    content: List[Token]
    properties: Dict[str, Union[str, int]]

    def __eq__(self, other):
        if other is None:
            return False
        return other.content == self.content and other.properties == self.properties


    def __hash__(self):
        return int(hashlib.md5((str(self.content) + str(self.properties)).encode()).hexdigest(), 16)


Context = FrozenSet[Expression]

Resolver = Callable[[Token, Context], Context]

Linker = Callable[[Expression, Context], Context]


def tokenize(text: str, groups: Dict[str, Dict[str, str]]) -> List[Token]:
    '''Converts <text> into a list of Tokens according to regex in <groups>'''
    tokens: List[Token] = []
    text = text.strip('\r\n')
    index: int = 0

    while True:
        matches: List[Tuple[int, str]] = []
        for gname in groups.keys():
            match = re.search(groups[gname]['open'], text[index:])
            if match:
                matches.append((match.span()[0], gname))

        if len(matches) > 0:
            next_match = min(matches, key=lambda x: x[0])
            match_index = next_match[0] + index
            match_type = next_match[1]
            close_match = re.search(groups[match_type]['close'], text[match_index:])
            if close_match:
                close_index = close_match.span()[1] + match_index
                if index != match_index:
                    tokens.append(Token('plaintext', text[index:match_index]))
                tokens.append(Token(match_type, text[match_index:close_index]))
                index = close_index
        else:
            if len(text[index:]) > 0:
                tokens.append(Token('plaintext', text[index:]))
            break

    return tokens


def parse(
        lines: List[str],
        token_patterns: Dict[str, Dict[str, str]]) -> Context:
    '''Tokenizes + converts a list of plaintexts into a list of blocks'''
    context = []
    for idx, line in enumerate([x for x in lines if x != '']):
        context.append(Expression(
            content=tokenize(line, token_patterns),
            properties={
                'index': idx
            }
        ))

    return frozenset(context)

TOKEN_REGEX = {
    'ref': {
        'open': r'\[\[',
        'close': r'\]\]'
    },
    'keyword': {
        'open': r'\\',
        'close': r'.(?=\s|$)'
    },
    'indent': {
        'open': r'\n*(\s\s|\t)*\-',
        'close': r'\-\s'
    }
}


context = parse(re.split(r'(\s*\-.*\n)', '''
- Hello [[World]]
- Goodbye [[Moon]]
- The [[Moon]] orbits the [[World]]
    - Our [[World]] is called [[Earth]]
    - Pretty \\cool
- [[Earth]] orbits the [[Sun]]'''), TOKEN_REGEX)


def sort_by_property(context, prop_name):
    return list(sorted(context, key=lambda x: x.properties[prop_name]))


def generate_id(exp: Expression) -> str:
    '''Returns a consistent hash for an expression'''
    return str(hash(exp))


def resolve_id(_id: str, ctx: Context) -> Context:
    for exp in ctx:
        if generate_id(exp) == _id:
            return frozenset([exp])
    return frozenset()


def resolve_reference(ref_value: str, ctx: Context) -> Optional[Expression]:
    for exp in ctx:
        if len(exp.content) == 2 and exp.content[0].type == 'indent':
            if exp.content[1].type == 'ref' and exp.content[1].value == ref_value:
                return exp


def get_indent(exp: Expression) -> int:
    '''Returns the amount of space before a "-" in a textblock'''
    if exp.content[0].type != 'indent':
        return 0
    return exp.content[0].value.index('-')


def get_exp_parent(child_exp: Expression, ctx: Context) -> Optional[Expression]:
    sorted_ctx = sort_by_property(ctx, 'index')
    child_indent = get_indent(child_exp)
    preceeding_ctx = sorted_ctx[:sorted_ctx.index(child_exp)]
    for exp in preceeding_ctx[::-1]:
        if child_indent > get_indent(exp):
            return exp
    return None


def get_parent(child_ctx: Context, ctx: Context) -> Context:
    parents = []
    for exp in child_ctx:
        parents.append(get_exp_parent(exp, ctx))
    return frozenset([x for x in parents if x])


def get_exp_children(parent_exp: Expression, ctx: Context) -> Context:
    '''Returns all blocks which have <parent> as their parent.'''
    sorted_ctx = sort_by_property(ctx, 'index')
    if parent_exp not in ctx:
        return frozenset([])
    following_ctx = sorted_ctx[sorted_ctx.index(parent_exp):]
    children = []
    for exp in following_ctx:
        if get_exp_parent(exp, ctx) == parent_exp:
            children.append(exp)
    return frozenset(children)


def get_children(parent_ctx: Context, ctx: Context) -> Context:
    children = []
    for exp in ctx:
        if get_exp_parent(exp, ctx) in parent_ctx:
            children.append(exp)
    return frozenset(children)

for exp in sort_by_property(context, 'index'):
    print(generate_id(exp), exp)

print('======')
a = resolve_id('1455753487410189595', context)
print(a)
print('------')
print(get_children(a, context))