#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re

from album import Album

class AlbumDownloadStrategy(Album):

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
        main_page_lines = self.getSrcLines(self.url)
        track_pages = [self.url + "/" + x
                for x in self.setOfRegexMatches('[^/]+\.mp3(?=">)', main_page_lines)]

        track_mp3_links = []
        for track_page in track_pages:
            track_lines = self.getSrcLines(track_page)
            track_mp3_link = self.setOfRegexMatches('(?<=id\="audio1" src\=")[^"]+',
                    track_lines)
            track_mp3_links.append(list(track_mp3_link)[0])

        track_mp3_links.sort(key=lambda x: x.split('/')[-1])

        return track_mp3_links

    @property
    def artist(self):
        return ""

    @property
    def album_name(self):
        return ""


def main():
    url = "https://downloads.khinsider.com/game-soundtracks/album/flashback-the-quest-for-identity-snes-"
    dl = AlbumDownloadStrategy(url)
    print dl.links

if __name__ == '__main__':
    main()

