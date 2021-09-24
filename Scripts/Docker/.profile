#!/bin/sh
######################################################################
# Author:      Lakshman Brodie - May 2021
# Date:        24 September 2021
# Description: .profile for Docker Images
#
######################################################################

date
uname -a
set -o vi
WORKDIR /usr/apps


export PATH=.:${PATH}

