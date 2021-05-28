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

print ("Python version: %s" % sys.version)


class zooException(Exception):
    def __init__(self, message):
        self.message = message



class animals(ABC):       
    LAME     = "LAME"
    HEALTHY  = "HEALTHY"
    LIVE     = "LIVE"
    DEAD     = "DEAD"
    MONKEY   = "Monkey"
    GIRAFFE  = "Giraffe"
    ELEPHANT = "Elephant"

    __hourly_min_rval = 0
    __hourly_max_rval = 20
    __feed_min_rval   = 10
    __feed_max_rval   = 25
    __feedRun         = 0
    __healthRunCount  = 0

    # Three random numbers, one for each type of animal used for feeding and
    # these class attributes are available in all instances
    m_feed_rnum = 0 
    g_feed_rnum = 0
    e_feed_rnum = 0

    __zoo = []  # A private array of derived animal objects

    @classmethod
    def loadData(cls, animal):
        animal.__zoo.append(animal)

    @classmethod
    def getObjectCount(cls):
        return (len(animals.__zoo)) # return size of __zoo

    @classmethod
    def getListData(cls):
        return cls.__zoo

    @classmethod
    def getObject(cls, idx):
        if (animals.getObjectCount() > idx):
            return(animals.__zoo[idx])
        else:
            str="\n*** Index provided: <%d> is bigger that size of list: <%d> ***\n" % (idx, animals.getObjectCount())
            try:
                raise zooException(str)
            except zooException as err:
                 
                print("\nanimals::getObject(): Fatal error:", err.message)
                return 1
            return 0

    @classmethod
    def getRangeFloat(cls, min, max):
        return(round(random.uniform(min, max), 3))

    @classmethod
    def genRandomValue(cls, min, max):
        return(round(random.uniform(min, max), 3))

    def setName(self, name, idx):
        return(name + "-" + str(idx)) 

    def setType(self):
        self.type = self.getAnimalType()
        return 0

    # These three class attributes are available to all instances 
    @classmethod
    def setFeedRval(cls, m, g, e):
        cls.m_feed_rnum = m
        cls.g_feed_rnum = g
        cls.e_feed_rnum = e

        print("\nanimals::setFeedRval(): m_feed_rnum=<%d>" % (cls.m_feed_rnum))
        print("animals::setFeedRval(): g_feed_rnum=<%d>" % (cls.g_feed_rnum))
        print("animals::setFeedRval(): e_feed_rnum=<%d>\n" % (cls.e_feed_rnum))
        return 0 

    def getMonkeyFeedRnum(self):
        # return class attribute from an instance method
        return (self.__class__.m_feed_rnum)

    def getGiraffeFeedRnum(self):
        # return class attribute from an instance method
        return (self.__class__.g_feed_rnum)

    def getElephantFeedRnum(self):
        # return class attribute from an instance method
        return (self.__class__.e_feed_rnum)

    def initValues(self, type, idx):
        # Set initial default values for all new animal instances
        self.setName(type, idx)
        self.type = self.setType()
        self.setStatus(animals.HEALTHY) 
        self.setHealth(100)
        self.feedRuns = 0      

    @classmethod
    def printBanner(cls, str):
        print("\n#############################################################")
        print("########## %s ##########" %(str));
        print("#############################################################")
        return 0
        
    def printInstance(self):
        rval      = "  Animal type  specific feed random number (0 == not fed yet!)"
        fedNum    = "   ** number of times fed **"
        healthRed = "   ** number of times health reduced **"
        if (self.getFeedValue() < 0):
            feed_s ="    ** FeedVal is -1 as animal is yet to be fed! **" 

        print("\n---------- printInstance() ----------")
        print("    Name      = %s" % self.getName())
        print("    Idx       = %d" % self.getIdx())
        print("    Health    = %d  (Threshold=%d)" % (self.getHealth(), self.getThresholdConst()))
        print("    FeedVal   = %d  %s" % (self.getFeedValue(), rval))
        print("    FeedRuns  = %s  %s" % (self.getFeedRun(), fedNum))
        print("    HealthRun = %s  %s" % (self.getHealthRunDown(), healthRed))
        print("    Status    = %s" % self.getStatus())
        return 0

    def printAllInstances(self):
        str = "printAllInstances() is dumping zoo list data"
        animals.printBanner(str);
        for obj in animals.getListData():
            obj.printInstance()
        
    def printHealthAttr(self):
        feed_s =   "   ** number of times fed **"
        health_s = "   ** number of times health reduced **"
        print("---------- <%s> ----------" % (self.getName()))
        print("    Health     = %d" % self.getHealth())
        print("    Status     = %s" % self.getStatus())
        print("    Threshold  = %s" % self.getThresholdConst())
        print("    FeedRuns   = %s  %s" % (self.getFeedRun(), feed_s))
        print("    HealthDown = %s  %s" % (self.getHealthRunDown(), health_s))
        return 0

    def changeStatus(self):
        chg = False
        if (self.getStatus() == animals.DEAD):
            return 0

        elif (self.getStatus() == animals.LAME and
                            self.getHealth() < self.getThresholdConst()):
            print("adjustHealthDownAllAnimals(1): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.DEAD, self.getName()))
            chg=True
            self.setStatus(animals.DEAD)

        elif (self.getStatus() == animals.LAME and
                 (self.getHealth() >= self.getThresholdConst())):
            print("adjustHealthDownAllAnimals(2): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.LIVE, self.getName()))
            self.setStatus(animals.LIVE)
            chg=True

        elif ((self.getType() == animals.ELEPHANT) and
                 (self.getHealth() < self.getThresholdConst())):
            print("adjustHealthDownAllAnimals(3): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.LAME, self.getName()))
            self.setStatus(animals.LAME)

        elif (self.getHealth() < self.getThresholdConst()):
            print("adjustHealthDownAllAnimals(4): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.DEAD, self.getName()))
            self.setStatus(animals.DEAD)

        else:
            print("adjustHealthDownAllAnimals(5): No change to status (%-7s) for <%-11s>" % (self.getStatus(), self.getName()))

        return 0

    # genFeedValue() needs to be called before each feed run as it
    # generates 3 random numbers that are class attributes.  This means they
    # are available to all instances of the class vie the get methods
    @classmethod
    def genFeedValue(cls):
        ret = 0
        # Generate three random values between 10 and 25
        m = animals.genRandomValue(10, 25)
        g = animals.genRandomValue(10, 25)
        e = animals.genRandomValue(10, 25)

        # Set the three values generated above in class attributes
        animals.setFeedRval(m, g, e)
        return ret


    # set the new health for one animal.  This method expects the caller to
    # have alreday regenerated the feed randon values.
    def feedAnimal(self):
        if (self.getStatus() == animals.DEAD):
            if 'DEBUG' in os.environ: 
                print("animals::feedAnimal(): %s is dead!" % (self.getName()))
            return 0

        if 'DEBUG' in os.environ: 
            print("animals::feedAnimal(): animal status = <%s>" % (self.getStatus()))
        val = animals.getFeedCount()  # get the incremented count
        # Set the number of feed runs that the LIVE/LAME instance has had
        self.setFeedRun(val) # The instance now has the number of feed runs
        rnum = self.getFeedValue()
        chealth =  self.getHealth()  # current health
        nhealth = (self.getHealth() + (self.getHealth() * (rnum/100)))

        # We don't want health to be more than 100% so use the lambda ternary
        # below to cap nhealth at 100% 
        nhealth = ((lambda: nhealth, lambda: 100)[ nhealth > 100]())
        self.setHealth(nhealth)          

        # The status may change for elephants as they may go LAME -> HEALTHY
        self.changeStatus();

        if 'DEBUG' in os.environ: 
            print("animals::feedAnimal(): %-11s oldHealth=<%-.2f> newHealth= <%-.2f>" % (self.getName(), chealth, nhealth)) 
        return 0            


    def feedAllAnimals(self):

        print("\nanimals::feedAllAnimals(): Feeding all animals")
        # Generate the feed random values
        animals.genFeedValue()

        str = "feedAllAnimals() is feeding all animals in zoo list"
        animals.printBanner(str);

        animals.incrementFeedCount()  # Increment the feed run count
        # Now we need to iterate around the zoo list/array
        for obj in animals.getListData():
            obj.feedAnimal()
        return 0

    def adjustHealthDown(self, value):
        type = self.getType()
        if (self.getStatus() == animals.DEAD):
            if 'DEBUG' in os.environ: 
                print("animals::adjustHealthDown(): %s is dead!" % (self.getName()))
            return 0

        v = self.getHealthRunCount()
        self.setHealthRunDown(v)
        health = self.getHealth() - (self.getHealth() * (value/100))
        self.setHealth(health)
        self.changeStatus()
        return 0

    def adjustHealthDownAllAnimals(self):
        print("\nanimals::adjustHealthDownAllAnimals(): Adjusting health down")
        str = "adjustHealthDownAllAnimals() is adjusting the health of all animals in zoo list"
        animals.printBanner(str);

        animals.incrementHealthRunCount()
        # Now we need to iterate around the zoo list/array
        for obj in animals.getListData():
            # Generate a random value for each animal
            val = animals.genRandomValue(0, 20)
            obj.adjustHealthDown(val)
        return 0

    def runWrapper(self):

        # print contents of animals.zoo list array
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.feedAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.feedAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.feedAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.feedAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.feedAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.adjustHealthDownAllAnimals()
        self.printAllInstances()

        self.feedAllAnimals()
        self.printAllInstances()
        return 0

    @classmethod
    def incrementFeedCount(cls):
        # We need to ensure that we don't feed dead animals!
        cls.__feedRun += 1
        return 0

    @classmethod
    def getFeedCount(cls):
        # This method uses the value set by incrementFeedCount() 
        return (cls.__feedRun)

    # The arg val passed here should be obtained from incrementFeedCount()
    def setFeedRun(self, val):
        # This method used the value set by incrementFeedCount() 
        self.feedRuns = val

    def getFeedRun(self):
        # This method used the value set by incrementFeedCount() 
        return(self.feedRuns)

    @classmethod
    def incrementHealthRunCount(cls):
        cls.__healthRunCount += 1
        return 0

    # This returns value set by incrementHealthRunCount()
    @classmethod
    def getHealthRunCount(self):
        return (animals.__healthRunCount)

    # The arg val passed here should be obtained from incrementHealthRunCount()
    def setHealthRunDown(self, val):
        pass 

    def getHealthRunDown(self):
        pass

    def getName(self):
        pass

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
    def setHealth(self):
        pass

    @abstractmethod
    def getHealth(self):
        pass

    @abstractmethod
    def setStatus(self, status):
        pass

    @abstractmethod
    def getStatus(self):
        pass

    @abstractmethod
    def setFeedValue(self):
        pass

    # getFeedValue() returns the animal specific random value used to calculate
    # feed quantity.  The correct derived class method is invoked
    # polymorphically when iterating around the zoo list/array
    @abstractmethod
    def getFeedValue(self):
        pass



class monkey(animals):
    __animalType = animals.MONKEY
    __threshold = 30


    def __init__(self, idx):  # ctor method

        # Define instance attributes below 
        self.__name = animals.setName(self, self.__animalType, idx)
        self.__idx = idx
        self.__status = ""
        self.__health = 0
        self.initValues(self.getType(), idx)
        self.feedRun=0
        self.feedValue = 0
        self.feedRuns = 0
        self.__healthRunDown = 0
        print("monkey::ctor   name = <%-11s>  idx=<%-2d>  health=<%f>" %
                             (self.getName(), self.getIdx(), self.getHealth()))
        
    @classmethod
    def monkeyFactory(cls, idx): # return an annonyamous instance
        return monkey(idx)

    def getName(self):
        return self.__name

    @classmethod 
    def getType(cls):
        return (cls.__animalType) 

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
        return self.__threshold

    def getAnimalType(self):
        return self.__animalType

    def setFeedValue(self, val):
        self.feedValue = val
        return 0

    # The arg val passed here should be obtained from incrementHealthRunCount()
    def setHealthRunDown(self, val):
        if (self.getStatus() != animals.DEAD):
            self.__healthRunDown = val

    def getHealthRunDown(self):
        return(self.__healthRunDown)

    # getFeedValue() returns the animal specific random value used to calculate
    # feed quantity.  The correct derived class method is invoked
    # polymorphically when iterating around the zoo list/array
    def getFeedValue(self):
        # return class attribute from an instance method
        return (animals.m_feed_rnum)


class giraffe(animals):
    __animalType = animals.GIRAFFE
    __threshold = 50

    def __init__(self, idx):  # ctor method

        # Define instance attributes below 
        self.__name = animals.setName(self, self.__animalType, idx)
        self.__idx = idx
        self.initValues(self.getType(), idx)
        self.__health = 100
        self.feedRun=0
        self.feedValue = 0
        self.feedRuns = 0
        self.__healthRunDown = 0
        print("giraffe::ctor  name = <%-11s>  idx=<%-2d>  health=<%f>" %
                             (self.getName(), self.getIdx(), self.getHealth()))
        
    @classmethod
    def giraffeFactory(cls, idx): # return an annonyamous instance
        return giraffe(idx)

    def getName(self):
        return self.__name

    @classmethod 
    def getType(cls):
        return (cls.__animalType) 

    def setIdx(self, idx):
        self.__idx = idx
        return 0

    def getIdx(self):
        return self.__idx

    def setHealth(self, health):
        if (self.getStatus() != animals.DEAD):
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
        return self.__threshold

    def getAnimalType(self):
        return self.__animalType

    def setFeedValue(self, val):
        self.feedValue = val
        return 0

    # The arg val passed here should be obtained from incrementHealthRunCount()
    def setHealthRunDown(self, val):
        self.__healthRunDown = val

    def getHealthRunDown(self):
        return(self.__healthRunDown)

    # getFeedValue() returns the animal specific random value used to calculate
    # feed quantity.  The correct derived class method is invoked
    # polymorphically when iterating around the zoo list/array
    def getFeedValue(self):
        # return class attribute from an instance method
        return (self.__class__.g_feed_rnum)


class elephant(animals):
    __animalType = animals.ELEPHANT
    __threshold = 70

    def __init__(self, idx):  # ctor method

        # Define instance attributes below 
        self.__name = animals.setName(self, self.__animalType, idx)
        self.__idx = idx
        self.initValues(self.getType(), idx)
        self.__health = 100
        self.feedRun=0
        self.feedValue = 0
        self.feedRuns = 0
        self.__healthRunDown = 0
        print("elephant::ctor name = <%-11s>  idx=<%-2d>  health=<%f>" %
                             (self.getName(), self.getIdx(), self.getHealth()))
        
    @classmethod
    def elephantFactory(cls, idx): # return an annonyamous instance
        return elephant(idx)

    def getName(self):
        return self.__name

    @classmethod 
    def getType(cls):
        return (cls.__animalType) 

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
        return self.__threshold

    def getAnimalType(self):
        return self.__animalType
    
    def setFeedValue(self, val):
        self.feedValue = val
        return 0

    # The arg val passed here should be obtained from incrementHealthRunCount()
    def setHealthRunDown(self, val):
        self.__healthRunDown = val

    def getHealthRunDown(self):
        return(self.__healthRunDown)

    # getFeedValue() returns the animal specific random value used to calculate
    # feed quantity.  The correct derived class method is invoked
    # polymorphically when iterating around the zoo list/array
    def getFeedValue(self):
        # return class attribute from an instance method
        return (self.__class__.e_feed_rnum)



class main():

    def runner(self):
    
        health=100
        i = idx = 0 
        # Populate array with five animals of each type
        while (i < 5):
            i += 1
            idx += 1
            animals.loadData(monkey.monkeyFactory(idx))
            idx += 1
            animals.loadData(giraffe.giraffeFactory(idx))
            idx += 1
            animals.loadData(elephant.elephantFactory(idx))

        m = animals.getObject(1)
        if (m == 1):
            exit(1 )
        m.runWrapper()
        print("========================================")



#####################################################
############### CALL MAIN FUNCTION ##################
#####################################################

mainFunc = main()
animals.printBanner("Starting zoo simulation")
print("")
ret = mainFunc.runner()
print("==================================")
exit(ret)


'''
            if (obj.getAnimalType() == animals.MONKEY):
                obj.setFeedValue(m)

            elif (obj.getAnimalType() == animals.GIRAFFE):
                obj.setFeedValue(g)

            elif (obj.getAnimalType() == animals.ELEPHANT):
                obj.setFeedValue(e)

            else:
                # We should never get here!
                # Someone has probably added a new derived class...
                print("genFeedValue(): Have you added a new derived class?") 
                ret=1
'''
