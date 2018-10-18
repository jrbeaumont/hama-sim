import random
from src.Beads import *

coordinates = []

class Container:
    lengthInCubes = 0 # Number of squares in legnth, width and depth (square/cube required)
    cubeLength = 0 # Number of pixels in each sub-cube
    dimensions = 0 # Can be 2 or 3, for 2D or 3D
    numberOfBeads = 0 # Total number of beads in the system
    volume = 0 # (cubeLength * lengthInCubes) ** dimensions
    length = lengthInCubes * cubeLength
    noOfCubes = length ** dimensions
    beads = numberOfBeads
    cubes = []
    special = 0

    def __init__ (self, cubesInVolLength, cubeLength, dimensions, numberOfBeads):
        self.lengthInCubes = cubesInVolLength
        self.cubeLength = cubeLength
        self.dimensions = dimensions
        self.numberOfBeads = numberOfBeads
        self.volume = (self.cubeLength * self.lengthInCubes) ** self.dimensions
        self.length = self.lengthInCubes * self.cubeLength
        self.noOfCubes = self.length ** self.dimensions
        self.beads = numberOfBeads
        if (dimensions == 2):
            for i in range(0, cubesInVolLength):
                l = []
                for j in range(0, cubesInVolLength):
                    # newCube = Cube(i, j, self.cubeLength, 1, self.special, self)
                    newCube = Cube(i, j, 0, self.cubeLength, 0, self.special, self)
                    l.append(newCube)
                self.cubes.append(l)
        else:
            for i in range(0, cubesInVolLength):
                l = []
                for j in range(0, cubesInVolLength):
                    m = []
                    for k in range(0, cubesInVolLength):
                        newCube = Cube(i, j, k, self.cubeLength, 0, self.special, self)
                        m.append(newCube)
                    l.append(m)
                self.cubes.append(l)

class Cube:
    container = None
    length = 0
    noOfBeads = 0
    originCoord = Vector(0.0, 0.0, 0.0)
    arrayPosX = 0
    arrayPosY = 0
    arrayPosZ = 0
    beads = []

    last = None

    def __init__ (self, x, y, cubeLength, noOfBeads, special, container):
        self.length = cubeLength
        self.beads = []
        self.arrayPosX = x
        self.arrayPosY = y
        self.originCoord = Vector((x * cubeLength), (y * cubeLength), 0.0)
        self.container = container
        for i in range(0, noOfBeads):
            rng = random.SystemRandom()
            randX = rng.uniform(self.originCoord.x, (self.originCoord.x + (self.length)))
            randY = rng.uniform(self.originCoord.y, (self.originCoord.y + (self.length)))
            randVector = Vector(randX, randY, 0.0)
            newBead = BeadB(self, randVector, 0.0)
            self.beads.append(newBead)
            if (self.last != None):
                euclidianDistance(self.last.position, newBead.position)
            self.last = newBead;

    def __init__ (self, x, y, z, cubeLength, noOfBeads, special, container):
        self.length = cubeLength
        self.beads = []
        self.arrayPosX = x
        self.arrayPosY = y
        self.arrayPosZ = z
        self.originCoord = Vector((x * cubeLength), (y * cubeLength), (z * cubeLength))
        self.container = container
        for i in range(0, noOfBeads):
            rng = random.SystemRandom()
            randX = rng.uniform(self.originCoord.x, (self.originCoord.x + (self.length)))
            randY = rng.uniform(self.originCoord.y, (self.originCoord.y + (self.length)))
            randVector = Vector(randX, randY, 0.0)
            newBead = BeadB(self, randVector, 0.0)
            self.beads.append(newBead)
            if (self.last != None):
                euclidianDistance(self.last.position, newBead.position)
            self.last = newBead;

    def passBead(self, bead):
        cubesInVolLength = self.container.lengthInCubes
        x = bead.position.x
        y = bead.position.y
        z = bead.position.z
        newParentX = self.arrayPosX
        newParentY = self.arrayPosY
        newParentZ = self.arrayPosZ
        if (x >= self.originCoord.x + self.length):
            newParentX = self.arrayPosX + 1
            if (newParentX >= cubesInVolLength):
                newParentX = 0
                x = x - (cubesInVolLength * self.length)
        if (x < self.originCoord.x):
            newParentX = self.arrayPosX - 1
            if (newParentX < 0):
                newParentX = cubesInVolLength - 1;
                x = x + (cubesInVolLength * self.length)
        if (y >= self.originCoord.y + self.length):
            newParentY = self.arrayPosY + 1
            if (newParentY >= cubesInVolLength):
                newParentY = 0
                y = y - (cubesInVolLength * self.length)
        if (y < self.originCoord.y):
            newParentY = self.arrayPosY - 1
            if (newParentY < 0):
                newParentY = cubesInVolLength - 1;
                y = y + (cubesInVolLength * self.length)
        if (z >= self.originCoord.z + self.length):
            newParentZ = self.arrayPosZ + 1
            if (newParentZ >= cubesInVolLength):
                newParentZ = 0
                z = z - (cubesInVolLength * self.length)
        if (z < self.originCoord.z):
            newParentZ = self.arrayPosZ - 1
            if (newParentZ < 0):
                newParentZ = cubesInVolLength - 1;
                z = z + (cubesInVolLength * self.length)
        if (newParentX != self.arrayPosX or newParentY != self.arrayPosY or newParentZ != self.arrayPosZ):
            self.remove(bead)
            bead.position.x = x
            bead.position.y = y
            bead.position.z = z
            if (self.container.dimensions == 2):
                bead.container = self.container.cubes[newParentX][newParentY]
                self.container.cubes[newParentX][newParentY].beads.append(bead)
            else:
                bead.container = self.container.cubes[newParentX][newParentY][newParentZ]
                self.container.cubes[newParentX][newParentY][newParentZ].beads.append(bead)

    def remove(self, bead):
        for b in self.beads:
            if bead.position.x == b.position.x and bead.position.y == b.position.y and bead.position.z == b.position.z:
                self.beads.remove(b)
                return
