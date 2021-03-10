from main.main_imports import *
from main.main_settings import *

def to_classname(s):
  s = s.title().replace('_', '')
  return s


def to_dict(x):
  if (x == None):
    x = {}
  elif (type(x) == str):
    x = json.loads(x)
  return x


def get_interface_conf(ifx):
  conf = interfaces_conf[ifx]
  conf['interface'] = ifx
  return conf


# get the interface name based on the path string
def get_ifx(r):
  s = ''
  p = r.scope['path']
  if ('/api/' in p):
    s = p.split('/api/')[1].split('/')[0]
  return s

