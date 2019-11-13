import xlrd

from car.models import Car
from cm.settings import MEDIA_ROOT


class ExcelUpdate:
    def __init__(self, file_name):

        self.file_name = (MEDIA_ROOT + 'car/' + str(file_name))
        self.workbook = xlrd.open_workbook(self.file_name)
        self.table = self.workbook.sheets()[0]
        self.nrows = self.table.nrows
        self.cases = []

    def update_cases(self):
        old_cars = Car.objects.all()
        cars = [item.VIN for item in old_cars]
        for x in range(1, self.nrows):
            row = self.table.row_values(x)
            if row[1] in cars and row[1]:
                Car.objects.filter(VIN=row[1]).update(dept=row[4])
