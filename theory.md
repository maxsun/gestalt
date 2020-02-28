
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

**Context** is a pair `(Q, A)`, whose uncertainty is reduced by a piece of information.
```
Context = Tuple[Question, Answer]
```

 A **piece of information** relative to a context is a pair `(Q, A)` whose answers are a subset of the context's -- therefore less ambiguous.
```
Let x = (Q_1, A_1)
Let y = (Q_2, A_2)
# Info(a, c) implies that 'a' is informative to 'c'.
Info(x, y) <=> Q_1 = Q_2 && A_1 < A_2
```

**Lemma (4):** since an answer to question `Q` is a piece of information which informs on `Q`, an answer to a question is also a pair: `(Q, A)`. Therefore, we see that `A` is a set of `(Q, A)` pairs.

The prevalence of the Question-Answer pairs and their role as both questions and answers reflects the fundamental nature of their structure. As we will see, they are the building blocks of information. For this reason, we define:

**Information Structure:** a Name and a corresponding set of nested Information Structures: `InformationStructure = (ID, Set[InformationStructure])`. This basic structure is isomorphic to the Question-Answer pairs, and -- with a few additions -- can be used for describing all types of information.

With this model, we are able to construct descriptions of many things:
```
('Person', [
	('Name', [('John', [])]),
	('Age', [('21', [])]),
	('Inventory', [
		('working lantern', []),
		('broken lantern', []),
	])
])
```
In this model, we represent a Person who has a name, age, and inventory, which contain atoms representing their possible values. This represents the possibility that his inventory contains either a "working lantern" or a "broken lantern".

