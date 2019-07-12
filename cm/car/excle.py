import xlrd

from car.models import Car
from cm.settings import MEDIA_ROOT


class ExcelImport:
    def __init__(self, file_name):
        # self.file_name = unicode(file_name, "utf-8")
        # 文件路径修改
        self.file_name = (MEDIA_ROOT + 'car/' + str(file_name))
        # print self.file_name
        self.workbook = xlrd.open_workbook(self.file_name)
        self.table = self.workbook.sheets()[0]
        # 获取总行数
        self.nrows = self.table.nrows
        self.cases = []

    def get_cases(self):
        # 从第二行开始
        cars = [item.VIN for item in Car.objects.all()]
        for x in range(1, self.nrows):
            row = self.table.row_values(x)
            if row[1] not in cars and row[1]:
                self.cases.append(
                    Car(
                        car_num=row[0],
                        VIN=row[1],
                        ICCID=row[2],
                        driver=row[3],
                        dept=row[4]
                    )
                )
