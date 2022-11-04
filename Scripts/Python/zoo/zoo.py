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
from inspect import currentframe, getframeinfo
from curses import wrapper
import datetime, itertools, os, sys, random, time
import logging, pwd, platform, curses, traceback

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

    menu_options = {

            1:    'Feed All Animals',
            2:    'Adjust Health Down',
            3:    'Print All Instances',
            4:    'Exit',
    }

    __zoo = []  # A private array of derived animal objects
    __lastOption = 1
    __script = "%s" % (os.path.basename(sys.argv[0]))
    __logdir = "/tmp"
    __starStr = "***************************************************************"
    __fatalStr = "*** FATAL ERROR ***"
    __warningStr = "*** WARNING ***"

    @classmethod
    def getScriptName(cls):
        return cls.__script

    @classmethod
    def getSstr(cls):
        return cls.__starStr

    @classmethod
    def getWstr(cls):
        return cls.__warningStr

    @classmethod
    def getFstr(cls):
        return cls.__fatalStr

    @classmethod
    def dummyInput(cls):
        __func = "%s:dummyInput():" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        logger.info("\n%s" % (__func))
        promptStr = "\n\n\t\t...Press any key to continue\n"
        logger.info("%s %s" % (__func, promptStr))
        dummy = input(promptStr)
        return 0

    @classmethod
    def setLastOption(cls, option):
        __func = "%s:setLastOption()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        logger.info("\n%s" % (__func))
        logger.info("%s Setting __lastOption to '%s'" % (__func, str(option)) )
        cls.__lastOption = option
        return 0

    @classmethod
    def getLastOption(cls):
        __func = "%s:getLastOption()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        logger.info("\n%s" % (__func))
        logger.info("%s Returning __lastOption '%s'" % (__func, cls.__lastOption))
        return cls.__lastOption

    @classmethod
    def cursesMenu(cls):
        __func = "%s:cursesMenu()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        logger.info("\n%s" % (__func))
        option = 0
        try:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()

            stdscr.keypad(1)
            stdscr.border(1)
            stdscr.clear()
            spacing = 2
            (maxcol, maxline) = stdscr.getmaxyx()
            start_line = 10
            line = start_line
            print("%s: maxcol=%d  maxline=%d" % (__func, maxcol, maxline))
            col = int(maxcol/2)
            stdscr.addstr(line -3, col + 10, 'MAIN MENU', curses.A_UNDERLINE) 
            rev_pos = 0
            col += 8
            for key in animals.menu_options.keys():
                if (key ==  1):  
                    stdscr.addstr(line, col, "%s" % (animals.menu_options[key]), curses.A_REVERSE)
                    rev_pos = key
                else:
                    stdscr.addstr(line, col, "%s" % (animals.menu_options[key]), curses.A_NORMAL)
                line += spacing 

            navigation = "Up/Down \u2191\u2193    Use <CR> for selection     <q> for Exit"
            stdscr.addstr(line + 1, col - 10, "%s" % (navigation), curses.A_STANDOUT)
            statusLine = line + 3
            statusCol = col - 10
            logfile = cls.getLogfile()
            current_branch = "method not implemented as yet!"
            #stdscr.addstr(statusLine, statusCol, "Status messages" % curses.A_NORMAL)
            stdscr.addstr(line - spacing, col + 5, "")

            key = 0
            option = 1
            prev = 1
            line = start_line
            while True:
                ch = int(stdscr.getch())
                if (ch == ord('q')): 
                    option = len(animals.menu_options)

                if (ch == ord('q') or ch == ord('\n')): 
                    break

                elif (int(ch) > int(48) and int(ch) <= (48 + len(animals.menu_options))):
                    option = it(ch) - 48

                elif (ch == curses.KEY_DOWN):
                    prev = option
                    option += 1
                    if (option > len(animals.menu_options)):
                        stdscr.addstr(line, col, "%s" % (animals.menu_options[prev]), curses.A_NORMAL)
                        option = 1
                        key = 0
                        option = key
                        line = start_line
                        stdscr.addstr(line, col, "%s" % (animals.menu_options[option]), curses.A_REVERSE)
                        continue
                    key += 1
                    stdscr.addstr(line, col, "%s" % (animals.menu_options[prev]), curses.A_NORMAL)

                    line += spacing
                    stdscr.addstr(line, col, "%s" % (animals.menu_options[option]), curses.A_REVERSE)

                elif (ch == curses.KEY_UP):
                    prev = option
                    option -= 1
                    if (option < 1):
                        option = len(animals.menu_options)
                        stdscr.addstr(line, col, "%s" % (animals.menu_options[prev]), curses.A_NORMAL)
                        line = start_line + (len(animals.menu_options) * spacing) - spacing
                        stdscr.addstr(line, col, "%s" % (animals.menu_options[option]), curses.A_REVERSE)
                        continue
                    stdscr.addstr(line, col, "%s" % (animals.menu_options[prev]), curses.A_NORMAL)

                    line -= spacing
                    stdscr.addstr(line, col, "%s" % (animals.menu_options[option]), curses.A_REVERSE)
        except:
            traceback.print_exc()

        finally:
            stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

        logger.info("%s Returning option '%d'" % (__func, option))
        cls.setLastOption(option)
        return option

    @classmethod
    def handleInput(self):
        __func = "%s:handleInput()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        ret = 1
        try:
            cwd = os.getcwd()
        except OSError as e:
            logger.critical("%s getcwd() encountered an error for '%s'" % (__func, str(e)))
            frameinfo = getframeinfo(currentframe())
            logger.debug("%s %s lineno %s" % (__func, frameinfo.filename, frameinfo.lineno))
            return 1
        if (__name__ == '__main__'):
            while (True):
                option = self.cursesMenu()
                logger.info("%s: cursesMenu() returned option '%s'" % (__func, str(option)))
                
                if (option == 1):
                    os.system('clear')
                    ret = self.feedAllAnimals(self)
                    ret = animals.dummyInput()

                elif (option == 2):
                    os.system('clear')
                    ret = self.adjustHealthDownAllAnimals(self)
                    ret = animals.dummyInput()

                elif (option == 3):
                    os.system('clear')
                    ret = self.printAllInstances(self)
                    ret =     animals.dummyInput()

                elif (option == len(animals.menu_options)):
                    os.system('clear')
                    ret = len(animals.menu_options)
                    break

                else:
                    print("\n\n            '%s' is an invalid option" % (str(option)))
                    logger.warning("\n\n            '%s' is an invalid option" % (str(option)))
                    time.sleep(3)
        return ret

    @classmethod
    def getTime(cls):
        __func = "%s:getTime()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        logger.info("\n%s" % (__func))
        ts = datetime.datetime.now()
        ts_fmt = "%d/%m/%Y %H:%M:%S"
        fmt_time = ts.strftime(ts_fmt)
        return fmt_time

    @classmethod
    def returnLoggerObject(cls):
        __func = "%s:returnLoggerObject()" % (cls.getScriptName())
        # Return a reference to the same logger instance consistently
        return logging.getLogger(cls.getScriptName())

    @classmethod
    def getLogfile(cls):
        __func = "%s:getLogfile()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()
        
        uid = pwd.getpwuid(os.getuid())[0]
        script = (cls.getScriptName()).split('.')[0]
        dt = datetime.datetime.now()
        ts_fmt = "%A"
        day_of_week = dt.strftime(ts_fmt)[0:3]

        logfile = "%s/%s-%s-%s.log" % (cls.__logdir, script, uid, day_of_week)
        logger.info("\n%s" % (__func))

        print("%s Returning logfile ('%s')" % (__func, logfile))
        logger.info("%s Returning logfile ('%s')" % (__func, logfile))
        return logfile

    @classmethod
    def turnLoggingOn(cls):
        __func = "%s:turnLoggingOn" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        logfile = cls.getLogfile()
        logger.setLevel(logging.INFO)
        logger.setLevel(logging.WARNING)
        logger.setLevel(logging.CRITICAL)
        logger.setLevel(logging.DEBUG)
         
        fmt = "%d/%m/%Y %H:%M:%S"
        current_date = datetime. datetime.now()
        fmt_current_date = current_date.strftime(fmt)
        today = datetime.datetime.strptime(fmt_current_date, fmt)

        try:
            # Calculate logfile modification time since epoch.  Unlike WINDOWS, there is no
            # file creation time in UNIX so we use mtime instead of ctime.
            mtime = os.path.getmtime(logfile)
            fmt_mtime = time.strftime(fmt, time.localtime(mtime))
            log_modified_date = datetime.datetime.strptime(fmt_mtime, fmt)
            msg = "%s Found existing logfile '%s'" % (__func, logfile)
        except FileNotFoundError as e:
            log_modified_date = today
            frameinfo = getframeinfo(currentframe())
            line_no = "%s %s lineno %s" % (__func, frameinfo.filename, frameinfo.lineno)
            msg = "%s\n\n%s ** %s ** Logfile '%s' is missing.  Creating a new logfile..." % (line_no, __func, e, logfile)
            logger.info("%s ** %s ** Logfile '%s' is missing.  Creating a new logfile..." % (__func, e, logfile))
            time.sleep(2)

        # Open/create logfile
        log_fd = logging.FileHandler(logfile)
        logger.addHandler(log_fd)

        # Start updating logfile
        logger.info("\n%s" % (__func))
        print ("Python version: %s" % sys.version)
        logger.info("Python version: %s" % sys.version)

        print(msg) 
        logger.info(msg) 

        # Calculate when the log was last modified.  If the logfile is
        # more than 6 days old rename it.
        age_of_logfile = (today - log_modified_date).days
        log_move = 0
        if (age_of_logfile > 6):
            old_logfile = "%s.old" % (logfile)
            os.rename(logfile, old_logfile)
            log_move = 1

        if (log_move == 1):
            logger.info(
                "%s Logfile '%s' was last modified on '%s'"
                     % (__func, logfile, log_modified_date)
            )
            logger.info(
                "%s Renamed '%s' to '%s' as it was '%d' days old"
                     % (__func, logfile, old_logfile, age_of_logfile)
            )

        else:
            logger.info("%s Not renaming logfile '%s' as it was last modified on '%s' - only '%d' day(s) ago" % (__func, logfile, log_modified_date, age_of_logfile))
        print("%s Logging output to '%s'" % (__func, logfile))    
        logger.info("%s Logging output to '%s'" % (__func, logfile))    
        return 0

    @classmethod
    def logStart(cls):
        __func = "%s:logStart()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        logger.info("\n%s" % (__func))
        logfile = cls.getLogfile()
        print("\n\n")
        logger.info("\n\n")
        print(
            "%s\n%s Starting '%s' on '%s' for '%s' at '%s'"
                 % (cls.getSstr(), __func, cls.getScriptName(), platform.node(),
                     pwd.getpwuid(os.getuid())[0], cls.getTime())
        )
        logger.info(
            "%s\n%s Starting '%s' on '%s' for '%s' at '%s'"
                 % (cls.getSstr(), __func, cls.getScriptName(), platform.node(),
                     pwd.getpwuid(os.getuid())[0], cls.getTime())
        )
        print(cls.getSstr())
        logger.info(cls.getSstr())
        print("\n\n")
        logger.info("\n\n")
        return 0

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
        __func = "%s:getObject()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        if (animals.getObjectCount() > idx):
            return(animals.__zoo[idx])
        else:
            str="\n*** Index provided: <%d> is bigger that size of list: <%d> ***\n" % (idx, animals.getObjectCount())
            try:
                raise zooException(str)
            except zooException as err:
                frameinfo = getframeinfo(currentframe())
                print("%s %s lineno %s" % (__func, frameinfo.filename, frameinfo.lineno))
                logger.info("%s %s lineno %s" % (__func, frameinfo.filename, frameinfo.lineno))
                print("\nanimals::getObject(): Fatal error:", err.message)
                logger.info("\nanimals::getObject(): Fatal error:", err.message)
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
        __func = "%s:setFeedRval()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        cls.m_feed_rnum = m
        cls.g_feed_rnum = g
        cls.e_feed_rnum = e

        print("\nanimals::setFeedRval(): m_feed_rnum=<%d>" % (cls.m_feed_rnum))
        logger.info("\nanimals::setFeedRval(): m_feed_rnum=<%d>" % (cls.m_feed_rnum))
        print("animals::setFeedRval(): g_feed_rnum=<%d>" % (cls.g_feed_rnum))
        logger.info("animals::setFeedRval(): g_feed_rnum=<%d>" % (cls.g_feed_rnum))
        print("animals::setFeedRval(): e_feed_rnum=<%d>\n" % (cls.e_feed_rnum))
        logger.info("animals::setFeedRval(): e_feed_rnum=<%d>\n" % (cls.e_feed_rnum))
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
        __func = "%s:printBanner()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

        print("\n#############################################################")
        logger.info("\n#############################################################")
        print("########## %s ##########" %(str));
        logger.info("########## %s ##########" %(str));
        print("#############################################################")
        logger.info("#############################################################")
        return 0
        
    def printInstance(self):
        __func = "%s:printInstance()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        rval      = "  Animal type  specific feed random number (0 == not fed yet!)"
        fedNum    = "   ** number of times fed **"
        healthRed = "   ** number of times health reduced **"
        if (self.getFeedValue() < 0):
            feed_s ="    ** FeedVal is -1 as animal is yet to be fed! **" 

        print("\n---------- printInstance() ----------")
        logger.info("\n---------- printInstance() ----------")
        print("    Name      = %s" % self.getName())
        logger.info("    Name      = %s" % self.getName())
        print("    Idx       = %d" % self.getIdx())
        logger.info("    Idx       = %d" % self.getIdx())
        print("    Health    = %f  (Threshold=%d)" % (self.getHealth(), self.getThresholdConst()))
        logger.info("    Health    = %f  (Threshold=%d)" % (self.getHealth(), self.getThresholdConst()))
        print("    FeedVal   = %d  %s" % (self.getFeedValue(), rval))
        logger.info("    FeedVal   = %d  %s" % (self.getFeedValue(), rval))
        print("    FeedRuns  = %s  %s" % (self.getFeedRun(), fedNum))
        logger.info("    FeedRuns  = %s  %s" % (self.getFeedRun(), fedNum))
        print("    HealthRun = %s  %s" % (self.getHealthRunDown(), healthRed))
        logger.info("    HealthRun = %s  %s" % (self.getHealthRunDown(), healthRed))
        print("    Status    = %s" % self.getStatus())
        logger.info("    Status    = %s" % self.getStatus())
        return 0

    def printAllInstances(self):
        __func = "%s:printAllInstances()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        str = "printAllInstances() is dumping zoo list data"
        animals.printBanner(str);
        for obj in animals.getListData():
            obj.printInstance()
        
    def printHealthAttr(self):
        __func = "%s:printHealthAttr()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        feed_s =   "   ** number of times fed **"
        health_s = "   ** number of times health reduced **"
        print("---------- <%s> ----------" % (self.getName()))
        logger.info("---------- <%s> ----------" % (self.getName()))
        print("    Health     = %f" % self.getHealth())
        logger.info("    Health     = %f" % self.getHealth())
        print("    Status     = %s" % self.getStatus())
        logger.info("    Status     = %s" % self.getStatus())
        print("    Threshold  = %s" % self.getThresholdConst())
        logger.info("    Threshold  = %s" % self.getThresholdConst())
        print("    FeedRuns   = %s  %s" % (self.getFeedRun(), feed_s))
        logger.info("    FeedRuns   = %s  %s" % (self.getFeedRun(), feed_s))
        print("    HealthDown = %s  %s" % (self.getHealthRunDown(), health_s))
        logger.info("    HealthDown = %s  %s" % (self.getHealthRunDown(), health_s))
        return 0

    def changeStatus(self):
        __func = "%s:changeStatus()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        chg = False
        if (self.getStatus() == animals.DEAD):
            return 0

        elif (self.getStatus() == animals.LAME and
                            self.getHealth() < self.getThresholdConst()):
            print("adjustHealthDownAllAnimals(1): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.DEAD, self.getName()))
            logger.info("adjustHealthDownAllAnimals(1): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.DEAD, self.getName()))
            chg=True
            self.setStatus(animals.DEAD)

        elif (self.getStatus() == animals.LAME and
                 (self.getHealth() >= self.getThresholdConst())):
            print("adjustHealthDownAllAnimals(2): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.LIVE, self.getName()))
            logger.info("adjustHealthDownAllAnimals(2): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.LIVE, self.getName()))
            self.setStatus(animals.LIVE)
            chg=True

        elif ((self.getType() == animals.ELEPHANT) and
                 (self.getHealth() < self.getThresholdConst())):
            print("adjustHealthDownAllAnimals(3): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.LAME, self.getName()))
            logger.info("adjustHealthDownAllAnimals(3): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.LAME, self.getName()))
            self.setStatus(animals.LAME)

        elif (self.getHealth() < self.getThresholdConst()):
            print("adjustHealthDownAllAnimals(4): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.DEAD, self.getName()))
            logger.info("adjustHealthDownAllAnimals(4): Status now %-7s -> %-7s for <%-11s>" % (self.getStatus(), animals.DEAD, self.getName()))
            self.setStatus(animals.DEAD)

        else:
            print("adjustHealthDownAllAnimals(5): No change to status (%-7s) for <%-11s>" % (self.getStatus(), self.getName()))
            logger.info("adjustHealthDownAllAnimals(5): No change to status (%-7s) for <%-11s>" % (self.getStatus(), self.getName()))

        return 0

    # genFeedValue() needs to be called before each feed run as it
    # generates 3 random numbers that are class attributes.  This means they
    # are available to all instances of the class vie the get methods
    @classmethod
    def genFeedValue(cls):
        __func = "%s:genFeedValue()" % (cls.getScriptName())
        logger = cls.returnLoggerObject()

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
        __func = "%s:feedAnimal()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        if (self.getStatus() == animals.DEAD):
            if 'DEBUG' in os.environ: 
                print("animals::feedAnimal(): %s is dead!" % (self.getName()))
                logger.info("animals::feedAnimal(): %s is dead!" % (self.getName()))
            return 0

        if 'DEBUG' in os.environ: 
            print("animals::feedAnimal(): animal status = <%s>" % (self.getStatus()))
            logger.info("animals::feedAnimal(): animal status = <%s>" % (self.getStatus()))
        val = animals.getFeedCount()  # get the incremented count
        # Set the number of feed runs that the LIVE/LAME instance has had
        self.setFeedRun(val) # The instance now has the number of feed runs
        rnum = self.getFeedValue()
        chealth =  self.getHealth()  # current health
        nhealth = (self.getHealth() + (self.getHealth() * float(rnum/100)))

        # We don't want health to be more than 100% so use the lambda ternary
        # below to cap nhealth at 100% 
        nhealth = float(((lambda: nhealth, lambda: 100)[ nhealth > 100]()))
        self.setHealth(nhealth)          

        # The status may change for elephants as they may go LAME -> HEALTHY
        self.changeStatus();

        if 'DEBUG' in os.environ: 
            print("animals::feedAnimal(): %-11s oldHealth=<%-.2f> newHealth= <%-.2f>" % (self.getName(), chealth, nhealth)) 
            logger.info("animals::feedAnimal(): %-11s oldHealth=<%-.2f> newHealth= <%-.2f>" % (self.getName(), chealth, nhealth)) 
        return 0            


    def feedAllAnimals(self):
        __func = "%s:feedAllAnimals()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        print("\nanimals::feedAllAnimals(): Feeding all animals")
        logger.info("\nanimals::feedAllAnimals(): Feeding all animals")
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
        __func = "%s:adjustHealthDown()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        type = self.getType()
        if (self.getStatus() == animals.DEAD):
            if 'DEBUG' in os.environ: 
                print("animals::adjustHealthDown(): %s is dead!" % (self.getName()))
                logger.info("animals::adjustHealthDown(): %s is dead!" % (self.getName()))
            return 0

        v = self.getHealthRunCount()
        self.setHealthRunDown(v)
        health = self.getHealth() - (self.getHealth() * (value/100))
        self.setHealth(health)
        self.changeStatus()
        return 0

    def adjustHealthDownAllAnimals(self):
        __func = "%s:adjustHealthDownAllAnimals()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        print("\nanimals::adjustHealthDownAllAnimals(): Adjusting health down")
        logger.info("\nanimals::adjustHealthDownAllAnimals(): Adjusting health down")
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
        __func = "%s:runWrapper()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        ret = animals.handleInput()

        """
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
        """
        return ret

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
        __func = "%s:__init__()" % (self.getScriptName())
        logger = self.returnLoggerObject()

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
        logger.info("monkey::ctor   name = <%-11s>  idx=<%-2d>  health=<%f>" %
                             (self.getName(), self.getIdx(), self.getHealth()))
        
    def __del__(self):
        __func = "%s:__del__()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        print("monkey::dtor   name = <%-11s>  idx=<%-2d>  health=<%f>" %
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
        self.__health = float(health)
        return 0

    def getHealth(self):
        return float(self.__health)

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
        __func = "%s:__init__()" % (self.getScriptName())
        logger = self.returnLoggerObject()


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
        logger.info("giraffe::ctor  name = <%-11s>  idx=<%-2d>  health=<%f>" %
                             (self.getName(), self.getIdx(), self.getHealth()))

    def __del__(self):
        __func = "%s:__del__()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        print("giraffe::dtor  name = <%-11s>  idx=<%-2d>  health=<%f>" %
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
            self.__health = float(health)
        return 0

    def getHealth(self):
        return float(self.__health)

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
        __func = "%s:__init__()" % (self.getScriptName())
        logger = self.returnLoggerObject()

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
        logger.info("elephant::ctor name = <%-11s>  idx=<%-2d>  health=<%f>" %
                             (self.getName(), self.getIdx(), self.getHealth()))

    def __del__(self):
        __func = "%s:__del__()" % (self.getScriptName())
        logger = self.returnLoggerObject()

        print("elephant::dtor name = <%-11s>  idx=<%-2d>  health=<%f>" %
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
        self.__health = float(health)
        return 0

    def getHealth(self):
        return float(self.__health)

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
        __func = "%s:runner()" % (animals.getScriptName())
        logger = animals.returnLoggerObject()

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
        logger.info("========================================")



#####################################################
############### CALL MAIN FUNCTION ##################
#####################################################

animals.turnLoggingOn()
animals.logStart()
mainFunc = main()
animals.printBanner("Starting zoo simulation")
print("")
ret = mainFunc.runner()
print("==================================")
sys.exit(ret)

