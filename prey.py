from graphics import *
from math import *
from predator import *

class Prey(object):
    
    def __init__(self, index, x, y, heading, window):
        self.index = index
        self.x = x
        self.y = y
        self.heading = heading
        self.window = window

        self.neighbors = 0

        self.body = Circle(Point(x,y),10)
        self.body.draw(self.window)
        self.body.setFill("orange")
        self.body.setOutline("black")

    #Getter methods
    def getIndex(self):
        return self.index

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getHeading(self):
        return self.heading

    def getNeighborNumber(self):
        return self.neighbors

    
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

        if targetXp > 0 and targetYp > 0:
            ttheta = (2 * pi) - ttheta
        elif targetXp < 0 and targetYp < 0:
            ttheta = pi - ttheta
        elif targetXp > 0 and targetYp < 0:
            ttheta = pi + ttheta

        #Put heading between 0 and 2pi
        if ttheta < 0:
            ttheta = (2*pi) + ttheta

        return ttheta

    def setNeighborNumber(self,preyList):
        #RETURNS THE AVERGE HEADING, NOT THE NEIGHBOR NUMBER
        neighbors = 0
        sumHeading = 0
        
        for p in preyList:
            dist = sqrt((self.x - p.getX())**2 + (self.y - p.getY())**2)

            if dist < 70:
                sumHeading += p.getHeading()
                neighbors += 1

        self.neighbors = neighbors

        return sumHeading/float(neighbors)

    def calculateInputs(self,preyList,predator):
        inputs = []
        
        #Input: neighbors, heading of neighbors
        schoolHeading = self.setNeighborNumber(preyList)
        schoolHeading /= 2 * pi
        
        neighbors = self.getNeighborNumber()

                
        if neighbors > 2:
            self.body.setFill("purple")
        else:
            self.body.setFill("orange")

        if neighbors >= 3:
            neighbors = 1
        elif neighbors == 2:
            neighbors = .7
        elif neighbors == 1:
            neighbors = .3
        else:
            neighbors = 0
            
        inputs.append(neighbors)
        inputs.append(schoolHeading)

        #Input: distance from predator
        predDist = sqrt((self.x - predator.getX())**2 + (self.y - predator.getY())**2)
        if predDist < 29 and predator.getKill():
            self.body.undraw()
            return "DEAD"

        if predDist > 500:
            predDist = 1
        else:
            predDist /= float(500) 
            

        inputs.append(predDist)

        #Input: prey's heading relative to predator
        ptheta = self.getAngleDifference(predator)
        ptheta /= 2*pi

        inputs.append(ptheta)

        #Input: information about three closest
        potentialFriends = []

        if len(preyList) < 4:
            #Biological motivation: not being able to find food
            #It has no will to live, no safety in numbers
            return "DEAD"

        for p in preyList:
            if p != self:
                dist = sqrt((self.x - p.getX())**2 + (self.y - p.getY())**2)
                potentialFriends.append([p,dist])

        for i in range(3):
            first = potentialFriends[0]

            for p in potentialFriends:
                if p[1] < first[1]:
                    first = p

            potentialFriends.remove(first)

            dist = sqrt((self.x - first[0].getX())**2 + (self.y - first[0].getY())**2)
            if dist > 500:
                dist = 1
            else:
                dist /= 500
                
            inputs.append(dist)

            angDiff = self.getAngleDifference(first[0])

            angDiff /= 2*pi
            
            inputs.append(angDiff)
                
        return inputs

    def move(self,translate,rotate):
        translate /= 5
        translate += .05

        rotate -= .5
        rotate /= 10

        #0 is down, pi is up, pi/2 is right
        #negative is turn clockwise, positive is ccw
        self.heading += rotate

        #Make heading positive if it is negative
        if self.heading < 0:
            self.heading = (2 * pi) + self.heading
        if self.heading > 2*pi:
            self.heading %= 2*pi
        
        
        #Change the heading if too close to walls
        if self.y < 15:
            if self.heading <= pi and self.heading > pi/2:
                self.heading -= pi/2
            elif self.heading > pi and self.heading < 3*pi/2:
                self.heading += pi/2
        elif self.y > (self.window.getHeight() - 15):
            if self.heading >= 0 and self.heading < pi/2:
                self.heading += pi/2
            elif self.heading < 2*pi and self.heading > 3*pi/2:
                self.heading -= pi/2
        elif self.x < 15:
            if self.heading > pi and self.heading <= 3*pi/2:
                self.heading -= pi/2
            elif self.heading > 3*pi/2 and self.heading < 2*pi:
                self.heading += pi/2
        elif self.x > (self.window.getWidth() - 15):
            if self.heading > 0 and self.heading <= pi/2:
                self.heading -= pi/2
            elif self.heading > pi/2 and self.heading < pi:
                self.heading += pi/2
        
        #Make heading positive if it is negative
        if self.heading < 0:
            self.heading = (2 * pi) + self.heading
        
        dx = translate * sin(self.heading)
        dy = translate * cos(self.heading)

        self.x += dx
        self.y += dy            

        self.body.move(dx,dy)
        
        return
