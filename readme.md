This project consists of 3 main parts:
- the context data structure and utilities
- a plaintext-to-context parser
- a Graphql API + server


# Types
- Token
- Expression
- Context

# Functions

## Parsing-Related
- tokenize
- parse

## Property Parsers
`:: Expression => Union[int, str]`
- parse_id
- parse_indent

## Context Utilities
- get_links_to
- sort_by_property

## Resolvers
`:: Union[int, str], Context => Context`
- resolve_id
- resolve_reference

## Focus-Shifters
`:: Context, Context => Context`
- get_references
- get_parent
    - get_exp_parent
- get_children
    - get_exp_children


