#!/usr/bin/env sh

tagFile=$1
vim $tagFile --noplugin -n -c 'call BCFormat()' -c 'q'
cat -nv $tagFile
