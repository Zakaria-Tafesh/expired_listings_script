import traceback
import requests
from .logger import logger


base_url = 'https://api.dev.sweetly.ca/api/estimate/get/'


class GetEstimateAPI:
    url = base_url
    payload = {'address': ''}
    offer_price = ''
    offer_price_90 = ''
    offers_dict = {
        'offer_price': '',
        'offer_price_90': ''
    }

    @classmethod
    def update_offers_dict(cls):
        cls.offers_dict = {
            'offer_price': cls.offer_price,
            'offer_price_90': cls.offer_price_90
        }

    @classmethod
    def init_variables(cls):
        cls.url = base_url
        cls.payload = {'address': ''}
        cls.offer_price = ''
        cls.offer_price_90 = ''
        cls.offers_dict = {
            'offer_price': '',
            'offer_price_90': ''
        }

    @classmethod
    def get_estimate(cls, address):
        try:
            cls.init_variables()
            cls.payload = {'address': address}
            response = requests.request("GET", cls.url, data=cls.payload)
            logger.info(response)
            logger.info(response.text)

            if response.status_code < 300:
                resp_json = response.json()
                prices = resp_json.get('prices')
                cls.offer_price = prices.get('offer_price')
                cls.offer_price_90 = prices.get('offer_price_90')
                cls.update_offers_dict()
                logger.info(cls.offers_dict)

        except:
            traceback.print_exc()
        finally:
            return cls.offers_dict


# if __name__ == '__main__':
#     adrs = '12223 103 Street, Edmonton, AB'
#     estimate = GetEstimateAPI(adrs)
#     resp = estimate.get_estimate()
#     logger.info(resp)
