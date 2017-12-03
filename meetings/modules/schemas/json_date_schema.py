"""
schema for exported JSON date objects
"""

import arrow

def try_format_date(start, end, calendar, busy):
    """
    format_date with a validity check for the beginning and
    end times of the event being formatted, returning a 
    Nonetype instead of an exception if format invalid.
    """
    start = arrow.get(start)
    end = arrow.get(end)
    if not _assert_date_prams(start, end, calendar, busy):
        return None
    
    return _format_date(start, end, calendar, busy)

def _format_date(start, end, calendar, busy):
    """
    formats a start date, end date, calendar name, and business state into 
    an object using an object builder.

    Raises an exception if data prams are invalid.
    """
    return {
        # 'start' : arrow.get(start).format('YYYY-MM-DD HH:mm:ss'),
        # 'end' : arrow.get(end).format('YYYY-MM-DD HH:mm:ss'),
        'start' : arrow.get(start).isoformat(),
        'end' : arrow.get(end).isoformat(),
        'cal' : calendar,
        'busy' : busy
    }
    
def _assert_date_prams(start, end, calendar, busy):

    """assertion for existence of all parameters"""
    return start and end and calendar and busy != None and (end > start) and (end is not start)
