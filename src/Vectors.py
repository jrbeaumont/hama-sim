class Vector:
    x = 0.0
    y = 0.0
    # z = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def divide(n, d):
        newX = n.x / d
        newY = n.y / d
        # newZ = n.z / d
        return (Vector(newX, newY))

    def multiply(v, i):
        newX = v.x * i
        newY = v.y * i
        # newZ = n.z * i
        return (Vector(newX, newY))

    def add (v1, v2):
        newX = v1.x + v2.x
        newY = v1.y + v2.y
        # newZ = v1.z + v2.z
        return (Vector(newX, newY))

