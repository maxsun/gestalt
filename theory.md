# What is an Information Structure?

A **structure** is a representation of a set of objects with some additional facilities allowing it to be treated as a single object.

```python
Operations = Set[Callable[[Structure(s)], Structure]]
Structure = Tuple[Set, Operations]
```

The following argues that an **Information Structure** is a structure in which each object is a Question-Answer pair.

```python
Pair = (Question, Set[Pair])
Operations = Set[Callable[[Structure(s)], Structure]]
Information Structure = Tuple[Set[Pair], Operations]
```

It is important to remember that the formal representations are representations of metaphysical structures which are instantiated elsewhere in the world. The instances themselves are the physical manifestations of information in the world; the brain, for example.

## Construction:
1. Information is the resolution of uncertainty.
2. You can only have uncertainty by also having a question to be uncertain of.

Formally, we have Q — representing the question — and A — representing a set of possible answers to the question.
For example, we could have the question, “Who lives in that house?” and possible answers, “Alice,” “Brooks,” or “Ludwig.” A gain of information would reduce the number of possible answers, thus reducing the amount of uncertainty. The answer “Alice” is more specific than the answer “Alice or Brooks.”

3. A piece of information relative to a question (Q, A) is a subset of A, which reduces Q’s uncertainty.
4. A alone is not informative. Without context, A is meaningless. Here, we rely on Frege’s Context Principle: only ask for the meaning of something in context.
Therefore, a piece of information must be a pair (Q, A).

5. By providing a question Q, we contextualize A and make it informative about a Context, (Q, A).
The information pair’s answers are a subset of the contextual pair’s answers (making it informative relative the context).

6. Now it is clear that a Question is a pair (Q, A), and an Answer (or piece of information relative to a question) is also a pair (Q, A).

## Types
There are 4 types of Information Structures:

### Order-1: All questions are atomic.

```python
S = [
  (red, []),
  (green, []),
  (blue, [])
]
```

Example: “You can only reference things”

### Order-2: Questions are nested recursively.
```
S = [
  (name, [
    [(first, [
                (George, [])
              ]),
      (last,[
                (Washington, [])
              ])],
     [(first, [
                (John, [])
              ]),
      (last,[
                (Adams, [])
              ])],
  ])
]
```
It’s possible to express relationships between questions.

### Order-3: The answer to a question can be a reference to another question.
```
S = [
  (John F. Kennedy, [
    (Nickname, [
      (JFK, [])
    ])
  ]),
  (35th President, [@John F. Kennedy])
] 
```
It’s now possible to structure questions in multiple ways.
```
S = [
  (bools, [
    (True, []),
    (False, [])
  ]),
  (x, [
     (fst, [
        @True
      ]),
      (snd, [
        @False
      ])
   ]),
  (y, [
     (fst, [
        @False
      ]),
      (snd, [
        @False
      ])
   ])
]
```
Order-4: The question of a question can be a reference.

It is now possible to describe the external relationships of a piece of information.
```
S = [
  (bools, [
    (True, []),
    (False, [])
  ]),
  (x, [
     (fst, [
        @True
      ]),
      (snd, [
        @False
      ])
   ]),
  (and, [
     (@x, [
        @False
      ]),
   ]),
  (or, [
     (@x, [
        @True
      ]),
   ]),
]
```
Only in Order-4 Structures is it possible to describe something from both the outside, and the inside.
