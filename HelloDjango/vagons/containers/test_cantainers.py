import unittest
from unittest.mock import patch
from .containers_reader import Container, ContainerFile, ContainerList, NotContainerError


class TestContainer(unittest.TestCase):

    def test_find_container_number_in_line(self):
        lines = (
            ['простой тест ABCD1234567', 'ABCD1234567'],
            ['с прбелом ABCD 1234567', 'ABCD 1234567'],
            ['много пробелов ABCD    1234567', 'ABCD    1234567'],
            ['русские буквы ФЫВА1234567', 'ФЫВА1234567'],
            ['русские буквы ФЫВА 1234567', 'ФЫВА 1234567'],
            ['буквы в перемешку ФЫFF1234567', 'ФЫFF1234567'],
            ['разный регистр fGФы1234567', 'fGФы1234567'],
            ['в нижний регистр ffgg1234567', 'ffgg1234567'],
            # номер с нулями
            ['вафыаыаф в тр fвы выфв AAAA001234567', 'AAAA001234567'],
            ['вафыаыаф в тр fвы выфв AAAA01234567', 'AAAA01234567'],
            ['вафыаыаф в тр fвы выфв AAAA 01234567', 'AAAA 01234567'],
            ['вафыаыаф в тр fвы выфв AAПП  01234567', 'AAПП  01234567'],

            ['abcd1234567', 'abcd1234567'],
        )
        for text_line, result in lines:
            self.assertEqual(Container.find_container_number(text_line), result, msg=[text_line, result])

    def test_not_find_container_number_in_line(self):
        lines = (
            'dsadsadsd sdasd ',
            'dmfsfoa AAA1234567',
            'dasd AAAA123456dsadasd',
            'dasd AAAA  123456  dsadasd'
        )
        for text_line in lines:
            self.assertEqual(Container.find_container_number(text_line), None, msg=text_line)

    def test_container_number_prettify(self):
        containers_nums = [
            ['AAAA001234567', 'AAAA1234567'],
            ['AAAA01234567', 'AAAA1234567'],

            ['AAAA  001234567', 'AAAA1234567'],
            ['AAAA 01234567', 'AAAA1234567'],

            ['aaaa  001234567', 'AAAA1234567'],
            ['bbbb 01234567', 'BBBB1234567'],
        ]
        for container_num, result in containers_nums:
            self.assertEqual(Container.prettify_container_number(container_num), result, msg=[container_num, result])

    def test_ru_leters_in_container_numm(self):
        nums = [
            ['AAAA1234567', False],
            ['ФФФФ1234567', True],
            ['ФFFF1234567', True],
        ]
        for num, res in nums:
            vag = Container(num)
            self.assertEqual(vag.is_has_ru_letters(), res, msg=[num, res])

    def test_is_validate_append(self):
        try:
            container_list = ContainerList()
            for _ in range(5):
                c = Container('')
                container_list.append(c)
        except NotContainerError:
            self.fail()

    def test_is_validate_error_append(self):
        with self.assertRaises(NotContainerError) as context:
            containers_list = ContainerList()
            c = 'str'
            containers_list.append(c)

    def test_init_container_list_from_seq(self):
        conts = [Container(str(num)) for num in range(5)]
        container_list = ContainerList(*conts)
        self.assertTrue(len(container_list) == 5)

    def test_add_not_containers_from_seq(self):
        conts = [Container(str(num)) for num in range(5)]
        conts.append('1')
        with self.assertRaises(NotContainerError) as context:
            container_list = ContainerList(*conts)





class TestContainerFile(unittest.TestCase):

    def test_process(self):
        text = """ Контейнера, установленные на площадке   23.11.2022
        секции: 1 - 99                          11:59
        ────────────────────────────────────────────────────────────────────────────────
        коорд.│ N контейнера  │сост.│  п л о м б ы
        ────────────────────────────────────────────────────────────────────────────────
         1 111 LYGU4093473 /99 груж. 124026
         1 112 RZDU5254861 /99 пор.  
         1 121 SEKU5565976 /99 пор.  
         1 122 HNKU5108787 /99 пор.  
         1 131 HNKU6260710 /99 груж. 22293
         1 132 WIKU5221268 /99 груж. 23201
         1 133 HNKU6131694 /99 груж. 23310
         1 143 HNKU5120674 /99 груж. 121837
         1 162 TKRU4000934 /99 пор.  
         1 172 GAWU5026906 /99 пор.  """
        file = ContainerFile(text)
        file.process()
        self.assertEqual(len(file.containers),10)
        self.assertEqual(len(file.no_containers_lines),5)


if __name__ == '__main__':
    unittest.main()