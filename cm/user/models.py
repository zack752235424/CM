from django.db import models


class User(models.Model):
    """
    用户表
    0：默认未删除
    """
    username = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    pwd = models.CharField(max_length=32, verbose_name='密码')
    phone = models.IntegerField(null=True, unique=True, verbose_name='用户手机号码')
    is_delete = models.BooleanField(default=0, null=False, verbose_name='是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='自动创建当前保存的时间')
    roles = models.ManyToManyField(to="Role", verbose_name='角色')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username


class Role(models.Model):
    """
    角色表
    """
    rolename = models.CharField(max_length=32, verbose_name='角色名')
    permissions = models.ManyToManyField(to="Permission", verbose_name='角色权限')

    class Meta:
        db_table = 'role'

    def __str__(self):
        return self.rolename


class Permission(models.Model):
    """
    权限表
    """
    url = models.CharField(max_length=64, verbose_name='路由')
    title = models.CharField(max_length=32, verbose_name='路由名称')

    class Meta:
        db_table = 'permission'

    def __str__(self):
        return self.title
