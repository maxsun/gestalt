
# Perspectives

A **Perspective** is a set of Stances:
```
Perspective = Set[Stance]
```

A **Stance** is a Topic, and a context-sensitive mapping to Perspectives.
```
Stance = Tuple[Topic, Callable[[Perspective, ], Perspective]]
```

The larger a Perspective, the more *ambiguous*. The smaller, the more *specific*.
For example:
```python
# "The color of the White House grey and/or white."
ambiguous = [
    ('What color is the White House?', lambda ctx: [
      ('White', lambda _: []),
      ('Grey', lambda _: []),
    ])
  ]
# vs
# "The color of the White House is white."
specific = [
    ('What color is the White House?', lambda ctx: [
      ('White', lambda _: [])
    ])
  ]
```

A **Context** is a preexisting Perspective with which other Stances may be predicated.
There is a key difference between expressing a perspective based on Context, and an atomic one.
For example:
```python
# "The color of the White House is the White House's color."
referential = [
    ('What color is the White House?', lambda ctx: ctx['White House']['color'])
  ]
# vs
# "The color of the White House is white."
atomic = [
    ('What color is the White House?',lambda ctx: [
      ('White', lambda _: [])
    ])
  ]
```

Essentially, a Stance may either present an entirely new Perspective, or it may state something about existing ones.
