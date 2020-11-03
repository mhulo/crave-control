from main.main_imports import *
from main.main_settings import *

def to_classname(s):
  s = s.title().replace('_', '')
  return s


def get_interface_conf(ifx):
  conf = interfaces_conf[ifx]
  conf['interface'] = ifx
  return conf


def get_interface(path_str):
  s = ''
  if ('/api/' in path_str):
    s = path_str.split('/api/')[1].split('/')[0]
  return s





