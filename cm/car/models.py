from django.db import models

# Create your models here.


class Car(models.Model):
    """
    车辆表
    """
    VIN = models.CharField(max_length=32, null=False, unique=True, verbose_name='VIN号')
    car_num = models.CharField(max_length=16, null=True, verbose_name='车牌号')
    ICCID = models.CharField(max_length=32, null=True, verbose_name='ICCID号')
    driver = models.CharField(max_length=8, null=True, verbose_name='司机')
    dept = models.CharField(max_length=16, null=True, verbose_name='部门')

    class Meta:
        db_table = 'car'


class CaseFile(models.Model):
    """
    导入车辆表
    """
    file_name = models.FileField(upload_to='car', verbose_name="保存文件路径")  # 指定文件保存的路径名

    class Meta:
        db_table = 'case_file'
