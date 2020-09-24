
# most imports are imported in common.classes
from common.classes import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import time
from time import mktime, time
from django.views import View

# Create your views here.

class UserLogin(View):
  def post(self, request):
    username = request.POST['username']
    password = request.POST['password']

    username = (username.split('@'))[0]

    user = authenticate(request, username=username, password=password)
    if user is not None:
      if (user.is_active is True):
        login(request, user)
        data = { 'message': 'login success' }
    else:
      data = { 'message': 'login failed. account may be locked.' }

    return JsonResponse(data, safe=False)


class UserLogout(View):
  def post(self, request):
    logout(request)
    data = { 'message': 'logged out'}
    return JsonResponse(data, safe=False)


class UserCreate(View):
  def post(self, request):

    username = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    password_2 = request.POST['password_2']

    if (password == password_2):
      try:
        user = User.objects.get(username=username)
        data = { 'message': 'user already exists' }
      except:
        user = User.objects.create_user(username, email, password)
        user.is_active = False
        user.save()
        data = { 'message': 'registration success' }
    else:
      data = { 'message': 'passwords don\'t match' }

    return JsonResponse(data, safe=False)


