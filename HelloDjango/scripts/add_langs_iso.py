from archive.models import Languege
import os



# print(os.listdir())

def load_iso_from_file():
    file_path = 'scripts/Langs_Iso.csv'
    with open(file_path) as file:
        for line in file:
            if line.endswith('\n'):
                line = line[:-1]
            name, short = line.split(',')
            if not(len(name)> 20 or short == '—'):
                l = Languege()
                l.full = name
                l.short = short
                l.save()


def make_geo_active():
    langs = Languege.objects.all()
    geo_to_onn = ['ru', 'ro', 'bg', 'al', 'pl', 'lv', 'lt', 'mk', 'ar', 'tr', 'gr', 'fr', 'it', 'es', 'en', 'cz', 'hr','de']
    for lang in langs:
        if lang.short in geo_to_onn:
            lang.is_active = True
            lang.save()
            print(lang, 'Onn')

make_geo_active()

