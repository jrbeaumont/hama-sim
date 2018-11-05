import sys

sys.path.append('.')

import time

from src.Beads import *
from src.Calculations import *
from src.Containers import *
from src.Visualiser import *

allBeads = []
bondedBeads = []
allBonds = []

class BeadW(Bead):
    typeName = "Water"
    colour = "#0000ff"
    mass = 1.0
    cutoffRadius = 1.0
    typeNumber = 0

class BeadB(Bead):
    typeName = "Yellow Oil"
    colour = "#00ff00"
    mass = 1.0
    cutoffRadius = 1.0
    typeNumber = 1

interactionMatrix = [
 #    W   B
 # W
    [ 25, 25 ],
 # B
    [ 25, 25 ],
]

def addBeads(container, nW, nB):
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

    prevBead = None
    beadX = 4.25
    beadY = 4.25
    beadZ = 4.25
    for a in range(0, nB):
        vector = Vector(beadX, beadY, beadZ)
        for i in range(0, container.lengthInCubes):
            cubeX = i
            if (container.cubes[i][0][0].originCoord.x >= beadX):
                cubeX = i - 1
                break
        for j in range(0, container.lengthInCubes):
            cubeY = j
            if (container.cubes[cubeX][j][0].originCoord.y >= beadY):
                cubeY = j - 1
                break
        for k in range(0, container.lengthInCubes):
            cubeZ = k
            if (container.cubes[cubeX][cubeY][k].originCoord.z >= beadZ):
                cubeZ = k - 1
                break
        beadX -= 0.5
        # beadY -= 0.5
        # beadZ -= 0.5
        if (beadX < 0):
            beadX = 9.75
            # beadY = 9.75
            # beadZ = 9.75
        bead = BeadB(container.cubes[cubeX][cubeY][cubeZ], vector, interactionMatrix[BeadB.typeNumber])
        container.cubes[cubeX][cubeY][cubeZ].beads.append(bead)
        allBeads.append(bead)
        if (prevBead != None):
            bond = Bond(0.5, 128, prevBead, bead)
            prevBead.bonds.append(bond)
            bead.bonds.append(bond)
            allBonds.append(bond)
        bondedBeads.append(bead)
        prevBead = bead

def clearVisitedBonds(bs):
    for b in bs:
        b.bondsVisited = []

def averageBondLengths(bs):
    result = 0.0
    for b in bs:
        result += b.currentLength
        # print(b.currentLength)
    result /= len(bs)
    print("AVERAGE BOND LENGTH = " + str(result))

volX = 10
volY = 10
volZ = 10
cubeLength = 1
cubesPerDimension = 10
timestep = 0.02
temperature = 1

v = Container(cubesPerDimension, cubeLength, 3, temperature)
addBeads(v, 1990, 10)

prepVisualisation(v)
orderedUpdateVis(allBeads)

c = 0
while True:
    clearVisitedBonds(bondedBeads)
    # averageBondLengths(allBonds)
    performCalculations(v, timestep)
    orderedUpdateVis(allBeads)
