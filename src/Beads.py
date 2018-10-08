from coordinates import Coordinate
from src.Vectors import *
import math

interactionStrength = [
 #    A  B
 # A
    [ 1, 2 ],
 # B
    [ 2, 3 ]
]

class Bead:
    container = None
    position = Coordinate(x = 0, y = 0)
    velocity = Vector(0.0, 0.0);
    force = Vector(0.0, 0.0);
    mass = 0.0
    cutoffRadius = 20.0
    conservativeForce = []
    randomForce = []
    dragForce = []

    def __init__(self, creator, coord):
        self.container = creator
        self.position = coord

    def move(self, dx, dy):
        newX = self.position.x + dx
        newY = self.position.y + dy
        self.position = Coordinate(x = self.position.x + dx, y = self.position.y + dy)

class BeadA(Bead):
    typeName = "A"
    colour = "#ff0000"
    mass = 2.0
    interactionIndex = 0

class BeadB(Bead):
    typeName = "B"
    colour = "#000000"
    mass = 1.0
    interactionIndex = 1

def allBeadTypes():
    result = []
    result.append((BeadA.typeName, BeadA.colour))
    result.append((BeadB.typeName, BeadB.colour))
    return result

def euclidianDistance(i, j):
    result = math.sqrt(((i.x - j.x) ** 2) + ((i.y - j.y) ** 2))
    return result

def distanceVector(i, j):
    xResult = i.x - j.x
    yResult = i.y - j.y
    # zResult = i.z - j.z
    return Vector(xResult, yResult)

def conservativeForce(i, j):
    eucDistance = euclidianDistance(i.position, j.position)
    if (eucDistance <= i.cutoffRadius):
        vectorDistance = distanceVector(i.position, j.position)
        intStrength = interactionStrength[i.interactionIndex][i.interactionIndex]
        vectorDivide = Vector.divide(vectorDistance, eucDistance)
        result = intStrength * (1 - eucDistance/i.cutoffRadius)
        result = Vector.multiply(vectorDivide, result)
        return result

# https://en.wikipedia.org/wiki/Verlet_integration#Velocity_Verlet
