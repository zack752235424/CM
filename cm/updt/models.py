from django.db import models

# Create your models here.


class CarInfo(models.Model):
    """
    车辆总信息表
    """
    VIN = models.CharField(max_length=32, null=False, verbose_name='VIN号')
    ICCID = models.CharField(max_length=32, null=True, verbose_name='ICCID号')
    car_num = models.CharField(max_length=16, null=True, verbose_name='车牌号')
    latitude = models.CharField(max_length=32, null=True, verbose_name='纬度')
    longitude = models.CharField(max_length=32, null=True, verbose_name='经度')
    now_location = models.CharField(max_length=128, null=True, verbose_name='当前车辆位置')
    version = models.CharField(max_length=32, null=True, verbose_name='终端编号')
    create_time = models.DateTimeField(null=True, verbose_name='数据上传时间')

    class Meta:
        db_table = 'car_info'
