'''This module handles most of the program's behavior.'''

import os
import sys
import json
import subprocess
from datetime import datetime as dt
from datetime import timedelta

from .todo_item import TodoItem
from .todo_list_config import TodoListConfig
from . import glob
from .meta import __progname__

class PrefixNotDefined(Exception):
  '''Exception raised when there's an attempt to use a prefix that was not
  defined.'''

class TodoList:
  '''TodoList represents, wait for it... a todo list.'''

  def __init__(self):
    self.config = TodoListConfig()
    self.items = []
    self.max_id = -1

  @staticmethod
  def init():
    '''Initializes a list in the current directory. If a list exists, then it
    prints appropriate message to stderr and quits.'''

    if os.path.exists(glob.list_fname):
      print('{} already exists'.format(glob.list_fname), file=sys.stderr)
      print('remove it first with `{} rm list`'.format(__progname__),
        file=sys.stderr)
      exit(1)

    todo_list = TodoList()
    todo_list.to_file(force=True)
    return True

  @staticmethod
  def from_file(fname):
    '''Returns an instance of TodoList based on data from a file.'''

    todo_list = TodoList()
    try:
      with open(fname, 'r') as f:
        data = json.load(f)

      todo_list.config = TodoListConfig.from_dict(data['config'])

      for item in data['items']:
        item = TodoItem.from_dict(todo_list, item)
        todo_list.items.append(item)
        if item.id > todo_list.max_id:
          todo_list.max_id = item.id

      return todo_list

    except FileNotFoundError:
      return None

  @staticmethod
  def parse_date(due_):
    '''Returns a datetime.datetime instance based on an input string.'''

    if due_:
      for fmt in glob.date_fmts:
        try:
          due = dt.strptime(due_, fmt)
          break
        except ValueError:
          weekdays = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

          if due_.lower() in weekdays:
            timeptr = dt.now() + timedelta(days=1)
            while all([
              timeptr.weekday() != weekdays.index(due_.lower()),
              timeptr - dt.now() < timedelta(days=8)
            ]):

              timeptr += timedelta(days=1)
            due = timeptr

          else:
            due = None
    else:
      due = None

    if due:
      if due.year == 1900:
        due = due.replace(year=dt.now().year)

    return due

  @staticmethod
  def filter_overdue(items):
    '''Returns overdue items from the provided list.'''

    return [item for item in items if item.due_date is not None \
      and item.due_date < dt.now()]

  @staticmethod
  def sort_by_priority(items):
    '''Returns items from the provided list sorted by priority.'''

    return sorted(items,
      key=lambda m: 0 if m.priority is None else -m.priority)

  @staticmethod
  def sort_by_due_date(items):
    '''Returns items from the provided list sorted by due date.'''

    return sorted(items,
      key=lambda m: dt(1900, 1, 1) if m.due_date is None else m.due_date,
      reverse=True)

  @staticmethod
  def group_by_prefix(items, prefix):
    '''Returns a dict of items grouped by prefix.'''

    prefix_groups = {'no prefix': []}

    for item in items:
      prefixes = item.get_prefixes(prefix)
      if prefixes:
        for pref in prefixes:
          if pref in prefix_groups:
            prefix_groups[pref].append(item)
          else:
            prefix_groups[pref] = [item]
      else:
        prefix_groups['no prefix'].append(item)

    return prefix_groups

  def get_item(self, id_):
    '''Returs a tuple (index, item) from list of items belonging to the list
    based on an item id. If the item is not found, it returns (-1, None).'''

    for index, item in enumerate(self.items):
      if item.id == id_:
        return index, item
    return -1, None

  def add_todo_item(self, item: TodoItem):
    '''Appends a TodoItem to the list's item list.'''

    self.items.append(item)

  def add_item(self, due_: str, content_: str, priority_: int):
    '''Adds an item to the list based on certain parameters.
    Returns the item.'''

    due = TodoList.parse_date(due_)
    self.max_id += 1

    item = TodoItem(
      parent=self,
      id=self.max_id,
      content=' '.join(content_),
      due_date=due,
      priority=priority_,
      completed=False)
    self.add_todo_item(item)
    return item

  def remove_item(self, id_):
    '''Removes an item from the list based on its id.'''
    i, item = self.get_item(id_)
    if item:
      del self.items[i]

      if id_ == self.max_id:
        self.max_id = max([item.id for item in self.items])

      return True
    return False

  def edit_item(self, id_, content_, due_, priority_):
    '''Updates TodoItem's fields.'''

    i, item = self.get_item(id_)
    if item:
        if content_:
          self.items[i].content = content_
        if priority_:
          self.items[i].priority = priority_
        if due_:
          due = TodoList.parse_date(due_)
          self.items[i].due_date = due
        return True
    return False

  def set_completeness(self, id_, complete):
    '''Marks an item as completed (or not).'''

    i, item = self.get_item(id_)
    if item:
      self.items[i].completed = complete
      return True
    return False

  def list_items(self, **kwargs):
    '''Lists items from the list.'''

    items = self.items

    if kwargs.get('priority', False):
      items = TodoList.sort_by_priority(items)

    if kwargs.get('due', False):
      items = TodoList.sort_by_due_date(items)

    if not kwargs.get('all_', False):
      if kwargs.get('completed', False):
        items = [item for item in items if item.completed]

      elif kwargs.get('uncompleted', False):
        items = [item for item in items if not item.completed]

    if kwargs.get('overdue', False):
      items = TodoList.filter_overdue(items)

    for arg in kwargs.get('args', None):
      items = [item for item in items if arg in item.content]

    pref = kwargs.get('by_prefix', None)
    less = kwargs.get('less', False)
    self.print_filtered_items(items, pref, less)

  def print_filtered_items(self, items, pref=None, less=False):
    '''Outputs filtered and sorted items by prefix (or not)
    and pipe it to less (or not).'''

    items_ = items

    out = ''
    if pref:
      prefix_groups = TodoList.group_by_prefix(items_, pref)

      try:
        self.config.prefixes[pref]
      except KeyError:
        raise PrefixNotDefined

      for group, items_ in prefix_groups.items():
        if group == 'no prefix':
          prefix_name = ''
          group_name = '~none'
        else:
          prefix_name = pref
          group_name = group

        if items_:
          out += '{}: \033[38;5;{}m{}{}\033[0m\n'.format(
            self.config.prefixes[pref]['name'],
            self.config.prefixes[pref]['color'],
            prefix_name,
            group_name)
          for item in items_:
            out += str(item) + '\n'
    else:
      for item in items:
        out += str(item) + '\n'

    if less:
      with open(glob.less_tmp_fname, 'w') as f:
        f.write(out)
      subprocess.call(['less', '-R', glob.less_tmp_fname])
      os.remove(glob.less_tmp_fname)
    else:
      print(out, end='')

  def to_file(self, force=False):
    '''Saves the current state of the list to a file.'''

    if os.path.exists(glob.list_fname) or force:
      with open(glob.list_fname, 'w') as f:
        f.write(self.to_json())
    else:
      print('{} not found'.format(glob.list_fname))
      print('init list with `nt init`')

  def to_json(self):
    '''Returns a JSON representation of the class' data.'''

    data = {
      'config': self.config.to_dict(),
      'items': [item.to_dict() for item in self.items]
    }

    if self.config.pretty_json:
      return json.dumps(data, indent=2)
    return json.dumps(data)
