#-*- coding: utf-8 -*-
import re
import itertools
from datetime import date, timedelta, time
from decimal import Decimal
from period.constants import EXPRESSIONS
from period.tzinfo import build_tzinfo


class Parser(object):

    def __init__(self):
        #: These rules are named after predefined constants in period.constants
        self.rules = {
            self.handle_date: ('complete_date', 'basic_date', 'basic_week_date',
                               'ordinal_date', 'basic_date_format', 'week_date',
                               'basic_reduced_accuracy_week_date', 'month_date',
                               'year_date', 'century_date', 'complete_week_date'),
            self.handle_time: ('complete_time', 'basic_time',
                               'reduced_accuracy_time')}

    def parse(self, string):
        mapping = {}
        for handler, values in self.rules.items():
            for value in values:
                mapping[value] = handler

        if not string:
            return None
        for handler, expr in EXPRESSIONS:
            match = expr.match(string)
            if match:
                return mapping[handler](match)
        return None

    def handle_date(self, match):
        groups = match.groupdict()
        # sign, century, year, month, week, day,
        # FIXME: negative dates not possible with python standard types
        sign = (groups['sign'] == '-' and -1) or 1
        if 'century' in groups:
            return date(sign * (int(groups['century']) * 100 + 1), 1, 1)
        if not 'month' in groups: # weekdate or ordinal date
            ret = date(sign * int(groups['year']), 1, 1)
            if 'week' in groups:
                isotuple = ret.isocalendar()
                if 'day' in groups:
                    days = int(groups['day'] or 1)
                else:
                    days = 1
                # if first week in year, do weeks-1
                return ret + timedelta(weeks=int(groups['week']) -
                                        (((isotuple[1] == 1) and 1) or 0),
                                       days = -isotuple[2] + days)
            elif 'day' in groups: # ordinal date
                return ret + timedelta(days=int(groups['day'])-1)
            else:  # year date
                return ret
        # year-, month-, or complete date
        if 'day' not in groups or groups['day'] is None:
            day = 1
        else:
            day = int(groups['day'])
        return date(sign * int(groups['year']),
                    int(groups['month']) or 1, day)

    def handle_time(self, match):
        groups = match.groupdict()
        for key, value in groups.items():
            if value is not None:
                groups[key] = value.replace(',', '.')
        tzinfo = build_tzinfo(groups['tzname'], groups['tzsign'],
                              int(groups['tzhour'] or 0),
                              int(groups['tzmin'] or 0))
        if 'second' in groups:
            second = Decimal(groups['second'])
            microsecond = (second - int(second)) * Decimal(1e6)
            # int(...) ... no rounding
            # to_integral() ... rounding
            return time(int(groups['hour']), int(groups['minute']),
                        int(second), microsecond.to_integral(), tzinfo)
        if 'minute' in groups:
            minute = Decimal(groups['minute'])
            second = (minute - int(minute)) * 60
            microsecond = (second - int(second)) * Decimal(1e6)
            return time(int(groups['hour']), int(minute), int(second),
                        microsecond.to_integral(), tzinfo)
        else:
            microsecond, second, minute = 0, 0, 0
        hour = Decimal(groups['hour'])
        minute = (hour - int(hour)) * 60
        second = (minute - int(minute)) * 60
        microsecond = (second - int(second)) * Decimal(1e6)
        return time(int(hour), int(minute), int(second),
                    microsecond.to_integral(), tzinfo)
