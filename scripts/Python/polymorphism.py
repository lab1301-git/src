#!/usr/bin/python

######################################################################
# Author:      Lakshman Brodie - May 2021
# Description: Demonstrate polymorphism in Python.  All variables are
#              private and access is only via the get and set methods.
#
######################################################################

from abc import ABC, abstractmethod
from collections import Counter
from os import environ as env
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

        def setIdx():
           pass 

        def getIdx():
            pass 

        def setName():
           pass

        def getName():
           pass
      
        @staticmethod
        def printAttributes():
            list = Base.getListData()
            print("Printing contents of array Base.__data...")
            for obj in list:
                print("idx= %-3d name=%s" % (obj.getIdx(), obj.getName()))
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



#######################################
############### MAIN ##################
#######################################

list = []

x = 0
seq=0

# Load derived objects into an array in the base class via loadData() static
# method
while (x < 5):
    x += 1
    seq += 1
    Base.loadData(D1(seq, "D1"))
    seq += 1
    Base.loadData(D2(seq, "D2"))

# Two methods to get the count of derived objects in the array
print("\nObjectCount=%d" % Base.getObjectCount())
print("Base.getCount()=%d" % Base.getCount())

# Here we get the array and then loop around it printing contents
print("\nIterating around list Base.__data...")
list = Base.getListData()
for obj in list:
    print("getIdx() = %-3d Name=%s" % (obj.getIdx(), obj.getName()))


print("----------------------------")
# Call a static method that prints the contents of the array
print("\nPrint contents of array via base class method printAttributes()...\n")
Base.printAttributes()

print("==================================")
