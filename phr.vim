" Vim syntax file
" Language: Personal Health Records
" Maintainer: Paco Gomez
" Latest Revision: 2022 03 23

if exists("b:current_syntax")
  finish
endif

" Keywords
syn keyword phrDirective open close r record range

hi def link phrDirective ctermfg=cyan guifg=#00fff

