#!/bin/sh

######################################################################
# Author:      Lakshman Brodie - May 2021
# Date:        24th May 2021
# Description: Parse output of zoo simulation for testing purposes
######################################################################

awk ' 
                                           { LINE[NR] = $0     }
    /^Number of /                          { initial[a++] = NR }
    /^Printing vector contents\.\.\.\.$/   { end[b++] = NR     }
    END {


    # Array initial contains the line number of all matched patterns that
    # we are interested in
    for (a in initial) {
        start_pos=initial[a]
        #printf("start_pos=%d   end_pos=%d   a=%d\n", start_pos, end_pos, a)
        # The if statement below is a safety measure as we do not want to
        # go past  array boundary
        if (start_pos < NR) {
            n = split(LINE[start_pos], arrA)
            #printf("%d)=%s    (%d)\n", start_pos, LINE[start_pos], arrA[n])
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
        #printf("%s\n", LINE[i])
    }

}' ~/src/lab1301-git/src/C++/zooVisitorPattern/zooVisitor.out