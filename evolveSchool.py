from graphics import *
from math import *
from prey import Prey
from predator import Predator
from random import *
from math import *
import cPickle as pickle
import sys

# When using NEAT you must import the following
from neat import config, population, chromosome, genome, visualize
from neat.nn import nn_pure as nn

# When using NEAT you must create a configuration file to set the
# parameters of the evolution
config.load('config')

chromosome.node_gene_type = genome.NodeGene

def eval_fitness(population):
    for chromo in population:
        chromo.fitness = eval_individual(chromo)
        print "Fitness:", chromo.fitness

def eval_individual(chromo,logFP=None):
    brain = nn.create_phenotype(chromo)
    sumTime = 0
    sumPeople = 0
    sumDist = 0
    
    for trial in range(3):
        window = GraphWin("CS81 Final Project",1000,1000)
        window.setBackground("blue")
        
        preyList = []
        time = 0
        people = 0
        distance = 0
    
        p1 = Prey(0,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p2 = Prey(1,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p3 = Prey(2,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p4 = Prey(3,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p5 = Prey(4,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p6 = Prey(5,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p7 = Prey(6,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p8 = Prey(7,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p9 = Prey(8,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p10 = Prey(9,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p11 = Prey(10,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p12 = Prey(11,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p13 = Prey(12,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p14 = Prey(13,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p15 = Prey(14,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p16 = Prey(15,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p17 = Prey(16,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p18 = Prey(17,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p19 = Prey(18,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        p20 = Prey(19,(random()*800) + 100,(random()*800) + 100,choice([-1,1])*2*pi*random(),window)
        

        preyList.append(p1)
        preyList.append(p2)
        preyList.append(p3)
        preyList.append(p4)
        preyList.append(p5)
        preyList.append(p6)
        preyList.append(p7)
        preyList.append(p8)
        preyList.append(p9)
        preyList.append(p10)
        preyList.append(p11)
        preyList.append(p12)
        preyList.append(p13)
        preyList.append(p14)
        preyList.append(p15)
        preyList.append(p16)
        preyList.append(p17)
        preyList.append(p18)
        preyList.append(p19)
        preyList.append(p20)
    
        shark = Predator(1000,1000,5*pi/4,window)

        while (len(preyList) > 3) and time < 15000:
            time += 1
            
            for p in preyList:
                if time %50 == 0:
                    distance += p.getTraveled()
                    p.setPastX(p.getX())
                    p.setPastY(p.getY())
                    
                brain.flush()
                inputs = p.calculateInputs(preyList,shark)

                if inputs == "DEAD":
                    preyList.remove(p)

                else:
                    outputs = brain.pactivate(inputs)
                    p.move(outputs[0],outputs[1])

            if time == 4500:
                print "Shark attack!"
            if time > 4500:
                shark.move(preyList)

        window.close()

        people = len(preyList)
        time -= 4500
        time /= float(10500)
        people /= float(20)
        distance /= float(75000)

        sumTime += time
        sumPeople += people
        sumDist += distance
        
    return .4*(sumTime/3) + .4*(sumPeople/3) + .2*(sumDist/3)

# Tell NEAT that we want to use the above function to evaluate fitness
population.Population.evaluate = eval_fitness

# Create a population (the size is defined in the configuration file)
pop = population.Population()

# Run NEAT's genetic algorithm for at most 30 epochs
# It will stop if fitness surpasses the max_fitness_threshold in config file
pop.epoch(30, report=True, save_best=True)

# Plots the evolution of the best/average fitness
visualize.plot_stats(pop.stats)

# Visualizes speciation
visualize.plot_species(pop.species_log)

