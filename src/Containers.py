from coordinates import Coordinate
import random
from src.Beads import *

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
    special = False

    def __init__ (self, cubesInVolLength, cubeLength, dimensions, numberOfBeads):
        self.lengthInCubes = cubesInVolLength
        self.cubeLength = cubeLength
        self.dimensions = dimensions
        self.numberOfBeads = numberOfBeads
        self.volume = (self.cubeLength * self.lengthInCubes) ** self.dimensions
        self.length = self.lengthInCubes * self.cubeLength
        self.noOfCubes = self.length ** self.dimensions
        self.beads = numberOfBeads
        for i in range(0, cubesInVolLength):
            l = []
            for j in range(0, cubesInVolLength):
                newCube = Cube(i, j, self.cubeLength, 10, self.special, self)
                l.append(newCube);
            self.cubes.append(l)

class Cube:
    container = None
    length = 0
    noOfBeads = 0
    originCoord = Coordinate(x = 0, y = 0)
    arrayPosX = 0
    arrayPosY = 0
    beads = []

    last = None

    def __init__ (self, x, y, cubeLength, noOfBeads, special, container):
        self.length = cubeLength
        self.beads = []
        self.arrayPosX = x
        self.arrayPosY = y
        self.originCoord = Coordinate(x = (x * cubeLength), y = (y * cubeLength))
        self.container = container
        for i in range(0, noOfBeads):
            rng = random.SystemRandom()
            randX = rng.randint(self.originCoord.x, (self.originCoord.x + (self.length - 1)))
            randY = rng.randint(self.originCoord.y, (self.originCoord.y + (self.length - 1)))
            if special == False:
                newBead = BeadA(self, Coordinate(x = randX, y = randY))
                special = True
            else:
                newBead = BeadB(self, Coordinate(x = randX, y = randY))
            self.beads.append(newBead)
            if (self.last != None):
                euclidianDistance(self.last.position, newBead.position)
            self.last = newBead;

    def passBead(self, bead):
        cubesInVolLength = self.container.lengthInCubes
        x = bead.position.x
        y = bead.position.y
        newParentX = self.arrayPosX
        newParentY = self.arrayPosY
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
        if (newParentX != self.arrayPosX or newParentY != self.arrayPosY):
            self.remove(bead)
            bead.position.x = x
            bead.position.y = y
            bead.parent = self.container.cubes[newParentX][newParentY]
            self.container.cubes[newParentX][newParentY].beads.append(bead)
            # if (bead.beadType == "A"):
                # print("A special bead is moving")

    def remove(self, bead):
        for b in self.beads:
            if bead.position.x == b.position.x and bead.position.y == b.position.y:
                self.beads.remove(b)
                return
