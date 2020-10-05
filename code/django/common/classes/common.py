
import json
import datetime
import MySQLdb
import re
import requests
import copy
import hashlib
import base64
import sys
import random
import telnetlib
import logging

from django.core.cache import cache
from django.db import connection
from django.db import connections
from django.db.models import OuterRef, Subquery, Count
from django.db.models.functions import Lower, Substr
from django.apps import apps
from django.shortcuts import render
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader

from time import gmtime, strftime, sleep, mktime, time
from typing import Dict, List, Union, Iterable
from pprint import pprint
from operator import itemgetter
from requests.auth import HTTPBasicAuth
from calendar import monthrange


def crisp_curs():

  return connections['crpt'].cursor()
      
      
def crisp_proxies():
  
  #p = { 'https': '192.168.88.230:8080'}
  p = {}
  return p


def cust_format(o):
  if isinstance(o, (datetime.date, datetime.datetime)):
    ret_val = o.strftime('%Y-%m-%d %H:%M:%S')
  else :
    ret_val = o
  return ret_val


def list_raw(raw_qs):
  cols = raw_qs.columns
  res = []
  for row in raw_qs:
    #rec = {}
    #for col in cols:
    #  rec[col] = getattr(row, col)
    #res.append(rec)
    res.append(dict([col,getattr(row, col)] for col in cols))

  return res


def list_cur(cursor):
    # return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def table_to_model(db_table):

  ret_val = None

  from django.apps import apps
  for model in apps.get_models():
      if model._meta.db_table == db_table:
          ret_val =  model

  return ret_val


class FooBar:

    def __init__ (self):
        self.f = 'foo'
        self.x = 'BAR'

    def DoFoo(self):
        return 'foo'

    def DoBar(self):
        return self.f + ' ' + self.DoFoo() + ' Bar'

    def AddBar(self, y):
        return self.f + self.x + y


def hit_curl(curl_url, post_data=None):

  if post_data == None:
    resp = requests.get(curl_url, verify=False)
  else:
    post_data = post_data.encode('utf-8')
    headers = { 'Content-Type': 'application/json' }
    resp = requests.post(curl_url, data=post_data, headers=headers, verify=False)

  #resp = requests.get(url).json()
  #resp = 'hello'
  return resp   


def url_decode(url):

  s = url.replace('__', '/')

  return s


def to_md5(raw_str, length=16):

  s = hashlib.md5(raw_str.encode('UTF-8'))
  s = str(base64.b32encode(s.digest()))
  s = s.replace("'", "")
  s = s.replace("=", "")
  s = s[1:length]

  return s


def not_blank(val):
  if ((val == None) or (val == '')):
    ret_val = False
  else:
    ret_val = True

  return ret_val


# classes / functions for camelCaseKeys

CAMEL_CASE = 'camel'
SNAKE_CASE = 'snake'

def _unpack(data) -> Iterable:
    if isinstance(data, dict):
        return data.items()
    return data


def to_snake_case(value: str) -> str:
    """
    Convert camel case string to snake case
    :param value: string
    :return: string
    """
    first_underscore = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', first_underscore).lower()


def to_camel_case(value: str) -> str:
    """
    Convert the given string to camel case
    :param value: string
    :return: string
    """
    content = value.split('_')
    return content[0] + ''.join(word.title() for word in content[1:] if not word.isspace())


def case_keys(data: Union[Dict, List]=None, types=SNAKE_CASE, do_more=True) -> Union[Dict, List]:
    """
    Convert all keys for given dict/list to snake case recursively
    the main type are 'snake' and 'camel'
    :param data: dict | list
    :return: dict | list
    """
    if types not in (SNAKE_CASE, CAMEL_CASE):
        raise ValueError("Invalid parse type, use snake or camel")
    
    if not isinstance(data, (list, dict)):
        raise TypeError("Invalid data type, use list or dict")

    formatter = to_snake_case if types == 'snake' else to_camel_case
    formatted = type(data)()
    stop_at = ['results', 'traceData', 'sourceDetails']
    is_dict = lambda x: type(x) == dict
    is_list = lambda x: type(x) == list

    for key, value in _unpack(data):

        if is_dict(value):
          if do_more == False:
            formatted[key] = case_keys(value, types, False)
          elif key in stop_at:
            formatted[formatter(key)] = case_keys(value, types, False)
          else :
            formatted[formatter(key)] = case_keys(value, types, do_more)

        elif is_list(value) and len(value) > 0:
          if do_more == False:
            fkey = key
            do_more = False
          elif key in stop_at:
            fkey = formatter(key)
            fkey = key
            do_more = False
          else:
            fkey = formatter(key)
          formatted[fkey] = []
          for val in value:
              if isinstance(val, (list, dict)):
                  val = case_keys(val, types, do_more)
              formatted[fkey].append(val)

        else:
          if do_more == False:
            formatted[key] = cust_format(value)
          else:
            formatted[formatter(key)] = cust_format(value)

    return formatted


def case_obj(data: Union[Dict, List] = None, types=SNAKE_CASE, do_more=True) -> Union[Dict, List]:
    """
    Convert all keys for given dict/list to snake case recursively
    the main type are 'snake' and 'camel'
    :param data: dict | list
    :return: dict | list
    """
    is_dict = lambda x: type(x) == dict
    is_list = lambda x: type(x) == list

    if is_dict(data):
      formatted_obj = case_keys(data, types)
    elif is_list(data) and len(data) > 0:
      formatted_obj = []
      for val in data:
        formatted_obj.append(case_keys(val, types))

    return formatted_obj


def merge(a, b, path=None):
    #merges b into a by mutating a
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                #raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def nu(a):
  x = copy.deepcopy(a)
  return x


def merge_new(a, b):
    #merges b into a without mutation
    x = copy.deepcopy(a)
    y = copy.deepcopy(b)
    merge(x, y)
    return x


def replace_last(s, old, new, num_occurrences):

  li = s.rsplit(old, num_occurrences)
  return new.join(li)


def replace_last_edges(s, old, new, edges):

  # replaces last occurence of old with new
  # when surrounded by specific chars (edges) on either side
  # will stop when the replace count reaches 1

  r_count = 0
  if old in s:
    for v1 in edges:
      for v2 in edges:
        if (r_count < 1):
          li = s.rsplit(v1+old+v2, 1)
          if (len(li) > 1):
            new2 = v1+new+v2
            s = new2.join(li)
            r_count += 1

  return s


def replace_first_edges(s, old, new, edges):

  # replaces last occurence of old with new
  # when surrounded by specific chars (edges) on either side
  # will stop when the replace count reaches 1

  r_count = 0
  if old in s:
    for v1 in edges:
      for v2 in edges:
        if (r_count < 1):
          li = s.split(v1+old+v2, 1)
          if (len(li) > 1):
            new2 = v1+new+v2
            s = new2.join(li)
            r_count += 1

  return s


def replace_all_edges(s, old, new, edges):

  # replaces all occurences of old with new
  # when surrounded by specific chars (edges) on either side
  
  if old in s:
    for v1 in edges:
      for v2 in edges:
        #li = s.split(v1+old+v2)
        #if (len(li) > 1):
        #  new2 = v1+new+v2
        #  s = new2.join(li)
        s = s.replace(v1+old+v2, v1+new+v2)

  return s


def get_digits(s):

  ret_val = ''
  for c in list(s):
    if ((c.isdigit()) or (c == '-')) :
      ret_val += c

  return ret_val


def digits_str(s):

  ret_val = ''
  for c in list(s):
    if (c.isdigit()) :
      ret_val += c
    else:
      ret_val += '_'

  return ret_val


def has_digits(s):

  return any(i.isdigit() for i in s)


def to_title(s):

  s =  s.title()
  ret_val = s.replace("'S", "'s")

  return ret_val


def token_case(s):

  if (has_digits(s)):
    ret_val = s.upper()
  else:
    ret_val =  to_title(s)

  return ret_val


def degrees_to_decimal(s):

  parts = s.split(':')
  if (int(parts[0]) > 0):
    ret_val = int(parts[0]) + int(parts[1])/60 + float(parts[2])/3600
  else:
    ret_val = int(parts[0]) - int(parts[1])/60 - float(parts[2])/3600
  ret_val = str(ret_val)

  return ret_val
  
def get_prop(o, props):
  
  if props[0] in o:
    if (len(props) == 1):
      ret_val = o[props[0]]
    else:
      ret_val = get_prop(o[props[0]],props[1:])
  else:
    ret_val = props[0]
    
  return ret_val

  



