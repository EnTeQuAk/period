import pytz


def build_tzinfo(tzname, tzsign='+', tzhour=0, tzmin=0):
    """
    create a tzinfo instance according to given parameters.

    tzname:
      'Z'       ... return pytz.UTC
      '' | None ... return None
      other     ... return pytz.FixedOffset
    """
    if tzname is None or tzname == '':
        return None
    if tzname == 'Z':
        return pytz.UTC
    tzsign = ((tzsign == '-') and -1) or 1
    return pytz.FixedOffset((tzsign * tzhour * 60) + tzmin)
