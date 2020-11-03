import yaml


with open('/app/config/interfaces_conf.yml') as f:
  interfaces_conf = yaml.load(f, Loader=yaml.FullLoader)

with open('/app/config/widgets_conf.yml') as f:
  widgets_conf = yaml.load(f, Loader=yaml.FullLoader)

with open('/app/config/commands_conf.yml') as f:
  commands_conf = yaml.load(f, Loader=yaml.FullLoader)






