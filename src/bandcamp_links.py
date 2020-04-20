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
                    'track':x["track_num"],
                    'album':self.album_name,
                    'artist':self.artist,
                    'art_url':self.album_art
                } for x in get_links_json()
                  if x["file"] is not None]

    @property
    def artist(self):
        return self.query('h3>span>a').text().replace(' You own this', '')

    @property
    def album_name(self):
        return self.query('.trackTitle:first').text()

    @property
    def album_art(self):
        return self.query('a.popupImage>img').attr('src')


if __name__ == "__main__":
    tags = AlbumDownloadStrategy('https://exitoz.bandcamp.com/')
    print json.dumps(tags.tracks, indent=2)
