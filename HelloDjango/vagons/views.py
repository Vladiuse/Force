from django.shortcuts import render
from .vagons_reader import VagReader
from .people_counter import PeopleCounter


# Create your views here.

def index(requets):
    if requets.method != 'POST':
        return render(requets, 'vagons/index.html')
    else:
        file_text_1 = requets.POST['file_text_1']
        file_text_2 = requets.POST['file_text_2']
        vagons_1 = VagReader(file_text_1)
        vagons_2 = VagReader(file_text_2)
        content = {
            'vagons_1': vagons_1,
            'vagons_2': vagons_2,
            'unique_vagons_1': vagons_1 - vagons_2,
            'unique_vagons_2': vagons_2 - vagons_1,
            'jeneral_vagons': vagons_1 & vagons_2,
        }
        return render(requets, 'vagons/result.html', content)


def people_count(requests):
    if requests.method != 'POST':
        return render(requests,'vagons/people_count.html')
    else:
        text = requests.POST['text']
        counter = PeopleCounter(text)
        counter.proccess()
        content = {
            'counter': counter,
        }
        return render(requests,'vagons/people_count.html', content)
