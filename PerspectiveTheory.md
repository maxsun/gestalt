# Perspective Model of Communication

*Goal:* a model describing the behavior of informative representations.

A **Representation** is a recognizable and discrete piece of information which becomes meaningful when contextualized.
For example, when you read the word "garden", you use your existing knowledge of English and gardens to interpret the word's meaning.

An **Informative Representation** is a Representation, which provides information *relative to a preexisting context*.

**Information** is the resolution of uncertainty.
Therefore, in order to describe Information, we must be able to describe:
1. Uncertainty
2. The resolution of Uncertainty

Uncertainty requires:
1. a topic, to be uncertain of, and
2. a set of "plausible" stances towards the topic which represent the options to be uncertain of.

A **Perspective** is a topic, stances-set pair which facilitates uncertainty. Formally:
```python
Perspective = Tuple[Topic, Set[Stance]]
```

A Perspective's set of Stances is called its **views** set.
The Topic of a Perspective is just called its **topic**.

With Perspectives, we can represent uncertainty:
```python
# My perspective on the temperature is that it could be from 78 to 82
height = ("What temperature is it?", [78, 79, 80, 81, 82])
```

Critically, Stances *are* Perspectives. This is inspired by the fact that Perspectives are typically built upon component Perspectives. Formally, a Perspective is now:
```python
Perspective = Tuple[Topic, Set[Perspective]]
```

**Entropy** is a measurement of the uncertainty of a Perspective. Generally, the larger the views-set, the larger the uncertainty. However, because Perspectives may be recursively structures, Entropy must be measured recursively as well. Formally, we can represent a Perspective `p`'s entropy: `Entropy(p)`.

Formally, the Entropy of Perspective `p` is a weighted average of each of its consituent Perspectives' Entropy.

Using Entropy, we can define Information as a reduction in Entropy:
```python
# Info(q, a) implies `a` provides information towards `q`
Info(q, a) = Entropy(q - a) < Entropy(q)
```
Note that since both `q` and `a` are uncertainties, `q - a` represents a decrease in uncertainty -- aka Information.

We must now examine the addition and subtraction operations we can perform on Perspectives. In order for information to occur, there must be a subtraction operation which reduces a Perspective's uncertainty, as well as an addition opperation which increases a Perspective's total uncertainty.

Perspectives can only be added or subtracted if they share the same topic:
```
a.topic == b.topic # must be true
a + b - b = a - b + b # inverses
```
The **addition** of two Perspectives should result in a Perspective result in their recursive Union.
Any uncertainties in `a` or `b` must also be in `a + b`.

The **subtraction** of two Perspectives `a` and `b`, should result in a Perspective containing all the uncertainties within `a`, but not within `b`.
This operation removes the views in a Perspective which *are* contained in another Perspective.
The Perspective that all music is good, subtracted by the Perspective that Country Music is good, is the Perspective that all music, but Country is good.

In order to make sure any definitions of addition or subtraction are adequete, we must examine types of Information.

An **Atomic Perspective** is a Perspective with no views. Because it has no views, it is neither specific nor ambiguous; it is completely unquestionable.

Information can be provided in 3 ways:
1. **Direct Information** is information provided to a Perspective when the informative Perspective is of the same topic as the context.

2. **Indirect Information** is information provided to a Perspective by inference from information provided directly to another Perspective.

3. **Abstract Information** is information provided to a Perspective when the informative perspective allows for new inferences to be drawn or removed, thus providing information. 

Information provided in any way other than these 3 is either a mistake or a priori.

Abstract information requires the ability to **refer** to Topics in order to describe relationships between them.
Critically, reference is context-sensitive.


```
snow is snow
"snow" is snow
snow is "snow"
"snow" is "smow"

Snow is white.
Snow is literally white.

"Snow" is white.
The word "Snow" is the color white. This doesn't make sense.

Snow is "white".
Snow is the definition of what it means to be white.

"Snow" is "white".
In the abstract sense, snow is white.
The definition of snow is the definition of white.
```

