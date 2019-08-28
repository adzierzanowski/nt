import unittest

from nt.todo_list_config import TodoListConfig

class TodoListConfigTest(unittest.TestCase):
  def setUp(self):
    self.todo_list_config = TodoListConfig()

  def test_init(self):
    self.assertFalse(self.todo_list_config.pretty_json)
    self.assertEqual(self.todo_list_config.completed_str, '[x]')
    self.assertEqual(self.todo_list_config.uncompleted_str, '[ ]')

    for prefix in ('@', '+', '#'):
      self.assertIn(prefix, self.todo_list_config.prefixes)
      self.assertIn('color', self.todo_list_config.prefixes[prefix])
      self.assertIn('name', self.todo_list_config.prefixes[prefix])
  
  def test_from_dict(self):
    cfg_dict = {
      'prefixes': {
        '$': {
          'color': 4,
          'name': 'dollar'
        }
      },
      'pretty_json': True,
      'completed_str': 'YEAH',
      'uncompleted_str': 'DAMN'
    }
    cfg = TodoListConfig.from_dict(cfg_dict)

    self.assertIn('$', cfg.prefixes)
    self.assertIn('name', cfg.prefixes['$'])
    self.assertIn('color', cfg.prefixes['$'])

    self.assertTrue(cfg.pretty_json)
    self.assertEqual(cfg.completed_str, 'YEAH')
    self.assertEqual(cfg.uncompleted_str, 'DAMN')
