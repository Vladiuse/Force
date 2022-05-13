import requests as req
from pprint import pprint
from HelloDjango.settings import kt_api_key, kt_ip


class Keitaro:
    API_KEY = kt_api_key
    IP_ADDRESS = kt_ip
    headers = {
        'Api-Key': API_KEY,
    }

    def __init__(self):
        self.offers = {}

    def get_domains(self):
        url = f'http://{Keitaro.IP_ADDRESS}/admin_api/v1/domains'
        res = req.get(url, headers=Keitaro.headers)
        self.offers = res.json()
        return res.json()

    def get_offers(self):
        """Получить список офферов с кейтаро"""
        url = f'http://{Keitaro.IP_ADDRESS}/admin_api/v1/offers'
        res = req.get(url, headers=Keitaro.headers)
        self.offers = res.json()
        return res.json()

    def get_offer(self, offer_id):
        print('get offer KT')
        """Получить оффер с кейтаро по id"""
        url = f'http://{Keitaro.IP_ADDRESS}/admin_api/v1/offers/{offer_id}'
        res = req.get(url, headers=Keitaro.headers)
        offer = res.json()
        return offer

    def get_offers_dict(self):
        """Список словарей с ключем ади оффера"""
        result = {}
        for offer in self.offers:
            dic = {offer['id']: offer}
            result.update(dic)
        return result



if __name__ == '__main__':
    k = Keitaro()

