'''This module handles single todo list items.'''

from datetime import datetime as dt

from .constants import Constants
from .fmt import Fmt

class TodoItem:
  '''TodoItem is a direct mapping of JSON data.'''

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
        due = 'due: {}'.format(Fmt.fg(2))
      else:
        due = 'due: {}'.format(Fmt.fg(1))
      due += self.due_date.strftime(Constants.date_fmt)
      due += Fmt.end()

    if self.priority is None:
      priority = ''
    else:
      priority = 'priority: {}'.format(Fmt.fg(3))
      priority += str(self.priority)
      priority += Fmt.end()

    content = self.content.split(' ')
    for i, word in enumerate(content):
      for prefix, prefix_data in self.parent.config.prefixes.items():
        if word.startswith(prefix):
          content[i] = Fmt.fg(prefix_data['color'])
          content[i] += word
          content[i] += Fmt.fg(7)
          continue

    content = '{}{}{}'.format(Fmt.fg(7), ' '.join(content), Fmt.end())

    return '{}{:4}{} [{}]    {:20}    {:20}\n     {}\n'.format(
      Fmt.fg(4), self.id, Fmt.end(), completed, priority, due, content)

  @staticmethod
  def from_json(parent, data):
    '''Returns a TodoItem from JSON data. The first argument specifies a
    TodoList to which the TodoItem belongs.'''

    if data['due_date'] is None:
      due = None
    else:
      due = dt.strptime(data['due_date'], Constants.date_fmt)

    item = TodoItem(
      parent,
      data['id'],
      data['content'],
      due,
      data['priority'],
      data['completed']
    )
    return item

  def to_dict(self):
    '''Returns a dict representation of the class.'''

    if self.due_date is None:
      due = None
    else:
      due = self.due_date.strftime(Constants.date_fmt)

    data = {
      'id': self.id,
      'content': self.content,
      'due_date': due,
      'priority': self.priority,
      'completed': self.completed
    }
    return data

  def get_prefixes(self, prefix):
    '''Returns a list of words in TodoItem content that begins with a
    certain prefix.'''

    prefixes = []
    for word in self.content.split(' '):
      if word.startswith(prefix):
        prefixes.append(word[1:])
    return prefixes
