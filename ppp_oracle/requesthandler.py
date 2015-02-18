"""Request handler of the module."""

import functools

from ppp_datamodel import Triple as T
from ppp_datamodel import Resource as R
from ppp_datamodel import Missing as M
from ppp_datamodel import Sentence as S
from ppp_datamodel import TraceItem, Response

from ppp_libmodule.exceptions import ClientError

database = [
        (T(R('you'), R('identity'), M()),
        R('A question-answering tool.')),

        (T(R('your'), R('name'), M()),
        R('Platypus.')),

        (T(R('your'), R('creator'), M()),
        R('Projet Pensées Profondes members.')),

        (T(R('your'), R('website'), M()),
        R('http://projetpp.github.io/')),

        (T(T(R('your'), R('source code'), M()), R('location'), M()),
        R('http://github.com/ProjetPP/')),

        (T(R('I'), R('identity'), M()),
        R('An internaut.')),

        (S('P=NP?'),
        R('Maybe.')),

        (S('NP=P?'),
        R('Maybe.')),

        (T(R('I'), R('location'), M()),
        R('Try looking around yourself, I can\'t help much.')),

        (T(R('You'), R('location'), M()),
        R('askplatyp.us')),

        (S('Do you like me?'),
        R('Definitely. Wanna hug?')),

        (S('yes'),
        R('Sorry, I don\'t remember what we said earlier.')),

        (S('no'),
        R('Sorry, I don\'t remember what we said earlier.')),

        (S('42'),
        R('Answer to the Ultimate Question of Life, The Universe, and Everything.')),

        (S('Answer to the Ultimate Question of Life The Universe and Everything'),
        R('42')),

        (T(R('love'), R('definition'), M()),
        R('Baby don\'t hurt me.')) # https://www.youtube.com/watch?v=Ktbhw0v186Q
        ]


def eq(left, right, test_reverse=True):
    if left.type != right.type:
        return False
    elif isinstance(left, M):
        return True
    elif isinstance(left, R):
        return left.value.lower() == right.value.lower()
    elif isinstance(left, T):
        # Is there any equal predicate?
        pred_eq = (
                any(eq(x, y)
                    for x in left.predicate_set
                    for y in right.predicate_set) or
                any(eq(x, y)
                    for x in left.inverse_predicate_set
                    for y in right.inverse_predicate_set))
        if (pred_eq and eq(left.subject, right.subject) and \
                eq(left.object, right.object)):
            return True
        if test_reverse:
            return (eq(T(left.object, left.inverse_predicate, left.subject),
                       right,
                       test_reverse=False) or
                    eq(left,
                       T(right.object, right.inverse_predicate, right.subject),
                       test_reverse=False))
        return False
    else:
        # TODO
        return False

def answer(pattern, tree):
    if isinstance(pattern, M):
        return tree[1]
    elif eq(pattern, tree[0]):
        return tree[1]
    elif isinstance(pattern, S) and isinstance(tree[0], S) and \
            pattern.value.lower().strip(' ?.!') == tree[0].value.lower().strip(' ?.!'):
        return tree[1]
    else:
        # TODO
        return None


def select(tree):
    # Returns the first x in `database` such that answer(tree, y) is True
    # (for `database` made of (x, y) 2-tuples).
    try:
        return next(filter(bool, map(functools.partial(answer, tree), database)))
    except StopIteration:
        return None

class RequestHandler:
    def __init__(self, request):
        self.request = request

    def answer(self):
        output_tree = select(self.request.tree)
        if not output_tree:
            return []
        meas = {'accuracy': 1, 'relevance': 100000}
        trace = self.request.trace + [TraceItem('Oracle', output_tree, meas)]
        response = Response(language=self.request.language, tree=output_tree, measures=meas, trace=trace)
        return [response]
