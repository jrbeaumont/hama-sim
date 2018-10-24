import sys

sys.path.append('.')

import time

from src.Beads import *
from src.Calculations import *
from src.Containers import *
from src.Visualiser import *

allBeads = []

class BeadW(Bead):
    typeName = "Water"
    colour = "#0000ff"
    mass = 1.0
    cutoffRadius = 1.0
    typeNumber = 0

class BeadY(Bead):
    typeName = "Yellow Oil"
    colour = "#00ff00"
    mass = 1.0
    cutoffRadius = 1.0
    typeNumber = 1

class BeadR(Bead):
    typeName = "Red Oil"
    colour = "#ff0000"
    mass = 1.0
    cutoffRadius = 1.0
    typeNumber = 2

interactionMatrix = [
 #    W   Y   R
 # W
    [ 25, 75, 35 ],
 # Y
    [ 75, 25, 50 ],
 # R
    [ 35, 50, 25 ]
]

def addBeads(container, nW, nY, nR):
    cubeX = 0
    cubeY = 0
    cubeZ = 0
    for a in range(0, nW):
        randX = random.SystemRandom().uniform(0, container.cubeLength * container.lengthInCubes)
        randY = random.SystemRandom().uniform(0, container.cubeLength * container.lengthInCubes)
        randZ = random.SystemRandom().uniform(0, container.cubeLength * container.lengthInCubes)
        randVector = Vector(randX, randY, randZ)
        # randVector = Vector(randX, randY, 0.0)
        for i in range(0, container.lengthInCubes):
            cubeX = i
            if (container.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, container.lengthInCubes):
            cubeY = j
            if (container.cubes[cubeX][j][0].originCoord.y >= randY):
                cubeY = j - 1
                break
        for k in range(0, container.lengthInCubes):
            cubeZ = k
            if (container.cubes[cubeX][cubeY][k].originCoord.z >= randZ):
                cubeZ = k - 1
                break
        bead = BeadW(container.cubes[cubeX][cubeY][cubeZ], randVector, interactionMatrix[BeadW.typeNumber])
        container.cubes[cubeX][cubeY][cubeZ].beads.append(bead)
        allBeads.append(bead)
    for a in range(0, nY):
        randX = random.SystemRandom().uniform(0, container.cubeLength * container.lengthInCubes)
        randY = random.SystemRandom().uniform(0, container.cubeLength * container.lengthInCubes)
        randZ = random.SystemRandom().uniform(0, container.cubeLength * container.lengthInCubes)
        randVector = Vector(randX, randY, randZ)
        # randVector = Vector(randX, randY, 0.0)
        for i in range(0, container.lengthInCubes):
            cubeX = i
            if (container.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, container.lengthInCubes):
            cubeY = j
            if (container.cubes[cubeX][j][0].originCoord.y >= randY):
                cubeY = j - 1
                break
        for k in range(0, container.lengthInCubes):
            cubeZ = k
            if (container.cubes[cubeX][cubeY][k].originCoord.z >= randZ):
                cubeZ = k - 1
                break
        bead = BeadY(container.cubes[cubeX][cubeY][cubeZ], randVector, interactionMatrix[BeadY.typeNumber])
        container.cubes[cubeX][cubeY][cubeZ].beads.append(bead)
        allBeads.append(bead)
    for b in range(0, nR):
        randX = random.SystemRandom().uniform(0, container.cubeLength * container.lengthInCubes)
        randY = random.SystemRandom().uniform(0, container.cubeLength * container.lengthInCubes)
        randZ = random.SystemRandom().uniform(0, container.cubeLength * container.lengthInCubes)
        randVector = Vector(randX, randY, randZ)
        # randVector = Vector(randX, randY, 0.0)
        for i in range(0, container.lengthInCubes):
            cubeX = i
            if (container.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, container.lengthInCubes):
            cubeY = j
            if (container.cubes[cubeX][j][0].originCoord.y >= randY):
                cubeY = j - 1
                break
        for k in range(0, container.lengthInCubes):
            cubeZ = k
            if (container.cubes[cubeX][cubeY][k].originCoord.z >= randZ):
                cubeZ = k - 1
                break
        bead = BeadR(container.cubes[cubeX][cubeY][cubeZ], randVector, interactionMatrix[BeadR.typeNumber])
        container.cubes[cubeX][cubeY][cubeZ].beads.append(bead)
        allBeads.append(bead)

volX = 10
volY = 10
volZ = 10
cubeLength = 1
cubesPerDimension = 10
timestep = 0.02

v = Container(cubesPerDimension, cubeLength, 3, 1)
addBeads(v, 600, 300, 100)

prepVisualisation(v)
orderedUpdateVis(allBeads)

c = 0
while True:
    performCalculations(v, timestep)
    # if (c >= 10):
    # updateVisualisation(v)
    orderedUpdateVis(allBeads)
        # c = 0
    # else:
        # c += 1
    # time.sleep(5)
