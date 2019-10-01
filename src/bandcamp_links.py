#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re
import json

from album import Album

class DownloadInterface(Album):

    def __init__(self, url):
        self.url = url

    @property
    def links(self):
        tracklist = None
        for line in urllib.urlopen(self.url).readlines():
            if re.match(r"^\s*trackinfo: ", line):
                tracklist = json.loads(re.search(r"\[.*,$", line).group(0)[:-1])
                break

        links = []
        for track in tracklist:
            if not track["file"] is None:
                links.extend(track["file"].values())

        return links

    @property
    def artist(self):
        name = None
        for line in urllib.urlopen(self.url).readlines():
                name = re.search(r'".*,$', line).group(0)[1:-2]
            if re.match(r"^\s*artist: ", line):
                break

        return name

    @property
    def album_name(self):
        name = None
        for line in urllib.urlopen(self.url).readlines():
            if re.match(r"^\s*album_title: ", line):
                name = re.search(r'".*,$', line).group(0)[1:-2]
                break

        return name

    @property
    def album_art(self):
        for line in urllib.urlopen(self.url).readlines():
            if '"image_src"' in line:
                return re.search(r'(?<=href=")[^"]*', line).group(0)

        return None

