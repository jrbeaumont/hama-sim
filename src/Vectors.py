class Vector:
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def divide(n, d):
        newX = n.x / d
        newY = n.y / d
        newZ = n.z / d
        return (Vector(newX, newY, newZ))

    def multiply(v, i):
        newX = v.x * i
        newY = v.y * i
        newZ = v.z * i
        return (Vector(newX, newY, newZ))

    def add(v1, v2):
        newX = v1.x + v2.x
        newY = v1.y + v2.y
        newZ = v1.z + v2.z
        return (Vector(newX, newY, newZ))

    def subtract(v1, v2):
        newX = v1.x - v2.x
        newY = v1.y - v2.y
        newZ = v1.z - v2.z
        return (Vector(newX, newY, newZ))

    def dotProduct(v1, v2):
        xProd = v1.x * v2.x
        yProd = v1.y * v2.y
        zProd = v1.z * v2.z
        return (xProd + yProd + zProd)

