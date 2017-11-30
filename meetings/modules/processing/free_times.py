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

    # aggregates free times
    free_times = []

    tmp_start_time = begin
    tmp_end_time = None

    # add all in-between free times
    for event in busy:
        tmp_end_time = event['start']
        free_times = _try_append_date(tmp_start_time, tmp_end_time, free_times)
        tmp_start_time = event['end']
        # tmp_end_time = event['start']

        # tmp_date = json_date_schema.try_format_date(
        #     tmp_start_time, tmp_end_time,
        #     "N/A", True
        # )
        # free_times.append(tmp_date)
        # tmp_start_time = event['end']


    # add remaining time block between event and end
    free_times = _try_append_date(tmp_start_time, end, free_times)
    # tmp_date = json_date_schema.tryformat_date(
    #     tmp_start_time, end,
    #     "N/A", True
    # )
    # if(tmp_date is not None):
    #     free_times.append(tmp_date)

def _try_append_date(begin, end, append_list):
    """
    Attempts to add a formatted date object to 
    append_list. If it fails in formatting a date
    object, it will just return the source list.
    """
    tmp_date = json_date_schema.try_format_date(
       begin, end, "N/A", True
    )

    if(tmp_date is not None):
        append_list.append(tmp_date)

    return append_list