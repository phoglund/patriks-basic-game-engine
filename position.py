def make(x, y):
  return Position(x, y)


class Position(object):

  def __init__(self, x: float, y: float):
    self._x = x
    self._y = y

  @property
  def x(self) -> float:
    return self._x

  @property
  def y(self) -> float:
    return self._y

  @x.setter
  def x(self, value):
    self._x = value

  @y.setter
  def y(self, value):
    self._y = value

  def __eq__(self, other: 'Position'):
    return self.x == other.x and self.y == other.y

  def __add__(self, other: 'Position'):
    return make(self.x + other.x, self.y + other.y)

  def __iadd__(self, other: 'Position'):
    self.x += other.x
    self.y += other.y
    return self

  def __iter__(self):
    return iter((self.x, self.y))

  def __len__(self):
    return 2

  def __getitem__(self, key: int):
    if key not in (0, 1):
      raise IndexError('%s out of bounds' % key)
    return self.x if key == 0 else self.y

  def __setitem__(self, key: int, value: float):
    if key not in (0, 1):
      raise IndexError('%s out of bounds' % key)
    if key == 0:
      self.x = value
    else:
      self.y = value

  def __repr__(self):
    return '(%d, %d)' % (self.x, self.y)
