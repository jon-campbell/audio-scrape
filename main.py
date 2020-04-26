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
        self.urls = [arg for arg in argv[1:] if arg[0] != "-"]
        try:
            _, args = getopt.getopt(argv, "n:a:")
            self.no_download = '-n' in args
            self.is_apache = '-a' in args
        except:
            self.no_download = False
            self.is_apache = False

def main(args):
    def get_strategy(url):
        if args.is_apache:
            match = apache_links
        elif "khinsider" in url:
            match = khinsider_links
        else:
            match = bandcamp_links
        return match.AlbumDownloadStrategy(url)

    def execute(strategy):
        album_name = strategy.album_name
        artist_name = strategy.artist
        if not args.no_download:
            if hasattr(strategy, "tracks"):
                download.download_tracks(strategy.tracks, "mp3")
            else:
                download.download_list(strategy.links, "mp3")

    [execute(get_strategy(url)) for url in args.urls]

if __name__ == '__main__':
    main(Args(sys.argv))
