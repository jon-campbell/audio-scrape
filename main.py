#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys, getopt

from src import download
from src import bandcamp_links
from src import khinsider_links
from src import apache_links

class Args(object):
    def __init__(self, argv):
        self.urls = filter(lambda arg: arg[0] != "-", argv[1:])

        try:
            _, args = getopt.getopt(argv, "n:a:")
            self.no_download = '-n' in args
            self.is_apache = '-a' in args
        except:
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

def main(argv):
    args = Args(argv)
    strategies = map(lambda url: get_strategy(url, args), args.urls)

    for strategy in strategies:
        album_name = strategy.album_name
        artist_name = strategy.artist

        if not args.no_download:
            if hasattr(strategy, "tracks"):
                download.download_tracks(strategy.tracks, "mp3")
                download_album_art(strategy.album_art, 'cover')
            else:
                download.download_list(strategy.links, "mp3")


if __name__ == '__main__':
    main(sys.argv)
