from graphene import ObjectType, String, Schema, Field, List, Int
import graphene
from graphene.test import Client
import note as parser
from note import context, resolve_id


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
    plaintext = String()
    id = String()

    def resolve_content(parent, info):
        print(parent)
        return parent.content

    def resolve_prop(parent, info, key):
        # print('!!!!!!!')
        return parent.properties[key]

    def resolve_plaintext(parent, info):
        return ''.join([x.value for x in parent.content])

    def resolve_id(parent, info):
        return parser.parse_expression_id(parent)


class Context(ObjectType):

    expressions = List(Expression)
    id = String()

    children = Field(lambda: Context)
    parent = Field(lambda: Context)

    references = Field(lambda: Context)

    def resolve_expressions(parent, info):
        r = []
        for x in parent:
            r.append(x)
        return r

    def resolve_id(parent, info):
        return parser.parse_id(parent)

    def resolve_children(parent, info):
        return parser.get_children(parent, parser.context)

    def resolve_parent(parent, info):
        return parser.get_parent(parent, parser.context)

    def resolve_references(parent, info):
        return parser.get_references(parent, parser.context)



class ContextType(ObjectType):
    class Meta:
        model = Context



class UpdateContext(graphene.Mutation):

    id = String()
    expressions = List(Expression)

    class Arguments:
        id = String()


    def mutate(self, info, id):
        ctx = parser.resolve_id(id, parser.context)
        return UpdateContext(
            id=id,
            expressions=ctx)


class Query(ObjectType):
    allIds = List(String)
    context = Field(Context, id=String(), ref=String())
    parse = Field(Context, text=String())

    def resolve_context(parent, info, id=None, ref=None):
        if id:
            return parser.resolve_id(id, parser.context)
        if ref:
            return parser.resolve_reference(ref, parser.context)
        return parser.context

    def resolve_allIds(parent, info):
        ids = []
        for exp in parser.sort_by_property(parser.context, 'index'):
            ids.append(parser.parse_expression_id(exp))
        return ids

    def resolve_parse(parent, info, text):
        return parser.parse([text], parser.TOKEN_REGEX)


class Mutate(ObjectType):
    update_context = UpdateContext.Field()


schema = Schema(query=Query, mutation=Mutate)