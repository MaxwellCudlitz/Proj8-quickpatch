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

    if (arrow.get(end) > arrow.get(start) or not _assert_date_prams(start, end, calendar, busy)):
        return None
    
    return format_date(start, end, calendar, busy)


    

def format_date(start, end, calendar, busy):
    """
    formats a start date, end date, calendar name, and business state into 
    an object using an object builder.

    Raises an exception if data prams are invalid.
    """
    return ({
        'start' : arrow.get(start).to('local').format('YYYY-MM-DD HH:mm:ss'),
        'end' : arrow.get(end).to('local').format('YYYY-MM-DD HH:mm:ss'),
        'cal' : calendar,
        'busy' : busy
    })
    
def _assert_date_prams(start, end, calendar, busy):

    """assertion for existence of all parameters"""
    return start and end and calendar and busy != None and (end > start)
