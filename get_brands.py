import logging

from decouple import config

from lojaintegrada import Api

"""
Before running this example, create a .env file with two vars:

API_KEY='your-api-key'
APP_KEY='your-app-key'
"""

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG,
    datefmt='%I:%M:%S'
)

api_key = config('API_KEY')
app_key = config('APP_KEY')

api = Api(api_key, app_key)

for page in api.get_brands(limit=5):
    for obj in page['objects']:
        print(obj)
