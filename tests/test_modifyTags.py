import types
import pytest

import modifyTags


class MockResp:
    def __init__(self, status_code=200, json_data=None, content=b'', cookies_obj=None):
        self.status_code = status_code
        self._json = json_data or {}
        self.content = content
        self.cookies = cookies_obj

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")


def test_get_tag_id_found(monkeypatch):
    data = {'data': [{'id': 7, 'name': 'mytag'}]}

    def fake_get(url, cookies=None, headers=None):
        return MockResp(json_data=data)

    monkeypatch.setattr(modifyTags.requests, 'get', fake_get)
    tag_id = modifyTags.get_tag_id('http://api', {}, {}, 'mytag', type='song')
    assert tag_id == 7


def test_get_tag_id_wrong_type():
    # unsupported type returns None
    assert modifyTags.get_tag_id('http://api', {}, {}, 'x', type='unsupported') is None


def test_create_tag_success(monkeypatch):
    resp_json = {'data': {'id': 42}}

    def fake_post(url, cookies=None, headers=None, json=None):
        return MockResp(status_code=200, json_data=resp_json)

    monkeypatch.setattr(modifyTags.requests, 'post', fake_post)
    tag_id = modifyTags.create_tag('http://api', {}, {}, 'tagname', type='song')
    assert tag_id == 42


def test_create_tag_fail(monkeypatch):
    def fake_post(url, cookies=None, headers=None, json=None):
        return MockResp(status_code=500, json_data={})

    monkeypatch.setattr(modifyTags.requests, 'post', fake_post)
    tag_id = modifyTags.create_tag('http://api', {}, {}, 'tagname', type='song')
    assert tag_id is None


def test_add_tag_to_song_duplicate(monkeypatch):
    def fake_put(url, cookies=None, headers=None):
        return MockResp(status_code=500, content=b'Duplicate entry')

    monkeypatch.setattr(modifyTags.requests, 'put', fake_put)
    assert modifyTags.add_tag_to_song('http://api', {}, {}, 1, 2, type='song') == 200


def test_add_tag_to_song_ok(monkeypatch):
    def fake_put(url, cookies=None, headers=None):
        return MockResp(status_code=200)

    monkeypatch.setattr(modifyTags.requests, 'put', fake_put)
    assert modifyTags.add_tag_to_song('http://api', {}, {}, 1, 2, type='song') == 200


def test_remove_tag_returns_response(monkeypatch):
    called = {}

    def fake_delete(url, cookies=None, headers=None):
        called['url'] = url
        return MockResp(status_code=204)

    monkeypatch.setattr(modifyTags.requests, 'delete', fake_delete)
    resp = modifyTags.remove_tag('http://api', {}, {}, 5, 6, type='song')
    assert isinstance(resp, MockResp)
    assert called['url'].endswith('/api/tags/song/5/6')


def test_get_tag_id_person(monkeypatch):
    data = {'data': [{'id': 3, 'name': 'p1'}]}

    def fake_get(url, cookies=None, headers=None):
        return MockResp(json_data=data)

    monkeypatch.setattr(modifyTags.requests, 'get', fake_get)
    tag_id = modifyTags.get_tag_id('http://api', {}, {}, 'p1', type='person')
    assert tag_id == 3


def test_add_tag_to_song_error(monkeypatch):
    def fake_put(url, cookies=None, headers=None):
        return MockResp(status_code=500, content=b'Other error')

    monkeypatch.setattr(modifyTags.requests, 'put', fake_put)
    assert modifyTags.add_tag_to_song('http://api', {}, {}, 1, 2, type='song') == 500


def test_get_tag_id_not_found(monkeypatch):
    # Test the branch where tag is not found (line 37)
    data = {'data': [{'id': 7, 'name': 'othertag'}]}

    def fake_get(url, cookies=None, headers=None):
        return MockResp(json_data=data)

    monkeypatch.setattr(modifyTags.requests, 'get', fake_get)
    tag_id = modifyTags.get_tag_id('http://api', {}, {}, 'notfound', type='song')
    assert tag_id is None


def test_create_tag_invalid_type():
    # Test the branch where invalid type returns None (line 62)
    assert modifyTags.create_tag('http://api', {}, {}, 'tagname', type='invalid') is None
