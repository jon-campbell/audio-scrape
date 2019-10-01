nmap bc :call BCFormat()<CR>

:fu! BCFormat()
:    exec 'norm ggVG'
:    exec 'norm "+p'
:    v/:/d
:    %norm $F d$
:    w
:endf
