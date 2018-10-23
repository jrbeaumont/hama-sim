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

def addBeads(volume, aN, bN):
    cubeX = 0
    cubeY = 0
    for a in range(0, aN):
        randX = random.SystemRandom().uniform(0, 20)
        randY = random.SystemRandom().uniform(0, 20)
        randVector = Vector(randX, randY, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j].originCoord.y >= randY):
                cubeY = j - 1
                break
        volume.cubes[cubeX][cubeY].beads.append(BeadA(volume.cubes[cubeX][cubeY], randVector))
    for b in range(0, bN):
        randX = random.SystemRandom().uniform(0, 20)
        randY = random.SystemRandom().uniform(0, 20)
        randVector = Vector(randX, randY, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j].originCoord.y >= randY):
                cubeY = j - 1
                break
        volume.cubes[cubeX][cubeY].beads.append(BeadB(volume.cubes[cubeX][cubeY], randVector))

def waterTest(volume, wN, aN, bN, bonds):
    cubeX = 0
    cubeY = 0
    for a in range(0, wN):
        randX = random.SystemRandom().uniform(0, 20)
        randY = random.SystemRandom().uniform(0, 20)
        randVector = Vector(randX, randY, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j].originCoord.y >= randY):
                cubeY = j - 1
                break
        volume.cubes[cubeX][cubeY].beads.append(BeadC(volume.cubes[cubeX][cubeY], randVector))
    for a in range(0, aN):
        randX = random.SystemRandom().uniform(0, 20)
        randY = random.SystemRandom().uniform(0, 20)
        randVector = Vector(randX, randY, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j].originCoord.y >= randY):
                cubeY = j - 1
                break
        volume.cubes[cubeX][cubeY].beads.append(BeadA(volume.cubes[cubeX][cubeY], randVector))
    for b in range(0, bN):
        randX = random.SystemRandom().uniform(0, 20)
        randY = random.SystemRandom().uniform(0, 20)
        randVector = Vector(randX, randY, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j].originCoord.y >= randY):
                cubeY = j - 1
                break
        volume.cubes[cubeX][cubeY].beads.append(BeadB(volume.cubes[cubeX][cubeY], randVector))

    # GENERATE SOME BONDED BEADS PLEASE
    for c in range(0, bonds):
        randX = random.SystemRandom().uniform(0, 20)
        randY = random.SystemRandom().uniform(0, 20)
        randVector1 = Vector(randX, randY, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0].originCoord.x >= randX):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j].originCoord.y >= randY):
                cubeY = j - 1
                break
        bead1 = BeadA(volume.cubes[cubeX][cubeY], randVector1)
        volume.cubes[cubeX][cubeY].beads.append(bead1)
        randX2 = randX + random.SystemRandom().uniform(-1, 1)
        randY2 = randY + random.SystemRandom().uniform(-1, 1)
        if (randX2 > 20):
            randX2 = randX2 - 20
        elif (randX2 < 0):
            randX2 = randX2 + 20
        if (randY2 > 20):
            randY2 = randY2 - 20
        elif (randY2 < 0):
            randY2 = randY2 + 20
        randVector2 = Vector(randX2, randY2, 0.0)
        for i in range(0, cubesInVolLength):
            cubeX = i
            if (volume.cubes[i][0].originCoord.x >= randX2):
                cubeX = i - 1
                break
        for j in range(0, cubesInVolLength):
            cubeY = j
            if (volume.cubes[cubeX][j].originCoord.y >= randY2):
                cubeY = j - 1
                break
        bead2 = BeadB(volume.cubes[cubeX][cubeY], randVector2)
        volume.cubes[cubeX][cubeY].beads.append(bead2)
        Bond(bead1, bead2)

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

# def addBeads(volume, aN):
#     cubeX = 0
#     cubeY = 0
#     for a in range(0, aN):
#         randX = random.SystemRandom().uniform(0, 20)
#         randY = random.SystemRandom().uniform(0, 20)
#         randVector = Vector(randX, randY)
#         for i in range(0, cubesInVolLength):
#             cubeX = i
#             if (volume.cubes[i][0].originCoord.x >= randX):
#                 cubeX = i - 1
#                 break
#         for j in range(0, cubesInVolLength):
#             cubeY = j
#             if (volume.cubes[cubeX][j].originCoord.y >= randY):
#                 cubeY = j - 1
#                 break
#         volume.cubes[cubeX][cubeY].beads.append(BeadB(volume.cubes[cubeX][cubeY], randVector))

# def addBeads(volume):
#     for i in range(0, cubesInVolLength):
#         for j in range(0, cubesInVolLength):
#             cube = volume.cubes[i][j]
#             cube.beads.append(BeadB(cube, Vector(cube.originCoord.x + 0.5, cube.originCoord.y + 0.5)))
#             cube.beads.append(BeadA(cube, Vector(cube.originCoord.x + 1.5 + 0.05, cube.originCoord.y + 0.5 + 0.05)))
#             cube.beads.append(BeadB(cube, Vector(cube.originCoord.x + 0.5, cube.originCoord.y + 1.5)))
#             cube.beads.append(BeadA(cube, Vector(cube.originCoord.x + 1.5 + 0.05, cube.originCoord.y + 1.5 + 0.05)))

# def addBeads(volume):
#             volume.cubes[2][2].beads.append(BeadB(volume.cubes[2][2], Vector(5.5, 5.5)))
#             volume.cubes[2][2].beads.append(BeadB(volume.cubes[2][2], Vector(5.75, 5.5)))

# v = Container(cubesInVolLength, cubeLength, 2, numberOfBeads)
# addBeads(v, 200, 200)
# addBeads(v, 450)
# addBeads(v)
# waterTest(v, 300, 10, 40)
# waterTest(v, 350, 60, 50, 0)

v = Container(cubesInVolLength, cubeLength, 3, 0)
waterTest3D(v, 1500, 200, 100)

prepVisualisation(v)

# time.sleep(3)

while True:
    performCalculations(v, timestep)
    updateVisualisation(v)
    # updatePosition(v) # Randomly move beads (no calculations involved)
    # passBeads(v)
    time.sleep(0.05)
    # time.sleep(3)
