from coordinates import Coordinate
from src.Vectors import *
import math
import random

interactionStrength = [
 #    A  B
 # A
    [ 40, 200 ],
 # B
    [ 200, 40 ]
]
stochasticConstant = 2.5
dragCoefficient = 1

class Bead:
    ID = ""
    container = None
    position = Vector(0.0, 0.0)
    velocity = Vector(0.0, 0.0);
    acceleration = Vector(0.0, 0.0);
    cutoffRadius = 20.0
    conForce = []
    randForce = []
    dForce = []
    velocityHalfStep = Vector(0.0, 0.0)

    def __init__(self, creator, coord):
        self.container = creator
        self.position = coord
        self.ID = generateID(5)
        # self.velocity = Vector(random.SystemRandom().uniform(-20, 20), random.SystemRandom().uniform(-20, 20))

    def move(self, dx, dy):
        newX = self.position.x + dx
        newY = self.position.y + dy
        self.position = Vector(self.position.x + dx, self.position.y + dy)

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

def generateID(numberOfCharacters):
    randomID = ""
    rng = random.SystemRandom()
    for i in range(0, numberOfCharacters):
        val = rng.randint(0, 61)
        if (val <= 9):
            randomID += str(val)
        else:
            val -= 10
            if (val <= 25):
                randomID += chr(val + 65)
            else:
                val-= 26
                randomID += chr(val + 97)
    return randomID

def allBeadTypes():
    result = []
    result.append((BeadA.typeName, BeadA.colour))
    result.append((BeadB.typeName, BeadB.colour))
    return result

def euclidianDistance(i, j):
    result = math.sqrt(((i.x - j.x) ** 2) + ((i.y - j.y) ** 2))
    return result

def conservativeForce(i, j):
    eucDistance = euclidianDistance(i.position, j.position)
    if (eucDistance <= i.cutoffRadius):
        vectorDistance = Vector.subtract(i.position, j.position)
        intStrength = interactionStrength[i.interactionIndex][i.interactionIndex]
        vectorDivide = Vector.divide(vectorDistance, eucDistance)
        result = intStrength * (1 - (eucDistance/i.cutoffRadius))
        result = Vector.multiply(vectorDivide, result)
        return result

def randomForce(i, j, timestep, randNums):
    eucDistance = euclidianDistance(i.position, j.position)
    if (eucDistance <= i.cutoffRadius):
        vectorDistance = Vector.subtract(i.position, j.position)
        randNum = 0
        for c in i.ID:
            randNum += ord(c)
        for d in j.ID:
            randNum += ord(d)
        for x in range(0, 3):
            if (randNum % randNums[x][0] == 0):
                randNum = randNum * randNums[x][1]
        randNum /= 5 * 122 * 2
        result = Vector.multiply(Vector.divide(vectorDistance, eucDistance), stochasticConstant * randNum * (timestep ** (-0.5)))
        # print(i.ID + " AND " + j.ID + ": x = " + str(result.x) + ", y = " + str(result.y))
        return result

def dragForce(i, j):
    eucDistance = euclidianDistance(i.position, j.position)
    if (eucDistance <= i.cutoffRadius):
        vectorDistance = Vector.subtract(i.position, j.position)
        velocityDiff = Vector.subtract(i.velocity, j.velocity)
        dotProd = Vector.dotProduct(vectorDistance, velocityDiff)
        result = Vector.multiply(Vector.divide(vectorDistance, (eucDistance ** 2)), -1 * dragCoefficient * dotProd)
        return result
