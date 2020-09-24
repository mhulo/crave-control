from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
  #path('vue/1/', TemplateView.as_view(template_name='vue/1.html')),
  #path('vue/1/', Vue1.as_view()),
  #path('vue/2/', Vue2.as_view()),
 
  path('app/mssql/', MsSql.as_view()),
  path('vue/', VueIndex.as_view()),
  path('vue/2/', Vue2.as_view()),
  path('vue/3/', Vue3.as_view()),
]
