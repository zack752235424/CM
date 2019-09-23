import xlrd

from machine.models import Machine
from cm.settings import MEDIA_ROOT


class ExcelImport:
    def __init__(self, file_name):
        self.file_name = (MEDIA_ROOT + 'machine/' + str(file_name))
        self.workbook = xlrd.open_workbook(self.file_name)
        self.table = self.workbook.sheets()[0]
        self.nrows = self.table.nrows
        self.cases = []

    def get_cases(self):
        old_machines = Machine.objects.all()
        machines = [item.ICCID for item in old_machines]
        for x in range(1, self.nrows):
            row = self.table.row_values(x)
            if row[1] not in machines and row[1]:
                self.cases.append(
                    Machine(
                        ICCID=row[0],
                        product_num=row[1],
                        serial_num=row[2],
                        birthday=row[3],
                        dept=row[4]
                    )
                )
