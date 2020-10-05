from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
	# template routes
  path('app/cgate/admin/', login_required(TemplateView.as_view(template_name='cc_cgate/admin.html'))),

  path('api/cgate/test1/', Test1.as_view()),
  path('api/cgate/test2/', Test2.as_view()),
  path('api/cgate/test3/', Test3.as_view()),
]
