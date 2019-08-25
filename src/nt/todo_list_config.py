class TodoListConfig:
  def __init__(self, prefixes=None):
    if prefixes is None:
      self.prefixes = {
        '+': {'color': 5, 'name': 'project'},
        '#': {'color': 6, 'name': 'tag'},
        '@': {'color': 1, 'name': 'context'}
      }
    else:
      self.prefixes = prefixes

  def to_dict(self):
    data = {
      'prefixes': self.prefixes
    }
    return data

  @staticmethod
  def from_json(data):
    cfg = TodoListConfig()
    cfg.prefixes = data['prefixes']
    return cfg
