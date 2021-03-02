# written by Litong Peng (lp5629)


#the class that define each pixel
class pixel:
    __slots__ = ['x', 'y', 'z', 'color', 'before', 'g']

    def __init__(self, x, y, z, color, before, g):
        #the x coordinate
        self.x = x
        #the y coordinate
        self.y = y
        #the height
        self.z = z
        #its terrain
        self.color = color
        #the node linked before it
        self.before = before
        #its g value
        self.g = g

#the program that find pixel's neighbors
    def find_neighbors(self):
        x = self.x
        y = self.y
        neighbor = \
            [(x + 1, y),
             (x - 1, y),
             (x, y + 1),
             (x, y - 1),
             (x + 1, y + 1),
             (x - 1, y + 1),
             (x + 1, y - 1),
             (x - 1, y - 1)]
        neighbors = filter(lambda var: 0 <= var[0] < 395 and 0 <= var[1] < 500, neighbor)
        return list(neighbors)

    def __str__(self):
        return "X: " + str(self.x) + " Y: " + str(self.y)
