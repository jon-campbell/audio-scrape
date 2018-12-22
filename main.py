#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys, getopt

from src import download
from src import move
from src import bandcamp_links
from src import khinsider_links

class Args(object):
    def __init__(self, argv):
        self.urls = filter(lambda arg: arg[0] != "-", argv[1:])

        try:
            _, args = getopt.getopt(argv, "f:n:")
            self.no_folders = '-f' in args
            self.no_download = '-n' in args
        except:
            self.no_folders = False
            self.no_download = False


def get_provider(url):
    if "khinsider" in url:
        links_provider = khinsider_links
    else:
        links_provider = bandcamp_links

    return links_provider.DownloadInterface(url)

def download_album_art(rel, name):
    try:
        download.download(rel, "%s.jpg" % name)
        print "Downloaded album art"
    except:
        pass

def move_to_folders(album, artist):
    move.pattern_list(["*.mp3", "*.jpg"], album)
    print "Moved files to %s folder" % album

    move.item(album, artist)
    print "Moved album to %s folder" % artist

def main(argv):
    args = Args(argv)
    providers = map(get_provider, args.urls)

    for provider in providers:
        album_name = provider.album_name
        artist_name = provider.artist

        if not args.no_download:
            download.download_list(provider.links, "mp3")

            if hasattr(provider, "album_art"):
                download_album_art(provider.album_art, album_name)

        if not args.no_folders and album_name and artist_name:
            move_to_folders(album_name, artist_name)

if __name__ == '__main__':
    main(sys.argv)
