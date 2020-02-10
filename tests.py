import unittest
import re
import note as note
from note import Expression


class TestToken(unittest.TestCase):

    def test_instantiation(self):
        t1 = note.Token('some type', 'some value')
        self.assertEqual(t1.type, 'some type')
        self.assertEqual(t1.value, 'some value')
        self.assertIsInstance(t1, note.Token)

    def test_eq(self):
        t1 = note.Token('A', 'value')
        t1_copy = note.Token('A', 'value')
        self.assertEqual(t1, t1)
        self.assertEqual(t1, t1_copy)

        t2 = note.Token('B', 'value')
        t3 = note.Token('A', 'different value')
        self.assertNotEqual(t1, t2)
        self.assertNotEqual(t1, t3)
        self.assertNotEqual(t2, t3)


class TestExpression(unittest.TestCase):

    def test_instantiation(self):
        content = [note.Token('plaintext', 'Hello'), note.Token('ref', 'World')]
        props = {
            'position': '-1'
        }
        e1 = note.Expression(content, props)
        self.assertEqual(e1.content, content)
        self.assertEqual(e1.properties, props)
        self.assertIsInstance(e1, note.Expression)
    
    def test_eq(self):
        content = [note.Token('plaintext', 'Hello'), note.Token('ref', 'World')]
        props = {
            'position': '-1'
        }
        e1 = note.Expression(content, props)

        # Identical expressions are equal
        e1_copy = note.Expression(
            content=[note.Token('plaintext', 'Hello'), note.Token('ref', 'World')],
            properties={'position': '-1'}
        )
        self.assertEqual(e1, e1_copy)

        # Changing props makes not equal
        e2 = note.Expression(content, {})
        self.assertNotEqual(e1, e2)

        # Changing content makes not equal
        e3 = note.Expression([], props)
        self.assertNotEqual(e1, e3)


class TestContext(unittest.TestCase):

    def test_instantiation(self):
        e1 = note.Expression(
            content=[note.Token('plaintext', 'Hello'), note.Token('ref', 'World')],
            properties={}
        )
        e2 = note.Expression(
            content=[note.Token('plaintext', 'Goodbye'), note.Token('ref', 'Moon')],
            properties={}
        )
        context1 = frozenset([e1, e2])
        self.assertEqual(len(context1), 2)
        self.assertIn(e1, context1)
        self.assertIn(e2, context1)
        e3 = note.Expression(
            content=[note.Token('plaintext', 'Goodnight'), note.Token('ref', 'Stars')],
            properties={}
        )
        self.assertNotIn(e3, context1)

    def test_eq(self):
        e1 = note.Expression(
            content=[note.Token('plaintext', 'Hello'), note.Token('ref', 'World')],
            properties={}
        )
        e2 = note.Expression(
            content=[note.Token('plaintext', 'Goodbye'), note.Token('ref', 'Moon')],
            properties={}
        )
        context1 = frozenset([e1, e2])

        # Identity
        self.assertEqual(context1, context1)

        # Order doesn't matter
        context2 = frozenset([e2, e1])
        self.assertEqual(context1, context2)

        # Different expression objects doesn't matter if the expressions are equal
        context3 = frozenset([e1, note.Expression(
            content=[note.Token('plaintext', 'Goodbye'), note.Token('ref', 'Moon')],
            properties={}
        )])
        self.assertEqual(context1, context3)


        # If member expressions have different content, the contexts are different
        context4 = frozenset([e1, note.Expression(
            content=[note.Token('plaintext', 'Hi'), note.Token('ref', 'Sun')],
            properties={}
        )])
        self.assertNotEqual(context1, context4)

        # If member expressions have different properties, the contexts are different
        context5 = frozenset([e1, note.Expression(
            content=[note.Token('plaintext', 'Goodbye'), note.Token('ref', 'Moon')],
            properties={'position': '-1'}
        )])
        self.assertNotEqual(context1, context5)

        # Different number of expressions -> not equal
        context6 = frozenset([e1])
        self.assertNotEqual(context1, context6)


class TestTokenize(unittest.TestCase):

    def test_basic(self):
        TOKEN_REGEX = {
            'ref': {
                'open': r'\[\[',
                'close': r'\]\]'
            },
            'keyword': {
                'open': r'\\',
                'close': r'.(?=\s|$)'
            },
            'indent': {
                'open': r'\n*(\s\s|\t)*\-',
                'close': r'\-\s'
            }
        }
        # 1 reference
        tokens = note.tokenize('Hello [[World]]', TOKEN_REGEX)
        self.assertEqual(tokens, [
            note.Token(type='plaintext', value='Hello '),
            note.Token(type='ref', value='[[World]]')])

        # 1 indent and 1 keyword
        tokens2 = note.tokenize(r'  - \Bye Moon', TOKEN_REGEX)
        self.assertEqual(tokens2, [
            note.Token(type='indent', value='  - '),
            note.Token(type='keyword', value=r'\Bye'),
            note.Token(type='plaintext', value=' Moon')])

        # multiple references
        tokens3 = note.tokenize(r'The [[Moon]] orbits [[Earth]]', TOKEN_REGEX)
        self.assertEqual(tokens3, [
            note.Token(type='plaintext', value='The '),
            note.Token(type='ref', value='[[Moon]]'),
            note.Token(type='plaintext', value=r' orbits '),
            note.Token(type='ref', value='[[Earth]]')])


class TestParse(unittest.TestCase):

    def test_basic(self):
        TOKEN_REGEX = {
            'ref': {
                'open': r'\[\[',
                'close': r'\]\]'
            },
            'keyword': {
                'open': r'\\',
                'close': r'.(?=\s|$)'
            },
            'indent': {
                'open': r'\n*(\s\s|\t)*\-',
                'close': r'\-\s'
            }
        }
        context = note.parse(re.split(r'(\s*\-.*\n)', '''
- Hello [[World]]
- Goodbye [[Moon]]
- The [[Moon]] orbits the [[World]]
    - Our [[World]] is called [[Earth]]
    - Pretty \\cool'''), TOKEN_REGEX)

        for exp in context:
            self.assertIn(exp, [
                note.Expression(
                    content=[
                        note.Token('indent', '- '),
                        note.Token('plaintext', 'Hello '),
                        note.Token('ref', '[[World]]')],
                    properties={'index': '0'}),
                note.Expression(
                    content=[
                        note.Token('indent', '- '),
                        note.Token('plaintext', 'Goodbye '),
                        note.Token('ref', '[[Moon]]')],
                    properties={'index': '1'}),
                note.Expression(
                    content=[
                        note.Token('indent', '- '),
                        note.Token('plaintext', 'The '),
                        note.Token('ref', '[[Moon]]'),
                        note.Token('plaintext', ' orbits the '),
                        note.Token('ref', '[[World]]'), 
                        ],
                    properties={'index': '2'}),
                note.Expression(
                    content=[
                        note.Token('indent', '    - '),
                        note.Token('plaintext', 'Our '),
                        note.Token('ref', '[[World]]'),
                        note.Token('plaintext', ' is called '),
                        note.Token('ref', '[[Earth]]'), 
                        ],
                    properties={'index': '3'}),
                note.Expression(
                    content=[
                        note.Token('indent', '    - '),
                        note.Token('plaintext', 'Pretty '),
                        note.Token('keyword', '\\cool'),
                        ],
                    properties={'index': '4'})
            ])



if __name__ == '__main__':
    unittest.main()