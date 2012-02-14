#-*- coding: utf-8 -*-
from period.parser import Parser


def parse(string):
    parser = Parser()
    obj = Period(string, parser.parse(string))
    return obj


class Period(object):

    def __init__(self, expression, starting, until=None, tzinfo=None, recur=None):
        self.expression = expression
        self.starting = starting
        self.until = until
        self.tzinfo = tzinfo
        self.recur = recur

    def __repr__(self):
        tmpl = ('<{mod}.{cls} (expression="{expr}", starting={starting}, until={until}, '
                'tzinfo={tzinfo}, recur={recur})>')
        mod = type(self).__module__
        cls = type(self).__name__
        return tmpl.format(mod=mod, cls=cls, expr=self.expression,
                           starting=self.starting, until=self.until,
                           tzinfo=self.tzinfo, recur=self.recur)
