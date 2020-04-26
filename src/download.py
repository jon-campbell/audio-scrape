#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re

import urllib
import eyed3
from eyed3.id3 import Tag

def download(url, filename):
    """Download binary from url to file"""
    with open(filename, "wb+") as output:
        output.write(urllib.urlopen(url).read())

def padded(number, zeros):
    """Left pad the number with given number of zeros, returned as a string"""
    output = '0' * zeros + str(number)
    return output

def download_list(urls, filetype):
    def parse_filename(filename):
        invalid_chars = r"[\\/:*?<>|]"
        filename = re.sub(invalid_chars, "-", filename)
        return filename

    def insert_before_extension(filename, text):
        """Insert a string before the last dot in the filename"""
        parts = filename.split('.')
        parts[-2] += text
        return '.'.join(parts)

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
    def to_valid_filename(name):
        bad_path_characters = '<>:"/\\|?*'
        name = "".join([x if not x in bad_path_characters else '_' for x in name])
        return name.strip(".")

    is_first_track = True
    for track in tracks:
        (num, title, url, album, artist) = (
                track["track"],
                unicode(track["title"]),
                track["url"],
                unicode(track["album"]),
                unicode(track["artist"]))
        print("%s: %s . . . " % (num, title), end='')

        path = os.path.join(to_valid_filename(artist), to_valid_filename(album))
        if is_first_track:
            try:
                os.makedirs(path)
            except OSError:
                pass
            art_url = track["art_url"]
            art_path = os.path.join(path, "cover.jpg")
            download(art_url, art_path)
            is_first_track = False

        filename = "%s %s.%s" % (padded(num, 1)[-2:], to_valid_filename(title[:40]), filetype)
        filepath = os.path.join(path, filename)
        download(url.rstrip(), filepath)

        t = Tag(title=title, artist=artist, album=album, album_artist=artist, track_num=num)
        t.save(filepath)

        print("-> %s" % filepath)

