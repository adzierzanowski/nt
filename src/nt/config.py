import os
import json

def load_config():
  with open(os.path.expanduser('~/.ntrc'), 'r') as f:
    cfgdata = json.load(f)
  return cfgdata
