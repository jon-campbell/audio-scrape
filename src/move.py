#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob

def to_folder(album, artist):
    album = clean_name(album)
    artist = clean_name(artist)
    pattern_list(["*.mp3", "*.jpg"], album)
    item(album, artist)

def clean_name(name):
    bad_path_characters = '<>:"/\\|?*'
    name = "".join([x if not x in bad_path_characters else '_' for x in name])
    return name.strip(".")

def pattern_list(patterns, dest):
    for pattern in patterns:
        for file in glob.glob(pattern):
            item(file, dest)

def item(src, dest):
    try:
        os.renames(src, "%s/%s" % (dest.encode('utf-8'), src.encode('utf-8')))
    except:
        print "Couldn't move %s. Bad character or duplicate name." % src
