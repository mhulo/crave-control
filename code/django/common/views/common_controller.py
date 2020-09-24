
# most imports are imported in common.classes
from common.classes import *
from django.shortcuts import render
from django.views import View

# Create your views here.

class MsSql(View):
  def get(self, request):

    qry = 'SELECT TOP 20 * FROM dbo.bw_log_MTPartnerNBN ORDER BY LogDate DESC;'

    cursor = crisp_curs()
    res = cursor.execute(qry)
    ret_val = list_cur(res)

    return JsonResponse(ret_val, safe=False)


class VueIndex(View):
  def get(self, request):

    return render(request, 'vue/index.html', None)


class Vue2(View):
  def get(self, request):

    return render(request, 'vue/2.html', None)


class Vue3(View):
  def get(self, request):

    return render(request, 'vue/3.html', None)


class Vue2(View):
  def get(self, request):

    names = ('bob', 'dan', 'jack','lizzy', 'susan')

    items = []
    for i in range(100):
      items.append({
        'name': random.choice(names),
        'age': random.randint(20,80),
        'url': 'https://example.com',
      })

    context = {}
    context['items'] = json.dumps(items)

    return render(request, 'vue/2.html', context)


class Vue1(View):
  def get(self, request):

    names = ('bob', 'dan', 'jack','lizzy', 'susan')

    items = []
    for i in range(100):
      items.append({
        'name': random.choice(names),
        'age': random.randint(20,80),
        'url': 'https://example.com',
      })

    context = {}
    context['items'] = items

    #return render(request, 'vue/1.html', context=context)
    return render(request, 'vue/1.html', context)


