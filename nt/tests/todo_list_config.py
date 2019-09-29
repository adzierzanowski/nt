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

  def test_to_dict(self):
    d = self.todo_list_config.to_dict()

    self.assertIn('prefixes', d)
    self.assertIn('pretty_json', d)
    self.assertIn('completed_str', d)
    self.assertIn('uncompleted_str', d)
    self.assertEqual(d['completed_str'], '[x]')
    self.assertEqual(d['uncompleted_str'], '[ ]')

    for prefix in ('@', '+', '#'):
      self.assertIn(prefix, d['prefixes'])
      self.assertIn('color', d['prefixes'][prefix])
      self.assertIn('name', d['prefixes'][prefix])

  def test_add_prefix(self):
    self.todo_list_config.add_prefix('$', 'dollar', 4)

    self.assertIn('$', self.todo_list_config.prefixes)
    self.assertEqual(self.todo_list_config.prefixes['$'], {'name': 'dollar', 'color': 4})

  def test_remove_prefix(self):
    self.todo_list_config.add_prefix('$', 'dollar', 4)
    self.todo_list_config.remove_prefix('$')

    self.assertNotIn('$', self.todo_list_config.prefixes)
