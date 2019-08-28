'''This module handles single todo list items.'''

from dataclasses import dataclass
from datetime import datetime as dt

from . import glob
from .fmt import Fmt

@dataclass
class TodoItem:
  '''TodoItem is a direct mapping of JSON data.'''

  parent: object
  id: int
  content: str
  due_date: dt
  priority: int
  completed: bool

  def __str__(self):
    if self.completed:
      completed = self.parent.config.completed_str
    else:
      completed = self.parent.config.uncompleted_str

    if self.due_date is None:
      due = ''
    else:
      if dt.now() < self.due_date:
        due = 'due: {}'.format(Fmt.fg(2))
      else:
        due = 'due: {}'.format(Fmt.fg(1))
      due += self.due_date.strftime(glob.date_fmt)
      due += Fmt.end()

    if self.priority is None:
      priority = Fmt.fg(3) + Fmt.end()
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
          content[i] += Fmt.end()
          continue

    content = '{}{}{}'.format(Fmt.end(), ' '.join(content), Fmt.end())

    return '{}{:4}{} {}    {:30}    {:20}\n     {}\n'.format(
      Fmt.fg(4), self.id, Fmt.end(), completed, priority, due, content)

  @staticmethod
  def from_dict(parent, data):
    '''Returns a TodoItem from dictionary. The first argument specifies a
    TodoList to which the TodoItem belongs.'''

    if data['due_date'] is None:
      due = None
    else:
      due = dt.strptime(data['due_date'], glob.date_fmt)

    item = TodoItem(
      parent=parent,
      id=data['id'],
      content=data['content'],
      due_date=due,
      priority=data['priority'],
      completed=data['completed']
    )
    return item

  def to_dict(self):
    '''Returns a dict representation of the class.'''

    if self.due_date is None:
      due = None
    else:
      due = self.due_date.strftime(glob.date_fmt)

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
        prefixes.append(word[1:].strip('\t.,;:/'))
    return prefixes
