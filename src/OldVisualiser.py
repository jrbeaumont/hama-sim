import sys
from src.Beads import *

def updateBeadVisualisation(volume):
    o = "{\n"
    o+= "\t\"beads\": [\n"
    bonds = []
    for i in range(0, volume.lengthInCubes):
        for j in range(0, volume.lengthInCubes):
            for b in volume.cubes[i][j].beads:
                o+="\t\t{\"id\": \""+ b.ID +"\", "
                o+="\"x\": " + str(b.position.x) + ", \"y\": " + str(b.position.y) + ", "
                o+= "\"type\": \"" + b.typeName + "\"},"
                o+="\n"
                if (b.bond != None):
                    if b.bond not in bonds:
                        bonds.append(b.bond)
    o = o[:-2]
    o+="\n\t]\n\n"
    if bonds:
        o = o[:-2]
        o+=",\n\n\t\"bonds\": [\n"
        for b in bonds:
            o+="\t\t{\"bead1\": \"" + b.bead1.ID + "\", \"bead2\": \"" + b.bead2.ID + "\"},\n"
        o = o[:-2]
        o+="\n\t]\n"
    o+= '}\n'
    print(o)
    sys.stdout.flush()

def updateBeadVisualisation3D(volume):
    o = "{\n"
    o+= "\t\"beads\": [\n"
    bonds = []
    for i in range(0, volume.lengthInCubes):
        for j in range(0, volume.lengthInCubes):
            for k in range(0, volume.lengthInCubes):
                for b in volume.cubes[i][j][k].beads:
                    o+="\t\t{\"id\": \""+ b.ID +"\", "
                    o+="\"x\": " + str(b.position.x) + ", \"y\": " + str(b.position.y) + ", \"z\": " + str(b.position.z) + ", "
                    o+= "\"type\": \"" + b.typeName + "\"},"
                    o+="\n"
                    if (b.bond != None):
                        if b.bond not in bonds:
                            bonds.append(b.bond)
    o = o[:-2]
    o+="\n\t]\n\n"
    if bonds:
        o = o[:-2]
        o+=",\n\n\t\"bonds\": [\n"
        for b in bonds:
            o+="\t\t{\"bead1\": \"" + b.bead1.ID + "\", \"bead2\": \"" + b.bead2.ID + "\"},\n"
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

def prepareCubeLines(volume):
    o = "{\n"
    o+= "\t\"lines\": [\n"
    for i in range(1, volume.lengthInCubes):
        staticPos = i * volume.cubeLength;
        maxVal = volume.cubeLength * volume.lengthInCubes;
        o+="\t\t{\"x1\": " + str(staticPos) + ", \"y1\": 0, \"x2\": " + str(staticPos) + ", \"y2\": " + str(maxVal)+ "},\n"
        o+="\t\t{\"x1\": 0" + ", \"y1\": " + str(staticPos) + ", \"x2\": " + str(maxVal) + ", \"y2\": " + str(staticPos)+ "},\n"
    o = o[:-2]
    o+="\n\t]\n"
    o+= '}\n'
    print(o)
    sys.stdout.flush()