from unittest import TestCase
from ppp_datamodel.communication import Request
from ppp_datamodel import List as L
from ppp_datamodel import Triple as T
from ppp_datamodel import Resource as R
from ppp_datamodel import Missing as M
from ppp_libmodule.tests import PPPTestCase

from ppp_oracle.requesthandler import answer, select, eq

class FunctionsTest(TestCase):
    def testEq(self):
        self.assertTrue(eq(R('foo'), R('foo')))
        self.assertTrue(eq(R('foo'), R('Foo')))
        self.assertFalse(eq(R('foo'), R('bar')))
        self.assertFalse(eq(M(), R('bar')))
        self.assertTrue(eq(T(R('foo'), R('bar'), R('baz')),
                           T(R('foo'), R('bar'), R('baz'))))
        self.assertTrue(eq(T(R('foo'), R('bar'), R('Baz')),
                           T(R('Foo'), R('bAr'), R('baZ'))))
        self.assertFalse(eq(T(R('foo1'), R('bar'), R('Baz')),
                            T(R('Foo'), R('bAr'), R('baZ'))))
        self.assertTrue(eq(T(R('foo'), R('bar'), R('baz')),
                           T(R('foo'), L([R('bar')]), R('baz'))))
        self.assertTrue(eq(T(R('foo'), R('bar'), R('baz')),
                           T(R('foo'), L([R('bar'), R('qux')]), R('baz'))))
        self.assertTrue(eq(T(R('foo'), L([R('quux'), R('bar')]), R('baz')),
                           T(R('foo'), L([R('bar'), R('qux')]), R('baz'))))
        self.assertFalse(eq(T(R('foo'), L([R('quux'), R('baar')]), R('baz')),
                            T(R('foo'), L([R('bar'), R('qux')]), R('baz'))))

        # Equality on inverse predicates
        self.assertFalse(eq(T(R('foo'), R('quux'), R('baz'), R('bar')),
                            T(R('foo'), R('qux'), R('baz'), R('baar'))))
        self.assertTrue(eq(T(R('foo'), R('quux'), R('baz'), R('bar')),
                            T(R('foo'), R('qux'), R('baz'), R('bar'))))

        # Equality on swapped predicate / inverse-predicate
        self.assertTrue(eq(T(R('foo'), R('bar'), R('baz')),
                           T(R('baz'), R('qux'), R('foo'), R('bar'))))
        self.assertTrue(eq(T(R('baz'), R('qux'), R('foo'), R('bar')),
                           T(R('foo'), R('bar'), R('baz'))))
        self.assertFalse(eq(T(R('foo'), R('bar'), R('baz')),
                            T(R('foo'), R('qux'), R('baz'), R('bar'))))
        self.assertFalse(eq(T(R('foo'), R('qux'), R('baz'), R('bar')),
                            T(R('foo'), R('bar'), R('baz'))))
    def testAnswer(self):
        self.assertEqual(answer(M(), (M(), R('baz'))),
                         R('baz'))
        self.assertEqual(answer(R('foo'), (R('bar'), R('baz'))),
                         None)
        self.assertEqual(answer(T(R('foo'), R('bar'), M()),
                                (T(R('foo'), R('bar'), M()), R('baz'))),
                         R('baz'))
        self.assertEqual(answer(T(R('foo2'), R('bar'), M()),
                                (T(R('foo '), R('bar'), M()), R('baz'))),
                         None)
    def testSelect(self):
        self.assertEqual(select(T(R('you'), R('identity'), M())),
                         R('A question-answering tool.'))
        self.assertEqual(select(T(R('You'), R('identity'), M())),
                         R('A question-answering tool.'))
        self.assertEqual(select(T(R('I'), R('identity'), M())),
                         R('An internaut.'))
        self.assertEqual(select(T(T(R('your'), R('source code'), M()), R('location'), M())),
                         R('http://github.com/ProjetPP/'))

