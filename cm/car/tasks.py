from __future__ import absolute_import

from celery import task

from celery import shared_task



# from celery.task import tasks
# from celery.task import Task
from car.models import Task
from django_redis import get_redis_connection

@task()
# @shared_task
def add(x, y):
    print('123456')
    "%d + %d = %d" % (x, y, x + y)
    return x + y


# class AddClass(Task):
#  def run(x,y):
#    print "%d + %d = %d"%(x,y,x+y)
#    return x+y
# tasks.register(AddClass)


@shared_task
def get_data():
    print('123')
    r = get_redis_connection('default')
    data = {'car_online': [], 'car_offline': [], 'car_warning': []}
    car_online = r.zrange('car_online', 0, -1)
    if car_online:
        for item in car_online:
            car = r.geopos('car_online', item.decode('utf-8'))
            data['car_online'].append(
                Task(
                    VIN=item.decode('utf-8'),
                    longitude=car[0][0],
                    latitude=car[0][1],
                    type='car_online'
                )
            )
        Task.objects.bulk_create(data['car_online'])
    car_offline = r.zrange('car_offline', 0, -1)
    if car_offline:
        for item in car_offline:
            cars = r.geopos('car_offline', item.decode('utf-8'))
            data['car_offline'].append(
                Task(
                    VIN=item.decode('utf-8'),
                    longitude=cars[0][0],
                    latitude=cars[0][1],
                    type='car_offline'
                )
            )
        Task.objects.bulk_create(data['car_offline'])
    car_warning = r.zrange('car_warning', 0, -1)
    if car_warning:
        for item in car_warning:
            cars = r.geopos('car_warning', item.decode('utf-8'))
            data['car_warning'].append(
                Task(
                    VIN=item.decode('utf-8'),
                    longitude=cars[0][0],
                    latitude=cars[0][1],
                    type='car_warning'
                )
            )
        Task.objects.bulk_create(data['car_warning'])
    print('操作成功')
