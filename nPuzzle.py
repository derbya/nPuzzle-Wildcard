from enum import Enum
import calendar
import time
import math
import sys
import random
import heapq

identityCounter = 0

startTime = calendar.timegm(time.gmtime())

argumentDictionary = {}

def updateDictionary(argNum, arg):
    global argumentDictionary
    try:
        argumentDictionary.update( { arg : sys.argv[argNum + 1]  } )
    except IndexError:
        printUsage()
        exit()

def printUsage():
    print("\nUsage: python3 nPuzzle [-f filename] | [-r size] [-h heuristic]\n")
    print("All flags are optional, and defaults to '-r 4' '-h manhattan'\n")
    print("-f flag must be followed by a valid file name:                   -f file")
    print("-r flag must be followed by the size of the random puzzle:       -r 4")
    print("-h flag must be followed by a valid heuristic:                   -h manhattan")
    print("--help to print Usage")
    print("\nvalid heuristics: manhattan, hamming, definitelyadmissible, corners, zero, swap\n")

class Puzzle:
    def __init__(self, puzzle, weight, owner, moves):
        self.puzzle = puzzle
        self.weight = weight
        self.id = arrayToString(puzzle)
        self.owner = owner
        self.moves = moves

    def printPuzzleClass(self):
        print(self.puzzle)
        printPuzzle(self.puzzle)
        print("\nWeight: " + str(self.weight))
        print("id: " + self.id)
        print("parent: " + self.owner)
        print("moves: " + str(self.moves))


def returnSolvedExample(size):
    solvedPuzzle = []
    for i in range(size - 1):
        solvedPuzzle.append(i + 1)
    solvedPuzzle.append(0)
    return solvedPuzzle

def ifSolved(puzzle, solved):
    if puzzle == solved:
        return True
    else:
        return False

def getWeight(puzzle, solved, moves):
    return heuristicDictionary[heuristic](puzzle, solved, moves)

def swapMethod(puzzle, solved, moves):
    ret = moves
    puzzleCopy = puzzle.copy()
    while puzzleCopy != solved:
        zeroIndex = puzzleCopy.index(0)
        if solved[zeroIndex] != 0:
            swapNum = solved[zeroIndex]
            swapIndex = puzzleCopy.index(swapNum)
            puzzleCopy[swapIndex], puzzleCopy[zeroIndex] = puzzleCopy[zeroIndex], puzzleCopy[swapIndex]
        else:
            for i in range(theRoot * theRoot):
                if solved[i] != puzzleCopy[i]:
                    puzzleCopy[i], puzzleCopy[zeroIndex] = puzzleCopy[zeroIndex], puzzleCopy[i]
                    break
        ret += 1
    return ret

def sequenceScore(puzzle, solved):
    count = 0
    for i in range(len(puzzle) - 1):
        if puzzle[puzzle.index(i) + 1] == solved[solved.index(i) + 1]:
            count += 2
    return count

def manhattanSequence(puzzle, solved, moves):
    weight = moves
    for i in range(len(puzzle)):
        if i != 0:
            column = abs((puzzle.index(i) % theRoot) - (solved.index(i) % theRoot))
            row = abs(int(puzzle.index(i) / theRoot) - int(solved.index(i) / theRoot))
            weight += row + column
    return weight + sequenceScore()

def getZeroHeuristic(puzzle, solved, moves):
    return moves

def getCornerValues(puzzle, solved):
    corners = 0
    if puzzle.index(1) == solved.index(1):
        corners += 1
    if puzzle.index(theRoot) == solved.index(theRoot):
        corners += 1
    if puzzle.index(theRoot + theRoot - 1) == solved.index(theRoot + theRoot - 1):
        corners += 1
    if puzzle.index(theRoot + theRoot + theRoot - 2) == solved.index(theRoot + theRoot + theRoot - 2):
        corners += 1
    return corners / 2

def manhattanCorners(puzzle, solved, moves):
    weight = moves
    corners = getCornerValues(puzzle, solved)
    for i in range(len(puzzle)):
        if i != 0:
            column = abs((puzzle.index(i) % theRoot) - (solved.index(i) % theRoot))
            row = abs(int(puzzle.index(i) / theRoot) - int(solved.index(i) / theRoot))
            weight += row + column
    if weight - moves < corners:
        return weight
    return weight - corners

def definitelyAdmissible(puzzle, solved, moves):
    weight = 0
    for i in range(len(puzzle)):
        if i != 0:
            column = abs((puzzle.index(i) % theRoot) - (solved.index(i) % theRoot))
            row = abs(int(puzzle.index(i) / theRoot) - int(solved.index(i) / theRoot))
            weight += row + column
    return (weight * 1.05) + moves

def manhattan(puzzle, solved, moves):
    weight = moves
    for i in range(len(puzzle)):
        if i != 0:
            column = abs((puzzle.index(i) % theRoot) - (solved.index(i) % theRoot))
            row = abs(int(puzzle.index(i) / theRoot) - int(solved.index(i) / theRoot))
            weight += row + column
    return weight

def hamming(puzzle, solved, moves):
    weight = moves
    for i in range(len(puzzle)):
        if puzzle[i] != solved[i]:
            weight += 5
    return weight

def moveUp(puzzle):
    index = puzzle.index(0)
    if index < theRoot:
        return None
    else:
        puzzle[index], puzzle[int(index - theRoot)] = puzzle[int(index - theRoot)], puzzle[index]
    return puzzle

def returnMoveUp(puzzle, identity, moves, solved):
    global identityCounter
    newPuzzle = moveUp(puzzle.copy())
    if newPuzzle:
        return (Puzzle(newPuzzle,
            getWeight(newPuzzle, solved, moves),
            identity,
            moves + 1))
    return None

def moveDown(puzzle):
    index = puzzle.index(0)
    if index >= len(puzzle) - theRoot:
        return None
    else:
        puzzle[index], puzzle[int(index + theRoot)] = puzzle[int(index + theRoot)], puzzle[index]
    return puzzle

def returnMoveDown(puzzle, identity, moves, solved):
    global identityCounter
    newPuzzle = moveDown(puzzle.copy())
    if newPuzzle:
        return (Puzzle(newPuzzle,
            getWeight(newPuzzle, solved, moves),
            identity,
            moves + 1))
    return None

def moveRight(puzzle):
    index = puzzle.index(0)
    if index % theRoot == 0:
        return None
    else:
        puzzle[index], puzzle[index - 1] = puzzle[index - 1], puzzle[index]
    return puzzle

def returnMoveRight(puzzle, identity, moves, solved):
    global identityCounter
    newPuzzle = moveRight(puzzle.copy())
    if newPuzzle:
        return (Puzzle(newPuzzle,
            getWeight(newPuzzle, solved, moves),
            identity,
            moves + 1))
    return None

def moveLeft(puzzle):
    index = puzzle.index(0)
    if (index + 1) % theRoot == 0:
        return None
    else:
        puzzle[index], puzzle[index + 1] = puzzle[index + 1], puzzle[index]
    return puzzle
    

def returnMoveLeft(puzzle, identity, moves, solved):
    global identityCounter
    newPuzzle = moveLeft(puzzle.copy())
    if newPuzzle:
        return (Puzzle(newPuzzle,
            getWeight(newPuzzle, solved, moves),
            identity,
            moves + 1))
    return None

def insertChild(Puzzle, queue):
    insertCheck = False
    if not queue:
        pass
    else:
        for i in range(len(queue)):
            if queue[i].weight >= Puzzle.weight:
                queue.insert(i, Puzzle)
                insertCheck = True
                break
    if not insertCheck:
        queue.append(Puzzle)

def duplicatePuzzle(popped, poppedPuzzles):
    try:
        if poppedPuzzles[popped.id]:
            if poppedPuzzles[popped.id].weight <= popped.weight:
                return True
            else:
                return False
    except KeyError:
        return False

worldClock = 0

def arrayToString(array):
    return "'".join([str(num) for num in array])


def printPuzzle(puzzle):
    for i in range(len(puzzle)):
        if i % theRoot == 0 and i != 0:
            print("")
        print(str(puzzle[i]), end = " ")
        if puzzle[i] < 10:
            print(end = " ")
    print("")

def printStateOrder(start, end, poppedPuzzles):
    endPuzzle = end
    puzzleCount = 0
    printPuzzle(endPuzzle.puzzle)
    print("\n=====================================================\n")
    while True:
        puzzleCount += 1
        try:
            popped = poppedPuzzles[endPuzzle.owner]
        except KeyError:
            print(start)
            break
        if popped.puzzle == start:
            print(endPuzzle.puzzle)
            print(popped.puzzle)
            break
        print(endPuzzle.puzzle)
        endPuzzle = popped
    print("\n=====================================================")
    print(str(puzzleCount - 1) + " Steps to solve puzzle")

def solvePuzzle(queue, solved):
    global identityCounter
    startingPuzzle = queue[0][2].puzzle.copy()
    heapq.heapify(queue)
    poppedPuzzles = {}
    queuedPuzzles = {}
    while True:
        popped = heapq.heappop(queue)
        if ifSolved(popped[2].puzzle, solved):
            printStateOrder(startingPuzzle, popped[2], poppedPuzzles)
            print(str(len(poppedPuzzles) + len(queuedPuzzles) + len(queue)) + " Total States in Memory")
            print(str(len(poppedPuzzles) + 1) + " States Expanded")
            print(str(calendar.timegm(time.gmtime()) - startTime) + " Seconds")
            exit()
        if not duplicatePuzzle(popped[2], poppedPuzzles):
            currentMoves = []
            currentMoves.append(returnMoveDown(popped[2].puzzle, popped[2].id, popped[2].moves, solved))
            currentMoves.append(returnMoveRight(popped[2].puzzle, popped[2].id, popped[2].moves, solved))
            currentMoves.append(returnMoveLeft(popped[2].puzzle, popped[2].id, popped[2].moves, solved))
            currentMoves.append(returnMoveUp(popped[2].puzzle, popped[2].id, popped[2].moves, solved))
            for i in currentMoves:
                if i:
                    if not duplicatePuzzle(i, poppedPuzzles):
                        if not duplicatePuzzle(i, queuedPuzzles):
                            heapq.heappush(queue, (i.weight, i.id,  i))
                            queuedPuzzles.update( { i.id : i  } )
                        poppedPuzzles.update( { popped[2].id : popped[2] } )

def returnSolvedPuzzle(size):
    tab = []
    width = size
    height = size
    area = width * height
    for i in range(area):
        x = (i % width)
        y = int(i / width)
        if x >= y:
            depth = min(y, width - 1 - x)
            offset = (x - depth) + (y - depth)
        else:
            depth = min(x + 1, height - y)
            offset = (depth - x - 1) + (depth - y - 1)
        f = (width - 2 * depth)
        tab.append(((area - f * f + offset) + 1) % area)
    return tab

def generateRandomPuzzle(size):
    if size < 2:
        print("Size must be greater than 2 when using the -r flag")
        printUsage()
        exit()
    if size > 5:
        print("Warning! Puzzles over size 5 may take a while!")
    puzzle = returnSolvedPuzzle(size)
    #randomMoveNumber = random.randint(0, 1000000)
    randomMoveNumber = 200
    for i in range(randomMoveNumber):
        tempPuzzle = moveDictionary[random.randint(1, 4)](puzzle)
        if tempPuzzle:
            puzzle = tempPuzzle
    return puzzle

def getPuzzleFromFile(filename):
    tab = generateRandomPuzzle(4)
    print(filename)
    return tab

path = None
theRoot = 4
heuristic = "manhattan"
printFlag = None

heuristicDictionary = {
        "hamming" : hamming,
        "manhattan" : manhattan,
        "corners" : manhattanCorners,
        "zero" : getZeroHeuristic,
        "swap" : swapMethod,
        "definitelyadmissible" : definitelyAdmissible
        }

moveDictionary = {
        1 : moveLeft,
        2 : moveRight,
        3 : moveDown,
        4 : moveUp
        }

def main():
    puzzleQueue = []
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-f" or sys.argv[i] == "-h" or sys.argv[i] == "-r" or sys.argv[i] == "-p":
            updateDictionary(i, sys.argv[i])
        if sys.argv[i] == "--help":
            printUsage()
            exit()
    global path
    global theRoot
    global heuristic
    global printFlag
    try:
        path = argumentDictionary["-f"]
    except KeyError:
        pass
    try:
        theRoot = int(argumentDictionary["-r"])
    except KeyError:
        pass
    try:
        heuristic = argumentDictionary["-h"].lower()
    except KeyError:
        pass
    try:
        printFlag = argumentDictionary["-p"].lower()
    except KeyError:
        pass
    if path:
        filename = open(path, "r")
        fileString = filename.read().split()
        theRoot = int(fileString[0])
        startingPuzzle = []
        for i in range(1, theRoot * theRoot + 1):
            try:
                startingPuzzle.append(int(fileString[i]))
            except (IndexError, ValueError):
                print("Invalid Puzzle")
                exit()
    else:
        startingPuzzle = generateRandomPuzzle(theRoot)
    printPuzzle(startingPuzzle)
    print("")
    solvedPuzzle = returnSolvedPuzzle(theRoot)
    puzzleQueue.append((getWeight(startingPuzzle, solvedPuzzle, 0), arrayToString(startingPuzzle), Puzzle(startingPuzzle, getWeight(startingPuzzle, solvedPuzzle, 0), arrayToString(startingPuzzle), 0)))
    if printFlag:
        if argumentDictionary["-p"] == "notsolve":
            print(theRoot)
            printPuzzle(startingPuzzle)
            exit()
        print(theRoot)
        printPuzzle(startingPuzzle)
    solvePuzzle(puzzleQueue, solvedPuzzle)


main()
