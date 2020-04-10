#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re

import urllib
import eyed3
from eyed3.id3 import Tag

def parse_filename(filename):
    """Replace invalid characters with hyphens for safe filename"""
    invalid_chars = r"[\\/:*?<>|]"
    filename = re.sub(invalid_chars, "-", filename)
    return filename

def insert_before_extension(filename, text):
    """Insert a string before the last dot in the filename"""
    parts = filename.split('.')
    parts[-2] += text
    return '.'.join(parts)

def download(url, filename):
    """Download binary from url to file"""
    filename = parse_filename(filename)
    with open(filename, "wb+") as output:
        output.write(urllib.urlopen(url).read())

def padded(number, zeros):
    """Left pad the number with given number of zeros, returned as a string"""
    output = '0' * zeros + str(number)
    return output

def download_list(urls, filetype):
    """Download a list of urls to numbered binary files"""
    for num, url in enumerate(urls):
        print("Downloading file %s . . . " % (num + 1), end='')
        filename = "%s.%s" % (padded(num + 1, 1)[-2:], filetype)
        download(url.rstrip(), filename)

        aufile = eyed3.load(filename)
        try:
            title = aufile.tag.title
        except:
            title = 'untitled'

        new_filename = insert_before_extension(filename, ' ' + title)
        os.rename(filename, parse_filename(new_filename))

        message = "%s complete!" % new_filename
        print(message.encode('utf-8'))

def download_tracks(tracks, filetype):
    for track in tracks:
        (num, title, url, album, artist) = (
                track["track"],
                unicode(track["title"]),
                track["url"],
                unicode(track["album"]),
                unicode(track["artist"]))
        print("%s: %s . . . " % (num, title), end='')

        filename = "%s %s.%s" % (padded(num, 1)[-2:], title[:40], filetype)
        download(url.rstrip(), filename)

        t = Tag(title=title, artist=artist, album=album, album_artist=artist, track_num=num)
        t.save(filename)

        print("-> %s" % filename)
