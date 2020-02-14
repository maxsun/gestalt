
# Information

Something is informative if it reduces an observer’s uncertainty about the world. Consequently, something can only be informative when it exists in a greater context with other things which it can provide information about.

Contexts exist both physically and mentally — they are simply mediums which possess relationships between subsets/subspaces of themselves. A context is an individual state of some type of system — continuous or discrete. Often times, the entire state of the system is too complex to have full knowledge (or it’s continuous). In these cases, we only have partial information about the system’s state. However, we can additionally receive other partial states and gradually gain a better picture of the context, or we can learn patterns in states and eventually gain the ability to extract more information from partial states than was previously possible.

Uncertainty in a context arises from potential relationships between parts of the context that have not been ruled out. What constitutes a piece of information is subjective to an interpreter (aka relative to a context). It’s some type of signal which can enter the context and reduce its entropy.




# Definitions:
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


