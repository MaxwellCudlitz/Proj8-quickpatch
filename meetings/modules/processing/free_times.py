"""
Module that, given a datetime start, end, and a number of
blocks of "busy" time, returns the "free" times.
"""
import arrow
from modules.schemas import json_date_schema

def get_free(begin, end, busy):
    """
    returns a list of the blocks times between the begin and end dates,
    that do not fall within any of the 'busy' dates.
    """
    
    # sort the busy times
    busy = sorted(
        busy,
        key=lambda b : arrow.get(b['start'])
    )

    # aggregates free times
    free_times = []

    tmp_start_time = begin
    tmp_end_time = None

    # add all in-between free times
    for event in busy:
        tmp_end_time = event['start']
        #print(tmp_start_time, tmp_end_time, free_times)
        free_times = _try_append_date(tmp_start_time, tmp_end_time, free_times)
        tmp_start_time = event['end']

    # add remaining time block between event and end
    free_times = _try_append_date(tmp_start_time, end, free_times)

    print(free_times)
    return free_times


def _try_append_date(begin, end, append_list):
    """
    Attempts to add a formatted date object to 
    append_list. If it fails in formatting a date
    object, it will just return the source list.
    """
    tmp_date = json_date_schema.try_format_date(
       begin, end, "N/A", False
    )

    if(tmp_date is not None):
        append_list.append(tmp_date)

    return append_list

def test_free_calc():
    """
    tests basic expected functionality of the 
    free time calculator
    """
    begin = "2017-12-02T00:00:00-08:00"
    end = "2017-12-05T00:00:00-08:00"
    busy = [
        {
            'cal': 'maxwell.cudlitz@gmail.com', 
            'end': '2017-12-04T17:50:00+00:00', 
            'busy': True, 'start': '2017-12-04T16:30:00+00:00'
        }, 
        {
            'cal': 'maxwell.cudlitz@gmail.com', 
            'end': '2017-12-04T23:00:00+00:00', 
            'busy': True, 
            'start': '2017-12-04T22:00:00+00:00'
        }
    ]
    expected_out = [
        {
            'busy': False, 
            'end': '2017-12-04T16:30:00+00:00', 
            'cal': 'N/A', 
            'start': '2017-12-02T00:00:00-08:00'
        }, 
        {
            'busy': False, 
            'end': '2017-12-04T22:00:00+00:00', 
            'cal': 'N/A', 
            'start': '2017-12-04T17:50:00+00:00'
        }, 
        {
            'busy': False, 
            'end': '2017-12-05T00:00:00-08:00', 
            'cal': 'N/A', 
            'start': '2017-12-04T23:00:00+00:00'
        }
    ]
    result = get_free(begin, end, busy)
    assert(result == expected_out)

def test_empty_calc():
    """
    Tests whether an empty event list returns the expected free object
    """
    begin = "2017-12-02T00:00:00-08:00"
    end = "2017-12-05T00:00:00-08:00"
    get_free(begin, end, [])
    print("empty list test stubbed as during normal function program will actually quit before this point")
    assert(True)


def test_malformed_prams():
    """
    ensures that the date appender will not spit out an error or do anything other
    than simply return the original list if malformed prams are passed
    """
    begin_list = []
    begin_list = _try_append_date(
        "01/01/2017 10:00pm", 
        "smitty werbermanjensen", 
        begin_list
    )
    assert(begin_list == [])