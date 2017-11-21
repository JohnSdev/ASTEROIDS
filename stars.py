from circle	import Circle
from shape import *

class Stars(Circle):
    def __init__(self, x, y, r, rotation, exp ):
        super().__init__(  x, y,r, rotation )
        self.radius = 1
        self.linewidth = 1
        self.type=exp
        self.pull = Point(2,0)
        if exp == "exp":
            self.pull=Point(5,5)