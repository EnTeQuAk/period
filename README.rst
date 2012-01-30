Period: Date Time Parsing for Humans
------------------------------------

Ever tried to parse ``the 3rd Sunday of the month`` but in the same time ``jeden zweiten Tag des Jahres`` (means every second day of the year) and failed with the variety of libraries out there implementing parsing but ignoring internationalisation and timezone support?

Well, this is what Period is for.

How it works::

    >>> from period import parse
    >>> parse('now')['starting']
    datetime(2012, 01, 20)
    >>> parse('May 1st 2020')
    {'expression': 'May 1st 2020', 'starting': datetime(2020, 5, 1, 0, 0), until: None,
     'tzinfo': <UTC>, 'recur': None}
    datetime.datetime(2020, 5, 1, 0, 0)
    >>> expr = parse('every third day of the year 2pm', tzinfo='Europe/Berlin')
    >>> expr
    {'expression': 'every third day of the year 2pm', 'starting': datetime(2013, 1, 3, 1, 0, tzinfo=<UTC>),
     'until': None, 'tzinfo': <UTC>, 'recur': <period.rrule.rrule instance at 0x1e385a8>}
    >>> print expr['recur']
    u'byyearday:2;dtstart:2013-01-03T00:00:00+00:00;interval:1;bysecond:0;byminute:0;freq:0;byhour:0;'

This may just be a short demonstration and only what has come to my mind.  So stay tuned :-)


This library takes ideas from `Tickle <https://github.com/lifo/tickle>`_, `Chronic <https://github.com/mojombo/chronic>`_ and uses `python-dateutil <http://labix.org/python-dateutil>`_ as much as possible.
