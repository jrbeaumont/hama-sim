#!/usr/bin/env python3

import sys
import time
import math
import os
from src.Containers import *
from src.Beads import *
# from src.OldVisualiser import *
from src.Visualiser import *
from src.Calculations import *

cubesInVolLength = 10 # Number of squares in legnth, width and depth (square/cube required)
cubeLength = 1 # Number of pixels in each sub-cube
dimensions = 2 # Can be 2 or 3, for 2D or 3D
numberOfBeads = 400 # Total number of beads in the system
visualise = True
cubeLines = True
firstCalc = True
timestep = 0.01

def waterTestY(volume, wN, aN, bN, bonds):
    cubeX = 0
    cubeY = 0
    for a in range(0, wN):
        randX = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randY = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(randX, randY, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j][0].originCoord.y >= randY):
                cubeY = j - 1
                break
        volume.cubes[cubeX][cubeY][0].beads.append(BeadC(volume.cubes[cubeX][cubeY][0], randVector))
    for a in range(0, aN):
        randX = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randY = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(randX, randY, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j][0].originCoord.y >= randY):
                cubeY = j - 1
                break
        volume.cubes[cubeX][cubeY][0].beads.append(BeadA(volume.cubes[cubeX][cubeY][0], randVector))
    for b in range(0, bN):
        randX = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randY = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(randX, randY, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j][0].originCoord.y >= randY):
                cubeY = j - 1
                break
        volume.cubes[cubeX][cubeY][0].beads.append(BeadB(volume.cubes[cubeX][cubeY][0], randVector))

def waterTestZ(volume, wN, aN, bN, bonds):
    cubeX = 0
    cubeZ = 0
    for a in range(0, wN):
        randX = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randZ = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(randX, 0.0, randZ)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeZ = j
            if (volume.cubes[cubeX][0][j].originCoord.z >= randZ):
                cubeZ = j - 1
                break
        volume.cubes[cubeX][0][cubeZ].beads.append(BeadC(volume.cubes[cubeX][0][cubeZ], randVector))
    for a in range(0, aN):
        randX = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randZ = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(randX, 0.0, randZ)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeZ = j
            if (volume.cubes[cubeX][0][j].originCoord.z >= randZ):
                cubeZ = j - 1
                break
        volume.cubes[cubeX][0][cubeZ].beads.append(BeadA(volume.cubes[cubeX][0][cubeZ], randVector))
    for b in range(0, bN):
        randX = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randZ = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(randX, 0.0, randZ)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeZ = j
            if (volume.cubes[cubeX][0][j].originCoord.z >= randZ):
                cubeY = j - 1
                break
        volume.cubes[cubeX][0][cubeY].beads.append(BeadB(volume.cubes[cubeX][0][cubeY], randVector))

def waterTestYZ(volume, wN, aN, bN, bonds):
    cubeY = 0
    cubeZ = 0
    for a in range(0, wN):
        randY = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randZ = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(0.0, randY, randZ)
        for i in range(0, cubesInVolLength):
            cubeY = i
            if (volume.cubes[0][i][0].originCoord.y >= randY):
                cubeY = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeZ = j
            if (volume.cubes[0][cubeY][j].originCoord.z >= randZ):
                cubeZ = j - 1
                break
        volume.cubes[0][cubeY][cubeZ].beads.append(BeadC(volume.cubes[0][cubeY][cubeZ], randVector))
    for a in range(0, aN):
        randY = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randZ = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(0.0, randY, randZ)
        for i in range(0, cubesInVolLength):
            cubeY = i
            if (volume.cubes[0][i][0].originCoord.y >= randY):
                cubeY = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeZ = j
            if (volume.cubes[0][cubeY][j].originCoord.z >= randZ):
                cubeZ = j - 1
                break
        volume.cubes[0][cubeY][cubeZ].beads.append(BeadA(volume.cubes[0][cubeY][cubeZ], randVector))
    for b in range(0, bN):
        randY = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randZ = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(0.0, randY, randZ)
        for i in range(0, cubesInVolLength):
            cubeY = i
            if (volume.cubes[0][i][0].originCoord.y >= randY):
                cubeY = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeZ = j
            if (volume.cubes[0][cubeY][j].originCoord.z >= randZ):
                cubeZ = j - 1
                break
        volume.cubes[0][cubeY][cubeZ].beads.append(BeadB(volume.cubes[0][cubeY][cubeZ], randVector))

    # GENERATE SOME BONDED BEADS PLEASE
    # for c in range(0, bonds):
    #     randX = random.SystemRandom().uniform(0, 20)
    #     randY = random.SystemRandom().uniform(0, 20)
    #     randVector1 = Vector(randX, randY, 0.0)
    #     for i in range(0, cubesInVolLength):
    #         cubeX = i
    #         if (volume.cubes[i][0].originCoord.x >= randX):
    #             cubeX = i - 1
    #             break
    #     for j in range(0, cubesInVolLength):
    #         cubeY = j
    #         if (volume.cubes[cubeX][j].originCoord.y >= randY):
    #             cubeY = j - 1
    #             break
    #     bead1 = BeadA(volume.cubes[cubeX][cubeY], randVector1)
    #     volume.cubes[cubeX][cubeY].beads.append(bead1)
    #     randX2 = randX + random.SystemRandom().uniform(-1, 1)
    #     randY2 = randY + random.SystemRandom().uniform(-1, 1)
    #     if (randX2 > 20):
    #         randX2 = randX2 - 20
    #     elif (randX2 < 0):
    #         randX2 = randX2 + 20
    #     if (randY2 > 20):
    #         randY2 = randY2 - 20
    #     elif (randY2 < 0):
    #         randY2 = randY2 + 20
    #     randVector2 = Vector(randX2, randY2, 0.0)
    #     for i in range(0, cubesInVolLength):
    #         cubeX = i
    #         if (volume.cubes[i][0].originCoord.x >= randX2):
    #             cubeX = i - 1
    #             break
    #     for j in range(0, cubesInVolLength):
    #         cubeY = j
    #         if (volume.cubes[cubeX][j].originCoord.y >= randY2):
    #             cubeY = j - 1
    #             break
    #     bead2 = BeadB(volume.cubes[cubeX][cubeY], randVector2)
    #     volume.cubes[cubeX][cubeY].beads.append(bead2)
    #     Bond(bead1, bead2)

def waterTest3D(volume, wN, aN, bN):
    cubeX = 0
    cubeY = 0
    for a in range(0, wN):
        randX = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randY = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randZ = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(randX, randY, randZ)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j][0].originCoord.y >= randY):
                cubeY = j - 1
                break
        for k in range(0, cubesInVolLength):
            cubeZ = k
            if (volume.cubes[cubeX][cubeY][k].originCoord.z >= randZ):
                cubeZ = k - 1
                break
        volume.cubes[cubeX][cubeY][cubeZ].beads.append(BeadC(volume.cubes[cubeX][cubeY][cubeZ], randVector))
    for a in range(0, aN):
        randX = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randY = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randZ = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(randX, randY, randZ)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j][0].originCoord.y >= randY):
                cubeY = j - 1
                break
        for k in range(0, cubesInVolLength):
            cubeZ = k
            if (volume.cubes[cubeX][cubeY][k].originCoord.z >= randZ):
                cubeZ = k - 1
                break
        volume.cubes[cubeX][cubeY][cubeZ].beads.append(BeadA(volume.cubes[cubeX][cubeY][cubeZ], randVector))
    for b in range(0, bN):
        randX = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randY = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randZ = random.SystemRandom().uniform(0, cubeLength * cubesInVolLength)
        randVector = Vector(randX, randY, randZ)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j][0].originCoord.y >= randY):
                cubeY = j - 1
                break
        for k in range(0, cubesInVolLength):
            cubeZ = k
            if (volume.cubes[cubeX][cubeY][k].originCoord.z >= randZ):
                cubeZ = k - 1
                break
        volume.cubes[cubeX][cubeY][cubeZ].beads.append(BeadB(volume.cubes[cubeX][cubeY][cubeZ], randVector))

    # GENERATE SOME BONDED BEADS PLEASE
    # for c in range(0, bonds):
    #     randX = random.SystemRandom().uniform(0, 20)
    #     randY = random.SystemRandom().uniform(0, 20)
    #     randZ = random.SystemRandom().uniform(0, 20)
    #     randVector1 = Vector(randX, randY, randZ)
    #     for i in range(0, cubesInVolLength):
    #         cubeX = i
    #         if (volume.cubes[i][0][0].originCoord.x >= randX):
    #             cubeX = i - 1
    #             break
    #     for j in range(0, cubesInVolLength):
    #         cubeY = j
    #         if (volume.cubes[cubeX][j][0].originCoord.y >= randY):
    #             cubeY = j - 1
    #             break
    #     for k in range(0, cubesInVolLength):
    #         cubeZ = k
    #         if (volume.cubes[cubeX][cubeY][k].originCoord.z >= randZ):
    #             cubeZ = k - 1
    #             break
    #     bead1 = BeadA(volume.cubes[cubeX][cubeY][cubeZ], randVector1)
    #     volume.cubes[cubeX][cubeY][cubeZ].beads.append(bead1)
    #     randX2 = randX + random.SystemRandom().uniform(-1, 1)
    #     randY2 = randY + random.SystemRandom().uniform(-1, 1)
    #     randZ2 = randZ + random.SystemRandom().uniform(-1, 1)
    #     if (randX2 > 20):
    #         randX2 = randX2 - 20
    #     elif (randX2 < 0):
    #         randX2 = randX2 + 20
    #     if (randY2 > 20):
    #         randY2 = randY2 - 20
    #     elif (randY2 < 0):
    #         randY2 = randY2 + 20
    #     if (randZ2 > 20):
    #         randZ2 = randZ2 - 20
    #     elif (randZ2 < 0):
    #         randZ2 = randZ2 + 20
    #     randVector2 = Vector(randX2, randY2, randZ2)
    #     for i in range(0, cubesInVolLength):
    #         cubeX = i
    #         if (volume.cubes[i][0][0].originCoord.x >= randX2):
    #             cubeX = i - 1
    #             break
    #     for j in range(0, cubesInVolLength):
    #         cubeY = j
    #         if (volume.cubes[cubeX][j][0].originCoord.y >= randY2):
    #             cubeY = j - 1
    #             break
    #     for k in range(0, cubesInVolLength):
    #         cubeZ = k
    #         if (volume.cubes[cubeX][cubeY][k].originCoord.z >= randZ2):
    #             cubeZ = k - 1
    #             break
    #     bead2 = BeadB(volume.cubes[cubeX][cubeY][cubeZ], randVector2)
    #     volume.cubes[cubeX][cubeY][cubeZ].beads.append(bead2)
    #     Bond(bead1, bead2)

v = Container(cubesInVolLength, cubeLength, 3, 0)
# waterTest3D(v, 1500, 200, 100)
# waterTestY(v, 75, 25, 15, 0)
# waterTestZ(v, 75, 25, 15, 0)
waterTestYZ(v, 75, 25, 15, 0)

prepVisualisation(v)
# prepareVisualisation(v)
# prepareCubeLines(v)

# time.sleep(3)
while True:
    performCalculations(v, timestep)
    updateVisualisation(v)
    # updateBeadVisualisationY(v)
    # updateBeadVisualisationZ(v)
    # updateBeadVisualisationYZ(v)
    time.sleep(0.05)
    # time.sleep(3)
