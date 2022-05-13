from office.models import OfferPosition
offers = OfferPosition.objects.all()
for offer in offers:
    if offer.name in ['glikotril', 'glikotril']:
        # offer.delete()
        print(offer.name, 'delete')
print('END')