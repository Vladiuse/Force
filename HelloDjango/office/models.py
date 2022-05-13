from django.db import models
from django.contrib.auth.models import User
from .keitaro import Keitaro
from .api_servises import Beget
from pprint import pprint
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class Offer(models.Model):
    GREY = 'Не проверен'
    RED = 'Ошибка'
    YELLOW = 'Замечание'
    GREEN = 'Все ок'

    STATUS_HTML = {
        GREY: 'btn btn-secondary',
        RED: 'btn btn-danger',
        YELLOW: 'btn btn-warning',
        GREEN: 'btn btn-success',
    }
    CHOICE = (
        (GREY, GREY),
        (RED, RED),
        (YELLOW, YELLOW),
        (GREEN, GREEN),
    )
    kt_id = models.IntegerField(db_index=True)
    check_status = models.CharField(max_length=30, default=GREY)
    check_data = models.JSONField(default=dict, blank=True, null=True)

    @staticmethod
    def update_offers(offers_fr_kt: dict):
        """Синхронизировать записи с данными в Кейтаро"""
        offers_id = [offer['id'] for offer in offers_fr_kt]  # айди офферов с кейтаро
        offers_in_db_to_del = Offer.objects.exclude(kt_id__in=offers_id)  # исключаю айди которых нет в бд
        [offer.delete() for offer in offers_in_db_to_del]
        offers_id_db = [offer.kt_id for offer in Offer.objects.all()]  # получаю айди офферов что есть в бд
        offers_add = set(offers_id) - set(offers_id_db)  # получаю список айдишноков которых нет в бд
        for offer_id in offers_add:  # записываю новые офферы
            of = Offer()
            of.kt_id = offer_id
            of.save()

    @staticmethod
    def get_offers_w_full_data():
        """получить офферы с данными из модели и кейтаро"""
        k = Keitaro()
        Offer.update_offers(offers_fr_kt=k.get_offers())
        offers_db = Offer.objects.all().order_by('-kt_id')
        offers_id_kt = k.get_offers_dict()
        for offer in offers_db:
            offer.kt_data = offers_id_kt[offer.kt_id]
        return offers_db

    @staticmethod
    def get_offer_w_full_data(offer_id):
        """получить оффер с даммыми из модели и кейтаро"""
        offer_db = Offer.objects.get(kt_id=offer_id)
        k = Keitaro()
        offer_kt = k.get_offer(offer_id)
        offer_db.kt_data = offer_kt
        return offer_db

    def set_status(self, status):
        """Статус сайта от чекера"""
        for k, v in self.STATUS_HTML.items():
            if status == v:
                self.check_status = k
                break
        self.save()

    def get_status_html(self):
        try:
            return self.STATUS_HTML[str(self.check_status)]
        except KeyError:
            return 'No status key error'

    # def get_country(self):
    #     country = self.kt_data['country']
    #     print(country)
    #     chars = "[']"
    #     for c in chars:
    #         country = country.replace(c, '')
    #     return country


class CodeExample(models.Model):
    """
    Примеры кода Html, Css, JS
    """
    name = models.CharField(max_length=99, verbose_name='Пример кода')
    html_code = models.TextField(verbose_name='Html код', blank=True)
    css_code = models.TextField(verbose_name='Css код', blank=True)
    js_code = models.TextField(verbose_name='Js код', blank=True)

    def __str__(self):
        return self.name


class CopyPaste(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название копипасты', unique=True)

    def __str__(self):
        return self.name


class CopyPasteData(models.Model):
    name = models.CharField(max_length=50)
    data = models.TextField()
    group = models.ForeignKey(CopyPaste, on_delete=models.CASCADE, related_name='data')


class Domain(models.Model):
    """
    Домен
    """
    NEW = 'NEW'
    USE = 'USE'
    BAN = 'BAN'
    NEW_RU = 'Новый'
    USE_RU = 'Запускался'
    BAN_RU = 'Забанен'
    DOMAIN_STATUS = (
        (NEW, NEW_RU),
        (USE, USE_RU),
        (BAN, BAN_RU),
    )

    HTML_CLASS = {
        NEW: 'success',
        USE: 'warning',
        BAN: 'danger',
    }

    name = models.CharField(max_length=99, verbose_name='название домена', unique=True)
    # url = models.URLField(max_length=300, blank=True, null=True, unique=True)
    beget_id = models.IntegerField(verbose_name='id домена на beget', unique=True)
    description = models.TextField(max_length=999, verbose_name='доп. информация', blank=True)

    # some info
    facebook = models.CharField(max_length=99, choices=DOMAIN_STATUS, default=NEW)
    google = models.CharField(max_length=99, choices=DOMAIN_STATUS, default=NEW)
    tiktok = models.CharField(max_length=99, choices=DOMAIN_STATUS, default=NEW)

    def get_root_domain(self):
        if self.name.count('.') == 2:
            return self.name[self.name.find('.') + 1:]
        return self.name

    def get_http(self):
        return f'http://{self.name}/'

    def get_https(self):
        return f'https://{self.name}/'

    def black_page(self):
        """Получить ссылку на скрытую страницу"""
        return self.get_http_site() + 'black.html'

    def get_html_facebook(self):
        return Domain.HTML_CLASS[self.facebook]

    def get_html_google(self):
        return Domain.HTML_CLASS[self.google]

    def get_html_tiktok(self):
        return Domain.HTML_CLASS[self.tiktok]

    def get_http_site(self):
        return f'http://{self.name}/'

    def get_https_site(self):
        return f'https://{self.name}/'

    def is_sub(self):
        if self.name.count('.') >= 2:
            return True

    def is_root(self):
        if self.name.count('.') == 1:
            return True

    def __str__(self):
        return self.name


class RootDomain(Domain):
    is_full = models.BooleanField(default=False, verbose_name='Привышен ли лимит поддоменов')

    @staticmethod
    def update_domains():
        """Обновить список доменов"""
        b = Beget()
        all_root_domains_list = b.get_domains()
        beget_doms_id = [dom['id'] for dom in all_root_domains_list]
        db_doms_id = [dom.beget_id for dom in RootDomain.objects.all()]
        to_del = set(db_doms_id) - set(beget_doms_id)
        to_add = set(beget_doms_id) - set(db_doms_id)
        print('start_dell')
        for dom_id in to_del:
            dom = RootDomain.objects.get(beget_id=dom_id)
            dom.delete()
        for domain in all_root_domains_list:
            dom_id = domain['id']
            if dom_id in to_add:
                name = domain['fqdn']
                dom = RootDomain(name=name, beget_id=dom_id)
                dom.save()
        print('END_dell')
        all_sub_domains_list = b.get_sub_domains()
        beget_doms_id = [dom['id'] for dom in all_sub_domains_list]
        db_doms_id = [dom.beget_id for dom in SubDomain.objects.all()]
        to_del = set(db_doms_id) - set(beget_doms_id)
        to_add = set(beget_doms_id) - set(db_doms_id)
        print('START_ADD')
        for dom_id in to_del:
            dom = SubDomain.objects.get(beget_id=dom_id)
            dom.delete()
        for domain in all_sub_domains_list:
            dom_id = domain['id']
            if dom_id in to_add:
                name = domain['fqdn']
                root_dom = RootDomain.objects.get(beget_id=domain['domain_id'])
                dom = SubDomain(name=name, beget_id=dom_id, root_domain=root_dom)
                dom.save()
        print('END LOAD DOms')

    def __str__(self):
        return self.name


class OfferPosition(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название оффера', unique=True)

    def save(self, *args, **kwargs):
        name_clean = ''
        self.name = self.name.strip()
        self.name = self.name.lower()
        for c in self.name:
            if c.isalpha() or c == ' ':
                name_clean += c
        self.name = name_clean
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubDomain(Domain):
    root_domain = models.ForeignKey(RootDomain, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название страны')
    short_name = models.CharField(max_length=3)
    lang = models.CharField(max_length=5, verbose_name='Код языка страны')
    phone_code = models.IntegerField(blank=True, null=True)
    currency = models.CharField(max_length=10, verbose_name='Валюта страны', blank=True)
    names = models.JSONField(default={'names': []})

    @staticmethod
    def get_country_names():
        countrys = Country.objects.all()
        res = {}
        for c in countrys:
            name = c.short_name
            names = c.names['names']
            res.update({name: names})
        return res

    def __str__(self):
        return self.name


class DomCamp(models.Model):
    domain = models.CharField(max_length=50, verbose_name='Домен', unique=True)

    @staticmethod
    def update_spend(domain, spend, date):
        try:
            domain = DomCamp.objects.get(domain=domain)
        except DomCamp.DoesNotExist as error:
            domain = DomCamp(domain=domain)
            domain.save()
            print(f'Create domain_model: {domain}')
        try:
            spend_db = Spend.objects.get(domain=domain, date=date)
            spend_db.spend = spend
            spend_db.save()
        except Spend.DoesNotExist as error:
            spend_db = Spend(domain=domain, date=date, spend=spend)
            spend_db.save()
            print(f'Create Spend: {spend_db}')

    def today_spend(self):
        today = datetime.now().date()
        try:
            today_spend = self.spend_set.get(date=today)
            today_spend = today_spend.spend
            return today_spend
        except  ObjectDoesNotExist:
            return 'Нет трат'

    def all_spend(self):
        spends_db = self.spend_set.all()
        total = 0
        for spend_db in spends_db:
            total += spend_db.spend
        return total

    def __str__(self):
        return self.domain


class Spend(models.Model):
    domain = models.ForeignKey(DomCamp, on_delete=models.CASCADE)
    date = models.DateField()
    spend = models.FloatField()

    unique_together = ['domain', 'date']

    def __str__(self):
        return f'Spend: {self.domain}, {self.date}, {self.spend}'
