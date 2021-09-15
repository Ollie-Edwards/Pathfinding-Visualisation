
from tests import completeTests
completeTests()

##### IMPORTS #####

import pygame
from pygame.locals import *

from Colours import *
from Drawing import *
from NodeClass import Node

##### GAME OPTIONS #####
FPS = 200
fontSize = 10
lineColor = GREY
WIDTH = 600
boxWidth = 10
gapWidth = 1
NumberOfBoxesInRow = WIDTH//boxWidth

##### Node Data #####
openList = [] # stores all the open Nodes
closedList = [] # stores all the closed Nodes

startHasBeenSet = False # Whether or not the start has been placed (prevents being placed many times)
endHasBeenSet = False # Whether or not the end has been placed (prevents being placed many times)

startNode = None # the class of the start node will be stored here
endNode = None # the class of the end node will be stored here

##### Initialising Libraries ######

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

def afterGame():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

# RETURNS A 2D ARRAY OF A GIVEN WIDTH AND HEIGHT FULL OF NEWLY CREATED "NODE" CLASSES
def make_grid(): 
	grid = []
	for rowNum in range(NumberOfBoxesInRow):
		grid.append([])
		for colNum in range(NumberOfBoxesInRow):
			node = Node(rowNum, colNum, boxWidth)
			grid[rowNum].append(node)
	return grid
grid = make_grid()

# RETURNS A SINGLE NODE WITH THE LOWEST F COST
def getLowestOpenFCost(endNode, startNode):
    lowestFCost = float('inf') ## positive infinity
    lowestNode = ''
    openList = getOpenList()

    if openList == []:
        noSolutions(WIN, WIDTH)

    if openList != None:
        for node in openList: 
            if node.getFCost(endNode, startNode) < lowestFCost:
                lowestFCost = node.getFCost(endNode,startNode)
                lowestNode = node
    return lowestNode

# RETURNS A LIST OF ALL THE NEIGHBOURS OF A GIVEN NODE
def getNeighbours(node):
    neighbours = set([])

    row = node.rowNumber
    col = node.columnNumber

    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):            
            thisRow = row + i
            thisCol = col + j
            if (NumberOfBoxesInRow > thisRow >= 0) and (NumberOfBoxesInRow > thisCol >= 0):
                neighbours.add(grid[thisRow][thisCol])

    return list(neighbours)

# RETURNS A LIST OF ALL OPEN NODES
def getOpenList():
    openList = []
    for row in grid:
        for node in row:
            if node.isOpen:
                openList.append(node)

    return openList

# A* algorithm
def AStar():
    startNode.setOpen()
    pathFound = False
    while not pathFound:
        for event in pygame.event.get():
            if event.type == QUIT:
                pathFound = True # end game

        currentNode = getLowestOpenFCost(endNode, startNode) ## this will return a class object
        currentNode.isOpen = False # remove node from open
        currentNode.isClosed = True

        if currentNode == endNode:
            drawPath(WIN, startNode, endNode, clock, FPS, grid, WIDTH, lineColor, gapWidth)
            afterGame()

        for neighbour in getNeighbours(currentNode):
            if neighbour.isBarrier or neighbour.isClosed:
                pass
            else:
                if not(neighbour.isOpen): #or neighbour.getFCost() > currentNode.getFCost(): ## or path to the neighbour is shorter
                    neighbour.getFCost(endNode, startNode)
                    neighbour.parent = currentNode
                    if not(neighbour.isOpen):
                        neighbour.setOpen()
        for rows in grid:
            for node in rows:
                node.updateColor()

        drawNodeSquares(WIN, grid, startNode, endNode, WIDTH, lineColor, gapWidth)
        clock.tick(FPS)
        pygame.display.update()

def pregameSetup():
    global startNode, endNode
    global startHasBeenSet, endHasBeenSet
    global lineColor
    
    run = True
    while run:
        for event in pygame.event.get():
        # QUIT GAME
            if event.type == QUIT: 
                run = False
    
        # START VISUALISATION
            if pygame.key.get_pressed(): 
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    if startHasBeenSet and endHasBeenSet:
                        run = False
                        AStar()
                        
        # GET THE NODE CURRENTLY CLICKED
            if pygame.mouse.get_pressed():
                x, y = pygame.mouse.get_pos()
                clickedRow, clickedCol = x//boxWidth, y//boxWidth
                clickedNode = grid[clickedRow][clickedCol]

        # SET START/END NODES OR BARRIER
            if pygame.mouse.get_pressed()[0]: # LEFT
                clickedNode.setStatesFalse()

                ## if the end has NOT been set but the start HAS been set
                if startHasBeenSet and not endHasBeenSet: 
                    # CHECK WHETHER THE START AND END NODES HAVE BEEN PLACED ON THE SAME SQUARE
                    if not (startNode.rowNumber, startNode.columnNumber) == (clickedNode.rowNumber, clickedNode.columnNumber): 
                        clickedNode.isEnd = True
                        endHasBeenSet = True
                        endNode = clickedNode

                if not startHasBeenSet:
                    clickedNode.isStart = True
                    startHasBeenSet = True
                    startNode = clickedNode

                # IF START AND END HAVE BEEN SET, SETBARRIER
                else: 
                    if not(clickedNode.isEnd or clickedNode.isStart): ## if the square is not the start node or the end node
                        clickedNode.setBarrier()

            # IF THE CLICKED IS NOT A START/END NODE REMOVE IT
            if pygame.mouse.get_pressed()[2]: # RIGHT
                if not(clickedNode.isEnd or clickedNode.isStart): ## if the square is not the start node or the end node
                    clickedNode.setEmpty()
                    
        drawNodeSquares(WIN, grid, startNode, endNode, WIDTH, lineColor, gapWidth)
        clock.tick(FPS)

        pygame.display.update()

pregameSetup()
