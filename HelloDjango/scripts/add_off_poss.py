# from office.models import OfferPosition
# from django.db import IntegrityError
#
# with open('/home/vlad/PycharmProjects/DjangoForce/HelloDjango/scripts/offers.txt') as file:
#     for offer in file:
#         if offer.endswith('\n'):
#             offer_name = offer[:-1]
#         of_db = OfferPosition(name=offer_name)
#         try:
#             of_db.save()
#             print(f'Add: {of_db.name}')
#         except IntegrityError as error:
#             # print(f'{offer_name}: {error}')
#             pass
# print('End')



import requests as req

url = 'https://api.kma.biz/?method=getoffers&token=yPf3Y8hngbMwOR7Zi_kT3uDECXh5ej3J&return_type=json'
res = req.get(url)
offers = res.json()['offers']
# offers_list = []
with open('offers.txt', 'w') as file:
    for offer in offers:
        name = offer['name']
        if 'Glikotril' in name or offer['id'] == '6758':
            print(offer)

        # if '-' in name:
        #     name = name.split('-')[0].strip()
        #     file.write(name +'\n')
