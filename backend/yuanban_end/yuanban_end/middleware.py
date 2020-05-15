from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.views.generic.base import RedirectView
import json
from django.http import JsonResponse
from backendusers.common import Common


class LoginMiddleware(MiddlewareMixin, Common):
    def process_request(self, request):
        url = request.path.split('/')
        print(url)
        if len(url) > 2 and ('teacher' in url) and ('userlogin' not in url):
            login = request.session.get('login')
            if not login:
                # return HttpResponseRedirect(reverse('user:login'))
                return JsonResponse(self.msg(20000, remsg='请先登录'))
            else:
                request.useruuid = login
        # elif url[1] == "user":
        #     agent = request.session.get('agent')
        #     if not agent:
        #         return HttpResponseRedirect(reverse('login'))
        #     else:
        #         try:
        #             User_ext.objects.get(uuid=agent, del_state=1)
        #         except:
        #             return HttpResponseRedirect(reverse('login'))
        #         else:
        #             request.adminuuid = agent
        if request.method == "POST":
            body = request.body
            if isinstance(body, bytes):
                body = str(body, encoding='utf-8')
            request.POST = json.loads(body)
