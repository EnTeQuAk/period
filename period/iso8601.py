#-*- coding: utf-8 -*-
import re
import itertools
from datetime import date, timedelta


#: All possible date format regular expressions.
DATE_REGEXES = []

#: Compile set of regular expressions to parse ISO dates.
#:
#: Besides the fact that it would be necessary to fix the number
#: of year digits we do not because we parse a bit more fuzzy
#: to support a wider range of formats.
#: Thus we cannot distinguish between various ISO date formats
#: but just "support them".
#: ISO 8601 expanded DATE formats allow an arbitrary number of year
#: digits with a leading +/- sign.
#: TODO: We currently only support 4 and 6 yeardigits, support for more
#:       should be not be that hard.

cases = [(1, 6), (0, 4)]


for sign, yeardigits in cases:
    # 1. complete dates:
    #    YYYY-MM-DD or +- YYYYYY-MM-DD... extended date format
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})"
                                  r"-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
                                  % (sign, yeardigits)))
    #    YYYYMMDD or +- YYYYYYMMDD... basic date format
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})"
                                  r"(?P<month>[0-9]{2})(?P<day>[0-9]{2})" 
                                  % (sign, yeardigits)))
    # 2. complete week dates:
    #    YYYY-Www-D or +-YYYYYY-Www-D ... extended week date
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})"
                                  r"-W(?P<week>[0-9]{2})-(?P<day>[0-9]{1})"
                                  % (sign, yeardigits)))
    #    YYYYWwwD or +-YYYYYYWwwD ... basic week date
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})W"
                                  r"(?P<week>[0-9]{2})(?P<day>[0-9]{1})"
                                  % (sign, yeardigits)))
    # 3. ordinal dates:
    #    YYYY-DDD or +-YYYYYY-DDD ... extended format
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})"
                                  r"-(?P<day>[0-9]{3})"
                                  % (sign, yeardigits)))
    #    YYYYDDD or +-YYYYYYDDD ... basic format
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})"
                                  r"(?P<day>[0-9]{3})"
                                  % (sign, yeardigits)))
    # 4. week dates:
    #    YYYY-Www or +-YYYYYY-Www ... extended reduced accuracy week date
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})"
                                  r"-W(?P<week>[0-9]{2})"
                                  % (sign, yeardigits)))
    #    YYYYWww or +-YYYYYYWww ... basic reduced accuracy week date 
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})W"
                                  r"(?P<week>[0-9]{2})"
                                  % (sign, yeardigits)))
    # 5. month dates:
    #    YYY-MM or +-YYYYYY-MM ... reduced accuracy specific month
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})"
                                  r"-(?P<month>[0-9]{2})"
                                  % (sign, yeardigits)))
    # 6. year dates:
    #    YYYY or +-YYYYYY ... reduced accuracy specific year
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}(?P<year>[0-9]{%d})"
                                  % (sign, yeardigits)))

#: Must be appended at last.
for sign, yeardigits in cases:
    # 7. century dates:
    #    YY or +-YYYY ... reduced accuracy specific century
    DATE_REGEXES.append(re.compile(r"(?P<sign>[+-]){%d}"
                                   r"(?P<century>[0-9]{%d})"
                                  % (sign, yeardigits - 2)))


def parse_date(string):
    """
    Parse an ISO 8601 string into a period.Period object.
    """
    for pattern in DATE_REGEXES:
        match = pattern.match(string)
        if match:
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
    raise ValueError('Unrecognised ISO 8601 date format: %r' % string)
