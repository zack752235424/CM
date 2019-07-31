import base64
import requests


def translate(longitude,latitude):
    """
    经纬度转换
    :param longitude: 经度
    :param latitude: 纬度
    :return:
    """
    url = 'http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x=%f&y=%f' % (longitude, latitude)
    response = requests.get(url)
    data = response.json()
    longitude = data['x']
    latitude = data['y']
    res = base64.b64decode(longitude)
    longitude = res.decode()
    res = base64.b64decode(latitude)
    latitude = res.decode()
    return (longitude, latitude)
