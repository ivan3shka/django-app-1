import csv
from xml.dom.xmlbuilder import Options

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse



class ExportAsCSVMixins:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta
        field_names = [field for field in meta.fields]

        response = HttpResponse(content='text/csv')
        response['Content-Disposition'] = (f'attachment;'
                                           f' filename = {meta}-export.csv')

        csv_writer = csv.writer(response)

        csv_writer.writerow(field_names)

        for obj in queryset:
            csv_writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_csv.short_description = 'Export as CSV'
