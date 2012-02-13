Period: Date Time Parsing for Humans
------------------------------------

Ever tried to parse ``the 3rd Sunday of the month`` but in the same time ``jeden zweiten Tag des Jahres`` (means every second day of the year) and failed with the variety of libraries out there implementing parsing but ignoring internationalisation and timezone support?

Well, this is what Period is for.

How it works::

    >>> from period import parse
    >>> period = parse('now')
    >>> period
    <period.Period at 0x2e6c0d0>
    >>> period.starting
    datetime(2012, 01, 20)
    >>> str(parse('May 1st 2020'))
    <period.Period (expression="May 1st 2020", starting=datetime(2020, 5, 1, 0, 0),
                    until=None, tzinfo=<UTC>, recur=None)>
    >>> period = parse('every third day of the year 2pm', tzinfo='Europe/Berlin')
    >>> str(period)
    <period.Period (expression='every third day of the year 2pm',
                    starting=datetime(2013, 1, 3, 1, 0, tzinfo=<UTC>),
                    until=None, tzinfo=<UTC>, recur=<period.rrule.rrule instance at 0x1e385a8>)>
    >>> print period.recur
    u'byyearday:2;dtstart:2013-01-03T00:00:00+00:00;interval:1;bysecond:0;byminute:0;freq:0;byhour:0;'

This may just be a short demonstration and only what has come to my mind.  So stay tuned :-)

This library takes ideas from `Tickle <https://github.com/lifo/tickle>`_, `Chronic <https://github.com/mojombo/chronic>`_ and tries to reuse existing packages as much as possible.

But I also aim to replace `python-dateutil <http://labix.org/python-dateutil>`_ to fix it's packaging and create a simpler API.

Key features
------------

 * Forces UTC, if no tzinfo is given, UTC is used.  If a tzinfo is applied, it's converted to UTC
   This also is implemented in an iso8601 compatible way by assuming that applied dates
   are given in local time if no timezone is given.
 * Compatible with Python 3.2+ and Python 2.7+ (maybe 2.6+ I cannot test this right now)
 * Simple API that does what it's supposed to do without any clutter
 * Add features if needed, do not clutter the API with features no one uses.
