#!/usr/bin/env sh
youtube-dl -ci -x -f best[ext!=webm] -o '%(playlist_index)s.%(title)s.%(ext)s' $1

