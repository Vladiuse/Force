import re

class VagReader:

    def __init__(self, text):
        self.text = text
        self.vagons_rows = []
        self.no_wagons_rows = []

    def process(self):
        for row in self.text.split('\n'):
            row = row.strip()
            vagon = re.search('\D{4}\s*\d{7}', row)
            if vagon:
                vagon_data = [row, vagon.group(0)]
                self.vagons_rows.append(vagon_data)
            else:
                self.no_wagons_rows.append(row)

    def get_vagon_rows(self):
        vagons_rows = [vag_data[0] for vag_data in self.vagons_rows]
        return '\n'.join(vagons_rows)

    def get_no_vagon_rows(self):
        return '\n'.join(self.no_wagons_rows)

    def __sub__(self, instance):
        s1 = set([vag_row[1] for vag_row in self.vagons_rows])
        s2 = set([vag_row[1] for vag_row in instance.vagons_rows])
        unigue = s1 - s2
        unigue_rows = filter(lambda vag_row: vag_row[1] in unigue, self.vagons_rows)
        unigue_rows = [vag_row[0]+'\n' for vag_row in unigue_rows]
        return unigue_rows
        # return '\n'.join(unigue_rows)

    def __and__(self, instance):
        s1 = set([vag_row[1] for vag_row in self.vagons_rows])
        s2 = set([vag_row[1] for vag_row in instance.vagons_rows])
        jeneral = s1 & s2
        jeneral_rows = filter(lambda vag_row: vag_row[1] in jeneral, self.vagons_rows)
        jeneral_rows = [vag_row[0]+'\n' for vag_row in jeneral_rows]
        return jeneral_rows
        # return '\n'.join(jeneral_rows)



#
# s = 'ass AA1AA1234556 dsda '
# res = re.search('\D{4}\s*\d{7}', s)
# print(res)
# print(res.group(0))