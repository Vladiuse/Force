from django.shortcuts import render, redirect
from .vagons_reader import VagReader
from .people_counter import PeopleCounter
from .containers.containers_reader import ContainerReader



# Create your views here.

def index(requet):
    if requet.method == 'POST':
        file_name_1 = requet.POST['file_name_1']
        file_name_2 = requet.POST['file_name_2']
        file_text_1 = requet.POST['file_text_1']
        file_text_2 = requet.POST['file_text_2']
        print(file_name_1, file_name_2)
        reader = ContainerReader(file_text_1, file_text_2)
        content = {

            'file_name_1': file_name_1,
            'file_name_2': file_name_2,
            'reader': reader
        }
        return render(requet, 'vagons/new_result.html', content)
    else:
        return render(requet, 'vagons/index.html')
    # if requets.method != 'POST':
    #     return render(requets, 'vagons/index.html')
    # else:
    #     file_text_1 = requets.POST['file_text_1']
    #     file_text_2 = requets.POST['file_text_2']
    #     vagons_1 = VagReader(file_text_1)
    #     vagons_2 = VagReader(file_text_2)
    #     content = {
    #         'vagons_1': vagons_1,
    #         'vagons_2': vagons_2,
    #         'unique_vagons_1': vagons_1 - vagons_2,
    #         'unique_vagons_2': vagons_2 - vagons_1,
    #         'jeneral_vagons': vagons_1 & vagons_2,
    #     }
    #     return render(requets, 'vagons/result.html', content)

def result(request):
    return render(request, 'vagons/new_result.html')

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
