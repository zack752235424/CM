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
    spare_1 = models.CharField(max_length=128, null=True, verbose_name='备用1')
    spare_2 = models.CharField(max_length=128, null=True, verbose_name='备用2')

    class Meta:
        db_table = 'back'
        index_together = [
            'VIN',
            'create_time'
        ]
