######################################################################
# Author:      Lakshman Brodie - May 2021
# Date:        30th July 2021
# Description: Dockerfile to pull and build C++/Java code
#
######################################################################

FROM ubuntu:latest

LABEL maintainer="lab1301@gmail.com"

RUN apt-get update  -y && \
    apt-get install -y sudo curl git-core gnupg build-essential && \
    apt-get install -y python3 && \
    apt-get install -y maven && \
    apt-get install -y vim

RUN groupadd --gid 6001 devusr \
    && useradd --home-dir /home/devusr --create-home --uid 6001 \
        --gid 6001 --shell /bin/bash --skel /dev/null devusr


LABEL version="1.0"
LABEL description="Binaries and scripts of github repo: lab1301-git"


WORKDIR /usr/apps
RUN apt clean && \
        mkdir logs bin && \
        git clone https://github.com/lab1301-git/src && \
        chown -R devusr logs bin src && \
        chgrp -R devusr logs bin src && \ 
        chmod -R 755 logs bin src

USER devusr

RUN cd src/C++/zooVisitorPattern && \
        make zooVisitor && \
        ./zooVisitor > zooVisitor.out 2>&1 && \
    cd ../zooPolymorphism && \
        make zoo &&  \
        ./zoo > zoo.out 2>&1    && \
    cd ../polymorphism && \
        make polymorphism &&  \
        ./polymorphism > polymorphism.out 2>&1
    cd ../../Scripts//Python/polymorphism && \
        polymorphism.py > polymorphism.out 2>&1 && \
    cd ../zoo && \
        zoo.py > zoo.out 2>&1

RUN cd src/Eclipse/Java/zooSimulation && \
        mvn clean package 2>&1 | tee bld-log && \
        mvn compile 2>&1 | tee -a bld-log && \
        mvn package 2>&1 | tee -a bld-log && \
    cd src/Eclipse/Java/polymorphism && \
        mvn clean package 2>&1 | tee bld-log && \
        mvn compile 2>&1 | tee -a bld-log && \
        mvn package 2>&1 | tee -a bld-log

