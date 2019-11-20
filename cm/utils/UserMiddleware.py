from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

from user.models import User


class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.path == '/user/login/':
            return None
        if 'user_id' in request.session:
            if (request.path,) in User.objects.get(pk=request.session.get('user_id')).roles.first().permissions.values_list('url').all():
                return None
            else:
                return render(request, 'error.html')
        return HttpResponseRedirect(reverse('user:login'))
