import yaml


with open('/app/config/interfaces_conf.yml') as f:
  interfaces_conf = yaml.load(f, Loader=yaml.FullLoader)

with open('/app/config/devices_conf.yml') as f:
  devices_conf = yaml.load(f, Loader=yaml.FullLoader)

with open('/app/config/cards_conf.yml') as f:
  cards_conf = yaml.load(f, Loader=yaml.FullLoader)

with open('/app/config/icons_conf.yml') as f:
  icons_conf = yaml.load(f, Loader=yaml.FullLoader)

with open('/app/config/commands_conf.yml') as f:
  commands_conf = yaml.load(f, Loader=yaml.FullLoader)

