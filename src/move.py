#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob

def pattern_list(lisp, destination):
    for pattern in lisp:
        for filename in glob.glob(pattern):
            item(filename, destination)

def item(filename, destination):
    try:
        os.renames(filename, "%s/%s" % (destination.encode('utf-8'), filename.encode('utf-8')))
    except:
        print "Couldn't move %s. Bad character or duplicate name." % filename
