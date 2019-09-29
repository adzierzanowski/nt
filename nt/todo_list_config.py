'''This module handles per-list configuration.'''

from . import glob
from .glob import f

class TodoListConfig:
  '''TodoListConfig defines configuration of the TodoList.'''

  keys = (
    'completed_str',
    'uncompleted_str',
    'pretty_json'
  )

  def __init__(self, prefixes=None):
    if prefixes is None:
      self.prefixes = {
        '+': {'color': 5, 'name': 'project'},
        '#': {'color': 6, 'name': 'tag'},
        '@': {'color': 1, 'name': 'context'}
      }
    else:
      self.prefixes = prefixes

    for key in TodoListConfig.keys:
      setattr(self, key, getattr(glob, key))

  @staticmethod
  def from_dict(data):
    '''Returns TodoListConfig based on dictionary.'''

    cfg = TodoListConfig()
    cfg.prefixes = data['prefixes']

    for key in TodoListConfig.keys:
      if key in data:
        setattr(cfg, key, data[key])
      else:
        setattr(cfg, key, getattr(glob, key))

    return cfg

  def to_dict(self):
    '''Returns a dict representation of an instance.'''

    data = {
      'prefixes': self.prefixes
    }

    for key in TodoListConfig.keys:
      data[key] = getattr(self, key)
    return data

  def add_prefix(self, symbol, name, color):
    '''Adds a new prefix definition.'''

    self.prefixes[symbol] = {'name': name, 'color': color}

  def remove_prefix(self, symbol):
    '''Removes a prefix definition form the config.'''

    del self.prefixes[symbol]

  def dump(self):
    '''Prints current configuration.'''

    print('List of defined prefixes:')
    for prefix, prefix_data in self.prefixes.items():
      color = prefix_data['color']
      print(f'{f:fg({color})}{prefix}{prefix_data}{f:e}')

    print()
    for key in TodoListConfig.keys:
      print(key + ':', getattr(self, key))
