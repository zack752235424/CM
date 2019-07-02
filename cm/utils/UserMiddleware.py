from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin



class UserAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 登录和注册不需要做登录校验，因此直接过滤掉请求url

        if request.path == '/user/login/':
            return None
        if 'user_id' in request.session:
            # 表示不运行以下的所有代码，直接去访问路由文件，并执行视图函数

            sdf = 1
            sadf =2

            return None
        return HttpResponseRedirect(reverse('user:login'))
