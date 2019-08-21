from django.db import models

# Create your models here.


class CarUpdate(models.Model):
    """
    远程升级日志表
    """
    VIN = models.CharField(max_length=1024, null=True, verbose_name='VIN号')
    ICCID = models.CharField(max_length=1024, null=True, verbose_name='ICCID号')
    version = models.CharField(max_length=32, null=True, verbose_name='版本号')
    ip = models.CharField(max_length=512, null=True, verbose_name='升级文件传输地址')
    ftp = models.CharField(max_length=32, null=True, verbose_name='用户名')
    pwd = models.CharField(max_length=32, null=True, verbose_name='密码')
    create_time = models.DateTimeField(auto_now=True, null=True, verbose_name='添加数据时间')
    spare_1 = models.CharField(max_length=128, null=True, verbose_name='备用1')
    spare_2 = models.CharField(max_length=128, null=True, verbose_name='备用2')

    class Meta:
        db_table = 'car_update'
