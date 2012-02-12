#-*- coding: utf-8 -*-

#TODO: for now only an alias for iso8601 parsing, will be expanded later.
from period.iso8601 import parse_date as parse_iso8601

def parse(string):
    obj = Period(string, parse_iso8601(string))
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
