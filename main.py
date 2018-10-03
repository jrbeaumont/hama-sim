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

class Volume:
    volume = (cubeLength * cubesInVolLength) ** dimensions
    length = cubesInVolLength * cubeLength
    noOfCubes = length ** dimensions
    beads = numberOfBeads
    cubes = []

    def __init__ (self):
        for i in range(0, cubesInVolLength):
            l = []
            for j in range(0, cubesInVolLength):
                newCube = Cube(Coordinate(x = (i * cubeLength), y = (j * cubeLength)), 10)
                l.append(newCube);
            self.cubes.append(l)

class Cube:
    length = cubeLength
    volume = length ** dimensions
    noOfBeads = 0
    originCoord = Coordinate(x = 0, y = 0)
    beads = []

    def __init__ (self, coord, noOfBeads):
        self.beads = []
        self.originCoord = coord
        for i in range(0, noOfBeads):
            rng = random.SystemRandom()
            randX = rng.randint(self.originCoord.x, (self.originCoord.x + (self.length - 1)))
            randY = rng.randint(self.originCoord.y, (self.originCoord.y + (self.length - 1)))
            newBead = Bead(Coordinate(x = randX, y = randY))
            self.beads.append(newBead)
        # print("Cube x: ", self.originCoord.x, " y: ", self.originCoord.y, " has beads: ", self.beads, "\n")

class Bead:
    globalCoord = Coordinate(x = 0, y = 0)

    def __init__(self, coord):
        self.globalCoord = coord

def generate_d3_json_data(volume):
    o = "{\n"
    o+= "\t\"beads\": [\n"
    beads = []
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            c = 0
            for b in volume.cubes[i][j].beads:
                o+="\t\t{\"id\": \"bead_" + str(c) + "_in_" + str(i) + "_" + str(j) + "\", "
                c+=1
                o+="\"x\": " + str(b.globalCoord.x) + ", \"y\": " + str(b.globalCoord.y) + "},\n"
    o = o[:-2]
    o+="\t]\n"
    o+= '}\n'
    print(o)
    sys.stdout.flush()

def updatePosition(volume):
    for i in range(0, cubesInVolLength):
        for j in range(0, cubesInVolLength):
            for b in volume.cubes[i][j].beads:
                b.globalCoord = Coordinate(x = b.globalCoord.x + 10, y = b.globalCoord.y)

v = Volume()

for x in range(0,1000):
    if (visualise):
        generate_d3_json_data(v)
    updatePosition(v)
    time.sleep(0.01)
