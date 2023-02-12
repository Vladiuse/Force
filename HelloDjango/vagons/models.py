import re
from django.db import models
from django.utils import timezone
from .containers import Container, ClientContainer
from datetime import datetime
from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class ClientDoc(models.Model):
    QUERY = """
    SELECT client_name, COUNT(*)as count , 
    ROUND(AVG(DATEDIFF(NOW(), date))) as past,
    CASE
        WHEN COUNT(*) > 1 THEN MAX( DATEDIFF(NOW(), date))
        ELSE '-'
    END as max,
    CASE
        WHEN COUNT(*) > 1 THEN MIN( DATEDIFF(NOW(), date))
        ELSE '-'
    END as min
    FROM vagons_clientcontainerrow
    GROUP BY client_name ORDER BY past DESC;
    """
    name = models.CharField(max_length=40, verbose_name='Имя документа', default='No name')
    document = models.TextField(verbose_name='Текст документа')
    load_date = models.DateField(default=timezone.now, editable=False)
    document_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, default='Нет описания')

    class Meta:
        ordering = ['-document_date', '-pk']

    def save(self, **kwargs):
        print('Self PK', self.pk)
        if self.pk:
            super().save()
            print('Save')
        else:
            super().save()
            self.read_doc()
            print('Save n read')


    def read_doc(self):
        self.find_n_save_rows()
        self.get_doc_date()

    def find_n_save_rows(self):
        rows = []
        for line in str(self.document).split('\n'):
            cont = Container.find_container_number(line)
            date = re.search(r'\d\d\.\d\d.\d{4}', line)
            client_name = ClientContainer.get_client_name_from_row(line)
            if cont and date:
                date = datetime.strptime(date.group(0), '%d.%m.%Y').date()
                row = ClientContainerRow(document=self,container=cont,client_name=client_name,date=date)
                rows.append(row)
        print('END')
        ClientContainerRow.objects.bulk_create(rows)

    def get_doc_date(self):
        pass

    def document_text_rows(self):
        return str(self.document).split('\n')

    def client_count(self):
        with connection.cursor() as cursor:
            cursor.execute(self.QUERY)
            # rows = cursor.fetchall()
            rows = dictfetchall(cursor)
        return rows




class ClientContainerRow(models.Model):
    document = models.ForeignKey(ClientDoc, on_delete=models.CASCADE, related_query_name='row', related_name='rows')
    container = models.CharField(max_length=11, )
    client_name = models.CharField(max_length=30)
    date = models.DateField()

    def __str__(self):
        return f'{self.client_name}{self.container}'

