#!/usr/bin/env sh

tagFile=$1
xclip -o \
  | sed -E \
    -e 's/^ *//' \
    -e 's/ *$//' \
    -e 's/ +[0-9]?[0-9]:[0-9][0-9]$//' \
    -e 's/^[0-9]+\.? //' \
  > $tagFile
cat -nv $tagFile
