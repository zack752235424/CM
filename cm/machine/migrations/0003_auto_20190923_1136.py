# Generated by Django 2.0.4 on 2019-09-23 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machine', '0002_machinefile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinefile',
            name='file_name',
            field=models.FileField(upload_to='machine', verbose_name='保存文件路径'),
        ),
    ]
