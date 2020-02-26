from structure import *

def _and(ctx: Structure, arg: Structure) -> Structure:
    fst = arg.get('fst', ctx=ctx) == ctx.take(['True'])
    snd = arg.get('snd', ctx=ctx) == ctx.take(['True'])
    return ctx.take(['True']) if fst and snd else ctx.take(['False'])

def _or(ctx: Structure, arg: Structure) -> Structure:
    fst = arg.get('fst', ctx=ctx) == ctx.take(['True'])
    snd = arg.get('snd', ctx=ctx) == ctx.take(['True'])
    return ctx.take(['True']) if fst or snd else ctx.take(['False'])


ops = Structure(set([
    ('and', _and),
    ('or', _or)
]))

bools = Structure(set([
    ('True', lambda ctx, arg: Structure(set())),
    ('False', lambda ctx, arg: Structure(set()))
]))


x = Structure(set([
    ('x', lambda ctx, arg: Structure(set([
        ('fst', lambda ctx, arg: ctx.take(['True'])),
        ('snd', lambda ctx, arg: ctx.take(['False']))
        ])))
]))

my_context = ops + bools + x

print(my_context.get('and', my_context.get('x'))) # False
print('')
print(my_context.get('or', my_context.get('x'))) # True