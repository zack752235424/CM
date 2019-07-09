from django.db import models

# Create your models here.


class Car(models.Model):
    """
    车辆表
    """
    VIN = models.CharField(max_length=32, verbose_name='VIN号')

    class Meta:
        db_table = 'car'


class CarOnline(models.Model):
    """
    车辆在线表
    """
    VIN = models.CharField(max_length=32, verbose_name='VIN号')
    latitude = models.CharField(max_length=32, verbose_name='纬度')
    longitude = models.CharField(max_length=32, verbose_name='经度')

    class Meta:
        db_table = 'car_online'


class CarOffline(models.Model):
    """
    车辆离线表
    """
    VIN = models.CharField(max_length=32, verbose_name='VIN号')
    latitude = models.CharField(max_length=32, verbose_name='纬度')
    longitude = models.CharField(max_length=32, verbose_name='经度')

    class Meta:
        db_table = 'car_offline'


class CarInfo(models.Model):
    """
    车辆总信息表
    """
    ICCID = models.CharField(null=True, max_length=32, verbose_name='ICCID号')
    VIN = models.CharField(max_length=32, verbose_name='VIN号')
    status = models.BooleanField(default=0, verbose_name='车辆状态,默认离线')
    car_num = models.CharField(null=True, max_length=16, verbose_name='车牌号')
    location = models.CharField(null=True, max_length=64, verbose_name='GPS定位')
    now_location = models.CharField(null=True, max_length=128, verbose_name='当前车辆位置')
    terminal_num = models.CharField(null=True, max_length=32, verbose_name='终端编号')
    create_time = models.DateTimeField(null=True, verbose_name='数据上传时间')

    class Meta:
        db_table = 'car_info'
