from unittest import TestCase
from ppp_datamodel.communication import Request
from ppp_datamodel import Triple, Resource, Missing, Sentence
from ppp_libmodule.tests import PPPTestCase

from ppp_oracle import app
from ppp_oracle.requesthandler import answer, select

class RequestHandlerTest(PPPTestCase(app)):
    def testWhoAreYou(self):
        t = {'type': 'triple',
             'subject': {'type': 'resource', 'value': 'you'},
             'predicate': {'type': 'resource', 'value': 'identity'},
             'object': {'type': 'missing'}}
        q = {'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
             'tree': t}
        answers = self.request(q)
        self.assertEqual(len(answers), 1, answers)
        answer = answers[0].tree
        self.assertEqual(answer, Resource('Question-answering tool'))

    def testPEqNp(self):
        t = {'type': 'sentence', 'value': 'P=NP?'}
        q = {'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
             'tree': t}
        answers = self.request(q)
        self.assertEqual(len(answers), 1, answers)
        answer = answers[0].tree
        self.assertEqual(answer, Resource('maybe'))
