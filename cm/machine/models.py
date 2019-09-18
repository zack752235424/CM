from django.db import models

# Create your models here.


class Machine(models.Model):
    ICCID = models.CharField(max_length=32, null=True, verbose_name='ICCID号')
    product_num = models.CharField(max_length=32, null=True, verbose_name='货号')
    serial_num = models.CharField(max_length=32, null=True, verbose_name='流水号')
    birthday = models.CharField(max_length=32, null=True, verbose_name='出厂日期')
    dept = models.CharField(max_length=16, null=True, verbose_name='部门')
    create_time = models.DateTimeField(auto_now=True, null=True, verbose_name='添加数据时间')
    spare_1 = models.CharField(max_length=128, null=True, verbose_name='备用1')
    spare_2 = models.CharField(max_length=128, null=True, verbose_name='备用2')

    class Meta:
        db_table = 'machine'


class MachineFile(models.Model):
    """
    导入设备表
    """
    file_name = models.FileField(upload_to='car', verbose_name="保存文件路径")  # 指定文件保存的路径名

    class Meta:
        db_table = 'machine_file'
