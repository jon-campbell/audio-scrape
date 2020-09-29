#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from HTMLParser import HTMLParser
import urllib
import re
import json

from album import Album

class AlbumDownloadStrategy(Album):

    def __init__(self, url):
        self.query = pq(url, encoding='utf8')
        self._url = url

    @property
    def links(self):
        return map(lambda x: x["url"], self.tracks)

    @property
    def tracks(self):
        def get_links_json():
            return json.loads(self.query('script[data-tralbum]:first').attr('data-tralbum'))['trackinfo']

        return [{
                    'url':x["file"].values()[0],
                    'title':x["title"].strip(),
                    'track':x["track_num"],
                    'album':self.album_name.strip(),
                    'artist':self.artist.strip(),
                    'art_url':self.album_art
                } for x in get_links_json()
                  if x["file"] is not None]

    @property
    def artist(self):
        return self.query('h3>span>a').text().replace(' You own this', '').encode('latin-1').decode('utf-8')

    @property
    def album_name(self):
        return self.query('.trackTitle:first').text().encode('latin-1').decode('utf-8')

    @property
    def album_art(self):
        return self.query('a.popupImage>img').attr('src')


if __name__ == "__main__":
    tags = AlbumDownloadStrategy('<script data-tralbum="{&quot;prop&quot;: &quot;val&quot;}" />')
    print json.dumps(tags.tracks, indent=2)
