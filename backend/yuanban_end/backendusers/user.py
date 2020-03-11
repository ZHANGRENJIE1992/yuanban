from .userbase import BaseUser
import random
from .models import User as Admin_ext
from django.http import Http404


class User(BaseUser):
    def __init__(self, **kwargs):
        uuid = kwargs.get('uuid')
        if uuid:
            try:
                self.admin = Admin_ext.objects.get(uuid=uuid, del_state=1)
            except:
                raise Http404

    def login(self, request, cellphone, password):
        currentAuthority = 'guest'
        status = 'error'
        if cellphone and password:
            try:
                admin = Admin_ext.objects.get(cellphone=cellphone, del_state=1)
                assert self.check_password(password, admin.password)
            except:
                return self.msg(20000, remsg='用户名或密码错误')
            else:
                request.session['login'] = admin.uuid
                status= 'ok'
                if admin.system_role == 1:
                    currentAuthority = 'admin'
                elif admin.system_role == 0:
                    currentAuthority = 'user'
                return self.msg(10000, remsg='登陆成功', currentAuthority=currentAuthority, status=status)
        return self.msg(20000, currentAuthority=currentAuthority, status=status)

    def make_password(self, password):
        '''加密'''
        salt = self.uid(5)
        print(444555, password)
        return self.encode(
            password, salt, iterations=random.randint(10000, 99999))

    def check_password(self, password, encoded):
        '''验证密码'''
        return self.verify(password, encoded)

    def myInfoEdit(self, field):
        try:
            assert field.get("realname")
            assert self.update(self.admin, field)
        except:
            return self.msg(0, "1005")
        else:
            return self.msg(1, "1004")

    def myPwd(self, oldpwd, newpwd):
        try:
            assert oldpwd and newpwd
            if self.check_password(oldpwd, self.admin.password):
                self.admin.password = self.make_password(newpwd)
                self.admin.save()
            else:
                return self.msg(0, '1012')
        except:
            return self.msg(0, '1005')
        else:
            return self.msg(1, '1004')
