
# most imports are imported in common.classes
from common.classes import *
from cc_cgate.classes import *
from cc_cgate.models import *
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


class Test(View):
    def get(self, request):
      ret_str = FooBar().AddBar('xxx')
      return HttpResponse(ret_str)

