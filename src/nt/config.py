import os
import json
import shutil

class Config:
  def __init__(self, cfgdata):
    self.cfgdata = cfgdata

    self.data_directory = cfgdata['data_directory']
    self.current_dir = cfgdata['current_dir']

def load_config():
  with open(os.path.expanduser('~/.ntrc'), 'r') as f:
    cfgdata = json.load(f)
  return Config(cfgdata)
