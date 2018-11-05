from src.Vectors import *
import math
import random

interactionMatrix = [
 #    A     B   C
 # A
    [ 1.0,  0.05, 0.75 ],
 # B
    [ 0.05, 0.01, 0.75 ],
 # C
    [ 0.75, 0.75, 0.5  ]
]

class Bead:
    ID = ""
    container = None
    position = Vector(0.0, 0.0, 0.0)
    velocity = Vector(0.0, 0.0, 0.0)
    acceleration = Vector(0.0, 0.0, 0.0)
    cutoffRadius = 1.0
    conForce = Vector(0.0, 0.0, 0.0)
    randForce = Vector(0.0, 0.0, 0.0)
    dForce = Vector(0.0, 0.0, 0.0)
    bonds = []
    bondsVisited = []
    bondForce = Vector(0.0, 0.0, 0.0)
    velocityHalfStep = Vector(0.0, 0.0, 0.0)
    dragCoefficient = 4.5
    stochasticConstant = 0.0
    interactions = []

    def __init__(self, creator, coord, interactions):
        self.stochasticConstant = math.sqrt(2 * self.dragCoefficient * creator.container.temp)
        self.container = creator
        self.position = coord
        self.ID = generateID(5)
        self.interactions = interactions

    def move(self, dx, dy):
        newX = self.position.x + dx
        newY = self.position.y + dy
        self.position = Vector(self.position.x + dx, self.position.y + dy)

# class BeadA(Bead):
#     typeName = "A"
#     colour = "#ff0000"
#     mass = 1.0
#     typeNumber = 0

# class BeadB(Bead):
#     typeName = "B"
#     colour = "#000000"
#     mass = 1.0
#     typeNumber = 1

# class BeadC(Bead):
#     typeName = "C"
#     colour = "#0000ff"
#     mass = 1.0
#     typeNumber = 2

class Bond:
    eqLength = 0.0
    currentLength = 0.0
    U = 0.0
    k = 0.0
    bead1 = None
    bead2 = None

    def __init__(self, eqL, konstant, b1, b2):
        self.eqLength = eqL
        self.k = konstant
        self.bead1 = b1
        self.bead2 = b2
        eucDistance = getShortestDistances(b1.container.container, b1.position, b2.position)[0]
        self.U = self.newU(eucDistance)
        self.bead1.bonds.append(self)
        self.bead2.bonds.append(self)

    def getOtherBead(self, bead):
        if (bead.position.x == bead1.position.x and bead.position.y == bead1.position.y and bead.position.z == bead1.position.z):
            return bead1
        elif (bead.position.x == bead2.position.x and bead.position.y == bead2.position.y and bead.position.z == bead2.position.z):
            return bead2

    def newU(self, eucDistance):
        return (self.k / 2) * ((eucDistance - self.eqLength) ** 2)

    def calculateBondForce(self):
        if (self not in self.bead1.bondsVisited) and (self not in self.bead2.bondsVisited):
            # print("BOND BETWEEN " + self.bead1.ID + " AND " + self.bead2.ID)
            n = getShortestDistances(self.bead1.container.container, self.bead1.position, self.bead2.position)
            eucDistance = n[0]
            self.currentLength = eucDistance
            vecDistance = n[1]
            nU = self.newU(eucDistance)
            f = Vector.multiply(vecDistance, -1 * (1 / eucDistance) * (self.U))
            # print("FORCE OF THIS BOND = (" + str(f.x) + ", " + str(f.y) + ", " + str(f.z) + ")")
            self.bead1.bondForce = Vector.add(self.bead1.bondForce, f)
            self.bead2.bondForce = Vector.add(self.bead2.bondForce, (Vector.multiply(f,-1)))
            self.U = nU
            self.bead1.bondsVisited.append(self)
            self.bead2.bondsVisited.append(self)

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
    result.append((BeadA.typeName, BeadA.colour, BeadA.cutoffRadius))
    result.append((BeadB.typeName, BeadB.colour, BeadB.cutoffRadius))
    result.append((BeadC.typeName, BeadC.colour, BeadC.cutoffRadius))
    return result

def getShortestDistances(volume, i, j):
    maxDistance = volume.cubeLength * 2
    tempI = Vector(i.x, i.y, i.z)
    tempJ = Vector(j.x, j.y, j.z)

    xDiff = tempI.x - tempJ.x
    if (xDiff > maxDistance or xDiff < (-1 * maxDistance)):
        if (xDiff < 0):
            tempI.x = tempI.x + (volume.lengthInCubes * volume.cubeLength)
        else:
            tempJ.x = tempJ.x + (volume.lengthInCubes * volume.cubeLength)

    yDiff = tempI.y - tempJ.y
    if (yDiff > maxDistance or yDiff < (-1 * maxDistance)):
        if (yDiff < 0):
            tempI.y = tempI.y + (volume.lengthInCubes * volume.cubeLength)
        else:
            tempJ.y = tempJ.y + (volume.lengthInCubes * volume.cubeLength)

    zDiff = tempI.z - tempJ.z
    if (zDiff > maxDistance or zDiff < (-1 * maxDistance)):
        if (zDiff < 0):
            tempI.z = tempI.z + (volume.lengthInCubes * volume.cubeLength)
        else:
            tempJ.z = tempJ.z + (volume.lengthInCubes * volume.cubeLength)

    e = math.sqrt(((tempI.x - tempJ.x) ** 2) + ((tempI.y - tempJ.y) ** 2) + ((tempI.z - tempJ.z) ** 2))
    v = Vector.subtract(tempI, tempJ)

    # print("tempI : x = " + str(tempI.x) + ", y = " + str(tempI.y) + ", z = " + str(tempI.z))
    # print("tempJ : x = " + str(tempJ.x) + ", y = " + str(tempJ.y) + ", z = " + str(tempJ.z))
    # print("EUC = " + str(e))
    # print("VEC : x = " + str(v.x) + ", y = " + str(v.y) + ", z = " + str(v.z))

    return (e, v)

def conservativeForce(i, j, eucDistance, vectorDistance):
    if (eucDistance < i.cutoffRadius):
        intStrength = i.interactions[j.typeNumber]
        vectorDivide = Vector.divide(vectorDistance, eucDistance)
        result = intStrength * (1 - (eucDistance/i.cutoffRadius))
        result = Vector.multiply(vectorDivide, result)
        # print(i.ID + " -> " + j.ID + " conservative result = (" + str(result.x) + ", " + str(result.y) + ", " + str(result.z) + ")")
        return result

def randomForce(i, j, eucDistance, vectorDistance, timestep, randNums):
    if (eucDistance < i.cutoffRadius):
        randNum = 0
        for c in i.ID:
            val = ord(c) - 48
            if (val > 9):
                val -= 7
            if (val > 35):
                val -= 6
            randNum += val
        for d in j.ID:
            val = ord(d) - 48
            if (val > 9):
                val -= 7
            if (val > 35):
                val -= 6
            randNum += val
        for x in range(0, len(randNums)):
            if (randNum % randNums[x][0] == 0):
                randNum = randNum * randNums[x][1]
        randNum /= (5 * 61 * 2)
        result = Vector.multiply(Vector.divide(vectorDistance, eucDistance), (1 - (eucDistance/i.cutoffRadius)) * i.stochasticConstant * randNum * (timestep ** (-0.5)))
        return result

def dragForce(i, j, eucDistance, vectorDistance):
    if (eucDistance < i.cutoffRadius):
        velocityDiff = Vector.subtract(i.velocity, j.velocity)
        dotProd = Vector.dotProduct(vectorDistance, velocityDiff)
        result = Vector.multiply(Vector.divide(vectorDistance, (eucDistance ** 2)), -1 * i.dragCoefficient * ((1 - (eucDistance/i.cutoffRadius)) ** 2) * dotProd)
        return result
