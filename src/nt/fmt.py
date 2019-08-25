'''String formatting. For now, only foreground colors.'''

import sys

class Fmt:
  '''String formatter. Methods of this class detect if the program output
  is redirected. If it is, then the color information is removed.'''

  @staticmethod
  def fg(color):
    '''Returns a foreground color ANSI escape code.'''

    if sys.stdout.isatty():
      return '\033[38;5;{}m'.format(color)
    return ''

  @staticmethod
  def end():
    '''Returns end of formatting ANSI escape code.'''

    if sys.stdout.isatty():
      return '\033[0m'
    return ''
