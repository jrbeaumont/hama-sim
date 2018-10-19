from src.Vectors import *
import math
import random

interactionStrength = [
 #    A     B   C
 # A
    [ 1.0,  0.05, 0.75 ],
 # B
    [ 0.05, 0.01, 0.75 ],
 # C
    [ 0.75, 0.75, 0.5  ]
]

dragCoefficient = 0.998
temp = 0.05
stochasticConstant = math.sqrt(2 * dragCoefficient * temp)

class Bead:
    ID = ""
    container = None
    position = Vector(0.0, 0.0, 0.0)
    velocity = Vector(0.0, 0.0, 0.0);
    acceleration = Vector(0.0, 0.0, 0.0);
    cutoffRadius = 1.0
    conForce = []
    randForce = []
    dForce = []
    bond = None
    bondForce = None
    velocityHalfStep = Vector(0.0, 0.0, 0.0)

    def __init__(self, creator, coord):
        self.container = creator
        self.position = coord
        self.ID = generateID(5)

    def move(self, dx, dy):
        newX = self.position.x + dx
        newY = self.position.y + dy
        self.position = Vector(self.position.x + dx, self.position.y + dy)

class BeadA(Bead):
    typeName = "A"
    colour = "#ff0000"
    mass = 1.0
    interactionIndex = 0

class BeadB(Bead):
    typeName = "B"
    colour = "#000000"
    mass = 1.0
    interactionIndex = 1

class BeadC(Bead):
    typeName = "C"
    colour = "#0000ff"
    mass = 1.0
    interactionIndex = 2

class Bond:
    eqLength = 0.75
    U = 0.0
    k = 1
    bead1 = None
    bead2 = None

    def __init__(self, bead1, bead2):
        self.bead1 = bead1
        self.bead2 = bead2
        eucDistance = euclidianDistance(bead1.container.container, bead1.position, bead2.position)
        self.U = self.newU(eucDistance)
        self.bead1.bond = self
        self.bead2.bond = self

    def getOtherBead(self, bead):
        if (bead.position.x == bead1.position.x and bead.position.y == bead1.position.y and bead.position.z == bead1.position.z):
            return bead1
        elif (bead.position.x == bead2.position.x and bead.position.y == bead2.position.y and bead.position.z == bead2.position.z):
            return bead2

    def ensureBeadsAreNeighbours(self):
        iPos = Vector(self.bead1.position.x, self.bead1.position.y, self.bead1.position.z)
        jPos = Vector(self.bead2.position.x, self.bead2.position.y, self.bead2.position.z)
        ix = self.bead1.container.arrayPosX
        jx = self.bead2.container.arrayPosX
        iy = self.bead1.container.arrayPosY
        jy = self.bead2.container.arrayPosY
        iz = self.bead1.container.arrayPosZ
        jz = self.bead2.container.arrayPosZ
        if (ix == 0 and jx == self.bead1.container.container.lengthInCubes - 1):
            iPos.x = iPos.x + self.bead1.container.container.length
        if (jx == 0 and ix == self.bead1.container.container.lengthInCubes - 1):
            jPos.x = jPos.x + self.bead1.container.container.length
        if (iy == 0 and jy == self.bead1.container.container.lengthInCubes - 1):
            iPos.y = iPos.y + self.bead2.container.container.length
        if (jy == 0 and iy == self.bead1.container.container.lengthInCubes - 1):
            jPos.y = jPos.y + self.bead1.container.container.length
        if (iz == 0 and jz == self.bead1.container.container.lengthInCubes - 1):
            iPos.z = iPos.z + self.bead2.container.container.length
        if (jz == 0 and iz == self.bead1.container.container.lengthInCubes - 1):
            jPos.z = jPos.z + self.bead1.container.container.length
        return (iPos, jPos)

    def newU(self, eucDistance):
        # n = self.ensureBeadsAreNeighbours()
        # iPos = n[0]
        # jPos = n[1]
        # eucDistance = euclidianDistance(self.bead1.container.container, iPos, jPos)
        return (self.k / 2) * ((eucDistance - self.eqLength) ** 2)

    def calculateBondForce(self):
        n = self.ensureBeadsAreNeighbours()
        iPos = n[0]
        jPos = n[1]
        # iPos = self.bead1.position
        # jPos = self.bead2.position
        eucDistance = euclidianDistance(self.bead1.container.container, self.bead1.position, self.bead2.position)
        nU = self.newU(eucDistance)
        vectorDistance = Vector.subtract(iPos, jPos)
        f = Vector.multiply(vectorDistance, -1 * (1 / eucDistance) * (self.U))
        self.bead1.bondForce = f
        self.bead2.bondForce = Vector.multiply(f,-1)
        self.U = nU

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

def euclidianDistance(volume, i, j):
    result = math.sqrt(((i.x - j.x) ** 2) + ((i.y - j.y) ** 2) + ((i.z - j.z) ** 2))
    origResult = math.sqrt(((i.x - j.x) ** 2) + ((i.y - j.y) ** 2) + ((i.z - j.z) ** 2))
    # print("original result = " + str(result))
    r = []
    # I
    r.append(math.sqrt(((i.x - j.x) ** 2) + ((i.y - j.y) ** 2) + (((i.z + volume.length) - j.z) ** 2)))
    r.append(math.sqrt(((i.x - j.x) ** 2) + (((i.y + volume.length) - j.y) ** 2) + ((i.z - j.z) ** 2)))
    r.append(math.sqrt(((i.x - j.x) ** 2) + (((i.y + volume.length) - j.y) ** 2) + (((i.z + volume.length) - j.z) ** 2)))
    r.append(math.sqrt((((i.x + volume.length) - j.x) ** 2) + ((i.y - j.y) ** 2) + ((i.z - j.z) ** 2)))
    r.append(math.sqrt((((i.x + volume.length) - j.x) ** 2) + ((i.y - j.y) ** 2) + (((i.z + volume.length) - j.z) ** 2)))
    r.append(math.sqrt((((i.x + volume.length) - j.x) ** 2) + (((i.y + volume.length) - j.y) ** 2) + ((i.z - j.z) ** 2)))
    r.append(math.sqrt((((i.x + volume.length) - j.x) ** 2) + (((i.y + volume.length) - j.y) ** 2) + (((i.z + volume.length) - j.z) ** 2)))

    # J
    r.append(math.sqrt(((i.x - j.x) ** 2) + ((i.y - j.y) ** 2) + ((i.z - (j.z + volume.length)) ** 2)))
    r.append(math.sqrt(((i.x - j.x) ** 2) + ((i.y - (j.y + volume.length)) ** 2) + ((i.z - j.z) ** 2)))
    r.append(math.sqrt(((i.x - j.x) ** 2) + ((i.y - (j.y + volume.length)) ** 2) + ((i.z - (j.z + volume.length)) ** 2)))
    r.append(math.sqrt(((i.x - (j.x + volume.length)) ** 2) + ((i.y - j.y) ** 2) + ((i.z - j.z) ** 2)))
    r.append(math.sqrt(((i.x - (j.x + volume.length)) ** 2) + ((i.y - j.y) ** 2) + ((i.z - (j.z + volume.length)) ** 2)))
    r.append(math.sqrt(((i.x - (j.x + volume.length)) ** 2) + ((i.y - (j.y + volume.length)) ** 2) + ((i.z - j.z) ** 2)))
    r.append(math.sqrt(((i.x - (j.x + volume.length)) ** 2) + ((i.y - (j.y + volume.length)) ** 2) + ((i.z - (j.z + volume.length)) ** 2)))

    for x in r:
        if x < result:
            result = x


    # print("final result = " + str(result))
    # if (result != origResult):
    #     input()
    return result

def conservativeForce(i, j, eucDistance, vectorDistance):
    if (eucDistance < i.cutoffRadius):
        intStrength = interactionStrength[i.interactionIndex][j.interactionIndex]
        vectorDivide = Vector.divide(vectorDistance, eucDistance)
        result = intStrength * (1 - (eucDistance/i.cutoffRadius))
        result = Vector.multiply(vectorDivide, result)
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
            val = ord(c) - 48
            if (val > 9):
                val -= 7
            if (val > 35):
                val -= 6
            randNum += val
        for x in range(0, len(randNums)):
            if (randNum % randNums[x][0] == 0):
                randNum = randNum * randNums[x][1]
        randNum /= 5 * 61 * 2
        result = Vector.multiply(Vector.divide(vectorDistance, eucDistance), (1 - (eucDistance/i.cutoffRadius)) * stochasticConstant * randNum * (timestep ** (-0.5)))
        return result

def dragForce(i, j, eucDistance, vectorDistance):
    if (eucDistance < i.cutoffRadius):
        velocityDiff = Vector.subtract(i.velocity, j.velocity)
        dotProd = Vector.dotProduct(vectorDistance, velocityDiff)
        result = Vector.multiply(Vector.divide(vectorDistance, (eucDistance * eucDistance)), -1 * dragCoefficient * ((1 - (eucDistance/i.cutoffRadius)) ** 2) * dotProd)
        return result
