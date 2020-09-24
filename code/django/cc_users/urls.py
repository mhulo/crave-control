from django.urls import path
from django.views.generic import TemplateView

from . import views
from cc_users.views import *

urlpatterns = [
  # template routes
  path('app/login/', TemplateView.as_view(template_name='cc_users/index.html'), name='login'),

  # api routes
  path('api/users/login/', UserLogin.as_view()),
  path('api/users/logout/', UserLogout.as_view()),
  path('api/users/register/', UserCreate.as_view()),
]
