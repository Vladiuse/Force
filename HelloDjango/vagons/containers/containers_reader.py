import re
from collections import Counter
import json


class NotContainerError(Exception):
    pass


class Container:
    LETTERS_WEIGHT = {
        'A': 10, 'B': 12, 'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20,
        'K': 21, 'L': 23, 'M': 24, 'N': 25, 'O': 26, 'P': 27, 'Q': 28, 'R': 29, 'S': 30, 'T': 31,
        'U': 32, 'V': 34, 'W': 35, 'X': 36, 'Y': 37, 'Z': 38,
    }

    def __init__(self, container_id: str, source_text_line=''):
        self.id = container_id
        self.text_line = source_text_line

    @property
    def json(self):
        return {'id': self.id, 'text_line': self.text_line}

    @staticmethod
    def find_container_number(text_line):
        v_number = re.search('[A-zА-я]{4}\s{0,4}0{0,2}\d{7}', text_line)
        if v_number:
            return v_number.group(0)
        return None

    @staticmethod
    def prettify_container_number(container_number):
        """Уюирает 00 или 0 у номера контейнера и убирает пробелы"""
        container_number = container_number.replace(' ', '')
        container_number = container_number.upper()
        if container_number[4:6] == '00' and len(container_number) == 13:
            container_number = container_number[:4] + container_number[6:]
        if container_number[4:5] == '0' and len(container_number) == 12:
            container_number = container_number[:4] + container_number[5:]
        return container_number

    def is_has_ru_letters(self):
        return not bool(re.search('[A-z]{4}\d{7}', self.id))

    def is_container_number_correct(self):
        if self.is_has_ru_letters():
            return False
        res = 0
        if not self.id:
            return None
        for pos, char in enumerate(self.id[:-1]):

            if pos < 4:
                number = Container.LETTERS_WEIGHT[char] * 2 ** pos
            else:
                number = int(char) * 2 ** pos
            res += number

        if self.id[-1] == str(res % 11)[-1]:
            return True
        else:
            return False

    def __hash__(self):
        res = ''
        for char in self.id:
            res += str(ord(char))
        return int(res)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id

    def __str__(self):
        return self.id

    def __repr__(self):
        return str({'id': self.id, 'text_line': self.text_line})


class ContainerList:

    def __init__(self, *containers):
        self.containers = list(containers)
        self._validate()

    @staticmethod
    def create_container_list_from_seq(seq):
        c_list = ContainerList()
        for num in seq:
            c = Container(num)
            c_list.append(c)
        return c_list

    def _validate(self):
        if not all([isinstance(item, Container) for item in self.containers]):
            raise NotContainerError

    def append(self, elem):
        if not (isinstance(elem, Container)):
            raise NotContainerError
        self.containers.append(elem)

    def __str__(self):
        return f'<ContainerList:len={len(self)}> {self.containers}'

    def __repr__(self):
        return str(self.containers)

    def __len__(self):
        return len(self.containers)

    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        self.i += 1
        try:
            return self.containers[self.i]
        except IndexError:
            raise StopIteration

    def __sub__(self, other):
        if not isinstance(other, ContainerList):
            raise NotImplemented
        s1 = set(self.containers)
        s2 = set(other.containers)
        res = s1 - s2
        return ContainerList(*res)

    def __and__(self, other):
        if not isinstance(other, ContainerList):
            raise NotImplemented
        s1 = set(self.containers)
        s2 = set(other.containers)
        res = s1 & s2
        return ContainerList(*res)

    def rus_containers(self):
        # ru_containers = list(filter(lambda container: container.is_has_ru_letters(), self.containers))
        ru_containers = filter(Container.is_has_ru_letters, self.containers)
        return ContainerList(*ru_containers)

    def unique(self):
        unique_containers = set(self.containers)
        return ContainerList(*unique_containers)

    def duplicates(self):
        counter = Counter()
        counter.update(self.containers)
        duplicates_containers = list()
        for k, v in counter.items():
            if v > 1:
                duplicates_containers.append(k)
        return ContainerList(*duplicates_containers)

    def incorrect_number_containers(self):
        incorrect_number = list(filter(lambda container: container.is_container_number_correct(), self.containers))
        return ContainerList(*incorrect_number)

    def json(self):
        li = list()
        for con in self.containers:
            li.append(con.json)
        return json.dumps(li)


class ContainerFile:

    def __init__(self, text_file):
        self.text_file = text_file
        self.containers = ContainerList()
        self.no_containers_lines = []

    def process(self):
        for char in '\r', '\t':
            self.text_file = self.text_file.replace(char, '\n')

        for line in self.text_file.split('\n'):
            container_number = Container.find_container_number(line)
            if container_number:
                container_number = Container.prettify_container_number(container_number)
                container = Container(container_number, source_text_line=line)
                self.containers.append(container)
            else:
                if line != '':
                    self.no_containers_lines.append(line)

    def get_no_containers_lines_json(self):
        res = json.dumps(self.no_containers_lines)
        return res


class ContainerReader:

    def __init__(self, file_text_1, file_text_2):
        self.file_1 = ContainerFile(file_text_1)
        self.file_2 = ContainerFile(file_text_2)
        self.file_1.process()
        self.file_2.process()

    def unique_containers_file_1(self):
        """Уникальные контейнеры для файла 1"""
        return self.file_1.containers - self.file_2.containers

    def unique_containers_file_2(self):
        """Уникальные контейнеры для файла 2"""
        return self.file_2.containers - self.file_1.containers

    def common_containers(self):
        """Общие контейнеры для 2х файлов"""
        return self.file_1.containers & self.file_2.containers

    def result(self):
        return {
            'file_1_unique_containers': self.unique_containers_file_1().json(),
            'file_2_unique_containers': self.unique_containers_file_1().json(),
            'common_containers': self.common_containers().json(),

        }
        # return {
        #     'file_1_unique_containers': list(self.unique_containers_file_1()),
        #     'file_2_unique_containers': list(self.unique_containers_file_2()),
        #     'file_1_ru_containers': self.file_1.containers.rus_containers(),
        #     'common_containers': list(self.common_containers()),
        #
        # }

    def result_no_containers(self):
        return {
            'file_1_no_conteiner_list': self.file_1.get_no_containers_lines_json(),
            'file_2_no_conteiner_list': self.file_2.get_no_containers_lines_json(),
        }


if __name__ == '__main__':
    c_list = ContainerList.create_container_list_from_seq(['AAAA1234567', 'AAAA1234567', 'AAAA1234567'])
    print(c_list.json())
