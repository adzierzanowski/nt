'''This module handles per-list configuration.'''

from .fmt import Fmt

class TodoListConfig:
  '''TodoListConfig defines configuration of the TodoList.'''

  def __init__(self, prefixes=None):
    if prefixes is None:
      self.prefixes = {
        '+': {'color': 5, 'name': 'project'},
        '#': {'color': 6, 'name': 'tag'},
        '@': {'color': 1, 'name': 'context'}
      }
    else:
      self.prefixes = prefixes

  @staticmethod
  def from_json(data):
    '''Returns TodoListConfig based on JSON data.'''

    cfg = TodoListConfig()
    cfg.prefixes = data['prefixes']
    return cfg

  def to_dict(self):
    '''Returns a dict representation of an instance.'''

    data = {
      'prefixes': self.prefixes
    }
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
      print('    {}{}{}'.format(
        Fmt.fg(prefix_data['color']),
        prefix,
        prefix_data['name']))

