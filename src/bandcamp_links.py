#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import urllib
import re
import json

from album import Album

class AlbumDownloadStrategy(Album):

    def __init__(self, url):
        self.query = pq(urllib.urlopen(url).read())
        self._url = url

    @property
    def links(self):
        def get_links_json():
            return [json.loads(re.search(r"\[.*,$", line).group(0)[:-1])
                    for line in urllib.urlopen(self._url).readlines()
                    if re.match(r"^\s*trackinfo: ", line)][0]

        return [y for x in get_links_json()
                  if x["file"] is not None
                  for y in x["file"].values()]

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
