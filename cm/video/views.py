from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from playback.models import Back


def index(request):
    return render(request, 'video.html')


def get_data(request):
    VIN = 'LDP52A965JN427533'
    opts = Back.objects.filter(VIN=VIN).first()
    result = {'VIN': 'LDP52A965JN427533', 'longitude': opts.longitude, 'latitude': opts.latitude}
    return JsonResponse(result)
