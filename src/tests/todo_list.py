import unittest

from nt.todo_list import TodoList
from nt.todo_list_config import TodoListConfig

class TodoListTest(unittest.TestCase):
  def setUp(self):
    self.todo_list = TodoList()

  def test_init(self):
    self.assertIsNotNone(self.todo_list)
    self.assertIsInstance(self.todo_list.config, TodoListConfig)
    self.assertEqual(self.todo_list.items, [])
    self.assertEqual(self.todo_list.max_id, -1)

  def test_parse_date(self):
    pass

  def test_group_by_prefix(self):
    pass

  def test_get_item(self):
    pass

  def test_add_todo_item(self):
    pass

  def test_remove_todo_item(self):
    pass

