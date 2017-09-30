#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob

def pattern_list(lisp, destination):
    for pattern in lisp:
        for filename in glob.glob(pattern):
            item(filename, destination)

def item(filename, destination):
    os.renames(filename, "%s/%s" % (destination, filename))
