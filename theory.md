
# What is an Information Structure?

An **Information Structure** is an abstract model of information manifestations.  
Information, or the resolution of uncertainty, lies at the heart of communication and computation -- but in order for information to occur in the world, it must have some type of manifestation which facilitates both uncertainty, and its resolution. This Information Structure model supplies a formal representation of both of these requirements; allowing it to be used to model any process involving the interpretation, extraction, or communication of information.

## Construction:

**Definition:** "Information" is the resolution of uncertainty.

**Lemma (1):** You can only have uncertainty by also having a question to be uncertain of.

Therefore, we must have a question `Q`. 

**Lemma (2):** Without choices to choose between, you cannot have uncertainty.

Therefore, we must also have a set of possible answers, `A`.

**Lemma (3):** Without context, information cannot occur. Because information is a reduction in uncertainty, there must be preexisting information with uncertainty to reduce.

**Definition** "Context" is a pair `(Q, A)`, whose uncertainty is reduced by a piece of information.

**Definition:** A "piece of information" relative to a context is a pair `(Q, A)` whose answers are more specific than the context's.

Formally, `x=(Q1, A1)` is informative relative to context `c=(Q2, A2)` *if and only if* `Q1 = Q2` and `A1 <is a subset of> A2`.

**Lemma (4):** since an answer to question `Q` is a piece of information which informs on `Q`, an answer to a question is a pair `(Q, A)`. 

Therefore, we see that `A` is a set of `(Q, A)` pairs. Formally, a pair is:
```python
A = Set[Pair]
Pair = (Question, A)
```

This "Pair" type will be the basis of Information Structures. They represent the bare building blocks of information.


## Types
There are 4 types of Information Structures:

### Order-1: All questions answers are atomic.

```python
S = [
  ('red', []),
  ('green', []),
  ('blue', [])
]
```

Example: “You can only reference things”

### Order-2: Questions are nested recursively.
It’s possible to express relationships between questions.
```python
S = [
  ('name', [
    [
      ('first', [('George', [])]),
      ('last',[('Washington', [])])
    ],
    [
      ('first', [('John', [])]),
      ('last',[('Adams', [])])
    ],
  ])
]
```

### Order-3: The answer to a question can be a reference to another question.
```python
S = [
  ('John F. Kennedy', [
    ('Nickname', [('JFK', [])])
  ]),
  ('35th President', ['@John F. Kennedy'])
] 
```
It’s now possible to structure questions in multiple ways.
```python
S = [
  ('bools', [
    ('True', []),
    ('False', [])
  ]),
  ('x', [
    ('fst', ['@True']),
    ('snd', ['@False'])
  ]),
  ('y', [
    ('fst', ['@False']),
    ('snd', ['@False'])
  ])
]
```
### Order-4: The question of a question can be a reference.

It is now possible to describe the external relationships of a piece of information.
```python
S = [
  ('bools', [
    ('True', []),
    ('False', [])
  ]),
  ('x', [
    ('fst', ['@True']),
    ('snd', ['@False'])
  ]),
  ('and', [
    ('@x', ['@False']),
  ]),
  ('or', [
    ('@x', ['@True']),
  ]),
]
```
Only in Order-4 Structures is it possible to describe something from both the outside, and the inside.
