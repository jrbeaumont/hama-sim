#!/usr/bin/env python3

import sys
import time
import math
from coordinates import Coordinate
import os
from src.Containers import *
from src.Beads import *

cubesInVolLength = 4 # Number of squares in legnth, width and depth (square/cube required)
cubeLength = 100 # Number of pixels in each sub-cube
dimensions = 2 # Can be 2 or 3, for 2D or 3D
numberOfBeads = 160 # Total number of beads in the system
visualise = True
cubeLines = True
firstCalc = True
timestep = 1

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
                o+="\t\t{\"id\": \"bead_" + str(c) + "_in_" + str(i) + "_" + str(j) + "\", "
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
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                if (firstCalc):
                    f = Vector(0.0, 0.0)
                    performLocalCalculations(b, b.container)
                    for v in b.conservativeForce:
                        if (v != None):
                            f = Vector.add(f, v)
                    b.conservativeForce = []
                    b.acceleration = Vector.divide(f, b.mass)
                    f = Vector.multiply(b.acceleration, timestep)
                    b.velocity = Vector.add(b.velocity, f)
                    diffX = b.velocity.x * timestep
                    diffY = b.velocity.y * timestep
                    b.move(diffX, diffY)
                else:
                    vHalfStep = Vector.add(b.velocity, Vector.multiply(Vector.divide(b.acceleration, 2), timestep))
                    b.xStep = Vector.add(b.position, Vector.multiply(vHalfStep, timestep))
                    performLocalCalculations(b, b.container)
                    f = Vector(0.0, 0.0)
                    for v in b.conservativeForce:
                        if (v != None):
                            f = Vector.add(f, v)
                    b.conservativeForce = []
                    b.acceleration = Vector.divide(f, b.mass)
                    b.velocity = Vector.add(vHalfStep, Vector.divide(Vector.multiply(b.acceleration, timestep), 2))
    firstCalc = False

def performLocalCalculations(b1, cube):
    for b2 in cube.beads:
        if (b1 != b2):
            b1.conservativeForce.append(conservativeForce(b1, b2, b1.position, b2.position))

v = Container(cubesInVolLength, cubeLength, dimensions, numberOfBeads)

specialSet = False
if (visualise):
    prepareVisualisation(v)

if (cubeLines):
    prepareCubeLines(v)

# v.cubes[1][0].beads.append(BeadA(v.cubes[1][0], Vector(150, 50)))
# v.cubes[1][0].beads.append(BeadA(v.cubes[1][0], Vector(155, 50)))
v.cubes[1][1].beads.append(BeadB(v.cubes[1][1], Vector(150, 150)))
v.cubes[1][1].beads.append(BeadB(v.cubes[1][1], Vector(155, 150)))
# v.cubes[1][2].beads.append(BeadA(v.cubes[1][2], Vector(150, 250)))
# v.cubes[1][2].beads.append(BeadB(v.cubes[1][2], Vector(155, 250)))

while True:
    if (visualise):
        updateBeadVisualisation(v)
    performCalculations(v)
    # moveBeads(v)
    # updatePosition(v)
    passBeads(v)
    time.sleep(0.01)
