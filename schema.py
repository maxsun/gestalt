from graphene import ObjectType, String, Schema, Field, List, Int
import graphene
from graphene.test import Client
import note as parser


# class Block(ObjectType):
#     id = String()
#     content = List(Token)
#     linkIn = Field(LinkIn)
#     linkOut = Field(LinkOut)

#     def resolve_id(block, info):
#         return block.id

#     def resolve_content(block, info):
#         return block.content

#     def resolve_linkIn(block, info):
#         return block

#     def resolve_linkOut(block, info):
#         return block

class Value(graphene.Union):
    class Meta:
        types = (Int, String)


class Token(ObjectType):
    type = String()
    value = String()


class Expression(ObjectType):

    content = List(Token)
    prop = Field(String, key=String())
    
    parent = List(lambda: Expression)

    def resolve_content(parent, info):
        print(parent)
        return parent.content

    def resolve_prop(parent, info, key):
        # print('!!!!!!!')
        return parent.properties[key]


class Context(ObjectType):

    expressions = List(Expression)
    id = String()
    children = lambda: Context()

    def resolve_expressions(parent, info):
        r = []
        for x in parent:
            r.append(x)
        return r

    def resolve_id(parent, info):
        return parser.parse_id(parent)

    def resolve_children(parent, info):
        return parser.get_children(parser.context, parent)


class Query(ObjectType):
    allIds = List(String)
    context = Field(Context, id=String())

    def resolve_context(parent, info, id):
        return parser.resolve_id(id, parser.context)

    def resolve_allIds(parent, info):
        ids = []
        for exp in parser.sort_by_property(parser.context, 'index'):
            ids.append(parser.parse_expression_id(exp))
        return ids


schema = Schema(query=Query)