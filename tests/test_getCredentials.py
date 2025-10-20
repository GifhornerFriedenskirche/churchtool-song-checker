import pytest

import getCredentials


class DummyResp:
    def __init__(self, json_data=None, cookies=None, status_code=200):
        self._json = json_data or {}
        self._cookies = cookies or {}
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("Bad")

    @property
    def cookies(self):
        class C:
            def __init__(self, d):
                self._d = d

            def get_dict(self):
                return self._d

        return C(self._cookies)


def test_get_tokens_and_cookie_success(monkeypatch):
    # sequence of responses for post(login), get(csrf), get(login token)
    responses = [
        DummyResp(json_data={'data': {'personId': 11}}, cookies={'session': 'x'}),
        DummyResp(json_data={'data': 'csrf-token'}),
        DummyResp(json_data={'data': 'logintoken'})
    ]

    def fake_post(url, json=None, headers=None):
        # pop the first (post) response
        return responses.pop(0)

    def fake_get(url, cookies=None, headers=None):
        # Return and pop the first matching get response
        return responses.pop(0)

    monkeypatch.setattr(getCredentials.requests, 'post', fake_post)
    monkeypatch.setattr(getCredentials.requests, 'get', fake_get)

    headers, cookie = getCredentials.get_tokens_and_cookie('u', 'p', 'http://api')
    assert 'authorization' in headers
    assert headers['X-CSRFToken'] == 'csrf-token'
    assert isinstance(cookie, dict)
