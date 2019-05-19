from requests import Session

from lojaintegrada import Api


def test_build_session(mocker):
    api = Api(api_key='fake-api-key', app_key='fake-app-key')

    assert isinstance(api.session, Session)
    assert api.session.headers['Content-type'] == 'application/json'
    assert api.session.headers['Authorization'] == 'chave_api fake-api-key aplicacao fake-app-key'
