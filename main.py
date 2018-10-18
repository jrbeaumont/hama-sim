#!/usr/bin/env python3

import sys
import time
import math
import os
from src.Containers import *
from src.Beads import *

cubesInVolLength = 10 # Number of squares in legnth, width and depth (square/cube required)
cubeLength = 2 # Number of pixels in each sub-cube
dimensions = 2 # Can be 2 or 3, for 2D or 3D
numberOfBeads = 400 # Total number of beads in the system
visualise = True
cubeLines = True
firstCalc = True
timestep = 0.01

def passBeads(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            cube = volume.cubes[i][j]
            beads = cube.beads
            for b in beads:
                cube.passBead(b)

def updateBeadVisualisation(volume):
    o = "{\n"
    o+= "\t\"beads\": [\n"
    beads = []
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            c = 0
            for b in volume.cubes[i][j].beads:
                o+="\t\t{\"id\": \""+ b.ID +"\", "
                o+="\"x\": " + str(b.position.x) + ", \"y\": " + str(b.position.y) + ", "
                o+= "\"type\": \"" + b.typeName + "\"},"
                o+="\n"
                c += 1
    o = o[:-2]
    o+="\n\t]\n"
    o+= '}\n'
    print(o)
    sys.stdout.flush()

def prepareVisualisation(volume):
    o = "{\n"
    o+= "\t\"volume\": [\n"
    o+="\t\t{\"length\": " + str(volume.length) + "}\n"
    o+="\t]\n"
    o+= '}\n'
    print(o)
    sys.stdout.flush()
    beadTypes = allBeadTypes()
    p = "{\n"
    p+= "\t\"beadType\": [\n"
    for t in beadTypes:
        p+="\t\t{\"name\": \"" + str(t[0]) + "\", \"colour\": \"" + str(t[1]) + "\", \"cutoff\": " + str(t[2]) + "},\n"
    p = p[:-2]
    p+="\n\t]\n"
    p+= '}\n'
    print(p)
    sys.stdout.flush()
    updateBeadVisualisation(volume)

def prepareCubeLines(volume):
    o = "{\n"
    o+= "\t\"lines\": [\n"
    for i in range(1, cubesInVolLength):
        staticPos = i * cubeLength;
        maxVal = cubeLength * cubesInVolLength;
        o+="\t\t{\"x1\": " + str(staticPos) + ", \"y1\": 0, \"x2\": " + str(staticPos) + ", \"y2\": " + str(maxVal)+ "},\n"
        o+="\t\t{\"x1\": 0" + ", \"y1\": " + str(staticPos) + ", \"x2\": " + str(maxVal) + ", \"y2\": " + str(staticPos)+ "},\n"
    o = o[:-2]
    o+="\n\t]\n"
    o+= '}\n'
    print(o)
    sys.stdout.flush()

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
    calculateVelocityHafStep(volume)
    calculatePosition(volume)
    calculateAcceleration(volume, randNums)
    calculateVelocity(volume)


def calculateVelocityHafStep(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                b.velocityHalfStep = Vector.add(b.velocity, Vector.multiply(Vector.divide(b.acceleration, 2), timestep))

def calculatePosition(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                b.position = Vector.add(b.position, Vector.multiply(b.velocityHalfStep, timestep))

def calculateAcceleration(volume, randNums):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                performLocalCalculations(b, b.container, randNums)
                performNeighbourhoodCalculations(volume, b, i, j, randNums)
                f = Vector(0.0, 0.0)
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
                b.acceleration = Vector.divide(f, b.mass)

def calculateVelocity(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                b.velocity = Vector.add(b.velocityHalfStep, Vector.divide(Vector.multiply(b.acceleration, timestep), 2))

def performLocalCalculations(b1, cube, randNums):
    for b2 in cube.beads:
        if (b1.position.x != b2.position.x or b1.position.y != b2.position.y):
            eucDistance = euclidianDistance(b1.position, b2.position)
            vectorDistance = Vector.subtract(b1.position, b2.position)
            b1.conForce.append(conservativeForce(b1, b2, eucDistance, vectorDistance))
            b1.randForce.append(randomForce(b1, b2, eucDistance, vectorDistance, timestep, randNums))
            b1.dForce.append(dragForce(b1, b2, eucDistance, vectorDistance))

def performNeighbourhoodCalculations(volume, b, x, y, randNums):
    for xLoop in [x - 1, x, x + 1]:
        ipos = Vector(b.position.x, b.position.y)
        jposOffset = Vector(0.0, 0.0)
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
                    jpos = Vector.add(b2.position, jposOffset)
                    eucDistance = euclidianDistance(ipos, jpos)
                    vectorDistance = Vector.subtract(ipos, jpos)
                    b.conForce.append(conservativeForce(b, b2, eucDistance, vectorDistance))
                    b.randForce.append(randomForce(b, b2, eucDistance, vectorDistance, timestep, randNums))
                    b.dForce.append(dragForce(b, b2, eucDistance, vectorDistance))

# def addBeads(volume, aN, bN):
#     cubeX = 0
#     cubeY = 0
#     for a in range(0, aN):
#         randX = random.SystemRandom().uniform(0, 10)
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
#         volume.cubes[cubeX][cubeY].beads.append(BeadA(volume.cubes[cubeX][cubeY], randVector))
#     for b in range(0, bN):
#         randX = random.SystemRandom().uniform(11, 20)
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

def addBeads(volume, aN, bN):
    cubeX = 0
    cubeY = 0
    for a in range(0, aN):
        randX = random.SystemRandom().uniform(0, 20)
        randY = random.SystemRandom().uniform(0, 20)
        randVector = Vector(randX, randY)
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
        randVector = Vector(randX, randY)
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

def waterTest(volume, wN, aN, bN):
    cubeX = 0
    cubeY = 0
    for a in range(0, wN):
        randX = random.SystemRandom().uniform(0, 20)
        randY = random.SystemRandom().uniform(0, 20)
        randVector = Vector(randX, randY)
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
        randVector = Vector(randX, randY)
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
        randVector = Vector(randX, randY)
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

v = Container(cubesInVolLength, cubeLength, dimensions, numberOfBeads)

# addBeads(v, 200, 200)
# addBeads(v, 450)
# addBeads(v)
waterTest(v, 300, 50, 50)

if (visualise):
    prepareVisualisation(v)

if (cubeLines):
    prepareCubeLines(v)

time.sleep(3)

while True:
    if (visualise):
        updateBeadVisualisation(v)
    performCalculations(v)
    # updatePosition(v) # Randomly move beads (no calculations involved)
    passBeads(v)
    # time.sleep(0.0001)
    # time.sleep(3)
