#!/usr/bin/env python3

import sys
import time
import math
import os
from src.Containers import *
from src.Beads import *
# from src.OldVisualiser import *
from src.Visualiser import *

cubesInVolLength = 10 # Number of squares in legnth, width and depth (square/cube required)
cubeLength = 1 # Number of pixels in each sub-cube
dimensions = 2 # Can be 2 or 3, for 2D or 3D
numberOfBeads = 400 # Total number of beads in the system
visualise = True
cubeLines = True
firstCalc = True
timestep = 0.01

# def passBeads(volume):
#     for b in volume.cubes[0][0][0].beads:
#         if (b.position.x < 0):
#             b.position.x += cubeLength
#         elif (b.position.x >= cubeLength):
#             b.position.x -= cubeLength
#         if (b.position.y < 0):
#             b.position.y += cubeLength
#         elif (b.position.y >= cubeLength):
#             b.position.y -= cubeLength
#         if (b.position.z < 0):
#             b.position.z += cubeLength
#         elif (b.position.z >= cubeLength):
#             b.position.z -= cubeLength

def passBeads(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            if (volume.dimensions == 2):
                cube = volume.cubes[i][j]
                beads = cube.beads
                for b in beads:
                    cube.passBead(b)
            else:
                for k in range(0, cubesInVolLength):
                    cube = volume.cubes[i][j][k]
                    beads = cube.beads
                    for b in beads:
                        cube.passBead(b)

def updatePosition(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                rng = random.SystemRandom()
                b.move(rng.randint(-10, 10), rng.randint(-10, 10))

def performCalculations(volume):
    global firstCalc
    randNums = []
    randNum = random.SystemRandom().uniform(-1, 1)
    randNums.append((2, randNum))
    randNum = random.SystemRandom().uniform(-1, 1)
    randNums.append((3, randNum))
    randNum = random.SystemRandom().uniform(-1, 1)
    randNums.append((5, randNum))
    calculateVelocityHalfStep(volume)
    calculatePosition(volume)
    passBeads(volume)
    calculateAcceleration(volume, randNums)
    calculateVelocity(volume)

def calculateVelocityHalfStep(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            if (volume.dimensions == 2):
                for b in volume.cubes[i][j].beads:
                    b.velocityHalfStep = Vector.add(b.velocity, Vector.multiply(Vector.divide(b.acceleration, 2), timestep))
            else:
                for k in range(0, cubesInVolLength):
                    for b in volume.cubes[i][j][k].beads:
                        b.velocityHalfStep = Vector.add(b.velocity, Vector.multiply(Vector.divide(b.acceleration, 2), timestep))

def calculatePosition(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            if (volume.dimensions == 2):
                for b in volume.cubes[i][j].beads:
                    b.position = Vector.add(b.position, Vector.multiply(b.velocityHalfStep, timestep))
            else:
                for k in range(0, cubesInVolLength):
                    for b in volume.cubes[i][j][k].beads:
                        b.position = Vector.add(b.position, Vector.multiply(b.velocityHalfStep, timestep))

def calculateAcceleration(volume, randNums):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            if (volume.dimensions == 2):
                for b in volume.cubes[i][j].beads:
                    performLocalCalculations(volume, b, b.container, randNums)
                    performNeighbourhoodCalculations(volume, b, i, j, randNums)
                    f = Vector(0.0, 0.0, 0.0)
                    for v in b.conForce:
                        if (v != None):
                            f = Vector.add(f, v)
                    b.conForce = []
                    for v in b.randForce:
                        if (v != None):
                            f = Vector.add(f, v)
                    b.randForce = []
                    for v in b.dForce:
                        if (v != None):
                            f = Vector.add(f, v)
                    b.dForce = []
                    if (b.bondForce != None):
                        f = Vector.add(f, b.bondForce)
                    b.bondForce = None
                    b.acceleration = Vector.divide(f, b.mass)
            else:
                for k in range(0, cubesInVolLength):
                    for b in volume.cubes[i][j][k].beads:
                        performLocalCalculations(volume, b, b.container, randNums)
                        performNeighbourhoodCalculations3D(volume, b, i, j, k, randNums)
                        f = Vector(0.0, 0.0, 0.0)
                        for v in b.conForce:
                            if (v != None):
                                f = Vector.add(f, v)
                        b.conForce = []
                        for v in b.randForce:
                            if (v != None):
                                f = Vector.add(f, v)
                        b.randForce = []
                        for v in b.dForce:
                            if (v != None):
                                f = Vector.add(f, v)
                        b.dForce = []
                        if (b.bondForce != None):
                            f = Vector.add(f, b.bondForce)
                        b.bondForce = None
                        b.acceleration = Vector.divide(f, b.mass)

def calculateVelocity(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            if (volume.dimensions == 2):
                for b in volume.cubes[i][j].beads:
                    b.velocity = Vector.add(b.velocityHalfStep, Vector.divide(Vector.multiply(b.acceleration, timestep), 2))
            else:
                for k in range(0, cubesInVolLength):
                    for b in volume.cubes[i][j][k].beads:
                        b.velocity = Vector.add(b.velocityHalfStep, Vector.divide(Vector.multiply(b.acceleration, timestep), 2))

def performLocalCalculations(volume, b1, cube, randNums):
    for b2 in cube.beads:
        if (b1.position.x != b2.position.x or b1.position.y != b2.position.y or b1.position.z != b2.position.z):
            # if (b1.bond == None or b1.bond.getOtherBead != b2):
                eucDistance = euclidianDistance(volume, b1.position, b2.position)
                vectorDistance = Vector.subtract(b1.position, b2.position)
                b1.conForce.append(conservativeForce(b1, b2, eucDistance, vectorDistance))
                b1.randForce.append(randomForce(b1, b2, eucDistance, vectorDistance, timestep, randNums))
                b1.dForce.append(dragForce(b1, b2, eucDistance, vectorDistance))
                if (b1.bond != None and b1.bondForce == None):
                    b1.bond.calculateBondForce()

def performNeighbourhoodCalculations(volume, b, x, y, randNums):
    for xLoop in [x - 1, x, x + 1]:
        ipos = Vector(b.position.x, b.position.y, 0.0)
        jposOffset = Vector(0.0, 0.0, 0.0)
        if (xLoop < 0):
            xTest = cubesInVolLength - 1
            ipos.x = ipos.x + (volume.length)
        elif (xLoop >= cubesInVolLength):
            xTest = 0
            jposOffset.x = jposOffset.x + (volume.length)
        else:
            xTest = xLoop

        for yLoop in [y - 1, y, y + 1]:
            ipos.y = b.position.y
            jposOffset.y = 0.0
            if (xLoop != x or yLoop != y):
                if (yLoop < 0):
                    yTest = cubesInVolLength - 1
                    ipos.y = ipos.y + (volume.length)
                elif (yLoop >= cubesInVolLength):
                    yTest = 0
                    jposOffset.y = jposOffset.y + (volume.length)
                else:
                    yTest = yLoop

                for b2 in volume.cubes[xTest][yTest].beads:
                    # if (b.bond == None or b.bond.getOtherBead != b2):
                        jpos = Vector.add(b2.position, jposOffset)
                        eucDistance = euclidianDistance(volume, b.position, b2.position)
                        vectorDistance = Vector.subtract(ipos, jpos)
                        b.conForce.append(conservativeForce(b, b2, eucDistance, vectorDistance))
                        b.randForce.append(randomForce(b, b2, eucDistance, vectorDistance, timestep, randNums))
                        b.dForce.append(dragForce(b, b2, eucDistance, vectorDistance))

def performNeighbourhoodCalculations3D(volume, b, x, y, z, randNums):
    for xLoop in [x - 1, x, x + 1]:
        ipos = Vector(b.position.x, b.position.y, b.position.z)
        jposOffset = Vector(0.0, 0.0, 0.0)
        if (xLoop < 0):
            xTest = cubesInVolLength - 1
            ipos.x = ipos.x + (volume.length)
        elif (xLoop >= cubesInVolLength):
            xTest = 0
            jposOffset.x = jposOffset.x + (volume.length)
        else:
            xTest = xLoop

        for yLoop in [y - 1, y, y + 1]:
            ipos.y = b.position.y
            jposOffset.y = 0.0
            if (yLoop < 0):
                yTest = cubesInVolLength - 1
                ipos.y = ipos.y + (volume.length)
            elif (yLoop >= cubesInVolLength):
                yTest = 0
                jposOffset.y = jposOffset.y + (volume.length)
            else:
                yTest = yLoop

            for zLoop in [z - 1, z, z + 1]:
                ipos.z = b.position.z
                jposOffset.z = 0.0
                if (xLoop != x or yLoop != y or zLoop != z):
                    if (zLoop < 0):
                        zTest = cubesInVolLength - 1
                        ipos.z = ipos.z + (volume.length)
                    elif (zLoop >= cubesInVolLength):
                        zTest = 0
                        jposOffset.z = jposOffset.z + (volume.length)
                    else:
                        zTest = zLoop

                    for b2 in volume.cubes[xTest][yTest][zTest].beads:
                        jpos = Vector.add(b2.position, jposOffset)
                        eucDistance = euclidianDistance(volume, ipos, jpos)
                        vectorDistance = Vector.subtract(ipos, jpos)
                        b.conForce.append(conservativeForce(b, b2, eucDistance, vectorDistance))
                        b.randForce.append(randomForce(b, b2, eucDistance, vectorDistance, timestep, randNums))
                        b.dForce.append(dragForce(b, b2, eucDistance, vectorDistance))

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
waterTest3D(v, 150, 20, 20)

prepVisualisation(v)

# time.sleep(3)

while True:
    performCalculations(v)
    updateVisualisation(v)
    # updatePosition(v) # Randomly move beads (no calculations involved)
    # passBeads(v)
    time.sleep(0.05)
    # time.sleep(3)
