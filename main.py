#Joe Boninger and Melissa O'Connor

from graphics import *
from math import *
from prey import Prey
from predator import Predator
from random import *
from math import *
import sys

def testPredator():
    window = GraphWin("CS81 Final Project",1000,1000)
    window.setBackground("blue")

    preyList = []
    
    p1 = Prey(0,15,15,0,window)
    p2 = Prey(1,200,350,0,window)
    p3 = Prey(2,220,350,0,window)
    p4 = Prey(3,210,350,0,window)
    p5 = Prey(4,300,400,0,window)
    p6 = Prey(5,310,405,0,window)
    p7 = Prey(6,650,30,0,window)
    p8 = Prey(7,170,320,0,window)

    preyList.append(p1)
    preyList.append(p2)
    preyList.append(p3)
    preyList.append(p4)
    preyList.append(p5)
    preyList.append(p6)
    preyList.append(p7)
    preyList.append(p8)
    
    shark = Predator(650,650,0,window)

    while True:
        for p in preyList:
            p.setNeighborNumber(preyList)
            inputs = p.calculateInputs(preyList,shark)

            if inputs == "DEAD":
                preyList.remove(p)
                
            p.move(1,.5)
                
        shark.move(preyList)
    
        if window.checkMouse():
            sys.exit()
    return

def testInputs():
    window = GraphWin("CS81 Final Project",700,700)
    window.setBackground("blue")

    preyList = []
    
    p1 = Prey(0,350,350,pi,window)
    p2 = Prey(1,340,350,3*pi/2,window)
    p3 = Prey(2,370,350,pi/2,window)
    p4 = Prey(3,350,445,pi,window)

    preyList.append(p1)
    preyList.append(p2)
    preyList.append(p3)
    preyList.append(p4)

    shark = Predator(350,250,pi/2,window)

    print p1.calculateInputs(preyList,shark)

    window.getMouse()
    window.close()

def main():
    testPredator()
    #testInputs()
    
main()
    
