import re


class Vagon:

    def __init__(self, vagon_data):
        self.vagon_data = vagon_data + '\n'
        self.id = self.find_vagon()

    def __str__(self):
        return self.id + '\n'

    def find_vagon(self):
        vagon = re.search('', self.vagon_data)
        if vagon:
            vagon_id = vagon.group(0)
            return vagon_id

    def is_has_ru_letters(self):
        return not bool(re.search('[A-z]{4}\s*\d{7}', self.id))


class VagReader:

    def __init__(self, text):
        self.text = text
        self.vagons = []
        self.no_vagons_rows = []
        self.process()

    def process(self):
        for row in self.text.split('\n'):
            row = row.strip()
            vagon = Vagon(row)
            if vagon.id:
                self.vagons.append(vagon)
            else:
                self.no_vagons_rows.append(row)

    def get_no_vagon_rows(self) -> str:
        return '\n'.join(self.no_vagons_rows)

    def get_vagons_ids(self) -> set:
        """Получить все айди вагонов"""
        return set(vagon.id for vagon in self.vagons)

    def get_vagons_by_ids(self, ids):
        """отфильтровать вагоны по айди"""
        return filter(lambda vagon: vagon.id in ids, self.vagons)

    def sort_vagons(self, vagons: list) -> list:
        return sorted(vagons, key=lambda vagon: (vagon.id[:4], vagon.id[4:]))

    def rus_vagons(self):
        return list(filter(lambda vagon: vagon.is_has_ru_letters(), self.vagons))

    def __sub__(self, instance):
        unigue_ids = self.get_vagons_ids() - instance.get_vagons_ids()
        unique_vagons = list(self.get_vagons_by_ids(unigue_ids))
        return list(self.sort_vagons(unique_vagons))

    def __and__(self, instance):
        jeneral_ids = self.get_vagons_ids() & instance.get_vagons_ids()
        jeneral_vagons = list(self.get_vagons_by_ids(jeneral_ids))
        return list(self.sort_vagons(jeneral_vagons))
