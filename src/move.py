#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob

def to_folder(album, artist):
    album = clean_name(album)
    artist = clean_name(artist)
    organise(["*.mp3", "*.jpg"], album, artist)

def clean_name(name):
    bad_path_characters = '<>:"/\\|?*'
    name = "".join([x if not x in bad_path_characters else '_' for x in name])
    return name.strip(".")

def organise(file_patterns, album, artist):
    for pattern in file_patterns:
        for item in glob.glob(pattern):
            dest = "%s/%s/%s" % (artist, album, item)
            try:
                os.renames(item, dest)
            except:
                print "Couldn't move %s to %s" % (item, dest)

