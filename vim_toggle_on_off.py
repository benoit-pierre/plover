# -*- coding: utf-8 -*-
#!/usr/bin/env python

import vim

on_char = u'■'
off_char = u'□'

def toggle_on_off():
    fenc = vim.eval('&fenc')
    column = int(vim.eval('getpos(".")')[2]) - 1
    before_cursor = unicode(vim.current.line[:column], fenc)
    from_cursor = unicode(vim.current.line[column:], fenc)
    if not from_cursor:
        return
    if on_char == from_cursor[0]:
        from_cursor = off_char + from_cursor[1:]
    elif off_char == from_cursor[0]:
        from_cursor = on_char + from_cursor[1:]
    else:
        return
    line = (before_cursor + from_cursor).encode(fenc)
    vim.current.line = line

