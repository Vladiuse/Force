import re
from bs4 import BeautifulSoup
import os
import requests as req


def is_date_correct(date):
    """Проверка коректности даты"""
    date = date.replace('\\', '.')
    date = date.replace('//', '.')
    try:
        days, mounth, year = date.split('.')
        if int(days) not in range(1, 32):
            return False
        if int(mounth) not in range(1, 13):
            return False
        return True
    except ValueError:
        return False

def find_img_double(soup) -> set:
    """Поиск дублей карртинок в html """
    # soup = BeautifulSoup(text, 'lxml')
    images = soup.find_all('img')
    srcs = []
    srcs_double = set()
    for img in images:
        try:
            src = img['src']
            srcs.append(src)
        except KeyError:
            pass
    for src in srcs:
        if srcs.count(src) > 1:
            srcs_double.add(src)
    return srcs_double


SPAN_CLASS_BACK = 'back-warning '
SPAN_ERROR = 'error'
TOOLBAR_HTML_FILE = './checker/checker_class/front_data/block.html'
TOOLBAR_STYLES_FILE = './checker/checker_class/front_data/styles.css'
TOOLBAR_JS_FILE = './checker/checker_class/front_data/script.js'

class TextFixxer:
    """Внесение изменений в исходный код страницы"""

    def __init__(self, text):
        self.text = text


    def process(self):
        """Главная функция"""
        # text = re.sub(r'\D19\d\d\D|\D20\d\d\D', TextFixxer.wrap_years, text)
        # text = re.sub(r'\D\d{1,2}[./\\]\d{1,2}.\d{2,4}\D', TextFixxer.wrap_dates, text)
        self.text = re.sub(r'[-.\s](19|20)\d{2}[-.\s]', self.wrap_years, self.text)
        self.text = re.sub(r'[\s><-]\d{1,2}[./\\]\d{1,2}.\d{2,4}[\s><-]', self.wrap_dates, self.text)


    @staticmethod
    def wrap_years(string):
        """Поиск дат 19хх 20хх и оборачивание в тэг и класса"""
        _class = SPAN_CLASS_BACK
        res = f'<span class="{SPAN_CLASS_BACK}">{string.group(0)}</span>'
        return res

    @staticmethod
    def wrap_dates(string):
        """Поиск дат хх.хх.хххх и оборачивание в тэг"""
        date = string.group(0)
        _class = SPAN_CLASS_BACK
        print(date, '/' in date)
        if '\\' in date or '/' in date:
            _class += SPAN_ERROR
            print('add', )
        if not is_date_correct(date):
            _class += ' error' if not _class.endswith(SPAN_ERROR) else ''
        res = f'<span class="{_class}">{string.group(0)}</span>'
        return res


class DomFixxer:
    """Изменение верстки сайта"""

    def __init__(self, soup, url):
        self.soup = soup
        self.toolbar = None
        self.styles = None
        self.script = None
        self.url = url

    def process(self):
        self.load_files()
        self.add_bouble_img_in_tool()
        self.add_checked_url_in_toolbar()
        self.add_base_tag()


        self.add_html()
        self.add_css()
        self.add_js()


    def load_files(self):
        with open(TOOLBAR_HTML_FILE) as file:
            self.toolbar = file.read()
        self.toolbar = BeautifulSoup(self.toolbar, 'lxml')
        with open(TOOLBAR_STYLES_FILE) as file:
            self.styles = file.read()
        with open(TOOLBAR_JS_FILE) as file:
            self.script = file.read()


    def add_html(self):
        # div_soup = BeautifulSoup(self.toolbar, 'lxml')
        div_soup = self.toolbar.find('div', {"id": "oi-toolbar"})
        self.soup.html.body.insert(0, div_soup)


    def add_css(self):
        """Добавить стили на сайт"""
        styles_tag = self.soup.new_tag('style')
        styles_tag.string = self.styles
        self.soup.html.head.insert(0, styles_tag)


    def add_js(self):
        """Добавить скрипт на сайт"""
        script_tag = self.soup.new_tag("script")
        script_tag.string = self.script
        self.soup.html.body.append(script_tag)


    def add_bouble_img_in_tool(self):
        double_imgs_src = find_img_double(self.soup)
        div_toolbar = self.toolbar.find('div', {"id": "back-info"})
        if double_imgs_src:
            p_info = self.soup.new_tag('p')
            p_info.string = 'Картинки дубли:'
            div_toolbar.append(p_info)
        for img_scr in double_imgs_src:
            new_img = self.toolbar.new_tag('img', src=img_scr)
            div_toolbar.append(new_img)

    def add_checked_url_in_toolbar(self):
        self.toolbar.find(id="original-link")['data-href'] = self.url

    def add_base_tag(self):
        base = self.soup.find('base')
        if not base:
            url = self.url
            if '?' in self.url:
                url = self.url.split('?')[0]
            new_base = self.soup.new_tag('base')
            new_base['href'] = url
            print(new_base)
            self.soup.html.head.insert(0, new_base)


        print(base)

    def fix_relativ_path(self):
        pass







if __name__ == '__main__':
    url = 'https://a.diabetins-new.com/'
    res = req.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    dom = DomFixxer(soup, url)
    dom.process()
    # print(dom.soup)


SPAN_CLASS_BACK = 'back-warning '
SPAN_ERROR = 'error'


# class TextFixxer:
#     """Wrap дат в тэг"""

#     @staticmethod
#     def fix_dates(text):
#         """Главная функция"""
#         # text = re.sub(r'\D19\d\d\D|\D20\d\d\D', TextFixxer.wrap_years, text)
#         # text = re.sub(r'\D\d{1,2}[./\\]\d{1,2}.\d{2,4}\D', TextFixxer.wrap_dates, text)
#         text = re.sub(r'[-.\s](19|20)\d{2}[-.\s]', TextFixxer.wrap_years, text)
#         text = re.sub(r'[\s><-]\d{1,2}[./\\]\d{1,2}.\d{2,4}[\s><-]', TextFixxer.wrap_dates, text)
#         return text

#     @staticmethod
#     def wrap_years(string):
#         """Поиск дат 19хх 20хх и добавление тэга и класса"""
#         _class = SPAN_CLASS_BACK
#         print(string, type(string), string.group(0))
#         res = f'<span class="{SPAN_CLASS_BACK}">{string.group(0)}</span>'
#         return res

#     # text = re.sub(r'19\d\d|20\d\d',wrap_date_years, text)
#     # print(text)
#     @staticmethod
#     def wrap_dates(string):
#         """Поиск дат хх.хх.хххх"""
#         date = string.group(0)
#         _class = SPAN_CLASS_BACK
#         print(date, '/' in date)
#         if '\\' in date or '/' in date:
#             _class += SPAN_ERROR
#             print('add', )
#         if not is_date_correct(date):
#             _class += ' error' if not _class.endswith(SPAN_ERROR) else ''
#         res = f'<span class="{_class}">{string.group(0)}</span>'
#         return res

#     # dates = re.findall(r'\d{1,2}[./\\]\d{1,2}.\d{2,4}', text)
#     # print(dates)

#     # text = re.sub(r'\d{1,2}[./\\]\d{1,2}.\d{2,4}', wrap_dates, text)
#     # print(text)

 
# class DomFixxer:

#     @staticmethod
#     def add_elems_to_text(soup, url=''):
#         """Main"""
#         DomFixxer.add_html(soup)
#         DomFixxer.add_css(soup)
#         DomFixxer.add_js(soup)
#         DomFixxer.add_bouble_img_in_tool(soup)
#         # if url:



#     @staticmethod
#     def load_html_block():
#         with open('./checker/checker_class/front_data/block.html') as file:
#             text = file.read()
#         return text

#     @staticmethod
#     def load_css():
#         with open('./checker/checker_class/front_data/styles.css') as file:
#             text = file.read()
#         return text

#     @staticmethod
#     def load_js_script():
#         with open('./checker/checker_class/front_data/script.js') as file:
#             text = file.read()
#         return text

#     @staticmethod
#     def add_html(soup):
#         block_text = DomFixxer.load_html_block()
#         # print(block_text)
#         div_soup = BeautifulSoup(block_text, 'lxml')
#         div_soup = div_soup.find('div', {"id": "oi-toolbar"})
#         soup.html.body.insert(0, div_soup)

#     @staticmethod
#     def add_css(soup):
#         styles_text = DomFixxer.load_css()
#         styles_tag = soup.new_tag('style')
#         styles_tag.string = styles_text
#         soup.html.head.insert(0, styles_tag)

#     @staticmethod
#     def add_js(soup):
#         script_text = DomFixxer.load_js_script()
#         script_tag = soup.new_tag("script")
#         script_tag.string = script_text
#         soup.html.body.append(script_tag)

#     @staticmethod
#     def add_bouble_img_in_tool(soup):
#         double_imgs = DomFixxer.find_img_double(soup)
#         div_toolbar = soup.find('div', {"id": "back-info"})
#         if double_imgs:
#             p_info = soup.new_tag('p')
#             p_info.string = 'Картинки дубли:'
#             div_toolbar.append(p_info)
#         for img_scr in double_imgs:
#             new_img = soup.new_tag('img', src=img_scr)
#             print(new_img, 'new_img')
#             div_toolbar.append(new_img)

#     @staticmethod
#     def find_img_double(soup):
#         # soup = BeautifulSoup(text, 'lxml')
#         images = soup.find_all('img')
#         srcs = []
#         srcs_double = set()
#         for img in images:
#             try:
#                 src = img['src']
#                 srcs.append(src)
#             except KeyError:
#                 pass
#         for src in srcs:
#             if srcs.count(src) > 1:
#                 srcs_double.add(src)
#         return srcs_double




