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

def moveBeads(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                for v in b.conservativeForce:
                    Fc = Vector(0.0, 0.0)
                    if (v != None):
                        Fc = Vector.add(Fc, v)
                b.conservativeForce = []
                print("x: " + str(Fc.x) + ", y: " + str(Fc.y))

def performLocalCalculations(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b1 in volume.cubes[i][j].beads:
                for b2 in volume.cubes[i][j].beads:
                    if (b1 != b2):
                        b1.conservativeForce.append(conservativeForce(b1, b2))
                        # print(b1.conservativeForce)

v = Container(cubesInVolLength, cubeLength, dimensions, numberOfBeads)

specialSet = False
if (visualise):
    prepareVisualisation(v)

if (cubeLines):
    prepareCubeLines(v)

while True:
    if (visualise):
        updateBeadVisualisation(v)
    # performLocalCalculations(v)
    # moveBeads(v)
    updatePosition(v)
    passBeads(v)
    time.sleep(0.01)
