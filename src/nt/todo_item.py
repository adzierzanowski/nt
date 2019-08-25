from datetime import datetime as dt

from .constants import Constants

class TodoItem:
  def __init__(self, parent, id_, content, due_date, priority, completed=False):
    self.parent = parent
    self.id = id_
    self.content = content
    self.due_date = due_date
    self.priority = priority
    self.completed = completed

  def __str__(self):
    completed = 'x' if self.completed else ' '

    if self.due_date is None:
      due = ''
    else:
      if dt.now() < self.due_date:
        due = 'due: \033[38;5;2m'
      else:
        due = 'due: \033[38;5;1m'
      due += self.due_date.strftime(Constants.date_fmt)
      due += '\033[0m'

    if self.priority is None:
      priority = ''
    else:
      priority = 'priority: \033[38;5;3m'
      priority += str(self.priority)
      priority += '\033[0m'

    content = self.content.split(' ')
    for i, word in enumerate(content):
      for prefix, prefix_data in self.parent.config.prefixes.items():
        if word.startswith(prefix):
          content[i] = '\033[38;5;{}m'.format(prefix_data['color'])
          content[i] += word
          content[i] += '\033[38;5;7m'
          continue

    content = '\033[38;5;7m' + ' '.join(content) + '\033[0m'

    return '\033[38;5;4m{:4}\033[0m [{}]    {:20}    {:20}\n     {}\n'.format(
      self.id, completed, priority, due, content)

  @staticmethod
  def from_json(parent, data):
    item = TodoItem(
      parent,
      data['id'],
      data['content'],
      None if data['due_date'] is None else dt.strptime(data['due_date'], Constants.date_fmt),
      data['priority'],
      data['completed']
    )
    return item

  def to_dict(self):
    due = None if self.due_date is None else self.due_date.strftime(Constants.date_fmt)
    data = {
      'id': self.id,
      'content': self.content,
      'due_date': due,
      'priority': self.priority,
      'completed': self.completed
    }
    return data

  def get_prefixes(self, prefix):
    prefixes = []
    for word in self.content.split(' '):
      if word.startswith(prefix):
        prefixes.append(word[1:])
    return prefixes
