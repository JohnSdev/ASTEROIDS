from abc import ABC, abstractmethod
from circ import Circle
from labb import shape
from point import Point

c = Circle( Point( 2, 2 ), 1 )
d = Point( 2, 2 )
print (d.distanceFromOrigin())
print(c.isPointInside(d))

c2 = Circle( Point(2,1), 1)

print(c2.circleInside(c))