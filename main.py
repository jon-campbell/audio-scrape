#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys, getopt

from src import download
from src import move
from src import bandcamp_links
from src import khinsider_links
from src import apache_links

class Args(object):
    def __init__(self, argv):
        self.urls = filter(lambda arg: arg[0] != "-", argv[1:])

        try:
            _, args = getopt.getopt(argv, "f:n:a:")
            self.no_folders = '-f' in args
            self.no_download = '-n' in args
            self.is_apache = '-a' in args
        except:
            self.no_folders = False
            self.no_download = False
            self.is_apache = False


def get_strategy(url, args):
    if args.is_apache:
        match = apache_links
    elif "khinsider" in url:
        match = khinsider_links
    else:
        match = bandcamp_links

    return match.AlbumDownloadStrategy(url)

def download_album_art(rel, name):
    try:
        download.download(rel, "%s.jpg" % name)
        print "Downloaded album art"
    except:
        pass

def main(argv):
    args = Args(argv)
    strategies = map(lambda url: get_strategy(url, args), args.urls)

    for strategy in strategies:
        album_name = strategy.album_name
        artist_name = strategy.artist

        if not args.no_download:
            if hasattr(strategy, "tracks"):
                download.download_tracks(strategy.tracks, "mp3")
            else:
                download.download_list(strategy.links, "mp3")

            if hasattr(strategy, "album_art"):
                download_album_art(strategy.album_art, 'cover')

        if not args.no_folders and album_name and artist_name:
            move.to_folder(album_name, artist_name)

if __name__ == '__main__':
    main(sys.argv)
