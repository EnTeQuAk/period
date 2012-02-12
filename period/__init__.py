#-*- coding: utf-8 -*-

#TODO: for now only an alias for iso8601 parsing, will be expanded later.
from period.iso8601 import parse_date as parse_iso8601

def parse(string):
    obj = Period()
    obj.starting = parse_iso8601(string)
    return obj


class Period(object):
    starting = None
