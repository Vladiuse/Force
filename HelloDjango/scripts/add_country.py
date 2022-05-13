import csv
from office.models import Country

with open('/home/vlad/PycharmProjects/DjangoForce/HelloDjango/scripts/Lands - xxx.csv') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print('Headers: ', headers)
    for row in reader:
        print(row)
        name = row[0]
        short_code = row[1]
        lang = row[2]
        names = set(row[4:])
        if '' in names:
            names.remove('')
        names = {'names': list(names)}
        c = Country(name=name, short_name=short_code, lang=lang, names=names)
        c.save()