from datetime import datetime as dt

from constants import Constants

class TodoItem:
  def __init__(self, id_, content, due_date, priority, completed=False):
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
      due = 'due: \033[38;5;2m'
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
      if word.startswith('@'):
        content[i] = '\033[38;5;1m' + word + '\033[38;5;7m'

      elif word.startswith('+'):
        content[i] = '\033[38;5;5m' + word + '\033[38;5;7m'

      elif word.startswith('#'):
        content[i] = '\033[38;5;6m' + word + '\033[38;5;7m'

    content = '\033[38;5;7m' + ' '.join(content) + '\033[0m'

    return '\033[38;5;4m{:4}\033[0m [{}]    {}    {}\n     {}\n'.format(
      self.id, completed, due, priority, content)

  @staticmethod
  def from_json(data):
    item = TodoItem(
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
