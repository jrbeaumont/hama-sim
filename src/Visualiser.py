import sys
import os.path

def prepVisualisation(volume):
    if os.path.exists("config.json"):
        os.remove("config.json")

    o = "{\n"
    o+= "\t\"frames\": \"_frames\",\n"
    o+= "\t\"state\": \"state.json\"\n"
    o+= "}"

    with open("config.json", 'w') as f:
        print(o, file=f)

    if os.path.exists("state.json"):
        os.remove("state.json")

    s = open("state.json", "w")
    s.close()

    # if os.path.exists("_frames"):
        # os.rmdir("_frames")

    # updateVisualisation(volume)

def orderedUpdateVis(beads):
    o = "{\n"
    o+= "  \"beads\":[\n"
    for b in beads:
        o+="\t{\"id\":\""+ b.ID +"\", "
        o+="\"x\":" + "{0:.5f}".format(b.position.x) + ", \"y\":" + "{0:.5f}".format(b.position.y) + ", \"z\":" + "{0:.5f}".format(b.position.z) + ", "
        o+="\"vx\":" + "{0:.5f}".format(b.velocity.x) + ", \"vy\":" + "{0:.5f}".format(b.velocity.y) + ", \"vz\":" + "{0:.5f}".format(b.velocity.z) + ", "
        o+= "\"type\":" + str(b.typeNumber) + "},"
        o+="\n"
    o = o[:-2]
    o+="\n\t]\n\n}"
    out = open("state.json", "w")
    print(o, file=out)
    out.close()
    # print(o)
    print("u")
    sys.stdout.flush()

def updateVisualisation(volume):
    o = "{\n"
    o+= "  \"beads\":[\n"
    for i in range(0, volume.lengthInCubes):
        for j in range(0, volume.lengthInCubes):
            for k in range(0, volume.lengthInCubes):
                for b in volume.cubes[i][j][k].beads:
            # for b in volume.cubes[i][j].beads:
                    o+="\t{\"id\":\""+ b.ID +"\", "
                    o+="\"x\":" + "{0:.5f}".format(b.position.x) + ", \"y\":" + "{0:.5f}".format(b.position.y) + ", \"z\":" + "{0:.5f}".format(b.position.z) + ", "
                    o+="\"vx\":" + "{0:.5f}".format(b.velocity.x) + ", \"vy\":" + "{0:.5f}".format(b.velocity.y) + ", \"vz\":" + "{0:.5f}".format(b.velocity.z) + ", "
                    o+= "\"type\":" + str(b.typeNumber) + "},"
                    o+="\n"
    o = o[:-2]
    o+="\n\t]\n\n}"
    out = open("state.json", "w")
    print(o, file=out)
    out.close()
    # print(o)
    print("u")
    sys.stdout.flush()
