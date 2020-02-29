import unittest
import structure as Struct

class TestStructure(unittest.TestCase):

    def test_atomic_instance(self):
        '''Test the construction of an Atom'''
        rep = Struct.Rep('x')

        self.assertEqual(rep.name, 'x')
        self.assertEqual(rep.content, frozenset())

    def test_composite_instance(self):
        '''Test the construction of a complex instance'''
        rep = Struct.Rep('person', frozenset([
            Struct.Rep('name', frozenset([
                Struct.Rep('Max'),
                Struct.Rep('Maximilian')
                ])),
            Struct.Rep('age', frozenset([Struct.Rep('20')])),
            Struct.Rep('gender', frozenset([Struct.Rep('male')])),
        ]))

        self.assertEqual(rep.name, 'person')
        self.assertEqual(
            Struct.repset_names(rep.content),
            frozenset(['name', 'age', 'gender']))
        self.assertEqual(
            Struct.repset_get(rep.content, 'name'),
            Struct.repset([Struct.Rep('name', frozenset([
                Struct.Rep('Max'),
                Struct.Rep('Maximilian')
                ]))]),
        )


if __name__ == '__main__':
    unittest.main()
