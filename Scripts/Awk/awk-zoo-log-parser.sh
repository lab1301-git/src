#!/usr/bin/sh
######################################################################
# Author:      Lakshman Brodie
# Date:        5th October 2021
# Description: The awk programming language is very good for parsing text
#              and this program parses the output of the zoo simulation programs
#              for testing and reporting purposes.  This script could be called
#              from Jenkinsfile as part of the testing stage.  I expect I will be writing
#              a Python version of this program as well.
#
#              The purpose of this script is to report on the final status of each
#              animal.  The output files all differ so we can't have a generic parser.
#              The solution is to have functions for each logfile.  The header
#              of the functions tells you more.
#              This script recognises the following file formats:
#                  C++/zooPolymorphism/zoo.out
#                  C++/zooVisitorPattern/zooVisitor.out
#                  Eclipse/Java/zooSimulation/target/classes/zoo/zoo.out
#                  Scripts/Python/zoo/zoo.out
#####################################################################

SCRIPT=$(basename ${0})

if [ -z "${BASE_DIR}" ]
then
    BASE_DIR=${HOME}/src/lab1301-git/src
    echo "${SCRIPT}: BASE_DIR not set.  Setting BASE_DIR to '${BASE_DIR}'... "
else
    echo "${SCRIPT}: Env var BASE_DIR is set to '${BASE_DIR}'"
fi

if [ ! -z "${1}" ]
then
    INPUT=${1}
    echo "${SCRIPT}: We have been passed an arg ('${INPUT}')"
else
    INPUT=${BASE_DIR}/C++/zooVisitorPattern/zooVisitor.out
    echo "${SCRIPT}: *** WARNING **** No input file arg passed!"
    echo "${SCRIPT}: Setting input file to default of '${INPUT}'"
fi

if [ ! -r "${INPUT}" ]
then 
    echo "${SCRIPT}: **** FATAL - The specified input file '${INPUT}' is not accessible ****"
    exit 1
fi

awk '

    ############################################################
    # Function:    zoo_C_PlusPlus_logs()
    # Description: Process the output file, zooVisitor.out,
    #              generated by zooVisitor.cpp
    # Arguments:   None              
    # Returns:     0 - Success
    #              1 - Failure 
    ############################################################
    function zoo_C_PlusPlus_logs() {
        for (a in initial_val_c_plus_plus) {
            start_pos=initial_val_c_plus_plus[a]
            # The if statement below is a safety measure as we do not want to
            # go past  array boundary
            if (start_pos < NR) {
                n = split(LINE[start_pos], arrA)
                printf("We are starting with '%d' healthy '%s'\n", arrA[n], arrA[3])
             
            } else {
                printf("\n*** Warning! %d > %d ***\n", start_pos, NR)
                return(1) 
            }
        }

        # We are only interested in the Status of the animals at the
        # very end and that information is available in this loop
        count=0
        for (i=end_zoo_c_plus_plus[b - 1]; i<NR; i++) {
            if ( LINE[i] ~ /-----------/) {
                if (count > 0) {
                    printf(  \
                        "Animal id: %-2d %-8s has been fed %d times and has an health of <%-2.2f> and is <%s>\n",\
                        arrQ[q], arrP[p], arrS[s], arrR[r], arrT[t]\
                    )
                }
                continue
            } 
            if (LINE[i] ~ / Animal: /) {
                p = split(LINE[i], arrP) 
                count++
            } 
    
            if (LINE[i] ~ / id: /) {
                q = split(LINE[i], arrQ) 
                count++
            } 
    
            if (LINE[i] ~ / Health: /) {
                r = split(LINE[i], arrR) 
                count++
            } 
    
            if (LINE[i] ~ /Feed: /) {
                s = split(LINE[i], arrS) 
                count++
            } 
    
            if (LINE[i] ~ / Status: /) {
                t = split(LINE[i], arrT) 
                count++
            } 
    
            if (LINE[i] ~ / rnumFeed: /) {
                u = split(LINE[i], arrU) 
                count++
            } 
        }
        return(0)
    }

    ############################################################
    # Function:    zoo_java_log()
    # Description: Process the output file, zoo.out,
    #              generated by zoo.class
    # Arguments:   None              
    # Returns:     0 - Success
    #              1 - Failure 
    ############################################################
    function zoo_java_log() {

        for (a in a_count_java_zoo) {
            start_pos=a_count_java_zoo[c - 1]
            # The if below 
            if (start_pos > NR) {
                printf("\n'${SCXRIPT}':zoo_java_log(): start_pos > NR (%d > %d)\n", start_pos, NR)
                return(1) 
            }
            n = split(LINE[start_pos], arrA, "<")
            str=arrA[n]
            p = split(arrA[n], arrB, ">")  
        }
        printf("We are starting with '%s' healthy animals\n\n", arrB[p - 1])

        # We are only interested in the Status of the animals at the
        # very end and that information is available in this loop
        count=0
        for (i=end_zoo_java_log[d - 1] + 1; i<NR; i++) {
            if (LINE[i] ~ /^ Name: /) {
                p = split(LINE[i], arrP) 
                name=substr(arrP[p], 2, length(arrP[p]) - 2)
                count++
            } 

            if (LINE[i] ~ /^ Status: /) {
                q = split(LINE[i], arrQ) 
                status=substr(arrQ[q], 2, length(arrQ[q]) - 2)
                count++
            }

            if (LINE[i] ~ /^ Current Health: /) {
                r = split(LINE[i], arrR) 
                currentHealth=substr(arrR[r], 2, length(arrR[r]) - 2)
                count++
            } 

            if (LINE[i] ~ /^ Feed Runs: /) {
                s = split(LINE[i], arrS) 
                feedRun=substr(arrS[s], 2, length(arrS[s]) - 2)
                count++
            } 

            if (LINE[i] ~ /^ Feed Value: /) {
                t = split(LINE[i], arrT) 
                feedValue=substr(arrT[t], 2, length(arrT[t]) - 2)
                count++
            } 
             
            if ( LINE[i] ~ /--------------/) {
                if (count > 0) {
                    printf(  \
                        "Animal id: %-11s has been fed %d times and has an health of <%-2.2f> and is <%s>\n"   \
                         , name, feedRun, currentHealth, status  \
                    )
                }
                continue
            } 
        }
        return(0)
    }

    ############################################################
    # Function:    zoo_python_log()
    # Description: Process the output file, zoo.out,
    #              generated by zoo.py
    # Arguments:   None              
    # Returns:     0 - Success
    #              1 - Failure 
    ############################################################
    function zoo_python_log() {

            start_pos=a_count_python_zoo[e -1]
            # The if statement below is a safety measure as we do not want to
            # go past  array boundary.  The chances of it happening are probably nil though
            if (start_pos < NR) {
                n = split(LINE[start_pos], arrA)
                animalNum=substr(arrA[5], 6, 2)
                printf("We are starting with '%d' healthy animals\n", animalNum)
            } else {
                printf("\n*** Warning! %d > %d ***\n", start_pos, NR)
                return(1) 
            }

        # We are only interested in the Status of the animals at the
        # very end and that information is available in this loop
        count=0
        # The array end_zoo_python_log[f - 1] has the line number where printInstance() is called for the last time 
        # That is why we start the loop from that line number  
        for (i=end_zoo_python_log[f - 1] + 4; i<NR; i++) {
            if (LINE[i] ~ /--------/ || LINE[i] ~ /^========================================$/) { 
                if (count > 0) {
                    printf("Animal id: %-2d %-11s has been fed %d times and has an health of <%-2.2f> and is <%s>\n", arrQ[q], arrP[p], arrS[3], arrR[r - 1], arrT[t])
                }
                continue
            } 

            if (LINE[i] ~ / Name /) {
                p = split(LINE[i], arrP) 
                count++
            } 
    
            if (LINE[i] ~ / Idx /) {
                q = split(LINE[i], arrQ) 
                count++
            } 
    
            if (LINE[i] ~ / Health /) {
                r = split(LINE[i], arrR) 
                count++
            } 
    
            if (LINE[i] ~ /FeedRuns/) {
                s = split(LINE[i], arrS) 
                count++
            } 
    
            if (LINE[i] ~ / Status /) {
                t = split(LINE[i], arrT) 
                count++
            } 
        }
        return(0)
    }


                                           { LINE[NR] = $0                 }
    ###########################
    # Pattern matching for C++/zooVisitorPattern/zooVisitor.out
    #                      and C++/zooPolymorphism/zoo.cpp
    ###########################
    /^Number of /                          { initial_val_c_plus_plus[a++] = NR }
    /^Printing vector contents\.\.\.\.$/   { end_zoo_c_plus_plus[b++] = NR     }
    / rnumFeed: /                          { c_plus_plus[z++] = NR             }

    ###########################
    # Pattern matching for Eclipse/Java/zooSimulation/target/classes/zoo/zoo.out
    ###########################
    /::animalFactory\(\): Returning new obj/ { a_count_java_zoo[c++] = NR    }
    / Printing attributes of all instance/   { end_zoo_java_log[d++] = NR    }

    ###########################
    # Pattern matching for Scripts/Python/zoo/zoo.out
    ###########################
    /::ctor name = </                      { a_count_python_zoo[e++] = NR    }
    /printAllInstances\(\) is dumping zoo /  { end_zoo_python_log[f++] = NR    }

    END {

    # Array initial_val_c_plus_plus contains the line number of all matched patterns that
    # we are interested in

    if (ARGC != 2) {
        printf("USAGE:\n%s <zoo simulation logfile>\n", ARGV[0])
        exit
    }

    printf("Processing logfile: %s...\n", FILENAME)
    #printf("%s\n", ARGV[1])

    if (b > 0) {
        if (z > 0) {
            printf("\n********************************************")
            printf("\n**** Detected that the input file is from zooPolymorphism.cpp ****\n")
            printf("********************************************\n\n")
        } else {
            printf("\n********************************************")
            printf("\n**** Detected that the input file is from zooVisitor.cpp ****\n\n")
            printf("********************************************\n\n")
        } 
        ret = zoo_C_PlusPlus_logs()

    } else if (c > 0) {
        printf("\n********************************************")
        printf("\n**** Detected that the input file is from zoo.java ****\n")
        printf("********************************************\n\n")
        if (ret = zoo_java_log() != 0) {
            ret=1;
        }


    } else if (e > 0) {
        printf("\n********************************************")
        printf("\n**** Detected that the input file is from zoo.py ****\n")
        printf("********************************************\n\n")
        if (ret = zoo_python_log() != 0) {
            ret=1;
        }

    } else {
        printf("\n*** FATAL *** Unsupported file type passed as an argument\n")
        ret=1  
    }

    printf("\n********************************************")
    printf("\nFinished processing logfile: %s\n", FILENAME)
    printf("********************************************\n")
    exit(ret)
}' ${INPUT}
