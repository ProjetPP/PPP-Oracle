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
        R('Question-answering tool')),

        (T(R('your'), R('website'), M()),
        R('http://projetpp.github.io/')),

        (T(T(R('your'), R('source code'), M()), R('location'), M()),
        R('http://github.com/ProjetPP/')),

        (T(R('I'), R('identity'), M()),
        R('Internaut')),

        (S('P=NP?'),
        R('maybe')),

        (S('NP=P?'),
        R('maybe')),

        (T(R('I'), R('location'), M()),
        R('Try looking around yourself, I can\'t help much')),

        (T(R('You'), R('location'), M()),
        R('askplatyp.us')),

        (S('Do you like me?'),
        R('Definitely. Wanna hug?')),

        (S('yes'),
        R('Sorry, I don\'t remember what we said earlier.')),

        (S('no'),
        R('Sorry, I don\'t remember what we said earlier.'))
        ]


def eq(left, right):
    if left.type != right.type:
        return False
    elif isinstance(left, R):
        return left.value.lower() == right.value.lower()
    elif isinstance(left, T):
        return eq(left.subject, right.subject) and \
                eq(left.predicate, right.predicate) and \
                eq(left.object, right.object)
    else:
        # TODO
        return False

def answer(pattern, tree):
    if isinstance(pattern, M):
        return tree[1]
    elif eq(pattern, tree[0]):
        return R('yes')
    elif isinstance(pattern, T) and isinstance(tree[0], T):
        # Is there a subtree of the triple that is a missing?
        # I yes, just return what should be there
        if isinstance(pattern.subject, M) and \
                eq(pattern.predicate, tree[0].predicate) and \
                eq(pattern.object, tree[0].object):
            return tree[1]
        elif isinstance(pattern.object, M) and \
                eq(pattern.predicate, tree[0].predicate) and \
                eq(pattern.subject, tree[0].subject):
            return tree[1]
        elif isinstance(pattern.predicate, M) and \
                eq(pattern.subject, tree[0].subject) and \
                eq(pattern.object, tree[0].object):
            return tree[1]
        else:
            return None
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
