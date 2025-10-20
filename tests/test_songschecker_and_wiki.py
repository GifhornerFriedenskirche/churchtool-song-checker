import datetime
import types

import pytest

import songschecker
import wikiUpdate


def test_count_sng_files():
    arrangements = [
        {'name': 'A', 'files': [{'name': 'foo.sng'}, {'name': 'bar.txt'}]},
        {'name': 'B', 'files': [{'name': 'one.sng'}, {'name': 'two.sng'}]},
    ]
    counts = songschecker.count_sng_files(arrangements)
    assert counts == {'A': 1, 'B': 2}


def test_check_for_missing_sng_file_and_flags(monkeypatch):
    now = datetime.datetime(2020, 1, 1, 12, 0, 0)

    class DummyDT:
        class datetime:
            @staticmethod
            def now():
                return now

    monkeypatch.setattr(songschecker, 'datetime', DummyDT)

    json_data = {
        'data': [
            {'id': 1, 'name': 'Good Song', 'arrangements': [{'name': 'A', 'files': [{'name': 'a.sng'}]}]},
            {'id': 2, 'name': 'Bad Song', 'arrangements': [{'name': 'B', 'files': [{'name': 'b.txt'}]}]},
        ]
    }

    content, new_json = songschecker.check_for_missing_sng_file(json_data)
    assert 'Good Song' in content
    assert 'Bad Song' in content
    # flags set
    assert new_json['data'][0]['has_sng_file'] is True
    assert new_json['data'][1]['has_sng_file'] is False


def test_updateWiki_success(monkeypatch):
    # Mock requests for wikiUpdate
    class DummyResp:
        def __init__(self, json_data=None, status_code=200):
            self._json = json_data or {}
            self.status_code = status_code

        def json(self):
            return self._json

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception('Err')

    def fake_get(url, headers=None, cookies=None):
        return DummyResp(json_data={'data': [{'identifier': 'id123'}]})

    def fake_post(url, json=None, headers=None, params=None, cookies=None):
        return DummyResp(json_data={'status': 'success'})

    monkeypatch.setattr(wikiUpdate.requests, 'get', fake_get)
    monkeypatch.setattr(wikiUpdate.requests, 'post', fake_post)

    res = wikiUpdate.updateWiki('cat', 'page', 'content', 'http://api', {}, {})
    assert res == 'Update successful'


def test_updateWiki_failure(monkeypatch):
    # Test the failure branch (line 49)
    class DummyResp:
        def __init__(self, json_data=None, status_code=200):
            self._json = json_data or {}
            self.status_code = status_code

        def json(self):
            return self._json

        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception('Err')

    def fake_get(url, headers=None, cookies=None):
        return DummyResp(json_data={'data': [{'identifier': 'id123'}]})

    def fake_post(url, json=None, headers=None, params=None, cookies=None):
        return DummyResp(json_data={'status': 'failed'})  # Not 'success'

    monkeypatch.setattr(wikiUpdate.requests, 'get', fake_get)
    monkeypatch.setattr(wikiUpdate.requests, 'post', fake_post)

    res = wikiUpdate.updateWiki('cat', 'page', 'content', 'http://api', {}, {})
    assert res == 'Update failed'
