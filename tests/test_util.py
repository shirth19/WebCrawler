import os
import json
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import util


def test_extract_key():
    data = {'a': {'b': 1}, 'c': [ {'d': 2} ]}
    assert util.extract_key(data, 'b') == 1
    assert util.extract_key(data, 'd') == 2
    assert util.extract_key(data, 'z') is None


def test_extract_all_keys():
    data = {'a': {'text': 'first'}, 'b': [{'text': 'second'}, {'text': 'third'}]}
    results = list(util.extract_all_keys(data, 'text'))
    assert results == ['first', 'second', 'third']


def test_write_to_file(tmp_path):
    file_dir = tmp_path / 'out'
    util.write_to_file('sample', {'k': 'v'}, str(file_dir))
    file_path = file_dir / 'sample.json'
    with open(file_path) as f:
        content = json.load(f)
    assert content == {'k': 'v'}
