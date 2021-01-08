"""
TriMosaic Programming Language Interpreter
TheAvaliEngineer
"""

versionNumber = "1.1.6"

def version(): print("\n" * 20 + "TriMosaic Interpreter v" + versionNumber + "\nTheAvaliEngineer")
def readme():
    with open("documentation_"+ versionNumber + ".txt", "a") as file:
        file.write("TriMosaic Language Interpreter Guide\n")
        file.write("TheAvaliEngineer\n")
        file.write("Version " + versionNumber + "\n\n")
        file.write("This language is a stylized form of the esoteric programming language   \n")
        file.write("Brainfuck. Since this does not contain a Brainfuck interpreter, you     \n")
        file.write("will have to supply your own - there are online options such as:        \n")
        file.write("https://sange.fi/esoteric/brainfuck/impl/interp/i.html                  \n")
        file.write("https://copy.sh/brainfuck/                                              \n")
        file.write("\n      Basics of TriMosaic Code                                        \n")
        file.write("TriMosaic's patterns are created by forming triangles and points on a   \n")
        file.write("bitmap grid. A vertex, represented by a single 0% black pixel, can      \n")
        file.write("connect to up to four triangles on its 'north,' 'east,' 'south,' and    \n")
        file.write("'west' sides. Each triangle must be a unique 24-bit color, and the inte-\n")
        file.write("-rpreter can only decode 24-bit bitmaps.                                \n")
        file.write("TriMosaic represents operations as different forms of triangles, with   \n")
        file.write("the added information of whether or not the perimeter is even or odd.   \n")
        file.write("It includes whitespace characters for organization as well.             \n")
        file.write("\nThe function triMosaic.interpret(file_name) will export file_name.bmp \n")
        file.write("as a .bf file (the notation for a BrainF*ck file) which can be opened in\n")
        file.write("a text editor such as Notepad.\n")
        file.write("\n    Operation Chart\n\n")
        file.write(" EVEN  |Scalene| Isocl.|\n")
        file.write("   ODD |       |       |\n")
        file.write("========================\n")
        file.write("Acute  |   +   |   .   |\n")
        file.write("       |   -   |   ,   |\n")
        file.write("========================\n")
        file.write("Right  |   [   | SPACE |\n")
        file.write("       |   ]   |  TAB  |\n")
        file.write("========================\n")
        file.write("Obtuse |   >   | BREAK |\n")
        file.write("       |   <   |       |\n")


# Imports
import math
import numpy
from PIL import Image

# Functions

#Utility
def getFirstEntry(l): return l[0]

#Image handling

#Returns an array of RGB color codes
def convertBMPtoArray(fileName):
    im = Image.open(fileName)
    ImageArray = numpy.array(im)

    return ImageArray

#Returns an array of coordinate tuples
def findPixels(pixelValue, imageArray):
    outputList = []

    for row in range(len(imageArray)):
        for col in range(len(imageArray[0])):
            if numpy.array_equal(imageArray[row][col], pixelValue):
                #print("Found a pixel of value", pixelValue, "at position", row, col)
                outputList.append( (row, col) )

    return outputList

#From a coord tuple returns surroundings
def getSurroundings(coords, imageArray):
    #Coords, North px, East px, South px, West px

    nPX = numpy.array([]); ePX = numpy.array([]); sPX = numpy.array([]); wPX = numpy.array([])
    row = coords[0]
    col = coords[1]

    try: nPX = imageArray[row - 1][col]    #North
    except IndexError: print("!N")

    try: ePX = imageArray[row][col + 1]    #East
    except IndexError: print("!E")

    try: sPX = imageArray[row + 1][col]    #South
    except IndexError: print("!S")

    try: wPX = imageArray[row][col - 1]    #West
    except IndexError: print("!W")

    nPX = nPX.tolist(); ePX = ePX.tolist(); sPX = sPX.tolist(); wPX = wPX.tolist()
    outList = [coords, [nPX, ePX, sPX, wPX]]

    #for i in outList: #Removes whitespace
        #if i in [[], [255, 255, 255]]: outList.remove(i);

    print("Surroundings Out List:", outList)

    return [coords, [nPX, ePX, sPX, wPX]]

#From a list of surroundings finds trios
def matchPixelTrio(surroundArray): # [ [coords, [n, e, s, w]], [coords, [n, e, s, w]], [coords, [n, e, s, w]]
    coordGroups = []
    outputTrios = []
    group = []

    for self in surroundArray:
        print("Checking as vertex:", self[1])

        for color in self[1]:
            print(" "*4+"Creating new group; Color:", color)
            group = [self[0]]

            for check in surroundArray:
                if color == [] or color == [255, 255, 255]:
                    print(" "*8+"Encountered whitespace! Breaking")
                    break

                print(" "*8+"Checking vertex", check[0], "for color", color)

                if color in check[1] and self != check:
                    group.append(check[0])
                    print(" "*12+"Match found! Vertex", self[0],"&",check[0], "\n"+" "*12 + "Group:", group)

            print("Color group", color, "completed:", group)
            group = list(dict.fromkeys(group)) #Culls redundant entries
            print("Color group", color, "culled:", group)

            group.sort(key=getFirstEntry) #Sorts group to prevent multiple permutations appearing
            if len(group) == 3: coordGroups.append(group)

    for item in coordGroups: #Culls redundant entries
        if item not in outputTrios: outputTrios.append(item)
    return outputTrios

#Geometry stuff

def getTriSides(cornerList):
    sideC = math.dist(cornerList[0], cornerList[1])
    sideB = math.dist(cornerList[0], cornerList[2])
    sideA = math.dist(cornerList[1], cornerList[2])
    return [sideA, sideB, sideC]
def getTriArea(sideList):
    semiP = sum(sideList) / 2
    return math.sqrt(semiP * (semiP - sideList[0]) * (semiP - sideList[1]) * (semiP - sideList[2]))
def getTriAngles(sideList):
    angA = math.degrees(math.acos( (sideList[1]**2 + sideList[2]**2 - sideList[0]**2) / (2 * sideList[1] * sideList[2]) ))
    angB = math.degrees(math.acos( (sideList[2]**2 + sideList[0]**2 - sideList[1]**2) / (2 * sideList[2] * sideList[0]) ))
    angC = math.degrees(math.acos( (sideList[0]**2 + sideList[1]**2 - sideList[2]**2) / (2 * sideList[0] * sideList[1]) ))

    return [angA, angB, angC]

def buildTri(xList, yList):
        pointA = [xList[0], yList[0]]
        pointB = [xList[1], yList[1]]
        pointC = [xList[2], yList[2]]

        sideList = getTriSides([pointA, pointB, pointC])
        angList = getTriAngles(sideList)

        area = getTriArea(sideList)
        perimeter = sum(sideList)

        type = "scalene"
        if (sideList[0] == sideList[1]) or (sideList[1] == sideList[2]) or (sideList[0] == sideList[2]): type = "isosceles"
        if sideList[0] == sideList[1] and sideList[1] == sideList[2]: type = "equilateral"

        angle = "acute"
        if 90 in angList: angle = "right"
        elif angList[0] > 90 or angList[1] > 90 or angList[2] > 90: angle = "obtuse"

        return [area, perimeter, type, angle]

def decodeTri(tri):
    operation = chr(32)                                                     #Default: space (Won't be overriden if right, scalene)

    if int(tri[1]) % 2 == 0: #If even
        if tri[2] == "scalene":
            if tri[3] == "acute":       operation = "+"
            elif tri[3] == "right":     operation = "["
            else:                       operation = ">"
        else:
            if tri[3] == "acute":       operation = "."
            elif tri[3] == "right":     operation = " "
            else:                       operation = "\n"
    else: #Else if odd
        if tri[2] == "scalene":
            if tri[3] == "acute":       operation = "-"
            elif tri[3] == "right":     operation = "]"
            else:                       operation = "<"
        else:
            if tri[3] == "acute":       operation = ","
            elif tri[3] == "right":     operation = "\t"
            else:                       operation = "\n"
    return [tri[0], operation]

#Brainfuck Compiling
def outputBrainFuck(trisList, fileName):
    outList = []
    trisList.sort(reverse=True, key=getFirstEntry)

    for tri in trisList:
        outList.append(decodeTri(tri)[1])

    print("\nTriList:", trisList)
    print("\nInterpreted BrainF*ck:", ''.join(outList))

    with open(fileName + ".bf", "w") as file:
        file.write(''.join(outList))

# Interpreter program
def interpret(file_name):
    print("\n\nProcessing image..\n\n")
    imageArray = convertBMPtoArray(file_name)

    coordsList = findPixels([0, 0, 0], imageArray)

    surroundList = []
    for coordinate in coordsList:
        surroundList.append( getSurroundings(coordinate, imageArray) )

    trioList = matchPixelTrio(surroundList)
    triList = []

    for trio in trioList:
        print(trio)
        triList.append( buildTri( [ trio[0][0], trio[1][0], trio[2][0] ], [ trio[0][1], trio[1][1], trio[2][1] ] ) )

    outputBrainFuck(triList, file_name.split(".")[0])

    print("\n\nConversion complete!\n\n")

#Automatic version notification
readme()
version()
