######################################################################
# Author:      Lakshman Brodie - May 2021
# Date:        30th July 2021
# Description: Dockerfile to pull and build C++ code
#
######################################################################

FROM ubuntu:latest
FROM python:latest

LABEL maintainer="lab1301@gmail.com"

RUN apt-get update && \
    apt-get install -y sudo curl git-core gnupg  build-essential && \
    apt-get install -y vim


RUN groupadd --gid 6001 devusr \
    && useradd --home-dir /home/devusr --create-home --uid 6001 \
        --gid 6001 --shell /bin/bash --skel /dev/null devusr


LABEL version="1.0"
LABEL description="Binaries and scripts of github repo: lab1301-git"

RUN apt-get update
RUN apt clean


WORKDIR /usr/apps
RUN mkdir logs bin
#COPY *.py zoo zooVisitor polymorphism   .   #  DELME

RUN git clone https://github.com/lab1301-git/src



RUN chown -R devusr logs bin src
RUN chgrp -R devusr logs bin src
RUN chmod -R 755 logs bin src

USER devusr

RUN cd src/C++/zooVisitorPattern && make zooVisitor && ./zooVisitor > zooVisitor.out 2>&1 && \
    cd ../zooPolymorphism && make zoo &&  ./zoo > zoo.out 2>&1    && \
    cd ../polymorphism && make polymorphism &&  ./polymorphism > polymorphism.out 2>&1

