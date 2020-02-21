'''A note parser'''
from dataclasses import dataclass
from pprint import pprint
from typing import List, Callable, Dict, FrozenSet, Tuple, Optional, Union
import re
import hashlib


@dataclass(frozen=True)
class Token:
    '''Represents a value of a certain type'''
    type: str
    value: str


@dataclass(frozen=True)
class Expression:
    '''Represents a list of Tokens with a set of properties'''
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

Linker = Callable[[Context, Context], Context]


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
    '''Tokenizes + converts a list of texts into a Context'''
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
    - [[Sun]]
        - is very bright
- The [[Moon]] orbits the [[World]]
    - Our [[World]] is called [[Earth]]
    - Pretty \\cool
- [[Earth]] orbits the [[Sun]]
- [[Sun]]
    - is a star
'''), TOKEN_REGEX)


def sort_by_property(context: Context, prop_name: str) -> List[Expression]:
    '''Returns <context> as a list, sorted by <prop_name>'''
    return list(sorted(context, key=lambda x: x.properties[prop_name]))


def parse_expression_id(exp: Expression) -> str:
    '''Returns a consistent hash for an expression'''
    return str(hash(exp))
 

def parse_id(ctx: Context) -> str:
    '''Returns a consistent hash for a context'''
    return ':'.join([parse_expression_id(exp) for exp in ctx])


def resolve_id(_id: str, ctx: Context) -> Context:
    '''Returns the subset of <ctx> with <_id>'''
    results = []
    for exp in ctx:
        if parse_expression_id(exp) in _id.split(':'):
            results.append(exp)
    return frozenset(results)


def resolve_reference(ref_value: str, ctx: Context) -> Context:
    '''Returns the subset of <ctx> pointed to by <ref_value>'''
    refs = []
    for exp in ctx:
        if len(exp.content) == 2 and exp.content[0].type == 'indent':
            if exp.content[1].type == 'ref' and exp.content[1].value == ref_value:
                refs.append(exp)
    if len(refs) > 0:
        return frozenset(refs)
    return frozenset([Expression([Token('ref', ref_value)], {'index': -1})])


def get_references(subcontext: Context, ctx: Context) -> Context:
    '''Returns the subset of <ctx> which is references in <subcontext>'''
    refs = []
    for exp in subcontext:
        for token in exp.content:
            if token.type == 'ref':
                refs += resolve_reference(token.value, context)
    return frozenset(refs)


def parse_indent(exp: Expression) -> int:
    '''Returns the amount of space before a "-" in an expression's content'''
    if exp.content[0].type != 'indent':
        return 0
    return exp.content[0].value.index('-')


def get_exp_parent(child_exp: Expression, ctx: Context) -> Optional[Expression]:
    '''Returns the first less-indented expression preceeding <child_exp> in <ctx>'''
    sorted_ctx = sort_by_property(ctx, 'index')
    child_indent = parse_indent(child_exp)
    preceeding_ctx = sorted_ctx[:sorted_ctx.index(child_exp)]
    for exp in preceeding_ctx[::-1]:
        if child_indent > parse_indent(exp):
            return exp
    return None


def get_parent(child_ctx: Context, ctx: Context) -> Context:
    '''Returns the subset of <ctx> with parents in <child_ctx>'''
    parents = []
    for exp in child_ctx:
        parents.append(get_exp_parent(exp, ctx))
    return frozenset([x for x in parents if x])


def get_exp_children(parent_exp: Expression, ctx: Context) -> Context:
    '''Returns the subset of <ctx> which has <parent> as their parent'''
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
    '''Returns the subset of <ctx> with a parent in <parent_ctx>'''
    children = []
    for exp in ctx:
        if get_exp_parent(exp, ctx) in parent_ctx:
            children.append(exp)
    return frozenset(children)


def get_links_to(subcontext: Context, ctx: Context, link_func: Linker) -> Context:
    '''Returns the subset of <ctx> which links into <subcontext> according to <link_func>'''
    linked = []
    for exp in ctx:
        for l in link_func(frozenset([exp]), ctx):
            if l in subcontext:
                linked.append(exp)
                break
    return frozenset(linked)



# print('----')
# a = resolve_reference('[[Sun]]', context)
# pprint(get_children(a, context))

