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
        return map(lambda x: x["url"], self.tracks)

    @property
    def tracks(self):
        def get_links_json():
            return [json.loads(re.search(r"\[.*,$", line).group(0)[:-1])
                    for line in urllib.urlopen(self._url).readlines()
                    if re.match(r"^\s*trackinfo: ", line)][0]

        return [{
                    'url':x["file"].values()[0],
                    'title':x["title"],
                    'track':x["track_num"]
                } for x in get_links_json()
                  if x["file"] is not None]

    @property
    def artist(self):
        return self.query('h3>span>a').text()

    @property
    def album_name(self):
        return self.query('.trackTitle:first').text()

    @property
    def album_art(self):
        return self.query('a.popupImage>img').attr('src')


if __name__ == "__main__":
    tags = AlbumDownloadStrategy('https://dorianelectra.bandcamp.com/album/flamboyant-deluxe')
    print tags.artist
    print tags.album_name
    print tags.album_art
    print reduce(lambda a, x: "%s\n%s" % (a, x), map(lambda x: "%s: %s" % (x["title"], x["url"]), tags.links))
