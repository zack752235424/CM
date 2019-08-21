from django.db import models

# Create your models here.
from car.models import Car


class Can(models.Model):
    """
    CAN数据表
    1: 车辆登入报文
    2：实时信息报文
    3：补发信息报文
    4:车辆登出报文
    80:车辆升级报文
    1001: 信息上报错误
    1002： BCC校验失败
    1003： 车辆登录失败
    """
    create_time = models.DateTimeField(auto_now=True, null=True, verbose_name='服务器添加数据时间')
    ter_time = models.DateTimeField(null=True, verbose_name='终端发送时间')
    data = models.CharField(max_length=1024, null=False, verbose_name='报文数据')
    type = models.IntegerField(default=0, null=False, verbose_name='数据类型')
    car = models.ForeignKey(to="car.Car", on_delete=models.CASCADE, to_field="id", verbose_name='对应车辆')
    spare_1 = models.CharField(max_length=128, null=True, verbose_name='备用1')
    spare_2 = models.CharField(max_length=128, null=True, verbose_name='备用2')

    class Meta:
        db_table = 'can'
