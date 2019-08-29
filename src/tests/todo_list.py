import os
import unittest

from nt.todo_list import TodoList
from nt.todo_list_config import TodoListConfig

class TodoListTest(unittest.TestCase):
  def setUp(self):
    self.todo_list = TodoList()

  def test_init_(self):
    '''__init__()'''

    self.assertIsNotNone(self.todo_list)
    self.assertIsInstance(self.todo_list.config, TodoListConfig)
    self.assertEqual(self.todo_list.items, [])
    self.assertEqual(self.todo_list.max_id, -1)

  def test_init(self):
    '''init()'''

    try:
      self.todo_list.init()
    except SystemExit:
      pass

    self.assertTrue(os.path.exists('.todo.json'))
    os.remove('.todo.json')

  def test_parse_date(self):
    pass

  def test_group_by_prefix(self):
    pass

  def test_get_item(self):
    pass

  def test_add_item(self):
    pass

  def test_remove_item(self):
    pass

  def test_edit_item(self):
    pass

  def set_completness(self):
    pass

