from django.shortcuts import render, reverse, redirect
from .containers import ContainerReader, ClientReader
from .forms import ClientDocForm
from .models import ClientDoc, ClientContainerRow
from django.db.models import F
from django.utils import timezone
from django.http import HttpResponseRedirect


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
        reader = ClientReader(text)
        reader.process()
        content = {
            'reader': reader,
            'text': text,
        }
        return render(requests, 'vagons/clients/people_count.html', content)


def clients(request):
    clients_docs = ClientDoc.objects.defer('document').all()
    content = {
        'clients_docs': clients_docs
    }
    return render(request, 'vagons/clients/clients.html', content)


def client(request, document_id):
    client_doc = ClientDoc.objects.get(pk=document_id)
    if request.method == 'POST':
        form = ClientDocForm(request.POST, request.FILES,instance=client_doc)
        if form.is_valid():
            form.save()
        else:
            print('NOT VALID')
        return HttpResponseRedirect(
            reverse('vagons:show_client', args=(document_id,)))
    else:
        rows = ClientContainerRow.objects.filter(document=client_doc).annotate(past=client_doc.document_date - F('date'))
        form = ClientDocForm(instance=client_doc)
        content = {
            'client_doc': client_doc,
            'rows': rows,
            'form': form,
        }
    return render(request, 'vagons/clients/client.html', content)


def create_client(request):
    if request.method == 'POST':
        form = ClientDocForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vagons:clients')
        content = {
            'form': form
        }
        return render(request, 'vagons/clients/create.html', content)
    else:
        form = ClientDocForm()
        content = {
            'form': form
        }
        return render(request, 'vagons/clients/create.html', content)


def delete(request, document_id):
    doc = ClientDoc.objects.get(pk=document_id)
    doc.delete()
    return redirect('vagons:clients')
