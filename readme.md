
# Notes

## Datatypes
    - Token
        - a typed value
    - Expression
        - a list of Tokens and a dictionary of properties
    - Context
        - a set of Expressions

## Resolvers (token-level interpretation)
    - Token, Context -> Context
    - (what subset of Context does a Token evoke?)
    - functions which take an input and return a subset of the BlockGraph
    - for example, "find block with id"

## Linkers (expression-level interpretation)
    - Expression/Sub-Context, Context -> Context
    - (what subset of Context is relevant to a given Expression?)
    - functions which take a block and its context and return a related subset of the BlockGraph
    - some linkers just aggregate the graphs resolved to by Tokens
        - but others rely on more contextual information (like position in the Graph)
    - for example, "find children of block"

## Mutators
    - Context + relevant args -> Context
    - Functions which take an ExpressionGraph, perform edits to it, and return a modified ExpressionGraph

