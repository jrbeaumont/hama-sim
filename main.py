#!/usr/bin/env python3

import sys
import time
import math
from coordinates import Coordinate
import os
from src.Containers import *
from src.Beads import *

cubesInVolLength = 4 # Number of squares in legnth, width and depth (square/cube required)
cubeLength = 50 # Number of pixels in each sub-cube
dimensions = 2 # Can be 2 or 3, for 2D or 3D
numberOfBeads = 160 # Total number of beads in the system
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
        p+="\t\t{\"name\": \"" + str(t[0]) + "\", \"colour\": \"" + str(t[1]) + "\"},\n"
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
    randNum = random.SystemRandom().uniform(-1, 1)
    global firstCalc
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                if (firstCalc):
                    f = Vector(0.0, 0.0)
                    b.xStep = b.position
                    performLocalCalculations(b, b.container, randNum)
                    performNeighbourhoodCalculations(volume, b, i, j, randNum)
                    for v in b.conForce:
                        if (v != None):
                            f = Vector.add(f, v)
                    b.conForce = []
                    for v in b.randForce:
                        if (v != None):
                            f = Vector.add(f, v)
                    b.randForce = []
                    b.acceleration = Vector.divide(f, b.mass)
                    f = Vector.multiply(b.acceleration, timestep)
                    b.velocity = Vector.add(b.velocity, f)
                    diffX = b.velocity.x * timestep
                    diffY = b.velocity.y * timestep
                    b.move(diffX, diffY)
                else:
                    vHalfStep = Vector.add(b.velocity, Vector.multiply(Vector.divide(b.acceleration, 2), timestep))
                    b.xStep = Vector.add(b.position, Vector.multiply(vHalfStep, timestep))
                    performLocalCalculations(b, b.container, randNum)
                    performNeighbourhoodCalculations(volume, b, i, j, randNum)
                    f = Vector(0.0, 0.0)
                    for v in b.conForce:
                        if (v != None):
                            f = Vector.add(f, v)
                    b.conForce = []
                    for v in b.randForce:
                        if (v != None):
                            f = Vector.add(f, v)
                    b.randForce = []
                    b.acceleration = Vector.divide(f, b.mass)
                    b.velocity = Vector.add(vHalfStep, Vector.divide(Vector.multiply(b.acceleration, timestep), 2))
    firstCalc = False

def performLocalCalculations(b1, cube, randNum):
    for b2 in cube.beads:
        if (b1.position.x != b2.position.x or b1.position.y != b2.position.y):
            b1.conForce.append(conservativeForce(b1, b2, b1.xStep, b2.position))
            b1.randForce.append(randomForce(b1, b2, b1.xStep, b2.position, timestep, randNum))

def performNeighbourhoodCalculations(volume, b, x, y, randNum):
    tmpXStep = Vector(b.xStep.x, b.xStep.y)
    for xLoop in [x - 1, x, x + 1]:
        b.xStep.x = tmpXStep.x
        b.xStep.y = tmpXStep.y
        if (xLoop < 0):
            xTest = cubesInVolLength - 1
            b.xStep.x = b.xStep.x + (volume.length)
        elif (xLoop >= cubesInVolLength):
            xTest = 0
            b.xStep.x = b.xStep.x - (volume.length)
        else:
            xTest = xLoop
        for yLoop in [y - 1, y, y + 1]:
            b.xStep.y = tmpXStep.y
            if (xLoop != x or yLoop != y):
                if (yLoop < 0):
                    yTest = cubesInVolLength - 1
                    b.xStep.y = b.xStep.y + (volume.length)
                elif (yLoop >= cubesInVolLength):
                    yTest = 0
                    b.xStep.y = b.xStep.y - (volume.length)
                else:
                    yTest = yLoop
                performLocalCalculations(b, volume.cubes[xTest][yTest], randNum)
    b.xStep.x = tmpXStep.x
    b.xStep.y = tmpXStep.y

def moveBeads(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                b.position = b.xStep

v = Container(cubesInVolLength, cubeLength, dimensions, numberOfBeads)

# v.cubes[0][2].beads.append(BeadA(v.cubes[2][0], Vector(97.5, 50)))
# v.cubes[3][0].beads.append(BeadA(v.cubes[3][0], Vector(102.5, 50)))
# v.cubes[1][1].beads.append(BeadB(v.cubes[1][1], Vector(197.5, 150)))
# v.cubes[2][1].beads.append(BeadB(v.cubes[2][1], Vector(202.5, 150)))
# v.cubes[3][2].beads.append(BeadA(v.cubes[3][2], Vector(397.5, 250)))
# v.cubes[0][2].beads.append(BeadB(v.cubes[0][2], Vector(2.5, 250)))
# v.cubes[3][2].beads.append(BeadA(v.cubes[3][2], Vector(345, 200)))
# v.cubes[3][2].beads.append(BeadB(v.cubes[3][2], Vector(355, 200)))

# v.cubes[1][2].beads.append(BeadA(v.cubes[1][2], Vector(195, 205)))
# v.cubes[2][1].beads.append(BeadB(v.cubes[2][1], Vector(205, 195)))

if (visualise):
    prepareVisualisation(v)

if (cubeLines):
    prepareCubeLines(v)

time.sleep(3)

while True:
    if (visualise):
        updateBeadVisualisation(v)
    performCalculations(v)
    moveBeads(v)
    # updatePosition(v) # Randomly move beads (no calculations involved)
    passBeads(v)
    time.sleep(0.001)
    # time.sleep(5)
