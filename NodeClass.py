import pygame, math

from Colours import *

fontSize = 10
pygame.font.init()
font = pygame.font.SysFont('arial', fontSize)

class Node(object):
    def __init__(self, rowNumber, columnNumber, boxWidth): #gridTuple is in (row, collum) form
        self.rowNumber = rowNumber
        self.columnNumber = columnNumber
        self.gridPosition = (self.rowNumber, self.columnNumber)

        self.parent = None
        self.isBarrier = False
        self.isStart = False
        self.isEnd = False
        self.isPath = False
        self.isClosed = False
        self.isOpen = False
        self.isEmpty= True
 
        self.left = self.rowNumber * boxWidth
        self.right = self.left+boxWidth
        self.top = self.columnNumber * boxWidth
        self.bottom = self.top+boxWidth
        self.boxWidth = boxWidth

        self.centrePixel = ((self.left+self.right)/2),((self.top+self.bottom)/2) # pixel at the centre of the node
        self.color = BLACK # default color (will be changed)
        self.font = font

        self.gCost = None # distance from starting node
        self.hCost = None # distance from end node
        self.fCost = None # GCost + HCost

    def setStatesFalse(self): ## shouldnt effect start and end
        self.isBarrier = False
        self.isPath = False
        self.isClosed = False
        self.isOpen = False
        self.isEmpty = False

    def setBarrier(self): # sets isbarrier to true and all other states to false
        self.setStatesFalse()
        self.isBarrier = True

    def setClosed(self): # sets isclosed to true and all other states to false
        self.setStatesFalse()
        self.isClosed = True

    def setOpen(self): # sets isopen to true and all other states to false
        self.setStatesFalse()
        self.isOpen = True  

    def setPath(self): # sets ispath to true and all other states to false
        self.setStatesFalse()
        self.isPath = True

    def setEmpty(self):# sets isempty to true and all other states to false
        self.setStatesFalse()
        self.isEmpty = True

    def updateColor(self):
        if self.isBarrier:
            self.color = BLACK
        if self.isEmpty:
            self.color = WHITE
        if self.isClosed:
            self.color = RED
        if self.isOpen:
            self.color = GREEN
        if self.isPath: # must be near end
            self.color = CYAN
        if self.isEnd: # must be near end
            self.color = PURPLE
        if self.isStart:# must be near end
            self.color = PURPLE

    def draw_square(self, WIN):
        self.updateColor()
        rect = pygame.Rect(self.left, self.top, self.boxWidth, self.boxWidth) #Rect(left, top, width, height)
        pygame.draw.rect(WIN, self.color,rect) # surface, color, rectangle, width
	
    def getGCost(self, startNode): # distance from start # could have made this recursive
        totalDistance=0
        horisontalDistance = abs(startNode.rowNumber - self.rowNumber)
        verticalDistance = abs(startNode.columnNumber - self.columnNumber)
        totalDistance += math.sqrt((horisontalDistance**2)+(verticalDistance**2))
        return totalDistance

    def getHCost(self, endNode): # distance from end node
        horisontalDistance = abs((endNode.rowNumber) - int(self.rowNumber))
        verticalDistance = abs((endNode.columnNumber) - int(self.columnNumber))
        ## pythagoras theorem
        return math.sqrt((horisontalDistance**2)+(verticalDistance**2))

    def getFCost(self, endNode, startNode):
        return float(self.getHCost(endNode) + self.getGCost(startNode))