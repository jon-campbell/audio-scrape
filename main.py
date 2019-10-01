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


def get_provider(url, args):
    if args.is_apache:
        links_provider = apache_links
    elif "khinsider" in url:
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
    def clean_name(name):
        bad_path_characters = '<>:"/\\|?*'

        return "".join([x if not x in bad_path_characters else '_' for x in name])

    clean_album = clean_name(album)
    clean_artist = clean_name(artist)

    move.pattern_list(["*.mp3", "*.jpg"], clean_album)
    print "Moved files to %s folder" % clean_album

    move.item(clean_album, clean_artist)
    print "Moved album to %s folder" % clean_artist

def main(argv):
    args = Args(argv)
    providers = map(lambda url: get_provider(url, args), args.urls)

    for provider in providers:
        album_name = provider.album_name
        artist_name = provider.artist

        if not args.no_download:
            download.download_list(provider.links, "mp3")

            if hasattr(provider, "album_art"):
                download_album_art(provider.album_art, 'cover')

        if not args.no_folders and album_name and artist_name:
            move_to_folders(album_name, artist_name)

if __name__ == '__main__':
    main(sys.argv)
