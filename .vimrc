fu! BCFormat()
    :execute 'norm ggVG"+p'
    :v/\d\d:\d\d/d
    :%norm $F d$
endf

