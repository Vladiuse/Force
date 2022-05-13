s1 = 'ñ'
s2 = 'é'
from office.models import Country

countrys = Country.objects.all()
for c in countrys:
    names = c.names['names']
    new_values = []
    for name in names:
        if s1 in name or s2 in name:
            name = name.replace(s1, 'n')
            name = name.replace(s2, 'e')
            new_values.append(name)
    print(new_values)
    c.names['names'] += new_values
    c.save()