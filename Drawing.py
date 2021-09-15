import pygame, sys
from Colours import BLACK

def showTextInNode(WIN, text, centrePixel, font):
    #if not(self.isBarrier or self.isStart or self.isEnd):
    text = str(text)
    textsurface = font.render(text, False, (0, 0, 0))
    WIN.blit(textsurface,(centrePixel[0]-3, centrePixel[1]-10)) # -3 and -10 makes the text more centred

def noSolutions(WIN, WIDTH:int):
    for i in range(255, 0, -1):
        WIN.fill((i,i,i))
        pygame.time.wait(2)
        pygame.display.update()

    font = pygame.font.SysFont('arial', 80)
    textsurface = font.render('No Solutions', True, (255, 255, 255))
    WIN.blit(textsurface,((WIDTH//2)-180, (WIDTH//2)-200))

    pygame.display.update()

    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def drawLines(WIN, grid, WIDTH, lineColor, gapWidth):
    for x in grid:
        for column in x:
            verticalStart = 0, column.left
            verticalEnd = WIDTH, column.left
            pygame.draw.line(WIN, lineColor, verticalStart, verticalEnd, gapWidth) #surface, color, start, end, width

    for x in grid:
        for row in x:
            horizontalStart = row.left, 0
            horizontalEnd = row.left, WIDTH
            pygame.draw.line(WIN, lineColor, horizontalStart, horizontalEnd, gapWidth) #surface, color, start, end, width

def drawNodeSquares(WIN, grid, startNode, endNode, WIDTH, lineColour, gapWidth):
    WIN.fill(BLACK)
    for row in grid:
        for node in row:
            node.draw_square(WIN)
            if endNode != '' and startNode != '':
                if node.isOpen == True:
                    showTextInNode(WIN, node.getFCost(endNode, startNode), node.centrePixel, node.font) # window, text, centrepixel, font
    drawLines(WIN, grid, WIDTH, lineColour, gapWidth)
    
def UpdateAllColors(grid):
    for row in grid:
        for node in row:
            node.updateColor()

def drawPath(WIN, startNode, endNode, clock, FPS, grid, WIDTH, lineColour, gapWidth):
    parent = endNode.parent

    drawingPath = True
    while drawingPath:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()

        if parent.parent == None:
            drawingPath = False
            # pygame.time.wait(2000)
            # pygame.quit()
            # sys.exit()
            
        parent.setPath()

        UpdateAllColors(grid)
        drawNodeSquares(WIN, grid, startNode, endNode, WIDTH, lineColour, gapWidth)
        clock.tick(FPS)
        parent = parent.parent
        
        pygame.display.update()