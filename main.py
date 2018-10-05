#!/usr/bin/env python3

# from graph.core import *

# from graph.load_xml import load_graph_types_and_instances
# from graph.save_xml_stream import save_graph
import sys
import time
import math
# import csv

from coordinates import Coordinate
import random

# import os
# appBase=os.path.dirname(os.path.realpath(__file__))

# src=appBase+"/clock_tree_graph_type.xml"
# src=appBase+"/clock_tree_single_handlers_graph_type.xml"
# (graphTypes,graphInstances)=load_graph_types_and_instances(src,src)

cubesInVolLength = 4 # Number of squares in legnth, width and depth (square/cube required)
cubeLength = 1000 # Number of pixels in each sub-cube
dimensions = 2 # Can be 2 or 3, for 2D or 3D
numberOfBeads = 160 # Total number of beads in the system
visualise = True
cubeLines = True

class Volume:
    volume = (cubeLength * cubesInVolLength) ** dimensions
    length = cubesInVolLength * cubeLength
    noOfCubes = length ** dimensions
    beads = numberOfBeads
    cubes = []
    special = False

    def __init__ (self):
        for i in range(0, cubesInVolLength):
            l = []
            for j in range(0, cubesInVolLength):
                newCube = Cube(i, j, 100, self.special)
                l.append(newCube);
            self.cubes.append(l)

class Cube:
    length = cubeLength
    volume = length ** dimensions
    noOfBeads = 0
    originCoord = Coordinate(x = 0, y = 0)
    arrayPosX = 0
    arrayPosY = 0
    beads = []

    def __init__ (self, x, y, noOfBeads, special):
        self.beads = []
        self.arrayPosX = x
        self.arrayPosY = y
        self.originCoord = Coordinate(x = (x * cubeLength), y = (y * cubeLength))
        for i in range(0, noOfBeads):
            rng = random.SystemRandom()
            randX = rng.randint(self.originCoord.x, (self.originCoord.x + (self.length - 1)))
            randY = rng.randint(self.originCoord.y, (self.originCoord.y + (self.length - 1)))
            if special == False:
                newBead = Bead(self, Coordinate(x = randX, y = randY), "A")
                # print("Setting bead to special");
                special = True
            else:
                newBead = Bead(self, Coordinate(x = randX, y = randY), "B")
            self.beads.append(newBead)

    def passBead(self, bead):
        x = bead.globalCoord.x
        y = bead.globalCoord.y
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
            bead.globalCoord.x = x
            bead.globalCoord.y = y
            bead.parent = v.cubes[newParentX][newParentY]
            v.cubes[newParentX][newParentY].beads.append(bead)
            # if (bead.beadType == "A"):
                # print("A special bead is moving")

    def remove(self, bead):
        for b in self.beads:
            if bead.globalCoord.x == b.globalCoord.x and bead.globalCoord.y == b.globalCoord.y:
                self.beads.remove(b)
                return

class Bead:
    container = None
    globalCoord = Coordinate(x = 0, y = 0)
    beadType = "B";

    def __init__(self, creator, coord, beadType):
        self.container = creator
        self.globalCoord = coord
        self.beadType = beadType

    def move(self, dx, dy):
        newX = self.globalCoord.x + dx
        newY = self.globalCoord.y + dy
        self.globalCoord = Coordinate(x = self.globalCoord.x + dx, y = self.globalCoord.y + dy)


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
                o+="\"x\": " + str(b.globalCoord.x) + ", \"y\": " + str(b.globalCoord.y) + ", "
                o+= "\"type\": \"" + b.beadType + "\"},"
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
                b.move(rng.randint(-100, 100), rng.randint(-100, 100))


v = Volume()

specialSet = False
if (visualise):
    prepareVisualisation(v)

if (cubeLines):
    prepareCubeLines(v)

while True:
    if (visualise):
        updateBeadVisualisation(v)
    updatePosition(v)
    passBeads(v)
    time.sleep(0.01)
