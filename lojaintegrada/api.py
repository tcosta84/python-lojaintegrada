import logging
import requests
import time

from .exceptions import ApiError

logger = logging.getLogger(__name__)


class LIApi(object):
    """A Python API Wrapper for "Loja Integrada" e-commerce platform."""

    def __init__(self, api_key, app_key, rate_limit_retry_delay=10):
        """
        Parameters:
        -----------

            api_key (str):
                Your store's api key

            app_key (str):
                Your store's app key

            rate_limit_retry_delay (int):
                How many seconds to wait between retries.
                Defaults to 10.
        """

        self.root_uri = 'https://api.awsli.com.br'
        self.version = 'v1'
        self.rate_limit_retry_delay = rate_limit_retry_delay

        self.session = self._build_session(api_key, app_key)

    def get_brand(self, id):
        uri = '/api/{}/marca/{}'.format(self.version, id)
        url = '{}{}'.format(self.root_uri, uri)
        return self._make_request('GET', url)

    def get_category(self, id):
        uri = '/api/{}/categoria/{}'.format(self.version, id)
        url = '{}{}'.format(self.root_uri, uri)
        return self._make_request('GET', url)

    def get_customer(self, id):
        uri = '/api/{}/cliente/{}'.format(self.version, id)
        url = '{}{}'.format(self.root_uri, uri)
        return self._make_request('GET', url)

    def get_order(self, id):
        """Returns a single order given the order's ID.

        Params:
        -------
        :param key: int
            The order ID

        Raises:
        -------
            - ApiError
            - ApiRateLimitError
        """
        uri = '/api/{}/pedido/{}'.format(self.version, id)
        url = '{}{}'.format(self.root_uri, uri)
        return self._make_request('GET', url)

    def get_orders(self, limit=50, **filters):
        """Returns a generator containing orders."""
        uri = '/api/{}/pedido/search'.format(self.version)
        url = '{}{}'.format(self.root_uri, uri)
        return self._get_objects(url, limit=limit, **filters)

    def get_price(self, product_id):
        uri = '/api/{}/produto_preco/{}'.format(self.version, product_id)
        url = '{}{}'.format(self.root_uri, uri)
        return self._make_request('GET', url)

    def get_product(self, id):
        uri = '/api/{}/produto/{}'.format(self.version, id)
        url = '{}{}'.format(self.root_uri, uri)
        return self._make_request('GET', url)

    def get_product_images(self, id):
        uri = '/api/{}/produto_imagem/?produto={}'.format(self.version, id)
        url = '{}{}'.format(self.root_uri, uri)
        return self._make_request('GET', url)

    def get_products(self, limit=50, **filters):
        """Returns a generator containing products."""
        uri = '/api/{}/produto/'.format(self.version)
        url = '{}{}'.format(self.root_uri, uri)
        return self._get_objects(url, limit=limit, **filters)

    def get_status_history(self, limit=50, order_id=None):
        """Returns a generator containing status history."""
        uri = '/api/{}/situacao_historico/search'.format(self.version)
        url = '{}{}'.format(self.root_uri, uri)
        return self._get_objects(url, numero=order_id, limit=limit)

    def get_stock(self, product_id):
        uri = '/api/{}/produto_estoque/{}'.format(self.version, product_id)
        url = '{}{}'.format(self.root_uri, uri)
        return self._make_request('GET', url)

    def update_order_status(self, id, status):
        data = {'codigo': status}
        uri = '/api/{}/situacao/pedido/{}'.format(self.version, id)
        url = '{}{}'.format(self.root_uri, uri)
        return self._make_request('PUT', url, data=data)

    def get_paid_orders(self, limit=50, **filters):
        """Returns a generator containing orders with status "pedido pago"."""
        return self.get_orders(limit=limit, situacao_id=4, **filters)

    def get_in_separation_orders(self, limit=50, **filters):
        """Returns a generator containing orders with status "pedido_em_separacao"."""
        return self.get_orders(limit=limit, situacao_id=15, **filters)

    def mark_order_as_delivered(self, id):
        return self.update_order_status(id, 'pedido_entregue')

    def mark_order_as_in_separation(self, id):
        return self.update_order_status(id, 'pedido_em_separacao')

    def _get_objects(self, url, **params):
        while url:
            data = self._make_request('GET', url, params=params)
            yield data
            next_uri = data['meta']['next']
            if next_uri:
                url = '{}{}'.format(self.root_uri, next_uri)
                params = {}
            else:
                url = None

    def _build_session(self, api_key, app_key):
        s = requests.Session()
        s.headers.update({
            'Content-type': 'application/json',
            'Authorization': 'chave_api {} aplicacao {}'.format(
                api_key, app_key
            )
        })
        return s

    def _make_request(self, verb, url, params=None, data=None):
        retry_counter = 0
        while True:
            try:
                r = self.session.request(verb, url, params=params, json=data)
                r.raise_for_status()
                return r.json()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    logger.info('Rate limit reached.')

                    retry_counter += 1

                    logger.info('Retry #{}'.format(retry_counter))

                    sleep_time = self.rate_limit_retry_delay
                    logger.info(
                        'Sleeping for {} seconds before retrying ...'.format(sleep_time)
                    )
                    time.sleep(sleep_time)
                    logger.info('Waking up ... Ready to retry.')
                else:
                    raise ApiError(e.request, e.response)
            except requests.exceptions.RequestException as e:
                raise ApiError(e.request)
