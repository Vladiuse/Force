from office.models import DomCamp
from datetime import datetime, timedelta
# d = DomCamp
# date = datetime.now().date() - timedelta(days=1)
#
# print(date, 'date')
# d.update_spend(domain="example-new.com", spend=10.10, date = date)
today = datetime.now().date()
d = DomCamp.objects.get(domain='test.com')
print(d.today_spend())
