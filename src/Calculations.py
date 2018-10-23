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
    randNum = random.SystemRandom().uniform(-1, 1)
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
                        performLocalCalculations(volume, b, b.container, randNums, timestep)
                        performNeighbourhoodCalculations(volume, b, i, j, k, randNums, timestep)
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

def performLocalCalculations(volume, b1, cube, randNums, timestep):
    for b2 in cube.beads:
        if (b1.position.x != b2.position.x or b1.position.y != b2.position.y or b1.position.z != b2.position.z):
            distances = getShortestDistances(volume, b1.position, b2.position)
            eucDistance = distances[0]
            vectorDistance = distances[1]
            # eucDistance = euclidianDistance(volume, b1.position, b2.position)
            # vectorDistance = Vector.subtract(b1.position, b2.position)
            b1.conForce.append(conservativeForce(b1, b2, eucDistance, vectorDistance))
            b1.randForce.append(randomForce(b1, b2, eucDistance, vectorDistance, timestep, randNums))
            b1.dForce.append(dragForce(b1, b2, eucDistance, vectorDistance))
            if (b1.bond != None and b1.bondForce == None):
                b1.bond.calculateBondForce()

def performNeighbourhoodCalculations2D(volume, b, x, y, randNums):
    for xLoop in [x - 1, x, x + 1]:
        ipos = Vector(b.position.x, b.position.y, 0.0)
        jposOffset = Vector(0.0, 0.0, 0.0)
        if (xLoop < 0):
            xTest = volume.lengthInCubes - 1
            ipos.x = ipos.x + (volume.length)
        elif (xLoop >= volume.lengthInCubes):
            xTest = 0
            jposOffset.x = jposOffset.x + (volume.length)
        else:
            xTest = xLoop

        for yLoop in [y - 1, y, y + 1]:
            ipos.y = b.position.y
            jposOffset.y = 0.0
            if (xLoop != x or yLoop != y):
                if (yLoop < 0):
                    yTest = volume.lengthInCubes - 1
                    ipos.y = ipos.y + (volume.length)
                elif (yLoop >= volume.lengthInCubes):
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

def performNeighbourhoodCalculations(volume, b, x, y, z, randNums, timestep):
    for xLoop in [x - 1, x, x + 1]:
        ipos = Vector(b.position.x, b.position.y, b.position.z)
        jposOffset = Vector(0.0, 0.0, 0.0)
        if (xLoop < 0):
            xTest = volume.lengthInCubes - 1
            ipos.x = ipos.x + (volume.length)
        elif (xLoop >= volume.lengthInCubes):
            xTest = 0
            jposOffset.x = jposOffset.x + (volume.length)
        else:
            xTest = xLoop

        for yLoop in [y - 1, y, y + 1]:
            ipos.y = b.position.y
            jposOffset.y = 0.0
            if (yLoop < 0):
                yTest = volume.lengthInCubes - 1
                ipos.y = ipos.y + (volume.length)
            elif (yLoop >= volume.lengthInCubes):
                yTest = 0
                jposOffset.y = jposOffset.y + (volume.length)
            else:
                yTest = yLoop

            for zLoop in [z - 1, z, z + 1]:
                ipos.z = b.position.z
                jposOffset.z = 0.0
                if (xLoop != x or yLoop != y or zLoop != z):
                    if (zLoop < 0):
                        zTest = volume.lengthInCubes - 1
                        ipos.z = ipos.z + (volume.length)
                    elif (zLoop >= volume.lengthInCubes):
                        zTest = 0
                        jposOffset.z = jposOffset.z + (volume.length)
                    else:
                        zTest = zLoop

                    for b2 in volume.cubes[xTest][yTest][zTest].beads:
                        jpos = Vector.add(b2.position, jposOffset)
                        distance = getShortestDistances(volume, ipos, jpos)
                        eucDistance = distance[0]
                        vectorDistance = distance[1]
                        # eucDistance = euclidianDistance(volume, ipos, jpos)
                        # vectorDistance = Vector.subtract(ipos, jpos)
                        b.conForce.append(conservativeForce(b, b2, eucDistance, vectorDistance))
                        b.randForce.append(randomForce(b, b2, eucDistance, vectorDistance, timestep, randNums))
                        b.dForce.append(dragForce(b, b2, eucDistance, vectorDistance))
