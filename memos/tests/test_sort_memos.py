"""
Nose tests for sort() in flask_main.py
"""

from flask_main import sort_memos

import nose
import logging


good_record = [{'type': 'dated_memo', 'date': '2011-10-06T23:57:06.603000+00:00', 'text': 'Long time ago', 'token': '2a53afd6-64c3-4709-8369-525292f40750'},
               {'type': 'dated_memo', 'date': '2019-11-07T00:58:39.783000+00:00', 'text': 'Into da future', 'token': '3636e3d6-fb6d-4e91-92c8-f89e9d0d3844'},
               {'type': 'dated_memo', 'date': '2017-11-08T00:58:12.474000+00:00', 'text': 'Tomorrow', 'token': 'b16b751c-f5ad-4e3d-9a6e-aec91fbd6353'},
               {'type': 'dated_memo', 'date': '2017-11-07T00:54:55.459000+00:00', 'text': 'asd', 'token': 'bbdf133f-c2cd-4be9-a014-29bb7cc86c0e'},
               {'type': 'dated_memo', 'date': '2017-11-06T00:57:23.914000+00:00', 'text': 'it was yesterday', 'token': 'be752670-781c-4e28-9efc-642a37cf0d89'}]

bad_record = [{'type': 'dated_memo', 'text': 'Long time ago', 'token': '2a53afd6-64c3-4709-8369-525292f40750'},
              {'type': 'dated_memo', 'text': 'Into da future', 'token': '3636e3d6-fb6d-4e91-92c8-f89e9d0d3844'},
              {'type': 'dated_memo', 'text': 'Tomorrow', 'token': 'b16b751c-f5ad-4e3d-9a6e-aec91fbd6353'},
              {'type': 'dated_memo', 'text': 'asd', 'token': 'bbdf133f-c2cd-4be9-a014-29bb7cc86c0e'},
              {'type': 'dated_memo', 'text': 'it was yesterday', 'token': 'be752670-781c-4e28-9efc-642a37cf0d89'}]


def test_empty():
    """
    The record is empty.
    """
    assert sort_memos([]) == []


def test_good():
    """
    An list of memos with no errors
    """
    assert sort_memos(good_record) == [{'type': 'dated_memo', 'date': '2011-10-06T23:57:06.603000+00:00', 'text': 'Long time ago', 'token': '2a53afd6-64c3-4709-8369-525292f40750'},
                                 {'type': 'dated_memo', 'date': '2017-11-06T00:57:23.914000+00:00', 'text': 'it was yesterday', 'token': 'be752670-781c-4e28-9efc-642a37cf0d89'},
                                 {'type': 'dated_memo', 'date': '2017-11-07T00:54:55.459000+00:00', 'text': 'asd', 'token': 'bbdf133f-c2cd-4be9-a014-29bb7cc86c0e'},
                                 {'type': 'dated_memo', 'date': '2017-11-08T00:58:12.474000+00:00', 'text': 'Tomorrow', 'token': 'b16b751c-f5ad-4e3d-9a6e-aec91fbd6353'},
                                 {'type': 'dated_memo', 'date': '2019-11-07T00:58:39.783000+00:00', 'text': 'Into da future', 'token': '3636e3d6-fb6d-4e91-92c8-f89e9d0d3844'}]


def test_bad_date():
    """
    Can't compare because no dates to compare.
    """
    assert sort_memos(bad_record) == 'Error'


logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)