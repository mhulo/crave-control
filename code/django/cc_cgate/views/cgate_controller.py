
# most imports are imported in common.classes
from common.classes import *
from cc_cgate.classes import *
from django.views import View

# Create your views (aka controllers) here.
# Standard classnames and related routes are..
# .........
# QuoteList .. /api/quotes
# QuoteShow (single model) .. /api/quotes/53/
# QuoteShowFull (nested) .. /api/quotes/53/full/
# QuoteCreate .. /api/quotes/create
# QuoteUpdate .. /api/quotes/43/update/
# QuoteDelete .. /api/quotes/43/delete/


class Test1(View):
  def get(self, request):

    #cache.set('key1', 'val1')

    #ret_str = 'key set'
    ret_str = { 'key' : 'set' }

    return JsonResponse(ret_str, safe=False)
    #return HttpResponse(ret_str)


class Test2(View):
  def get(self, request):

    ret_str = cache.get('key1')

    return HttpResponse(ret_str)


class Test3(View):
  def get(self, request):

    #cmd = 'noop'
    cmd = 'get //NET1/254/56/* level'

    resp_text = Cgate().CommandSend(cmd)
    resp_json = Cgate().CgateToJson(resp_text)

    #return HttpResponse(resp)
    return JsonResponse(resp_json, safe=False)

