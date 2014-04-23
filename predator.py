from graphics import *
from math import *

class Predator(object):
    def __init__(self, x, y, heading, window):
        self.x = x
        self.y = y
        self.heading = heading
        self.window = window

        self.body = Circle(Point(x,y),20)
        self.body.draw(self.window)
        self.body.setFill("grey")
        self.body.setOutline("black")

        self.headLine = Circle(Point(x + 10 * sin(self.heading), y + 10 * cos(self.heading)),5)
        self.headLine.draw(self.window)
        self.headLine.setFill("black")

        self.kill = False

    
    #Getter methods
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getHeading(self):
        return self.heading

    def getKill(self):
        return self.kill

    def getAngleDifference(self,target):
        theta = self.heading
        
        #Get coordinates of target
        targetX = target.getX()
        targetY = target.getY()

        #print "original X:", targetX
        #print "original Y:", targetY

        #Alter coordinates so that self is the origin
        targetX -= self.x
        targetY -= self.y

        #print "subtracted X:", targetX
        #print "subtracted Y:", targetY

        #Apply a rotation to the coordinates so that they are in a
        #new coordinate plane where the heading of the predator
        #is the y-axis
        targetXp = (targetX * cos(theta)) - (targetY * sin(theta))
        targetYp = (targetX * sin(theta)) + (targetY * cos(theta))

        #print "rotated X:", targetXp
        #print "rotated Y:", targetYp

        #Get difference in heading
        if targetYp == 0:
            ttheta = pi/2
        else:
            ttheta = atan(abs(targetXp)/abs(targetYp))
        dist = sqrt((targetXp)**2 + (targetYp)**2)

        if dist < 20:
            self.kill = True
            self.body.setFill("red")
        else:
            self.kill = False
            self.body.setFill("grey")

        if targetXp > 0 and targetYp > 0:
            ttheta = (2 * pi) - ttheta
        elif targetXp < 0 and targetYp < 0:
            ttheta = pi - ttheta
        elif targetXp > 0 and targetYp < 0:
            ttheta = pi + ttheta

        #Put heading between -pi and pi
        if ttheta > pi:
            ttheta = ttheta - 2*pi

        return ttheta


    def move(self, preyList):
        potentialPrey = []
        for p in preyList:
            neighbors = p.getNeighborNumber()

            if neighbors < 3:
                dist = sqrt((self.x - p.getX())**2 + (self.y - p.getY())**2)
                potentialPrey.append([p,dist])

        if len(potentialPrey) == 0:
            #stand still if no targets
            if self.kill == True:
                self.kill = False
                self.body.setFill("grey")
            return
        
        #Do a linear search to find closest available prey
        minimum = potentialPrey[0]

        for p in potentialPrey:
            if p[1] < minimum[1]:
                minimum = p

        target = minimum[0]

        ttheta = self.getAngleDifference(target)

        if ttheta > 0:
            self.heading -= .05
        elif ttheta < 0:
            self.heading += .05

        if abs(ttheta) < (pi/6):
            dx = .3 * sin(self.heading)
            dy = .3 * cos(self.heading)

            self.x += dx
            self.y += dy
            self.body.move(dx,dy)

        self.headLine.undraw()
        self.headLine = Circle(Point(self.x + 10 * sin(self.heading), self.y + 10 * cos(self.heading)),5)
        self.headLine.draw(self.window)
        self.headLine.setFill("black")

        return

                
        
