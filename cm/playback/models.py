from django.db import models

# Create your models here.


class Back(models.Model):
    """
    轨迹回放表
    """
    VIN = models.CharField(max_length=32, null=False, verbose_name='VIN号')
    longitude = models.CharField(max_length=32, null=False, verbose_name='经度')
    latitude = models.CharField(max_length=32, null=False, verbose_name='纬度')
    create_time = models.DateTimeField(null=False, verbose_name='添加数据时间')

    class Meta:
        db_table = 'back'
