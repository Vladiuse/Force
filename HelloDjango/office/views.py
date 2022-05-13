from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests as req
import json
from pprint import pprint
from .keitaro import Keitaro
from .models import Offer, CodeExample, RootDomain, OfferPosition, CopyPaste, CopyPasteData, Country, DomCamp
from .checker import LinkChecker, SiteMap
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required

def log(data:dict, print_end=True):
    with open('log.txt', 'a') as file:
        today = datetime.now()
        file.write(f"Date:{today};Data: {str(data)}\n")
        if print_end:
            file.write('*'*100 + '\n')


@login_required
def index(request):
    h1_tag = '12xxx3'
    content = {'h1_tag': h1_tag}
    return render(request, 'office/index.html', content)

@login_required
def kt_domains(request):
    k = Keitaro()
    domain_data = k.get_domains()
    content = {'domain_data': domain_data}
    return render(request, 'office/domains_kt.html', content)

@login_required
def beget_domains(request):
    """Список доменов BEGET"""
    print('domain func')
    RootDomain.update_domains()
    domains_bd = RootDomain.objects.exclude(is_full=True).order_by('name')
    content = {'domains': domains_bd,
               # 'free_doms': free_doms,
               'page_title': 'Домены',
               }
    return render(request, 'office/beget_domains.html', content)


# def update_kt_offers():
#     k = Keitaro()
#     kt_offers = k.get_offers()  # данные по оферу с кейтаро
#     Offer.update_offers(offers=kt_offers)
#     return k.get_offers_dict()

@login_required
def offers(requests):
    """Список офферов с данными из кейтаро"""
    # kt_offer_data = update_kt_offers()
    # # print(kt_offer_data, 'kt_offer_data')
    offers = Offer.get_offers_w_full_data()
    content = {
        'page_title': 'Офферы',
        'offers': offers,
    }
    return render(requests, 'office/offers.html', content)

@login_required
def checker_offer(request, offer_id, mode):
    """Проверочник офферов"""
    offer_model = Offer.get_offer_w_full_data(offer_id)
    is_check_start = ''
    if not (mode == 0 and offer_model.check_status != 'Не проверен'):
        pass
        # с главной страницы
        url = offer_model.kt_data['local_path']
        url = f'http://{Keitaro.IP_ADDRESS}{url}'
        offers_positions_names = {'offers_positions_names': OfferPosition.objects.values('name')}
        country_names = {'country_names': Country.get_country_names()}
        other_data = {}
        other_data.update(offers_positions_names)
        other_data.update(country_names)
        # pprint(other_data)
        site = SiteMap(url=url, other_data=other_data)
        checker = LinkChecker(site=site)
        checker.process()
        offer_model.check_status = checker.result['result_text']
        new_check_data = {'main': checker.result,
                          'checkers': checker.results_from_checkers, }
        offer_model.check_data = new_check_data
        offer_model.save()
        is_check_start = 'Выполнена загрузка'
    content = {
        'offer': offer_model,
        'data': offer_model.check_data,
        'is_check_start': is_check_start,
        'page_title': f'Проверка [{offer_model.kt_id}]',
    }
    return render(request, 'office/offer.html', content)

@login_required
def code_examples(request):
    examples = CodeExample.objects.all()
    page_title = 'Копипаста'
    content = {
        'page_title': page_title,
        'examples': examples,
    }
    return render(request, 'office/code_examples.html', content)



@csrf_exempt
def copy_paste(request):
    if request.method == 'GET':
        values = CopyPaste.objects.values()
        copy_paste_values = [object for object in values]
        result = {
            'result': 'success',
            'buttons': copy_paste_values, }
    else:
        result = {
            'result': 'error',
        }
    return JsonResponse(result, safe=False)

@csrf_exempt
def code_examples_data(request):
    if request.method == 'GET':
        group_id = request.GET['group_id']
        group = CopyPaste.objects.get(pk=group_id)
        group_data = group.data.all()
        data = [{'name': data.name, 'value': data.data} for data in group_data]
        result = {
            'result': 'success',
            'buttons': data, }
    else:
        result = {
            'result': 'error',
        }
    return JsonResponse(result, safe=False)

@csrf_exempt
def add_button(request):
    print('ADD')
    print(request.POST)
    if request.method == 'POST':
        try:
            button_name = request.POST['group_name']
            button = CopyPaste(name=button_name)
            button.save()
            result = {
                'result': 'success',
                'id': button.pk
            }
            return JsonResponse(result, safe=False)
        except BaseException as error:
            result = {
                'result': 'error',
                'message': f'Wrong data: {error}',
                'data': str(request.POST)
            }
            return JsonResponse(result, safe=False)
    else:
        result = {
            'result': 'error',
            'message': 'Wrong method'
        }
        return JsonResponse(result, safe=False)

@csrf_exempt
def remove_button(request):
    print('remove')
    print(request.method)
    if request.method == 'POST':
        try:
            button_id = request.POST['group_id']
            button = CopyPaste.objects.get(pk=button_id)
            button.delete()
            result = {
                'result': 'success',
                'id': button.pk,
            }
            return JsonResponse(result, safe=False)
        except BaseException as error:
            result = {
                'result': 'error',
                'message': f'Wrong data: {error}'
            }
            return JsonResponse(result, safe=False)

    else:
        result = {
            'result': 'error',
            'message': 'Wrong method'
        }
        return JsonResponse(result, safe=False)


@csrf_exempt
def add_sub_button(request):
    print('add_sub_button')
    if request.method == 'POST':
        try:
            print(request.POST)
            group_id = request.POST['group_id']
            print(group_id, 'group_id')
            group = CopyPaste.objects.get(pk=group_id)
            sub_button_name = request.POST['name']
            data = request.POST['data']
            sub_button = CopyPasteData(name=sub_button_name, data=data, group=group)
            sub_button.save()
            result = {
                'result': 'success',
                'id': sub_button.pk
            }
            return JsonResponse(result, safe=False)
        except BaseException as error:
            result = {
                'result': 'error',
                'message': f'Wrong data: {error}'
            }
            return JsonResponse(result, safe=False)

    else:
        result = {
            'result': 'error',
            'message': 'Wrong method'
        }
        return JsonResponse(result, safe=False)
    pass

@csrf_exempt
def remove_sub_button(request):
    print('remove_sub_button')
    print(request.method)
    if request.method == 'POST':
        try:
            button_id = request.POST['sub_button_id']
            button = CopyPasteData.objects.get(pk=button_id)
            button.delete()
            result = {
                'result': 'success',
                'id': button.pk,
            }
            return JsonResponse(result, safe=False)
        except BaseException as error:
            result = {
                'result': 'error',
                'message': f'Wrong data: {error}'
            }
            return JsonResponse(result, safe=False)

    else:
        result = {
            'result': 'error',
            'message': 'Wrong method'
        }
        return JsonResponse(result, safe=False)


def join_urls(request):
    return render(request, 'office/join_urls.html')


def new_offers(requests):
    offers = Offer.get_offers_w_full_data()
    content = {'offers': offers}
    return render(requests, 'office/new_offers.html', content)


def dom_camps(request):
    """Получение данных по тратам"""
    domains = DomCamp.objects.all()
    content = {
        'page_title' : 'Spends',
        'domains': domains,
    }
    return render(request, 'office/dom_camps.html', content)


def update_spend(request):
    """Обновить данные по тратам"""
    log(request.get_full_path(), print_end=False)
    if request.method == 'GET':
        try:
            domain = request.GET['domain']
            spend = request.GET['spend']
            date = request.GET['date']
            if date == '0':
                # today
                date = datetime.now().date()
            else:
                # yestarday
                date = datetime.now().date() - timedelta(days=1)
            data = {
                'domain': domain,
                'spend': spend,
                'date': date
            }
            DomCamp.update_spend(domain=domain, spend=spend, date=date)
            answer = {'result': 'success', 'data': data}
            log(answer)
            return JsonResponse(answer, safe=False)
        except BaseException as error:
            answer = {'result': 'error', 'message': str(error)}
            log(answer)
            return JsonResponse(answer, safe=False)
    else:
        answer = {'result': 'error', 'message': 'wrong method'}
        log(answer)
        return JsonResponse(answer, safe=False)


def url_checker(request):
    offers_positions_names = {'offers_positions_names': OfferPosition.objects.values('name')}
    country_names = {'country_names': Country.get_country_names()}
    other_data = {}
    other_data.update(offers_positions_names)
    other_data.update(country_names)
    if request.method == 'POST':
        url = request.POST['url']

        site = SiteMap(url=url,
                       is_cloac=False, other_data=other_data)
        site.check_pages_conn()
        main_ckecker = LinkChecker(site=site, )
        main_ckecker.process()
        content = {'data': f'{url}', 'checker': main_ckecker}
    else:
        content = {'data':'Please, enter your url'}
    return render(request, 'office/url_checker.html', content)