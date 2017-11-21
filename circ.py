from labb import shape
from point import Point


class Circle( shape ):
  def __init__( self, pos, radius):
      super().__init__( pos )
      self._radius = float( radius )
      

  def area(self):
      return 3.14159 * self._radius ** 2

  def circumference(self):
      return 2 * 3.14159 * self._radius

  def draw( self ):
      print( "Drawing a circle..." )

  def isPointInside(self, point):
      diff = (point-self.getPosition())
      if diff.distanceFromOrigin() <= self._radius:
          return True
      else:
          return False

  def circleInside(self, cir):
      p1= self.getPosition()
      p2= cir.getPosition()
      print(p1-p2)
      distOrigin= (p1-p2).distanceFromOrigin()
      if distOrigin <= self._radius + cir._radius:
          return True
      else:
          return False