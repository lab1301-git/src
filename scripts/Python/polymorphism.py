#!/usr/bin/python

######################################################################
# Author:      Lakshman Brodie - May 2021
# Description: Demonstrate inheritance in Python.  All variables are
#              private and access is only via the get and set methods.
#              This also demonstrates dictionary and list containers
#
######################################################################

from abc import ABC, abstractmethod
import datetime, itertools, os, sys

print("-----------------------------")
str = "Entered polymorphism.py"
print(str)
now = datetime.datetime.now()
print("Date: %s" % now)
print ("Python version: %s" % sys.version)
#print(os.uname())
print("-----------------------------")

# Base is an abstract class as it contains abstract methods
class Base(ABC):       
        __count = 0  # private static/class variable
        __data = []  # A private array of derived objects
        __stats = {} # A private dictionary of stats on contents of __data 

        @staticmethod
        def loadData(self):
           self.__data.append(self)
           Base.__count += 1 # keep a count of all objects constructed
           if 'DEBUG' in os.environ: 
               print("Base::loadData: Inserted %d" % Base.getObjectCount(self))
           return 0

       
        # Return the number of objects in the container
        @staticmethod
        def getCount(): # Duplicate of getObjectCount()
            return Base.__count 

        @staticmethod
        def getListData():
            return Base.__data

        # getObjectCount() returns the number of objects in the container
        @staticmethod
        def getObjectCount():
           containerCount = 0
           for element in Base.__data:
               containerCount += 1
           return (containerCount)

        @abstractmethod
        def setIdx():
           pass 

        @abstractmethod
        def getIdx():
            pass 

        @abstractmethod
        def setName():
           pass

        @abstractmethod
        def getName():
           pass
      
        @staticmethod
        def printAttributes():
            list = Base.getListData()
            print("Printing contents of array Base.__data...")
            for obj in list:
                print("idx= %-3d name=%s" % (obj.getIdx(), obj.getName()))

            stats = Base.getDictData()
            print("\nPrinting contents of stats in dictionary: %s" % stats)
            return 0

        @staticmethod
        def insertKeyValue(key, value):
            if key not in Base.__stats.keys():
                Base.__stats[key] = value 
            return 0 

        @staticmethod
        def updateKeyValue(key, value):
            Base.__stats.update({key: value})

        @staticmethod
        def getDictData():
            return Base.__stats

        @classmethod
        def overridden(self):
           print("Base::overridden()")
           return 0

class D1(Base):
    __idx = 0
    __name = ""

    def __init__(self, idx, name):  # ctor method
        print("D1::ctor invoked (idx=%-2d  name=%s)." % (idx, name))
        self.setIdx(idx) 
        self.setName(name)

    def setIdx(self, idx):
        self.__idx = idx
        return 0

    def getIdx(self):
        return self.__idx

    def setName(self, name):
        self.__name = name
        return 0

    def getName(self):
        return self.__name

class D2(Base):
    __idx = 0
    __name = ""

    def __init__(self, idx, name):  # ctor method
        print("D2::ctor invoked (idx=%-2d  name=%s)." % (idx, name))
        self.setIdx(idx) 
        self.setName(name)

    def setIdx(self, idx):
        self.__idx = idx
        return 0

    def getIdx(self):
        return self.__idx

    def setName(self, name):
        self.__name = name
        return 0

    def getName(self):
        return self.__name

    def overridden(self):
        print("D2::overridden()")
 

# Class to run the program and appropriately named main()
class main():

    @classmethod
    def runner(self):
        #B = Base()  #  Base() is an abstract class so can't be instantiated
        list = []
        
        x = 0         # Used by while loop
        seq=0         # Used to keep a count of objects inserted into list Base.__data 
        loop_cnt = 0  # Used to update dictionary Base.__stats
        
        # Create key/value pair in dictionary for D1 and D2
        #Base.insertKeyValue("D1", 0)  # redundant code that should be deleted
        #Base.insertKeyValue("D2", 0)  # redundant code that should be deleted
        
        # Insert 5 derived D1 & D2 objects into Base.__data via loadData()
        # method via while loop
        print("\nInserting records in list Base.__data and updating stats in dictionary Base.__stats...")
        while (x < 5):
            x += 1
            seq += 1
            loop_cnt += 1
            Base.loadData(D1(seq, "D1"))
            Base.updateKeyValue("D1", loop_cnt)
            seq += 1
            Base.loadData(D2(seq, "D2"))
            Base.updateKeyValue("D2", loop_cnt)
        
        # Now load an additional 6th D2 object into Base.__data 
        seq += 1
        Base.loadData(D2((seq), "D2"))  # Update dictionary Base.__stats
        
        # Update the dictionary for the 6th object
        loop_cnt += 1
        Base.updateKeyValue("D2", loop_cnt)
        
        # We now have loaded five D1 and six D2 objects into the __data array 
        # Two methods to get the count of derived objects in the array
        print("\n#####################################")
        print("ObjectCount=%d" % Base.getObjectCount())
        print("Base.getCount()=%d" % Base.getCount())
        
        stats = Base.getDictData()
        print("\nPrinting contents of stats in dictionary: %s" % stats)
        print("#####################################\n")
        
        # Here we get the __data array/list and loop around it printing contents
        print("\nIterating around list Base.__data...")
        # The list below contains two different types of objects
        list = Base.getListData()
        for obj in list:
            print("getIdx() = %-3d Name=%s" % (obj.getIdx(), obj.getName()))
            obj.overridden()
        
        print("----------------------------")
        # Call a static method that prints the contents of the array and dictionary
        print("\nPrint contents of array via base class method printAttributes()...")
        Base.printAttributes()
        return 0




#######################################
############### CALL MAIN FUNCTION ##################
#######################################

mainFunc = main()
ret = mainFunc.runner()
print("==================================")
exit(ret)

