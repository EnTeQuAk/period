import re
import itertools
from datetime import date, timedelta, time


#: Regular expressions that can be tagged, sorted by priority.
EXPRESSIONS = []


# ISO 8601 time representations allow decimal fractions on least
#    significant time component. Command and Full Stop are both valid
#    fraction separators.
#    The letter 'T' is allowed as time designator in front of a time
#    expression.
#    Immediately after a time expression, a time zone definition is
#      allowed.
#    a TZ may be missing (local time), be a 'Z' for UTC or a string of
#    +-hh:mm where the ':mm' part can be skipped.
# TZ information patterns:
#    ''
#    Z
#    +-hh:mm
#    +-hhmm
#    +-hh =>
#    isotzinfo.TZ_REGEX

TZ_REGEX = r"(?P<tzname>(Z|(?P<tzsign>[+-])"\
           r"(?P<tzhour>[0-9]{2})(:(?P<tzmin>[0-9]{2}))?)?)"

EXPRESSIONS.extend([
    # 1. complete time:
    #    hh:mm:ss.ss ... extended format
    ('complete_time', r"T?(?P<hour>[0-9]{2}):"
                      r"(?P<minute>[0-9]{2}):"
                      r"(?P<second>[0-9]{2}([,.][0-9]+)?)"
                      + TZ_REGEX),


    #    hhmmss.ss ... basic format
    ('basic_time', r"T?(?P<hour>[0-9]{2})"
                   r"(?P<minute>[0-9]{2})"
                   r"(?P<second>[0-9]{2}([,.][0-9]+)?)"
                   + TZ_REGEX),

    # 2. reduced accuracy:
    #    hh:mm.mm ... extended format
    ('reduced_accuracy_time', r"T?(?P<hour>[0-9]{2}):"
                              r"(?P<minute>[0-9]{2}([,.][0-9]+)?)"
                              + TZ_REGEX),

    #    hhmm.mm ... basic format
    ('basic_time', r"T?(?P<hour>[0-9]{2})"
                   r"(?P<minute>[0-9]{2}([,.][0-9]+)?)"
                   + TZ_REGEX),

    #    hh.hh ... basic format
    ('basic_time', r"T?(?P<hour>[0-9]{2}([,.][0-9]+)?)"
                   + TZ_REGEX)
])



#: Compile set of regular expressions to parse ISO dates.
#:
#: Besides the fact that it would be necessary to fix the number
#: of year digits to support proper parsing, we do not because we parse a
#: bit more fuzzy to support a wider range of formats.
#: Thus we cannot distinguish between various ISO date formats
#: but just "support them".
#: ISO 8601 expanded DATE formats allow an arbitrary number of year
#: digits with a leading +/- sign.

EXPRESSIONS.extend([
    # 1. complete dates:
    #    YYYY-MM-DD or +- YYYYYY-MM-DD... extended date format
    ('complete_date', r"(?P<sign>[+-]){0,1}(?P<year>[0-9]{4,6})"
                      r"-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"),

    #    YYYYMMDD or +- YYYYYYMMDD... basic date format
    ('basic_date', r"(?P<sign>[+-]){0}(?P<year>[0-9]{4})"
                   r"(?P<month>[0-9]{2})(?P<day>[0-9]{2})"),

    #    YYYYMMDD or +- YYYYYYMMDD... basic date format
    ('basic_date', r"(?P<sign>[+-]){1}(?P<year>[0-9]{6})"
                   r"(?P<month>[0-9]{2})(?P<day>[0-9]{2})"),

    # 2. complete week dates:
    #    YYYY-Www-D or +-YYYYYY-Www-D ... extended week date
    ('complete_week_date', r"(?P<sign>[+-]){0,1}(?P<year>[0-9]{4,6})"
                           r"-W(?P<week>[0-9]{2})-(?P<day>[0-9]{1})"),

    #    YYYYWwwD or +-YYYYYYWwwD ... basic week date
    ('basic_week_date', r"(?P<sign>[+-]){0,1}(?P<year>[0-9]{4,6})W"
                        r"(?P<week>[0-9]{2})(?P<day>[0-9]{1})"),

    # 3. ordinal dates:
    #    YYYY-DDD or +-YYYYYY-DDD ... extended format
    ('ordinal_date', r"(?P<sign>[+-]){0,1}(?P<year>[0-9]{4,6})"
                     r"-(?P<day>[0-9]{3})"),

    #    YYYYDDD or +-YYYYYYDDD ... basic format
    ('basic_date_format', r"(?P<sign>[+-]){0,1}(?P<year>[0-9]{4,6})"
                          r"(?P<day>[0-9]{3})"),

    # 4. week dates:
    #    YYYY-Www or +-YYYYYY-Www ... extended reduced accuracy week date
    ('week_date', r"(?P<sign>[+-]){0,1}(?P<year>[0-9]{4,6})"
                  r"-W(?P<week>[0-9]{2})"),

    #    YYYYWww or +-YYYYYYWww ... basic reduced accuracy week date
    ('basic_reduced_accuracy_week_date', r"(?P<sign>[+-]){0,1}(?P<year>[0-9]{4,6})W"
                                         r"(?P<week>[0-9]{2})"),

    # 5. month dates:
    #    YYY-MM or +-YYYYYY-MM ... reduced accuracy specific month
    ('month_date', r"(?P<sign>[+-]){0,1}(?P<year>[0-9]{4,6})"
                   r"-(?P<month>[0-9]{2})"),

    # 7. century dates:
    #    YY or +-YYYY ... reduced accuracy specific century
    ('century_date', r"(?P<sign>[+-]){1}"
                     r"(?P<century>[0-9]{4})$"),

    ('century_date', r"(?P<sign>[+-]){0}"
                     r"(?P<century>[0-9]{2})$"),

    # 6. year dates:
    #    YYYY or +-YYYYYY ... reduced accuracy specific year
    ('year_date', r"(?P<sign>[+-]){0,1}(?P<year>[0-9]{4,6})"),

])



# Compile all regular expressions, eases debugging and boosts
# performance.
for idx, val in enumerate(EXPRESSIONS):
    EXPRESSIONS[idx] = (val[0], re.compile(val[1]))
