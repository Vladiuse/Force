from office.models import Offer
from django.db.models import Count, F, Value
offer = Offer.objects.get(kt_id=1)
offer.kt_data = {'1': 'kt'}
print(offer.kt_id)
print(offer.kt_data)
