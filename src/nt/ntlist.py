from ntentity import NTEntity

class NTListItem:
  def __init__(self):
    pass

class NTList(NTEntity):
  def __init__(self, dir_):
    NTEntity.__init__(self, type(self), dir_)
    self.items = []
