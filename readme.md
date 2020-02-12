This project consists of 3 main parts:
- the context data structure and utilities
- a plaintext-to-context parser
- a Graphql API + server

1. strings are structured atoms (not expressions or graphs!)
2. tokens are strings paired with a set of tagged types: `:: Tuple[str, Set[Type]]`
3. tokens are extracted from strings using some type of pattern/constraint matching
   1. fault tolerance is imporant in tokenization -- strings with unknown types should still be tokenized in some way
   2. tokens are the smallest meaningful units; single pieces of data, in context
4. expressions are structures of tokens
   1. (and atoms?) unsure
   2. e
5. graphs are structures of expressions
6. transforms are mappings between subgraphs within the same graph
7. resolvers are mappings from expressions to a subgraph within a graph




# Types

## Token
`:: Tuple[str, str]`

Tokens represent typed values. They're comprable to ["morphemes"](https://en.wikipedia.org/wiki/Morpheme) in linguistics; the smallest units of meaning in a language.

## Content
`:: List[Token]`

Content represents an ordered sequence of Tokens. It's comparable to an [expression](https://en.wikipedia.org/wiki/Sentence_(linguistics)) in linguistics. However, content only represents the abstract idea of a series of Tokens, rather than an instated instance of an expression.

## Properties
`:: Dict[str, Union[number, str]]`

Properties represent information about an object as it occurs in a context. Properties are not determined by the actual substance/content of an object; they are determined by how the object stands in relation to other objects and its environment. For example, the physical location of an object in space is a property of the object because its location is not determined by the object itself, but by the space it exists within.

## Expression
`:: Tuple[Content, Properties]`

An expression represents an instatiated peice of content: it is a content with properties because its been  instantiated in an environment

## Graph
`:: List[Expression]`

# Functions

## tokenize
`:: str => Content`

## parse
`:: List[str] => Graph`

## parse_id
`:: Expression => str`

## parse_indent
`:: Expression => int`

## get_links_to
`:: Graph, Graph, Transformer => Graph`

## sort_by_property
`:: Graph, str => List[Expression]`

## Resolvers
`:: Union[int, str], Graph => Graph`
- resolve_id
- resolve_reference

## Transformers
`:: Graph, Graph => Graph`
- get_references
- get_parent
    - get_exp_parent
- get_children
    - get_exp_children


