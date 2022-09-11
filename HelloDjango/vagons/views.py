from django.shortcuts import render
from .vagons_reader import VagReader


# Create your views here.

def index(requets):
    if requets.method != 'POST':
        return render(requets, 'vagons/index.html')
    else:
        file_text_1 = requets.POST['file_text_1']
        file_text_2 = requets.POST['file_text_2']
        vagons_1 = VagReader(file_text_1)
        vagons_2 = VagReader(file_text_2)
        vagons_1.process()
        vagons_2.process()
        content = {
            'vagons_1': vagons_1,
            'vagons_2': vagons_2,
            'unique_vagons_1': vagons_1 - vagons_2,
            'unique_vagons_2': vagons_2 - vagons_1,
            'jeneral_vagons': vagons_1 & vagons_2,
        }
        return render(requets, 'vagons/result.html', content)
