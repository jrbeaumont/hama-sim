from src.Beads import *
from src.Containers import *

# def passBeadsSingleCube(volume):
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
    for i in range(0, volume.lengthInCubes):
        for j in range(0, volume.lengthInCubes):
            if (volume.dimensions == 2):
                cube = volume.cubes[i][j]
                beads = cube.beads
                for b in beads:
                    cube.passBead(b)
            else:
                for k in range(0, volume.lengthInCubes):
                    cube = volume.cubes[i][j][k]
                    beads = cube.beads
                    for b in beads:
                        cube.passBead(b)

def performCalculations(volume, timestep):
    global firstCalc
    randNums = []
    randNum = random.SystemRandom().uniform(-1, 1)
    randNums.append((2, randNum))
    if (randNum < 0):
        randNum = random.SystemRandom().uniform(0, 1)
        randNums.append((3, randNum))
    else:
        randNum = random.SystemRandom().uniform(-1, 0)
        randNums.append((3, randNum))
    randNum = random.SystemRandom().uniform(-1, 1)
    randNums.append((5, randNum))
    calculateVelocityHalfStep(volume, timestep)
    calculatePosition(volume, timestep)
    passBeads(volume)
    calculateAcceleration(volume, randNums, timestep)
    calculateVelocity(volume, timestep)

def calculateVelocityHalfStep(volume, timestep):
    for i in range(0, volume.lengthInCubes):
        for j in range(0, volume.lengthInCubes):
            if (volume.dimensions == 2):
                for b in volume.cubes[i][j].beads:
                    b.velocityHalfStep = Vector.add(b.velocity, Vector.multiply(Vector.divide(b.acceleration, 2), timestep))
            else:
                for k in range(0, volume.lengthInCubes):
                    for b in volume.cubes[i][j][k].beads:
                        b.velocityHalfStep = Vector.add(b.velocity, Vector.multiply(Vector.divide(b.acceleration, 2), timestep))

def calculatePosition(volume, timestep):
    for i in range(0, volume.lengthInCubes):
        for j in range(0, volume.lengthInCubes):
            if (volume.dimensions == 2):
                for b in volume.cubes[i][j].beads:
                    b.position = Vector.add(b.position, Vector.multiply(b.velocityHalfStep, timestep))
            else:
                for k in range(0, volume.lengthInCubes):
                    for b in volume.cubes[i][j][k].beads:
                        b.position = Vector.add(b.position, Vector.multiply(b.velocityHalfStep, timestep))

def calculateAcceleration(volume, randNums, timestep):
    avgForce = Vector(0.0, 0.0, 0.0)
    beadCount = 0
    for i in range(0, volume.lengthInCubes):
        for j in range(0, volume.lengthInCubes):
            if (volume.dimensions == 2):
                for b in volume.cubes[i][j].beads:
                    performLocalCalculations(volume, b, b.container, randNums)
                    performNeighbourhoodCalculations2D(volume, b, i, j, randNums)
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
                for k in range(0, volume.lengthInCubes):
                    for b in volume.cubes[i][j][k].beads:
                        beadCount +=1
                        # print(b.ID + " STARTS WITH " + str(len(b.conForce)) + " CONSERVATIVE FORCES: ")
                        # input()
                        # printForces(b.conForce)
                        performLocalCalculations(volume, b, b.container, randNums, timestep)
                        # print(b.ID + " AFTER LOCAL HAS " + str(len(b.conForce)) + " CONSERVATIVE FORCES: ")
                        # input()
                        # printForces(b.conForce)
                        performNeighbourhoodCalculations(volume, b, i, j, k, randNums, timestep)
                        # print(b.ID + " AFTER NEIGHBOURHOOD HAS " + str(len(b.conForce)) + " CONSERVATIVE FORCES: ")
                        # input()
                        # printForces(b.conForce)
                        f = Vector(0.0, 0.0, 0.0)
                        # c = Vector(0.0, 0.0, 0.0)
                        # r = Vector(0.0, 0.0, 0.0)
                        # d = Vector(0.0, 0.0, 0.0)
                        # print(b.ID + " HAS " + str(len(b.conForce)) + " CONSERVATIVE FORCES: ")
                        # input()
                        # printForces(b.conForce)
                        # for v in b.conForce:
                        #     if (v != None):
                        #         c = Vector.add(c, v)
                        # b.conForce = []
                        f = Vector.add(f, b.conForce)
                        # print(b.ID + " CON FORCE: ")
                        # printForces([b.conForce])
                        b.conForce = Vector(0.0, 0.0, 0.0)
                        # for v in b.randForce:
                        #     if (v != None):
                        #         r = Vector.add(r, v)
                        # b.randForce = []
                        f = Vector.add(f, b.randForce)
                        b.randForce = Vector(0.0, 0.0, 0.0)
                        # for v in b.dForce:
                        #     if (v != None):
                        #         d = Vector.add(d, v)
                        # b.dForce = []
                        f = Vector.add(f, b.dForce)
                        b.dForce = Vector(0.0, 0.0, 0.0)
                        f = Vector.add(f, b.bondForce)
                        b.bondForce = Vector(0.0, 0.0, 0.0)
                        avgForce = Vector.add(avgForce, f)
                        b.acceleration = Vector.divide(f, b.mass)
    avgForce = Vector.divide(avgForce, 1000)
    # print("avgForce = (" + str(avgForce.x) + ", " + str(avgForce.y) + ", " + str(avgForce.z) + ")")
    # print("beadCount = " + str(beadCount))
    # input()

def calculateVelocity(volume, timestep):
    for i in range(0, volume.lengthInCubes):
        for j in range(0, volume.lengthInCubes):
            if (volume.dimensions == 2):
                for b in volume.cubes[i][j].beads:
                    b.velocity = Vector.add(b.velocityHalfStep, Vector.divide(Vector.multiply(b.acceleration, timestep), 2))
            else:
                for k in range(0, volume.lengthInCubes):
                    for b in volume.cubes[i][j][k].beads:
                        b.velocity = Vector.add(b.velocityHalfStep, Vector.divide(Vector.multiply(b.acceleration, timestep), 2))

def performLocalCalculations(volume, i, cube, randNums, timestep):
    for j in cube.beads:
        if (i.position.x != j.position.x or i.position.y != j.position.y or i.position.z != j.position.z):
            distances = getShortestDistances(volume, i.position, j.position)
            eucDistance = distances[0]
            vectorDistance = distances[1]
            if (eucDistance < i.cutoffRadius):
                i.conForce = Vector.add(i.conForce, conservativeForce(i, j, eucDistance, vectorDistance))
                i.randForce = Vector.add(i.randForce, randomForce(i, j, eucDistance, vectorDistance, timestep, randNums))
                i.dForce = Vector.add(i.dForce, dragForce(i, j, eucDistance, vectorDistance))
                if (i.bonds != None):
                    for p in i.bonds:
                        p.calculateBondForce()

# def performNeighbourhoodCalculations2D(volume, b, x, y, randNums):
#     for xLoop in [x - 1, x, x + 1]:
#         ipos = Vector(b.position.x, b.position.y, 0.0)
#         jposOffset = Vector(0.0, 0.0, 0.0)
#         if (xLoop < 0):
#             xTest = volume.lengthInCubes - 1
#             ipos.x = ipos.x + (volume.length)
#         elif (xLoop >= volume.lengthInCubes):
#             xTest = 0
#             jposOffset.x = jposOffset.x + (volume.length)
#         else:
#             xTest = xLoop

#         for yLoop in [y - 1, y, y + 1]:
#             ipos.y = b.position.y
#             jposOffset.y = 0.0
#             if (xLoop != x or yLoop != y):
#                 if (yLoop < 0):
#                     yTest = volume.lengthInCubes - 1
#                     ipos.y = ipos.y + (volume.length)
#                 elif (yLoop >= volume.lengthInCubes):
#                     yTest = 0
#                     jposOffset.y = jposOffset.y + (volume.length)
#                 else:
#                     yTest = yLoop

#                 for b2 in volume.cubes[xTest][yTest].beads:
#                     # if (b.bond == None or b.bond.getOtherBead != b2):
#                         jpos = Vector.add(b2.position, jposOffset)
#                         eucDistance = euclidianDistance(volume, b.position, b2.position)
#                         vectorDistance = Vector.subtract(ipos, jpos)
#                         b.conForce.append(conservativeForce(b, b2, eucDistance, vectorDistance))
#                         b.randForce.append(randomForce(b, b2, eucDistance, vectorDistance, timestep, randNums))
#                         b.dForce.append(dragForce(b, b2, eucDistance, vectorDistance))

def performNeighbourhoodCalculations(volume, i, x, y, z, randNums, timestep):
    c = 0
    for xLoop in [x - 1, x, x + 1]:
        # ipos = Vector(b.position.x, b.position.y, b.position.z)
        # jposOffset = Vector(0.0, 0.0, 0.0)
        if (xLoop < 0):
            xTest = volume.lengthInCubes - 1
            # ipos.x = ipos.x + (volume.length)
        elif (xLoop >= volume.lengthInCubes):
            xTest = 0
            # jposOffset.x = jposOffset.x + (volume.length)
        else:
            xTest = xLoop

        for yLoop in [y - 1, y, y + 1]:
            # ipos.y = b.position.y
            # jposOffset.y = 0.0
            if (yLoop < 0):
                yTest = volume.lengthInCubes - 1
                # ipos.y = ipos.y + (volume.length)
            elif (yLoop >= volume.lengthInCubes):
                yTest = 0
                # jposOffset.y = jposOffset.y + (volume.length)
            else:
                yTest = yLoop

            for zLoop in [z - 1, z, z + 1]:
                # ipos.z = b.position.z
                # jposOffset.z = 0.0
                if (xLoop != x or yLoop != y or zLoop != z):
                    if (zLoop < 0):
                        zTest = volume.lengthInCubes - 1
                        # ipos.z = ipos.z + (volume.length)
                    elif (zLoop >= volume.lengthInCubes):
                        zTest = 0
                        # jposOffset.z = jposOffset.z + (volume.length)
                    else:
                        zTest = zLoop

                    for j in volume.cubes[xTest][yTest][zTest].beads:
                        # jpos = Vector.add(b2.position, jposOffset)
                        distance = getShortestDistances(volume, i.position, j.position)
                        eucDistance = distance[0]
                        vectorDistance = distance[1]
                        if (eucDistance < i.cutoffRadius):
                            i.conForce = Vector.add(i.conForce, conservativeForce(i, j, eucDistance, vectorDistance))
                            i.randForce = Vector.add(i.randForce, randomForce(i, j, eucDistance, vectorDistance, timestep, randNums))
                            i.dForce = Vector.add(i.dForce, dragForce(i, j, eucDistance, vectorDistance))

def printForces(vs):
    for v in vs:
        print("\t(" + str(v.x) + ", " + str(v.y) + ", " + str(v.z) + ")")