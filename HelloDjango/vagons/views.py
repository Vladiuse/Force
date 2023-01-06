from django.shortcuts import render, redirect
from .vagons_reader import VagReader
from .people_counter import PeopleCounter
from .containers.containers_reader import ContainerReader


def index(requet):
    if requet.method == 'POST':
        file_name_1 = requet.POST['file_name_1']
        file_name_2 = requet.POST['file_name_2']
        file_text_1 = requet.POST['file_text_1']
        file_text_2 = requet.POST['file_text_2']
        if file_text_1 == file_text_2:
            error_text = f'Текст файла {file_name_1} и {file_name_2} одинаковы!'
            return render(requet, 'vagons/index.html', {'error_text': error_text})
        reader = ContainerReader(file_text_1, file_text_2)
        content = {

            'file_name_1': file_name_1,
            'file_name_2': file_name_2,
            'reader': reader
        }
        return render(requet, 'vagons/new_result.html', content)
    else:
        return render(requet, 'vagons/index.html')


def result(request):
    return render(request, 'vagons/new_result.html')


def people_count(requests):
    if requests.method != 'POST':
        return render(requests, 'vagons/people_count.html')
    else:
        text = requests.POST['text']
        counter = PeopleCounter(text)
        counter.proccess()
        content = {
            'counter': counter,
            'text': text,
        }
        return render(requests, 'vagons/people_count.html', content)
