######################################################################
# Author:      Lakshman Brodie - May 2021
# Date:        30th July 2021
# Description: Dockerfile to pull and build C++/Java code
#
######################################################################

FROM ubuntu:latest

LABEL maintainer="lab1301@gmail.com"
LABEL version="1.0"
LABEL description="Binaries and scripts of github repo: lab1301-git"
WORKDIR /usr/apps

RUN apt-get update  -y && \
    apt-get install -y sudo curl git-core gnupg build-essential && \
    apt-get install -y python3 && \
    apt-get install -y vim && \
    DEBIAN_FRONTEND='noninteractive' apt-get install -y maven && \
    apt-get update  -y && \
    groupadd --gid 6001 devusr && \
    useradd --home-dir /home/devusr --create-home --uid 6001 --gid 6001 --shell /bin/bash --skel /dev/null devusr && \
    apt clean && \
    mkdir logs bin && \
    git clone https://github.com/lab1301-git/src && \
    chown -R devusr logs bin src && \
    chgrp -R devusr logs bin src && \ 
    chmod -R 755 logs bin src

USER devusr

RUN cp /home/devusr/src/Scripts/Docker/.profile /home/devusr/.profile && \
    cd src/C++/zooVisitorPattern && \
        make zooVisitor 2>&1 | tee zooVisitor.out &&  \
           ./zooVisitor 2>&1 | tee -a zooVisitor.out && \
    cd ../zooPolymorphism && \
        make zoo 2>&1 | tee zoo.out &&  \
           ./zoo 2>&1 | tee -a zoo.out && \
    cd ../polymorphism && \
        make polymorphism 2>&1 | tee polymorphism.out &&  \
        ./polymorphism  2>&1 | tee -a polymorphism.out && \
    cd ../../Scripts/Python/polymorphism && \
        python3 polymorphism.py 2>&1 | tee polymorphism.py.out 2>&1 && \
    cd ../zoo && \
        python3 zoo.py 2>&1 | tee zoo.py.out 2>&1 && \
    cd ../../../Eclipse/Java/zooSimulation && \
        mvn clean package 2>&1 | tee bld-log && \
        mvn compile 2>&1 | tee -a bld-log && \
        mvn package 2>&1 | tee -a bld-log && \
    cd ../../../Eclipse/Java/polymorphism && \
        mvn clean package 2>&1 | tee bld-log && \
        mvn compile 2>&1 | tee -a bld-log && \
        mvn package 2>&1 | tee -a bld-log
