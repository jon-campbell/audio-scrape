#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re

from album import Album

class DownloadInterface(Album):

    def __init__(self, url):
        self.url = url

    def getSrcLines(self, url):
        return urllib.urlopen(url).readlines()

    def setOfRegexMatches(self, regex, search_list):
        out = set()
        for line in search_list:
            match = re.search(regex, line)
            if match:
                out.add(match.group(0))

        return out

    @property
    def links(self):
        source = self.getSrcLines(self.url)
        links = self.setOfRegexMatches('(?<=href=").*\.mp3(?=")', source)

        return map(lambda x: self.url + x, links)

    @property
    def artist(self):
        return ""

    @property
    def album_name(self):
        return ""


def main():
    url = "http://neilcic.com/mouthmisc/"
    dl = DownloadInterface(url)
    print dl.links

if __name__ == '__main__':
    main()

