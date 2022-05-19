import re
from bs4 import BeautifulSoup
import os


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


SPAN_CLASS = 'back-warning '
SPAN_ERROR = 'error'


class DateFixer:
    """Wrap дат в тэг"""

    @staticmethod
    def fix_dates(text):
        """Главная функция"""
        # text = re.sub(r'\D19\d\d\D|\D20\d\d\D', DateFixer.wrap_years, text)
        # text = re.sub(r'\D\d{1,2}[./\\]\d{1,2}.\d{2,4}\D', DateFixer.wrap_dates, text)
        text = re.sub(r'[-.\s](19|20)\d{2}[-.\s]', DateFixer.wrap_years, text)
        text = re.sub(r'[\s><-]\d{1,2}[./\\]\d{1,2}.\d{2,4}[\s><-]', DateFixer.wrap_dates, text)
        return text

    @staticmethod
    def wrap_years(string):
        """Поиск дат 19хх 20хх и добавление тэга и класса"""
        _class = SPAN_CLASS
        print(string, type(string), string.group(0))
        res = f'<span class="{SPAN_CLASS}">{string.group(0)}</span>'
        return res

    # text = re.sub(r'19\d\d|20\d\d',wrap_date_years, text)
    # print(text)
    @staticmethod
    def wrap_dates(string):
        """Поиск дат хх.хх.хххх"""
        date = string.group(0)
        _class = SPAN_CLASS
        print(date, '/' in date)
        if '\\' in date or '/' in date:
            _class += SPAN_ERROR
            print('add', )
        if not is_date_correct(date):
            _class += ' error' if not _class.endswith(SPAN_ERROR) else ''
        res = f'<span class="{_class}">{string.group(0)}</span>'
        return res

    # dates = re.findall(r'\d{1,2}[./\\]\d{1,2}.\d{2,4}', text)
    # print(dates)

    # text = re.sub(r'\d{1,2}[./\\]\d{1,2}.\d{2,4}', wrap_dates, text)
    # print(text)


class FrontElems:

    @staticmethod
    def add_elems_to_text(soup, url=''):
        """Main"""
        FrontElems.add_html(soup)
        FrontElems.add_css(soup)
        FrontElems.add_js(soup)
        FrontElems.add_bouble_img_in_tool(soup)
        # if url:



    @staticmethod
    def load_html_block():
        with open('./checker/checker_class/front_data/block.html') as file:
            text = file.read()
        return text

    @staticmethod
    def load_css():
        with open('./checker/checker_class/front_data/styles.css') as file:
            text = file.read()
        return text

    @staticmethod
    def load_js_script():
        with open('./checker/checker_class/front_data/script.js') as file:
            text = file.read()
        return text

    @staticmethod
    def add_html(soup):
        block_text = FrontElems.load_html_block()
        # print(block_text)
        div_soup = BeautifulSoup(block_text, 'lxml')
        div_soup = div_soup.find('div', {"id": "oi-toolbar"})
        soup.html.body.insert(0, div_soup)

    @staticmethod
    def add_css(soup):
        styles_text = FrontElems.load_css()
        styles_tag = soup.new_tag('style')
        styles_tag.string = styles_text
        soup.html.head.insert(0, styles_tag)

    @staticmethod
    def add_js(soup):
        script_text = FrontElems.load_js_script()
        script_tag = soup.new_tag("script")
        script_tag.string = script_text
        soup.html.body.append(script_tag)

    @staticmethod
    def add_bouble_img_in_tool(soup):
        double_imgs = FrontElems.find_img_double(soup)
        div_toolbar = soup.find('div', {"id": "back-info"})
        if double_imgs:
            p_info = soup.new_tag('p')
            p_info.string = 'Картинки дубли:'
            div_toolbar.append(p_info)
        for img_scr in double_imgs:
            new_img = soup.new_tag('img', src=img_scr)
            print(new_img, 'new_img')
            div_toolbar.append(new_img)

    @staticmethod
    def find_img_double(soup):
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



if __name__ == '__main__':
    with open('test.html') as file:
        text = file.read()
    text = DateFixer.fix_dates(text)
    print(text)



