#!/bin/env python3

import os

def add2bashrc():
    if os.name != "nt":
        os.system("echo python3 `pwd`/main.py  >> `echo $HOME`/.bashrc")
        os.system("echo python3 `pwd`/onefile.py  >> `echo $HOME`/.bashrc")
    

