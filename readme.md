*"Any road followed precisely to its end leads precisely nowhere. Climb the mountain just a little bit to test that it’s a mountain. From the top of the mountain, you cannot see the mountain."* -Dune

# Hollow Mountain
A functional, context-sensitive model of information.

## Types:
```python
Relation = Callable[[Structure, Structure], Structure]
NamedRelation = Tuple[str, Relation]
Structure = Set[NamedRelation]
```

A **Structure** is a collection of named relations between subsets of itself.
Each name is unique per Structure.

The contents of a Context can be accessed in 3 ways:

  1. `ctx[name]`: returns the Relation in `ctx` with `name`.
  2. `get(ctx, name, arg) = ctx[name](ctx, arg)`: returns the result of calling the Relation with `name` in `ctx`.
  3. `take(ctx, [names])`: returns a subset of the Context with name in `[names]`.


Two Structures *a* and *b* can be combined to produce a **sum** (a + b) or **difference** (a - b).
```python
a + b = a.union(b)
a - b = a.intersection(b).union(a)
```

**Relations** are functions which take 2 Structures ("Context" and "Argument") as arguments and returns a subset of the Context Structure:
```Relation :: Structure, Structure -> Structure```

