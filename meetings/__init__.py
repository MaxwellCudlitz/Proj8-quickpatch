import flask
from .modules.processing import free_times

def test_freetime():
    free_times.test_empty_calc()
    free_times.test_free_calc()
    free_times.test_malformed_prams()
