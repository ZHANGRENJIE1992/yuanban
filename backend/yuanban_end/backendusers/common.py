import re
import pytz
from datetime import datetime, date
from djtool.msgcode import tips
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.timezone import utc
from django.utils import timezone
import importlib
import shortuuid
import xlwt


class Common:


    @classmethod
    def msg(cls, code, data=None, **kwargs):
        result = {}
        result['code'] = int(code)
        print(type(kwargs))
        result['msg'] = '' if 'remsg' not in kwargs else kwargs.get('remsg', '')
        if kwargs.get('remsg'):
          del kwargs['remsg']
        if data is not None:
            result['data'] = data
        result.update(kwargs)
        return result

    @classmethod
    def mobile(cls, no):
        if isinstance(no, int):
            no = str(no)
        if isinstance(no, str):
            no = no.strip()
            pattern = re.compile(
                '^(0|86|17951)?(13[0-9]|15[012356789]|18[0-9]|14[57]|17[0-9])[0-9]{8}$'
            )
            if pattern.match(no):
                return pattern.match(no).group()
            return None
        return None

    @classmethod
    def email(cls, email):
        if isinstance(email, str):
            email = email.strip()
            pattern = re.compile(
                '^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$'
            )
            if pattern.match(email):
                return pattern.match(email).group()
            return None
        return None

    @classmethod
    def add_set(cls, a, b):
        if isinstance(a, list) and isinstance(b, list):
            return list(set(a) - set(b))
        return None

    @classmethod
    def del_set(cls, a, b):
        if isinstance(a, list) and isinstance(b, list):
            return list(set(b) - set(a))
        return None

    @classmethod
    def list_toInt(cls, a):
        b = []
        for i in a:
            if isinstance(i, int):
                b.append(i)
            else:
                b.append(int(i))
        return b

    @classmethod
    def page(cls, res, pg, **kwargs):
        paginator = Paginator(res, kwargs.get('pre', 10))
        try:
            page = paginator.page(pg)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page

    @classmethod
    def uuid(cls, length=1):
        uuid = ''
        for i in range(0, length):
            uuid += shortuuid.uuid()
        return uuid

    @classmethod
    def uid(cls, length=32):
        baselen = len(shortuuid.uuid())
        mod = divmod(length, baselen)
        return '{}{}'.format(cls.uuid(mod[0]), shortuuid.uuid()[0:mod[1]])

    @classmethod
    def utcToLocal(cls, t):
        return t.replace(
            tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))

    @classmethod
    def localToUtc(cls, str):
        tz = pytz.timezone('Asia/Shanghai')
        a = tz.localize(datetime.strptime(str, '%Y-%m-%d %H:%M:%S')).astimezone(pytz.utc)
        return a

    @classmethod
    def localUtc(cls):
        return timezone.now().replace(tzinfo=utc)

    @classmethod
    def ID(cls, pg, i, **kwargs):
        return (int(pg) - 1) * kwargs.get('pre', 10) + i

    @classmethod
    def ID_desc(cls, total, pg, i, **kwargs):
        return total - ((int(pg) - 1) * kwargs.get('pre', 10) + i) + 1

    @classmethod
    def year(cls, front=0, back=0, text=''):
        year = datetime.today().year
        l = [(y, '%s%s' % (y, text)) for y in range(year-front, year+back)]
        return tuple(l)

    @classmethod
    def expire(cls, d):
        today = date.today()
        if (d - today).days >= 0:
            return False
        return True

    @classmethod
    def import_model(cls, config):
        s = config.split('.')
        j = '.'.join(s[:-1])
        return getattr(importlib.import_module(j), s[-1])

    @classmethod
    def book_number(cls):
      return datetime.now().strftime("%Y%m%d") + shortuuid.uuid()


    @classmethod
    def date(cls, tp="-"):
        return datetime.now().strftime("%Y{}%m{}%d".format(tp, tp))


class Excel:
    def createExcel(self, title, data):
        wb = xlwt.Workbook()
        ws = wb.add_sheet('mysheet')
        n = 0
        for t in title:
            ws.write(0, n, t)
            n += 1
        i = 1
        for row in data:
            j = 0
            for val in row:
                ws.write(i, j, val)
                j += 1
            i += 1
        return wb

