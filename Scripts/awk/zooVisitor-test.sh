#!/usr/bin/sh
######################################################################
# Author:      Lakshman Brodie
# Date:        5th October 2021
# Description: Parse output of zoo simulation for testing purposes.
#              This script reports on the final status of each animal.
######################################################################

SCRIPT=$(basename ${0})
BASE=${HOME}/src/lab1301-git/src
INPUT=${BASE}/C++/zooVisitorPattern/zooVisitor.out

if [ ! -z "${1}" ]  && [ -r "${1}" ]
then
    echo "We have been passed an arg ('${1}')"
    echo "${SCRIPT}: Using file '${INPUT}'... "
    INPUT=${1}
else
    if [ ! -r "{$1}" ]
    then 
        echo "${SCRIPT}: **** FATAL - The specified input file '${1}' is not accessible ****"
        exit 1
    fi
fi

echo "${SCRIPT}: Using input file '${INPUT}'... "

awk ' 
                                           { LINE[NR] = $0     }
    /^Number of /                          { initial[a++] = NR }
    /^Printing vector contents\.\.\.\.$/   { end[b++] = NR     }

    END {

    # Array initial contains the line number of all matched patterns that
    # we are interested in

    if (ARGC != 2) {
        printf("USAGE:\n%s <zoo simulation logfile>\n", ARGV[0])
        exit
    }

    printf("Processing logfile: %s...\n", FILENAME)
    printf("%s\n", ARGV[1])
    for (a in initial) {
        start_pos=initial[a]
        # The if statement below is a safety measure as we do not want to
        # go past  array boundary
        if (start_pos < NR) {
            n = split(LINE[start_pos], arrA)
            printf("We are starting with '%d' healthy '%s'\n", arrA[n], arrA[3])
             
        } else {
            printf("\n*** Warning! %d > %d ***\n", start_pos, NR)
        }
    }

    printf("\n")
    # We are only interested in the Status of the animals at the
    # very end and that information is available in this loop
    count=0
    for (i=end[b - 1]; i<NR; i++) {
        if ( LINE[i] ~ /-----------/ || LINE[i] ~ /virtual /) {
            if (count > 0) {
                printf("Animal id: %-2d %-8s has been fed %d times and has an health of <%-2.2f> and is <%s>\n", arrQ[q], arrP[p], arrS[s], arrR[r], arrT[t])
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

        if (LINE[i] ~ / Feed: /) {
            s = split(LINE[i], arrS) 
            count++
        } 

        if (LINE[i] ~ / Status: /) {
            t = split(LINE[i], arrT) 
            count++
        } 
    }
}' ${INPUT}
