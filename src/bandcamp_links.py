#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import urllib
import re
import json

from album import Album

class AlbumDownloadStrategy(Album):

    def __init__(self, url):
        def get_links():
            tracklist = None
            for line in urllib.urlopen(url).readlines():
                if re.match(r"^\s*trackinfo: ", line):
                    tracklist = json.loads(re.search(r"\[.*,$", line).group(0)[:-1])
                    break

            links = []
            for track in tracklist:
                if not track["file"] is None:
                    links.extend(track["file"].values())

            return links

        self.query = pq(urllib.urlopen(url).read())
        self._links = get_links()

    @property
    def links(self):
        return self._links

    @property
    def artist(self):
        return self.query('h3>span>a').text()

    @property
    def album_name(self):
        return self.query('.trackTitle:first').text()

    @property
    def album_art(self):
        return self.query('a.popupImage>img').attr('src')

    @property
    def titles(self):
        return map(lambda x: x.text_content(), self.query('.track-title'))

if __name__ == "__main__":
    tags = AlbumDownloadStrategy('http://heavypsychsoundsrecords.bandcamp.com/album/acid-mammoth-under-acid-hoof/')
    print tags.artist
    print tags.album_name
    print tags.album_art
    print tags.titles
    print tags.links
