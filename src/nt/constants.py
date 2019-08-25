'''Runtime configuration.'''

class Constants:
  '''Some of these values are overriden when an ~/.ntrc file exists'''

  list_fname = '.todo.json'
  date_fmt = '%d.%m.%y %H:%M'
  date_fmts = [
    '%d.%m.%y %H:%M',
    '%d.%m.%Y %H:%M',
    '%d.%m.%y',
    '%d.%m.%Y',
    '%d.%m',
  ]
  command_tmp_fname = '~nt.todo.cmd'
  less_tmp_fname = '~nt.less'
  editor = 'nvim'
  rcfile = '~/.ntrc'
