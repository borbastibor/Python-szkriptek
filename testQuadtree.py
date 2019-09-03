import quadtree
import random
import pygame
from pygame.locals import *
import sys

##def createNewData():
##    return (random.randint(0,640),random.randint(0,480))

tree = quadtree.QuadTree(0,0,640,480)
points = []

##for i in range(80):
##    newdata = createNewData()
##    newNodeData = quadtree.NodeData(newdata[0], newdata[1], "adat")
##    tree.addData(newNodeData)
##    points.append(newNodeData)
    
pygame.init()
screen = pygame.display.set_mode((640,480), HWSURFACE | DOUBLEBUF)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            newNodeData = quadtree.NodeData(event.pos[0], event.pos[1], "adat")
            tree.addData(newNodeData)
            points.append(newNodeData)

    screen.fill((0,0,0))
    for i in points:
        retval = tree.root.searchForDataXY(i)
        if retval is not None:
            pygame.draw.rect(screen,(255,255,255), pygame.Rect(retval.x0, retval.y0, retval.width, retval.height), 2)
    pygame.display.update()
