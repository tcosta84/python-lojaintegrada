from unittest import mock

import pytest
from requests.exceptions import HTTPError, RequestException

from lojaintegrada import Api, ApiError


def test_make_request(mocker):
    mock_session = mocker.patch('lojaintegrada.requests.Session')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    res = api._make_request(
        'GET', 'https://api.awsli.com.br/api/v1/pedido/search'
    )

    mock_session.return_value.request.assert_called_with(
        'GET',
        'https://api.awsli.com.br/api/v1/pedido/search',
        json=None, params=None
    )

    mock_session.return_value.request.return_value.raise_for_status.assert_called_with()

    assert res == mock_session.return_value.request.return_value.json.return_value


def test_make_request_should_raise_general_exception_for_HTTPError(mocker):
    mock_session = mocker.patch('lojaintegrada.requests.Session')

    mock_session.return_value.request.side_effect = HTTPError(
        response=mock.Mock(
            status_code=400
        )
    )

    api = Api(api_key='fake-api-key', app_key='fake-app-key')

    with pytest.raises(ApiError):
        res = api._make_request(
            'GET', 'https://api.awsli.com.br/api/v1/pedido/search'
        )


def test_make_request_should_raise_general_exception_for_RequestException(mocker):
    mock_session = mocker.patch('lojaintegrada.requests.Session')

    mock_request = mock.Mock()
    mock_session.return_value.request.side_effect = RequestException(
        request=mock_request
    )

    api = Api(api_key='fake-api-key', app_key='fake-app-key')

    with pytest.raises(ApiError) as e:
        res = api._make_request(
            'GET', 'https://api.awsli.com.br/api/v1/pedido/search'
        )

    assert e.value.request == mock_request


def test_make_request_should_retry_when_rate_limit_reached(mocker):
    mock_sleep = mocker.patch('lojaintegrada.time.sleep')
    mock_session = mocker.patch('lojaintegrada.requests.Session')

    mock_session.return_value.request.side_effect = [
        HTTPError(
            response=mock.Mock(
                status_code=429
            )
        ),
        mock.DEFAULT
    ]

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    api._make_request('GET', 'https://api.awsli.com.br/api/v1/pedido/search')

    mock_sleep.assert_called_with(10)
    assert mock_session.return_value.request.call_count == 2
    mock_session.return_value.request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/pedido/search',
        json=None, params=None
    )


def test_make_request_should_retry_with_custom_dealy_when_rate_limit_reached(mocker):
    mock_sleep = mocker.patch('lojaintegrada.time.sleep')
    mock_session = mocker.patch('lojaintegrada.requests.Session')

    mock_session.return_value.request.side_effect = [
        HTTPError(
            response=mock.Mock(
                status_code=429
            )
        ),
        mock.DEFAULT
    ]

    api = Api(
        api_key='fake-api-key',
        app_key='fake-app-key',
        rate_limit_retry_delay=5
    )
    api._make_request('GET', 'https://api.awsli.com.br/api/v1/pedido/search')

    mock_sleep.assert_called_with(5)
    assert mock_session.return_value.request.call_count == 2
    mock_session.return_value.request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/pedido/search',
        json=None, params=None
    )
