from pprint import pprint
import re
# import paramiko
import requests as req
from bs4 import BeautifulSoup


# from .beget_api_keys import ssh_begget_login, ssh_begget_pass


def is_str_is_str_no_space(str_1: str, str_2: str):
    syblols = [' ', '\n', '\t']
    str_1 = ''.join(c for c in str_1 if c not in syblols)
    str_2 = ''.join(c for c in str_2 if c not in syblols)
    return str_2 in str_1


class StatusHTML:
    # HTML
    GREY = 'secondary'
    RED = 'danger'
    YELLOW = 'warning'
    GREEN = 'success'
    # Text
    GOOD = 'Все ок'
    REPRIMAND = 'Замечание'
    ERROR = 'Ошибка'
    DISABLED = 'Отключен'
    NONE = 'Не проверен'

    # result_code

    @staticmethod
    def get_checker_status_html(status):
        dic = {
            'good': StatusHTML.GREEN,
            'reprimand': StatusHTML.YELLOW,
            'error': StatusHTML.RED,
            'disabled': StatusHTML.GREY,
            'none': StatusHTML.GREY,
        }
        try:
            html_status = dic[status]
        except KeyError:
            html_status = 'html-key-error'
        return html_status

    @staticmethod
    def get_checker_status_text(status):
        dic = {
            'good': StatusHTML.GOOD,
            'reprimand': StatusHTML.REPRIMAND,
            'error': StatusHTML.ERROR,
            'disabled': StatusHTML.DISABLED,
            'none': StatusHTML.NONE,
        }
        try:
            html_status = dic[status]
        except KeyError:
            html_status = 'text_key_error'
        return html_status


class Page:

    def __init__(self, url):
        self.url = url
        self.status_code = None
        self.text = None
        self.soup = None

    def is_work(self):
        return self.status_code == 200

    def connect(self):
        try:
            res = req.get(self.url)
            res.encoding = 'utf-8'
            self.status_code = res.status_code
            self.text = res.text
            self.soup = BeautifulSoup(res.text, 'lxml')
            print(f'Page work: {self.url}')
            return True
        except req.exceptions.ConnectionError:
            print(f'Page dont work: {self.url}')
            return False

    def get_page_status_code(self):
        return self.status_code

    def get_text(self):
        return self.text

    def get_soup(self):
        return self.soup

    def get_text_no_spaces_soup(self):
        """Возвращает текст со страницы без верстки и пробелов"""
        text = self.soup.text.replace(' ', '')
        return text

    @staticmethod
    def find_text_block(text, start, end):
        """Вывод текста межды подстроками"""
        start_pos = text.find(start)
        end_pos = text.find(end, start_pos + 1)
        if start_pos != -1 and end_pos != -1:
            return text[start_pos + len(start):end_pos]


# class SHHConnector:
#
#     def __init__(self):
#         self.host = 'vladiuse.beget.tech'
#         self.username = ssh_begget_login
#         self.password = ssh_begget_pass
#         self.port = 22
#         self.connection = None
#         # подключение
#         self.connect()
#
#     def connect(self):
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh.connect(self.host, self.port, self.username, self.password)
#         self.connection = ssh
#
#     def ls_comm(self, command):
#         # TODO - что если папки не существует?
#         stdin, stdout, stderr = self.connection.exec_command(f'ls {command}')
#         return stdout
#
#     def cat_comm(self, command):
#         stdin, stdout, stderr = self.connection.exec_command(f'cat {command}')
#         return stdout


class PageFile:

    def __init__(self, file_name, connector):
        self.file_name = file_name
        self.connector = connector
        self.text = None
        self.soup = None
        self.file_data = None
        self.file_lines = []

    # def connect(self):
    #     file = self.connector.`cat_comm`(self.file_name)
    #     text = str(file.read())
    #     if text:
    #         self.text = text
    #         self.soup = BeautifulSoup(self.text, 'lxml')

    def connect(self):
        self.file_data = self.connector.cat_comm(self.file_name)


    def get_file_lines(self, count=0):
        if self.file_lines:
            return self.file_lines
        lines = []
        if count:
            for _ in range(count):
                line = self.file_data.readline()
                lines.append(line)
        else:
            lines = self.file_data.readlines()
        self.file_lines = lines
        return lines

    @staticmethod
    def get_variable_value(line):
        """получить значение переменной в строке - PHP"""
        if '=' not in line:
            return None
        variable, value = line.split('=')
        value = value.strip()
        is_php_comm_in_line = value.rfind('//')
        if is_php_comm_in_line != -1:
            value = value[:is_php_comm_in_line]
            value = value.strip()
        if value.endswith(';'):
            value = value[:-1]
        if value.startswith('"') and value.endswith('"'):
            return value.strip('"')
        if value.startswith("'") and value.endswith("'"):
            return value.strip("'")
        return value


class SiteMap:
    # pages
    # TODO - определить лишь файлы и способы подступа к ним?
    SUCCESS_PAGE = '/success/success.php'
    POLICY = '/policy.html'
    SPAS = '/spas.html'
    TERM = '/terms.html'
    # files
    WHITE = 'white.html'
    BLACK = 'black.html'
    S_API = 's_api.php'
    S_LOG = 's_log.txt'
    CLOAC_FILE = 'index.php'
    ORDER = 'https://trackerlead.biz/'
    MODAL_CSS = 'modal.css'
    MODAL_JS = 'modal.js'
    COMMENT_FORM_ATTR = 'data-comment-form'
    # geo list
    ALLOWED_GEO_LIST = ['by', 'ru', 'ee', 'lt', 'lv', 'pl']
    ALLOWED_INNER_LINKS = [
        'policy.html', 'terms.html',
        '/policy.html', '/terms.html',
        'policy2.php', '/policy2.php',
        'policy', 'terms',
    ]

    # SSH_CONNECTOR = SHHConnector()

    def __init__(self, url, is_cloac=False, dir_name=None, other_data=None):
        self.cloac = is_cloac
        # sitemap
        self.main = Page(url) if not is_cloac else Page(url + SiteMap.BLACK)
        # self.spas = Page(url=url.replace('index.html', SiteMap.SUCCESS_PAGE))
        self.policy = Page(url + SiteMap.POLICY)
        self.terms = Page(url + SiteMap.TERM)
        self.success = Page(url=url.replace('index.html', SiteMap.SUCCESS_PAGE))

        self.black = Page(url + '/' + SiteMap.BLACK)
        self.white = Page(url + '/' + SiteMap.WHITE)
        # site_files
        self.dir_name = dir_name
        self.files = set()
        self.other_data = other_data  # стороние данные для чекеров

        # self.index_php = PageFile(dir_name + '/' + SiteMap.CLOAC_FILE,
        #                           connector=SiteMap.SSH_CONNECTOR) if self.dir_name else None
        # self.api_php = PageFile(dir_name + '/' + SiteMap.ORDER,
        #                         connector=SiteMap.SSH_CONNECTOR) if self.dir_name else None

    def check_pages_conn(self):
        for page in [self.main, self.success]:
            page.connect()

    def check_pages_conn_old(self):
        for page in self.main, self.success:
            page.connect()

        # if self.dir_name:
        #     for page_file in self.index_php, self.api_php:
        #         page_file.connect()
        #     self.get_site_files()

    def get_site_files(self):
        pass
    #     data = self.SSH_CONNECTOR.ls_comm(self.dir_name)
    #     for file_name in data.readlines():
    #         if file_name.endswith('\n'):
    #             file_name = file_name[:-1]
    #         if '.' in file_name:
    #             self.files.add(file_name)


class LinkChecker:
    class Check:
        DESCRIPTION = 'No'
        KEY_NAME = 'No'

        STATUS_SET = {}

        def __init__(self, site):
            self.site = site
            self.description = self.DESCRIPTION
            self.key_name = self.KEY_NAME
            self.result_value = dict()  # возвращаемые значения
            self.info = set()  # информация об ошибоке
            self.errors = set()  # вывод примеров ошибок
            self.is_check = False
            self.result_code = ''  # error, remrimand ...
            # self.offers_names_db = offers_names_db

        def get_class_name(self):
            return self.__class__.__name__

        def get_result(self):
            result = {
                'name': self.get_class_name(),
                'description': self.description,
                'info': list(self.info),
                'errors': list(self.errors),
                'result_code': self.result_code,
                'result_value': self.result_value,
                'status_html': StatusHTML.get_checker_status_html(self.result_code),
                'status_text': StatusHTML.get_checker_status_text(self.result_code),
                'key_name': self.KEY_NAME,
            }
            return result

        def process(self):
            pass

        def get_result_status(self):
            """Получть статус проверки чекера"""
            if not self.info:
                self.result_code = 'good'
            else:
                res = set()
                for text_error in self.info:
                    res.add(self.STATUS_SET[text_error])
                if 'error' in res:
                    self.result_code = 'error'
                    return
                if 'reprimand' in res:
                    self.result_code = 'reprimand'
                    return
                # if 'good' in res:
                #     self.result_code = 'good'
                #     return
                if 'disabled' in res:
                    self.result_code = 'disabled'
                else:
                    self.result_code = 'none'

    class Req(Check):
        DESCRIPTION = 'Реквизиты'
        KEY_NAME = 'req'

        INCORRECT_REQ = 'Есть некоректные'
        NO_REQS = 'Реквизиты отсутсвуют'

        STATUS_SET = {
            INCORRECT_REQ: 'reprimand',
            NO_REQS: 'reprimand',
        }

        REQUISITES = {
            'name': 'ИП Гребенщиков',
            'unp': 'УНП 19345252',
            'address': 'г.Минск, ул. Радиальная, д. 40',
            'email': 'E-mail: zenitcotrade@gmail.com',
            'phone': 'Телефон: +375 29 679-00-99',
        }

        def process(self):
            self.find_req_fb()

        def find_req_fb(self):
            """Поиск реквизитов FaceBook"""
            FB_REQ = 'name', 'unp', 'address'
            self.find_reqs(FB_REQ)

        def find_req_tt(self):
            """Поиск реквизитов TikTok"""
            TT_REQ = self.REQUISITES.keys()
            self.find_reqs(TT_REQ)

        def find_reqs(self, reqs):
            page_text = self.site.main.get_text_no_spaces_soup()
            for req in reqs:
                req_text = self.REQUISITES[req].replace(' ', '')
                if req_text not in page_text:
                    self.errors.add(req)
                    self.info.add(self.INCORRECT_REQ)
            if len(self.errors) == len(reqs):  # если все реквизиты отсутствуют
                self.info = set()
                self.errors.clear()
                self.info.add(self.NO_REQS)

    class SaveComment(Check):
        """Поиск коментария от google chrome"""
        DESCRIPTION = 'Комметрарий от гугл хром'
        KEY_NAME = 'g_comm'
        SAVED_FROM = '<!-- saved from'

        COMM_ON_PAGE = 'Комментарий saved from на странице'
        COMM_ON_PAGE_BLACK = 'Комментарий saved from на странице(black)'
        STATUS_SET = {
            COMM_ON_PAGE: 'reprimand',
            COMM_ON_PAGE_BLACK: 'good',
        }

        def process(self):
            self.find_comm()

        def find_comm(self):
            text = self.site.main.get_text()
            lines = text.split('\n')[:5]
            for line in lines:
                if self.SAVED_FROM in line:
                    if not self.site.cloac:
                        self.info.add(self.COMM_ON_PAGE)
                    else:
                        self.info.add(self.COMM_ON_PAGE_BLACK)
                    self.errors.add(self.SAVED_FROM)
                    break

    class PolicyPage(Check):
        DESCRIPTION = 'Страница политики конфиденциальности'
        KEY_NAME = 'policy'
        POLICY_LINK = 'policy.html'
        LINK_TEXT = 'Политика конфиденциальности'

        INCORRECT_TEXT = 'Ошибка в подписи ссылки'
        NO_LINK = 'Нет ссылки на странице'
        PAGE_NOT_WORK = 'Страница не работает'

        STATUS_SET = {
            INCORRECT_TEXT: 'reprimand',
            NO_LINK: 'reprimand',
            PAGE_NOT_WORK: 'reprimand',
        }

        def process(self):
            self.find_link()
            self.check_page()

        def find_link(self):
            soup = self.site.main.get_soup()
            link = soup.find('a', href=self.POLICY_LINK)
            if not link:
                link = soup.find('a', href='/' + self.POLICY_LINK)
            if link:
                if self.LINK_TEXT not in link.text:
                    self.info.add(self.INCORRECT_TEXT)
            else:
                self.info.add(self.NO_LINK)

        def check_page(self):
            if not self.site.policy.is_work():
                self.info.add(self.PAGE_NOT_WORK)

    class TermsPage(PolicyPage):
        DESCRIPTION = 'Страница пользовательского соглашения'
        KEY_NAME = 'terms'
        POLICY_LINK = 'terms.html'
        LINK_TEXT = 'Пользовательское соглашение'

        def check_page(self):
            if not self.site.terms.is_work():
                self.info.add(self.PAGE_NOT_WORK)

    class SpasPage(Check):
        """
        Обработчик страницы отзыва
        """
        DESCRIPTION = 'Окно отзыва'
        ACTION = 'spas.html'

        NO_SPAS_FORM = 'Нет формы отзыва'
        NO_CSS_FILE = 'modal.css не найден'
        NO_JS_FILE = 'modal.js не найден'

        STATUS_SET = {
            NO_CSS_FILE: 'reprimand',
            NO_JS_FILE: 'reprimand',
            NO_SPAS_FORM: 'disabled',
        }

        def process(self):
            self.check_form()
            if self.NO_SPAS_FORM not in self.info:
                self.check_files()

        def check_form(self):
            soup = self.site.main.get_soup()
            form = soup.find('form', action=self.ACTION)
            if not form:
                self.info.add(self.NO_SPAS_FORM)

        def check_files(self):
            if SiteMap.MODAL_JS not in self.site.files:
                self.info.add(self.NO_JS_FILE)
            if SiteMap.MODAL_CSS not in self.site.files:
                self.info.add(self.NO_CSS_FILE)

    class SuccessPage(Check):
        # TODO - добавить провкрку наличия формы
        DESCRIPTION = 'Итоговая страница'
        KEY_NAME = 'success'

        PAGE_NOT_WORK = 'Страница не работает'
        NO_AGAIN_FROM = 'Форма повторного заказа не найдена'

        STATUS_SET = {
            PAGE_NOT_WORK: 'error',
        }

        def process(self):
            self.check_page()

        def check_page(self):
            if not self.site.success.is_work():
                self.info.add(self.PAGE_NOT_WORK)
                self.errors.add(self.site.success.url)

        def check_again_form(self):
            # TODO - хз как сделать
            soup = self.site.success.get_soup()
            form = soup.find('form', action='../' + SiteMap.ORDER)
            if not form:
                self.info.add(self.NO_AGAIN_FROM)
            else:
                form = LinkChecker.HTMLForm(form_soup=form)

    class FaceBookPixel(Check):
        """Пиклесль ФБ"""
        DESCRIPTION = 'Пиклесль ФБ'
        KEY_NAME = 'fb_pixel'
        FBP_DESCRIPTION = {'start': '<!-- Facebook Pixel Code -->', 'end': '<!-- End Facebook Pixel Code -->'}
        FBP_1 = {'start': "fbq('init', '",
                 'end': "');"}
        FBP_2 = {'start': "https://www.facebook.com/tr?id=",
                 'end': "&ev"}

        PIXEL_NOT_FOUND = 'Блок с пикселем не найден'
        ONE_NOT_CORRECT = 'Один из пикселей некоректен'

        STATUS_SET = {
            PIXEL_NOT_FOUND: 'disabled',
            ONE_NOT_CORRECT: 'error',
        }

        def process(self):
            self.find_pixel()

        def find_pixel(self):
            pixel_block = Page.find_text_block(self.site.success.get_text(),
                                               self.FBP_DESCRIPTION['start'], self.FBP_DESCRIPTION['end'])
            if pixel_block:
                fbp_1 = Page.find_text_block(pixel_block, self.FBP_1['start'], self.FBP_1['end'])
                fbp_2 = Page.find_text_block(pixel_block, self.FBP_2['start'], self.FBP_2['end'])
                if fbp_1 != fbp_2:
                    self.info.add(self.ONE_NOT_CORRECT)
                else:
                    self.result_value.update({'pixel': fbp_1})
            else:
                self.info.add(self.PIXEL_NOT_FOUND)

    class FbPixelImg(Check):
        # TODO write test
        DESCRIPTION = 'Пиклесль ФБ IMG'
        KEY_NAME = 'fb_pixel_img'

        FBP_DESCRIPTION = {'start': '<!-- Facebook Pixel Code -->', 'end': '<!-- End Facebook Pixel Code -->'}
        PIXEL_HTML = """<img height="1" width="1" src="https://www.facebook.com/tr?id=&ev=Lead&noscript=1"/>"""

        PIXEL_BLOCK_NOT_FOUND = 'Блок с пикселем не найден'
        PIXEL_IMG_NOT_FOUND = 'Пиксель Img ненайден'

        STATUS_SET = {
            PIXEL_BLOCK_NOT_FOUND: 'disabled',
            PIXEL_IMG_NOT_FOUND: 'disabled',
        }

        def process(self):
            self.find_pixel()

        def find_pixel(self):
            pixel_block = Page.find_text_block(self.site.success.get_text(),
                                               self.FBP_DESCRIPTION['start'], self.FBP_DESCRIPTION['end'])
            if pixel_block:
                if not is_str_is_str_no_space(pixel_block, self.PIXEL_HTML):
                    self.info.add(self.PIXEL_IMG_NOT_FOUND)
            else:
                self.info.add(self.PIXEL_BLOCK_NOT_FOUND)

    class TtPixel(Check):
        DESCRIPTION = 'Пиклесль TikTok'
        KEY_NAME = 'tt_pixel'
        TT = {'start': "ttq.load('",
              'end': "');"}

        PIXEL_NOT_FOUND = 'Пиксель не найден'

        STATUS_SET = {
            PIXEL_NOT_FOUND: 'disabled',
        }

        def process(self):
            self.find_pixel()

        def find_pixel(self):
            tt_pixel = Page.find_text_block(self.site.success.get_text(), self.TT['start'], self.TT['end'])
            if not tt_pixel:
                self.info.add(self.PIXEL_NOT_FOUND)
            else:
                self.result_value.update({'pixel': tt_pixel})

    class GoogleTag(Check):
        # TODO - сделать
        pass

    class PageLink(Check):
        """Поиск некоректных внутрених ссылок"""
        DESCRIPTION = 'Внутрение сслыки'
        KEY_NAME = 'links'
        # DO_NOT_CHECK = {'policy.html', 'terms.html',
        #                 '/policy.html', '/terms.html',
        #                 'spas.html'} # перенес SiteMap

        FIND_ALIEN = 'Есть ссылки на чужой лэнд'
        INCORRECT_INNER = 'Некоректные внутриние ссылки'
        NO_HREF = 'Есть ссылки без href'

        STATUS_SET = {
            FIND_ALIEN: 'error',
            INCORRECT_INNER: 'reprimand',
            NO_HREF: 'disabled',
        }

        def process(self):
            self.find_links()

        def find_links(self):
            soup = self.site.main.get_soup()
            links = soup.find_all('a')
            for link in links:
                try:
                    href = link['href']
                    if not (href.startswith('#') or href in SiteMap.ALLOWED_INNER_LINKS):
                        if href.startswith('http'):
                            self.info.add(self.FIND_ALIEN)
                            self.errors.add(href)
                        else:
                            if href:
                                self.info.add(self.INCORRECT_INNER)
                                self.errors.add(href)
                            else:
                                self.info.add(self.NO_HREF)
                                # TODO - добавлять ли в errors?
                except KeyError:
                    self.info.add(self.NO_HREF)

    class HTMLForm:
        # TODO получение атрибута max_length, required
        """html форма"""

        def __init__(self, form_soup):
            self.form = form_soup
            self.action = None
            self.name = None
            self.phone = None
            self.phone_minlength = None
            self.phone_required = None
            self.i_agree = None
            self.is_comment_form = False

        def process(self):
            self.find_action()
            self.find_name()
            self.find_phone()
            self.get_phone_minlength()
            self.check_if_comment_form()

        def find_action(self):
            try:
                self.action = self.form['action']
            except KeyError:
                self.action = 'not found'

        def find_name(self):
            name = self.form.find('input', {'name': 'name'})
            if name:
                self.name = name.get('name')

        def find_phone(self):
            phone = self.form.find('input', {'name': 'phone'})
            if phone:
                self.phone = phone.get('name')

        def get_phone_minlength(self):
            if self.phone:
                phone = self.form.find('input', {'name': 'phone'})
                self.phone_required = phone.get('required')
                try:
                    self.phone_minlength = phone['minlength']
                except KeyError:
                    pass

        def check_i_agree_input(self):
            pass

        def check_if_comment_form(self):
            try:
                self.form[SiteMap.COMMENT_FORM_ATTR]
                self.is_comment_form = True
            except KeyError:
                pass

    class OrderForm(HTMLForm):

        def is_order_form(self):
            pass

    class OrderForms(Check):
        # TODO - вывод данных по каждой формы в отдельности
        DESCRIPTION = 'Order формы'
        KEY_NAME = 'order_forms'

        NO_FORMS = 'Формы не найдены'
        # INCORRECT_FROM = 'Есть некоректная форма'
        # NO_ACTION = 'Отсутствует action в форме'
        INCORRECT_ACTION = 'Некоректный action в форме'
        NAME_ERROR = 'Нет инпута(ошибка) для имени'
        PHONE_ERROR = 'Нет инпута(ошибка) для телефона'
        NO_MIN_LEN = 'Минимальная длина номера не установлена'
        PHONE_NOT_REQUIRED = 'Номер не установлен как обязательный'
        COMMENT_FORM_ON_LAND = 'Есть форма для коментариев'

        STATUS_SET = {
            NO_FORMS: 'error',
            INCORRECT_ACTION: 'error',
            NAME_ERROR: 'error',
            PHONE_ERROR: 'error',
            NO_MIN_LEN: 'disabled',
            PHONE_NOT_REQUIRED: 'error',
            COMMENT_FORM_ON_LAND: 'disabled',
        }

        def __init__(self, site):
            super().__init__(site=site)
            self.forms = []
            self.order_forms_count = 0

        def process(self):
            self.find_forms()
            for form in self.forms:
                self.check_order_form(form)
            if not self.order_forms_count:
                self.info.add(self.NO_FORMS)
            self.count_order_n_comments_forms()

        def find_forms(self):
            soup = self.site.main.get_soup()
            forms = soup.find_all('form')
            for form in forms:
                self.forms.append(LinkChecker.HTMLForm(form))

        def check_order_form(self, form):
            form.process()
            if not form.is_comment_form:
                self.order_forms_count += 1
                if form.action != SiteMap.ORDER:
                    self.info.add(self.INCORRECT_ACTION)
                if form.name != 'name':
                    self.info.add(self.NAME_ERROR)
                if form.phone != 'phone':
                    self.info.add(self.PHONE_ERROR)
                if not form.phone_minlength:
                    self.info.add(self.NO_MIN_LEN)
                if form.phone_required is None:
                    self.info.add(self.PHONE_NOT_REQUIRED)

        def count_order_n_comments_forms(self):
            dic = {'order_forms': 0, 'other': 0}
            for form in self.forms:
                if not form.is_comment_form:
                    dic['order_forms'] += 1
                else:
                    dic['other'] += 1
            self.result_value.update(dic)
            if dic['other']:
                self.info.add(self.COMMENT_FORM_ON_LAND)

    class ApiOrderTT(Check):
        # TODo - success.php!
        """Проверка файла обработки заказа Trirazat API"""
        DESCRIPTION = 'Trirazat API'
        KEY_NAME = 'trirazat_api'

        REDIRECT_PAGE = '"Location: /success'
        OLD_VERSION = '"Location: /success/success.html?"'
        CORRECT_VERSION = '"Location: /success/success.php?name=$name&phone=$phone&"'
        FILE_NOT_FOUND = 'Файл не найден в папке сайта'

        NO_OFFER = 'Оффер не найден'
        NO_FLOW = 'Поток не найден'
        NO_COUNTRY = 'Страна не найдена'
        NO_PRICE = 'Цена не найдена'
        NO_COMM = 'Комментарий не найден'
        REDIRECT_LINE_NOT_FOUND = 'Строка редиректа не найдена'
        REDIRECT_LINE_OLD = 'Старая версия редиректа'
        INCORRECT_REDIRECT_LINE = 'Ошибка в строке редиректа'
        # TODO - add currency
        VARIABLES = {
            'flow': {
                'variable': '$data["flow"]',
                'not_found': NO_FLOW
            },
            'offer': {
                'variable': '$data["offer"]',
                'not_found': NO_OFFER
            },
            'base': {
                'variable': '$data["base"]',
                'not_found': NO_PRICE
            },
            'country': {
                'variable': '$data["country"]',
                'not_found': NO_COUNTRY
            },
            'comm': {
                'variable': '$data["comm"]',
                'not_found': NO_COMM
            },
        }

        STATUS_SET = {
            FILE_NOT_FOUND: 'error',
            NO_OFFER: 'error',
            NO_FLOW: 'error',
            NO_COUNTRY: 'disabled',
            NO_PRICE: 'disabled',
            NO_COMM: 'disabled',
            REDIRECT_LINE_NOT_FOUND: 'error',
            REDIRECT_LINE_OLD: 'error',
            INCORRECT_REDIRECT_LINE: 'error',
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.price = None
            self.flow = None
            self.offer = None
            self.country = None
            self.comm = None

        def process(self):
            if SiteMap.ORDER not in self.site.files:
                self.info.add(self.FILE_NOT_FOUND)
            else:
                self.find_variables_value()
                self.add_errors()
                self.find_redirect_page()

        def find_variables_value(self):
            file_lines = self.site.api_php.get_file_lines()
            for line in file_lines:
                for param, data in self.VARIABLES.items():
                    variable = data['variable']
                    if variable in line:
                        value = PageFile.get_variable_value(line)
                        self.result_value.update({param: value})
                        break

        def add_errors(self):
            # TODO - переделать. + функция дублируеться
            for param in self.VARIABLES.keys():
                try:
                    if not self.result_value[param]:
                        error = self.VARIABLES[param]['not_found']
                        self.info.add(error)
                except KeyError:
                    error = self.VARIABLES[param]['not_found']
                    self.info.add(error)

        def find_redirect_page(self):
            file_lines = self.site.api_php.get_file_lines()
            redirect_line = None
            for line in file_lines:
                if self.REDIRECT_PAGE in line:
                    redirect_line = line
                    break
            if not redirect_line:
                self.info.add(self.REDIRECT_LINE_NOT_FOUND)
                return
            if self.OLD_VERSION in redirect_line:
                self.info.add(self.REDIRECT_LINE_OLD)
                return
            if self.CORRECT_VERSION not in redirect_line:
                self.info.add(self.INCORRECT_REDIRECT_LINE)

    class OfferFind(Check):
        DESCRIPTION = 'Поиск офферов по тексту'
        KEY_NAME = 'offer_name'

        FIND_MORE_ONE_OFFER = 'Найдено больше одного оффера'
        OFFER_NOT_LOAD = 'Офферы не загружены'
        NO_OFFER_FOUNT = 'Не найден ни один оффер'

        STATUS_SET = {
            FIND_MORE_ONE_OFFER: 'error',
            OFFER_NOT_LOAD: 'disables',
            NO_OFFER_FOUNT: 'disables',
        }

        def process(self):
            land_text = self.site.main.get_text()
            offers = self.get_offers_list()
            find_offers = self.find_offers_in_text(land_text, offers)
            self.get_checker_result(find_offers)

        def get_offers_list(self):
            try:
                offers_names = self.site.other_data['offers_positions_names']
                result = [name['name'] for name in offers_names]
                return result
            except TypeError:
                self.info.add(self.OFFER_NOT_LOAD)
                return list()

        @staticmethod
        def find_offers_in_text(text: str, offers: list):
            """поиск офферов по тексту"""
            find_offers = dict()
            text = text.lower()
            for offer in offers:
                if offer in text:
                    result = re.findall(r'\W' + offer + r'\W', text)
                    dic = {offer: sum([text.count(pattern) for pattern in set(result)])}
                    find_offers.update(dic)
            return find_offers

        def get_checker_result(self, find_offers):
            """Обработака результатя поиска офферов по тексту"""
            offers_count = 0
            for offer, count in find_offers.items():
                if count:
                    offers_count += 1
            if offers_count > 1:
                self.info.add(self.FIND_MORE_ONE_OFFER)
                self.errors.update(find_offers)
            elif offers_count != 1:
                self.info.add(self.NO_OFFER_FOUNT)
                self.errors.update(find_offers)
            self.result_value.update(find_offers)

        # def get_checker_result(self, find_offers):
        #     """Обработака результатя поиска офферов по тексту"""
        #     if len(find_offers) > 1:
        #         self.info.add(self.FIND_MORE_ONE_OFFER)
        #         self.errors.update(find_offers)
        #     elif len(find_offers) != 1:
        #         self.info.add(self.NO_OFFER_FOUNT)
        #         self.errors.update(find_offers)
        #     self.result_value.update(find_offers)

        def find_most_count_word_in_land(self):
            """Поиск самого встречаемого слова по тексту
            - возможно это будет оффер которого нет в тексте"""
            pass

    class CountryFind(Check):
        """Поиск падежей стран по тексту"""

        DESCRIPTION = 'Поиск падежей стран по тексту'
        KEY_NAME = 'country_names'

        FIND_MORE_ONE_COUNTRY = 'Найдено больше одной страны'
        COUNTRY_NOT_LOAD = 'Страны не загружены'
        # NO_COUNTRY_FOUNT = 'Страные не найдены'

        STATUS_SET = {
            FIND_MORE_ONE_COUNTRY: 'error',
            COUNTRY_NOT_LOAD: 'disables',
            # NO_COUNTRY_FOUNT: 'disables',
        }

        def process(self):
            countrys_names = self.load_countrys_names()
            if not countrys_names:
                self.info.add(self.COUNTRY_NOT_LOAD)
            land_text = self.site.main.get_text()
            countrys_result = self.find_country_names(land_text, countrys_names)
            self.get_checker_result(countrys_result)


        def load_countrys_names(self):
            try:
                country_names = self.site.other_data['country_names']
                return country_names
            except TypeError:
                self.info.add(self.COUNTRY_NOT_LOAD)
                return list()

        @staticmethod
        def find_country_names(text, country_list: list):
            result = {}
            text = text.lower()
            for country_code, words in country_list.items():
                dic = {country_code: list()}
                for word in words:
                    if word in text:
                        dic[country_code].append(word)
                if dic[country_code]:
                    result.update(dic)

            return result

        def get_checker_result(self, countrys_result):
            if len(countrys_result) > 1:
                self.info.add(self.FIND_MORE_ONE_COUNTRY)
                self.errors.update(countrys_result)
            self.result_value.update(countrys_result)


    class HideClick(Check):

        DESCRIPTION = 'HideClick файл клоаки'
        KEY_NAME = 'hide_click'
        # variables
        WHITE_PAGE_VARIABLE = "$CLOAKING['WHITE_PAGE']"
        BLACK_PAGE_VARIABLE = "$CLOAKING['OFFER_PAGE']"
        DEBUG_MODE_VARIABLE = "$CLOAKING['DEBUG_MODE']"
        GEO_LIST_VARIABLE = "$CLOAKING['ALLOW_GEO']"
        # errors
        CLO_NOT_ACTIVE = 'Сайт не заклоачен'
        # variables FILE not found
        FILE_NOT_FOUND = 'Файл клоаки не найден в папке сайта'
        FILE_WHITE_NOT_FOUND = 'файл white.html не найден'
        FILE_BLACK_NOT_FOUND = 'файл black.html не найден'
        # TODO - <!DOCTYPE html> - предусмотреть этот вариант
        NO_WHITE = 'white не установлен'
        NO_BLACK = 'black не установлен'
        NO_DEBUG_MODE = 'Дебаг переменная не найдена'
        NO_GEO = 'Переменная гео не установлены'
        # не коректные значения
        BLACK_INCORRECT = 'Некоректное название black_page'
        WHITE_INCORRECT = 'Некоректное название white_page'
        DEBUG_INCORRECT = 'Не коректное значение debug'
        DEBUG_MODE_ON = 'Дебаг включен'

        GEO_LEN_ERROR = 'Неверная длина значения гео'
        GEO_CHAR_ERROR = 'Цифра или небуква в гео'
        GEO_INCORRECT_NAME = 'Не правильное название гео(нет в списке)'

        VARIABLES = {
            'white': {
                'variable': WHITE_PAGE_VARIABLE,
                'not_found': NO_WHITE,
            },
            'black': {
                'variable': BLACK_PAGE_VARIABLE,
                'not_found': NO_BLACK,
            },
            'debug': {
                'variable': DEBUG_MODE_VARIABLE,
                'not_found': NO_DEBUG_MODE,
            },
            'geo': {
                'variable': GEO_LIST_VARIABLE,
                'not_found': NO_GEO,
            },

        }

        STATUS_SET = {
            CLO_NOT_ACTIVE: 'disabled',
            FILE_NOT_FOUND: 'error',
            NO_WHITE: 'error',
            NO_BLACK: 'error',
            NO_GEO: 'error',
            NO_DEBUG_MODE: 'error',
            BLACK_INCORRECT: 'error',
            WHITE_INCORRECT: 'error',
            DEBUG_INCORRECT: 'error',
            DEBUG_MODE_ON: 'reprimand',
            GEO_LEN_ERROR: 'error',
            GEO_CHAR_ERROR: 'error',
            GEO_INCORRECT_NAME: 'error',
            FILE_WHITE_NOT_FOUND: 'error',
            FILE_BLACK_NOT_FOUND: 'error',
        }

        def process(self):
            if not self.site.cloac:
                self.info.add(self.CLO_NOT_ACTIVE)
                return
            if SiteMap.CLOAC_FILE not in self.site.files:
                self.info.add(self.FILE_NOT_FOUND)
                return
            self.find_html_pages()
            self.find_variables_value()
            self.add_errors()
            self.check_geo()
            self.check_black_name()
            self.check_debug_mode()
            self.check_white_name()

        def find_html_pages(self):
            if SiteMap.BLACK not in self.site.files:
                self.info.add(self.FILE_BLACK_NOT_FOUND)
            if SiteMap.WHITE not in self.site.files:
                self.info.add(self.FILE_WHITE_NOT_FOUND)

        def find_variables_value(self):
            # file_text = self.site.index_php.get_text()
            # file_lines = file_text.split('\n')[:20]  # обрезка файла
            file_lines = self.site.index_php.get_file_lines(20)
            for line in file_lines:
                for param, data in self.VARIABLES.items():
                    variable = data['variable']
                    if variable in line:
                        value = PageFile.get_variable_value(line)
                        self.result_value.update({param: value})
                        break

        def check_debug_mode(self):
            try:
                debug = self.result_value['debug']
                if debug not in ('on', 'off'):
                    self.info.add(self.DEBUG_INCORRECT)
                    self.errors.add(debug)
                else:
                    if debug == 'on':
                        self.info.add(self.DEBUG_MODE_ON)
            except KeyError:
                pass

        def check_white_name(self):
            try:
                white = self.result_value['white']
                if white != SiteMap.WHITE:
                    self.info.add(self.WHITE_INCORRECT)
                    self.errors.add(white)
            except KeyError:
                pass

        def check_black_name(self):
            try:
                black = self.result_value['black']
                if black != SiteMap.BLACK:
                    self.info.add(self.BLACK_INCORRECT)
                    self.errors.add(black)
            except KeyError:
                pass

        def check_geo(self):
            try:
                geo = self.result_value['geo']
                geo = geo.lower()
                geo_list = geo.split(',')
                for geo in geo_list:
                    if geo not in SiteMap.ALLOWED_GEO_LIST:
                        self.info.add(self.GEO_INCORRECT_NAME)
                        self.errors.add(geo)
                    if len(geo) != 2:
                        self.info.add(self.GEO_LEN_ERROR)
                        self.errors.add(geo)
                    for char in geo:
                        if not char.isalpha():
                            self.info.add(self.GEO_CHAR_ERROR)
                            self.errors.add(geo)
            except KeyError:
                pass

        def add_errors(self):
            for param in self.VARIABLES.keys():
                try:
                    if not self.result_value[param]:
                        error = self.VARIABLES[param]['not_found']
                        self.info.add(error)
                except KeyError:
                    error = self.VARIABLES[param]['not_found']
                    self.info.add(error)

    class WhitePage(Check):
        DESCRIPTION = 'Белая страница'
        KEY_NAME = 'white_page'

    # тело Главного чекера
    def __init__(self, site):
        self.site = site
        self.checkers = [
            # self.SaveComment,
            self.OrderForms,
            self.PageLink,
            # self.SpasPage,
            # self.PolicyPage,
            # self.TermsPage,
            # self.SuccessPage,
            # self.Req,
            # self.FaceBookPixel,
            # self.TtPixel,
            # self.ApiOrderTT,
            # self.HideClick,
            # self.FbPixelImg,
            self.OfferFind,
            self.CountryFind,
        ]
        self.results_from_checkers = []
        self.result = set()

    def process(self):
        self.site.check_pages_conn()
        for check_class in self.checkers:
            checker = check_class(self.site)
            checker.process()
            checker.get_result_status()
            self.results_from_checkers.append(checker.get_result())
            self.result.add(checker.result_code)
        self.get_general_result()

    def get_general_result(self):
        """Получить общий статус проверки сайта"""
        if 'error' in self.result:
            result_code = 'error'
        elif 'reprimand' in self.result:
            result_code = 'reprimand'
        else:
            result_code = 'good'
        # elif 'good' in self.result:
        #     result_code = 'good'
        # elif 'disabled' in self.result:
        #     result_code = 'disabled'
        # else:
        #     result_code = 'none'
        dic = {
            'result_code': result_code,
            'result_html': StatusHTML.get_checker_status_html(result_code),
            'result_text': StatusHTML.get_checker_status_text(result_code),
        }
        self.result = dic


if __name__ == '__main__':
    site = SiteMap(url='https://shouldsayit.ml/landers/vlad/bd-cardio-nrj-cpagetti-konfuz-magic-2/index.html',
                   is_cloac=False)
    site.check_pages_conn()
    main_ckecker = LinkChecker(site=site)
    main_ckecker.process()
    pprint(main_ckecker.results_from_checkers)
