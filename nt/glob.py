'''Runtime configuration.'''

from afmt import Formatter

list_fname = '.todo.json'
date_fmt = '%d.%m.%y %H:%M'
date_fmts = [
  '%d.%m.%y %H:%M',
  '%d.%m.%Y %H:%M',
  '%d.%m.%y',
  '%d.%m.%Y',
  '%d.%m',
]
command_tmp_fname = '~nt.cmd'
less_tmp_fname = '~nt.less'
editor = 'nvim'
rcfile = '.ntrc'
default_less_pipe = False
f = Formatter(styles={
  'due': 'fg(green)',
  'overdue': 'fg(red)',
  'index': 'fg(4)',
  'error': 'fg(red)',
  'success': 'fg(green)'
})

# per list default settings
completed_str = '[x]'
uncompleted_str = '[ ]'
pretty_json = False
