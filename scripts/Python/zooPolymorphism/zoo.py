#!/usr/bin/python

######################################################################
# Author:      Lakshman Brodie - May 2021
# Date:        24th May 2021
# Description: The code addresses the following specification: 
#
# Write a simple Zoo simulator which contains 3 different types of animals:
#  monkey,
#  giraffe
#  elephant
#
# The zoo should open with 5 of each type of animal.
# Each animal has a health value held as a percentage (100% is completely
# healthy)
# Every animal starts at 100% health. This value should be a floating point
# value.
#
# The application should act as a simulator, with time passing at the rate of 
# 1 hour with each iteration. Every hour that passes, a random value between 0
# and 20 is to be generated for each animal. This value should be passed to 
# the appropriate animal, whose health is then reduced by that percentage of 
# their current health.
#
# The user must be able to feed the animals in the zoo. When this happens,
# the zoo should generate three random values between 10 and 25; one for each
# type of animal. The health of the respective animals is to be increased by 
# the specified percentage of their current health. Health should be capped 
# at 100%.
#
# When an Elephant has a health below 70% it cannot walk. If its health does 
# not return above 70% once the subsequent hour has elapsed, it is pronounced 
# dead.
# When a Monkey has a health below 30%, or a Giraffe below 50%, it is
# pronounced dead straight away.
#
# This program demonstrates the OO "Is a" relationship via polymorphisim.
#
######################################################################

from abc import ABC, abstractmethod
import datetime, itertools, os, sys, random

class animals(ABC):       
    OK       = "OK"
    LAME     = "LAME"
    DEAD     = "DEAD"
    MONKEY   = "Monkey"
    GIRAFFE  = "Giraffe"
    ELEPHANT = "Elephant"

    __hourly_min_rval = 0
    __hourly_max_rval = 20
    __feed_min_rval   = 10
    __feed_max_rval   = 25

    __zoo = []  # A private array of derived animal objects

    @classmethod
    def loadData(cls, animal):
        animal.__zoo.append(animal)

    @classmethod
    def getListData(cls):
        return cls.__zoo

    @classmethod
    def getRangeFloat(cls, min, max):
        return(round(random.uniform(min, max), 3))

    @classmethod
    def genRandomValue(cls, min, max):
        return(round(random.uniform(min, max), 3))

    def setName(self, name, idx):
        return(name + "-" + str(idx)) 

    @abstractmethod
    def getName(self):
        pass

    def setType(self):
        self.type = self.getAnimalType()
        return 0

    def initValues(self, type, idx):
        # Set initial default values for all new animal instances
        self.setName(type, idx)
        self.type = self.setType()
        self.setStatus("OK") 
        self.setHealth(100)
        
    def printInstanceAttr(self):
        print("\n---------- printInstanceAttr() ----------")
        print("    Name   = %s" % self.getName())
        print("    Idx    = %d" % self.getIdx())
        print("    Health = %d" % self.getHealth())
        print("    Status = %s" % self.getStatus())
        return 0
        
    def printHealthAttr(self):
        print("---------- <%s> ----------" % (self.getName()))
        print("    Health     = %d" % self.getHealth())
        print("    Status     = %s" % self.getStatus())
        print("    Threshold  = %s" % self.getThresholdConst())
        print("    FeedRuns   = %s" % self.getFeedRuns())
        print("    FeedRuns   = %s" % self.getFeedRuns())
        print("    HealthRuns = %s" % self.getHealthRunDown())
        return 0

    def reduceHealth(self, value):
        type = self.getType()
        if (self.getStatus() == "DEAD"):
            #if 'DEBUG' in os.environ: 
            print("animals::reduceHealth(): %s is dead!" % (self.getName()))
            return 0

        health = self.getHealth() -  (self.getHealth() * (value/100))
        self.setHealth(health)
        self.changeStatus()
        return 0

    def changeStatus(self):
            chg = False
            if (self.getStatus() == "DEAD"):
                return 0

            elif (self.getStatus() == "LAME" and
                                self.getHealth() < self.getThresholdConst()):
                self.setStatus("DEAD")
                chg=True

            elif (self.getStatus() == "LAME" and
                     (self.getHealth() >= self.getThresholdConst())):
                setStatus("LIVE")
                chg=True

            elif ((self.getType() == "Elephant") and
                     (self.getHealth() < self.getThresholdConst())):
                self.setStatus("LAME")

            elif (self.getHealth() < self.getThresholdConst()):
                self.setStatus("DEAD")

            else:
                print("No change to status for <%s>" % (self.getName()))

            return 0

    @abstractmethod
    def getType(self):
        pass

    @abstractmethod
    def setIdx(self, idx):
        pass

    def getThreashold(self):
        return (self.__m_threshold)

    @abstractmethod
    def getIdx(self):
        pass
    
    @abstractmethod
    def setHealth(self, health):
        pass
    
    @abstractmethod
    def getHealth(self):
        pass

    @abstractmethod
    def getHealth(self):
        pass

    @abstractmethod
    def setHealthRunDown(self):
        pass

    @abstractmethod
    def getHealthRunDown(self):
        pass
     
    @abstractmethod
    def setFeedRuns(self):
        pass
     
    @abstractmethod
    def getFeedRuns(self):
        pass



class monkey(animals):
    __animalType = "Monkey"
    __m_threshold = 30


    def __init__(self, idx):  # ctor method

        # Define instance attributes below 
        self.__name = animals.setName(self, self.__animalType, idx)
        self.__idx = idx
        self.__status = ""
        self.__health = 0
        self.initValues(self.getType(), idx)
        self.feedRun=0
        self.healthRunDown=0
        print("monkey::ctor name=<%s>  idx=<%d>  health=<%f>" %
                             (self.getName(), self.getIdx(), self.getHealth()))
        
    @classmethod
    def monkeyFactory(cls, idx): # return an annonyamous instance
        return monkey(idx)

    def getName(self):
        return self.__name

    @classmethod 
    def getType(self):
        return (self.__animalType) 

    def setIdx(self, idx):
        self.__idx = idx
        return 0

    def getIdx(self):
        return self.__idx

    def setHealth(self, health):
        self.__health = health
        return 0

    def getHealth(self):
        return self.__health

    def setStatus(self, status):
        self.__status = status
        return 0

    def getStatus(self):
        return self.__status

    def getThresholdConst(self):
        return self.__m_threshold

    def getAnimalType(self):
        return self.__animalType

    def setHealthRunDown(self):
        self.healthRunDown += 1
        return 0

    def getHealthRunDown(self):
        return(self.healthRunDown)
     
    def setFeedRuns(self):
        self.feedRun += 1
        return 0
     
    def getFeedRuns(self):
        return(self.feedRun)


class giraffe(animals):
    __animalType = "Giraffe"
    __m_threshold = 50

    def __init__(self, idx):  # ctor method

        # Define instance attributes below 
        self.__name = animals.setName(self, self.__animalType, idx)
        self.__idx = idx
        self.initValues(self.getType(), idx)
        self.__health = 100
        self.feedRun=0
        self.healthRunDown=0
        print("giraffe::ctor name=<%s>  idx=<%d>  health=<%f>" %
                             (self.getName(), self.getIdx(), self.getHealth()))
        
    @classmethod
    def giraffeFactory(cls, idx): # return an annonyamous instance
        return giraffe(idx)

    def getName(self):
        return self.__name

    @classmethod 
    def getType(self):
        return (self.__animalType) 

    def setIdx(self, idx):
        self.__idx = idx
        return 0

    def getIdx(self):
        return self.__idx

    def setHealth(self, health):
        self.__health = health
        return 0

    def getHealth(self):
        return self.__health

    def setStatus(self, status):
        self.__status = status
        return 0

    def getStatus(self):
        return self.__status

    def getThresholdConst(self):
        return self.__m_threshold

    def getAnimalType(self):
        return self.__animalType

    def setHealthRunDown(self):
        self.healthRunDown += 1
        return 0

    def getHealthRunDown(self):
        return(self.healthRunDown)
     
    def setFeedRuns(self):
        self.feedRun += 1
        return 0
     
    def getFeedRuns(self):
        return(self.feedRun)



class elephant(animals):
    __animalType = "Elephant"
    __m_threshold = 70

    def __init__(self, idx):  # ctor method

        # Define instance attributes below 
        self.__name = animals.setName(self, self.__animalType, idx)
        self.__idx = idx
        self.initValues(self.getType(), idx)
        self.__health = 100
        self.feedRun=0
        self.healthRunDown=0
        print("elephant::ctor name=<%s>  idx=<%d>  health=<%f>" %
                             (self.getName(), self.getIdx(), self.getHealth()))
        
    @classmethod
    def elephantFactory(cls, idx): # return an annonyamous instance
        return elephant(idx)

    def getName(self):
        return self.__name

    @classmethod 
    def getType(self):
        return (self.__animalType) 

    def setIdx(self, idx):
        self.__idx = idx
        return 0

    def getIdx(self):
        return self.__idx

    def setHealth(self, health):
        self.__health = health
        return 0

    def getHealth(self):
        return self.__health

    def setStatus(self, status):
        self.__status = status
        return 0

    def getStatus(self):
        return self.__status

    def getThresholdConst(self):
        return self.__m_threshold

    def getAnimalType(self):
        return self.__animalType

    def setHealthRunDown(self):
        self.healthRunDown += 1
        return 0

    def getHealthRunDown(self):
        return(self.healthRunDown)
    
    def setFeedRuns(self):
        self.feedRun += 1
        return 0
     
    def getFeedRuns(self):
        return(self.feedRun)


class main():

    def runner(self):
    
        health=100
        i = idx = 0 
        while (i < 5):
            i += 1
            idx += 1
            animals.loadData(monkey.monkeyFactory(idx))
            idx += 1
            animals.loadData(giraffe.giraffeFactory(idx))
            idx += 1
            animals.loadData(elephant.elephantFactory(idx))

        print("\nDumping data from list/array:")
        zoo = animals.getListData()
        
        for obj in zoo:
            obj.printInstanceAttr()


            val=obj.genRandomValue(9, 20)
            print("\nReducing health...")
            obj.reduceHealth(val)
            obj.setHealthRunDown()
            obj.printHealthAttr()

            print("========================================")

            val=obj.genRandomValue(9, 20)
            print("\nReducing health...")
            obj.reduceHealth(val)
            obj.setHealthRunDown()
            obj.printHealthAttr()

            print("========================================")

            val=obj.genRandomValue(9, 20)
            print("\nReducing health...")
            obj.reduceHealth(val)
            obj.setHealthRunDown()
            obj.printHealthAttr()

            print("========================================")
            val=obj.genRandomValue(9, 20)
            print("\nReducing health...")
            obj.reduceHealth(val)
            obj.setHealthRunDown()
            obj.printHealthAttr()

            print("========================================")
            val=obj.genRandomValue(9, 20)
            print("\nReducing health...")
            obj.reduceHealth(val)
            obj.setHealthRunDown()
            obj.printHealthAttr()


        #print("Random value=%f" % (m.getRangeFloat(0, 20)))
        #print("Random value=%s" % (str(m.getRangeFloat(0, 20)) + "LL"))

        #print(m.getHealth())

#####################################################
############### CALL MAIN FUNCTION ##################
#####################################################

mainFunc = main()
ret = mainFunc.runner()
print("==================================")
exit(ret)

