#!/usr/bin/env python2

import sys
import re

from kinglet.theory import (
    WORD_PARTS,
    Stroke,
    strokes_from_text,
    strokes_to_text,
)


# Main entry-point for testing. {{{

def test():
    if '/' == sys.argv[1]:
        cap_state = {
            'shift': False,
            'capslock': False,
        }
        text = u''
        # steno -> text.
        for steno in sys.argv[2:]:
            steno = steno.replace('[ ]', '_')
            for part in steno.split('/'):
                if not part:
                    continue
                if '[' == part[0]:
                    assert ']' == part[-1]
                    text += part[1:-2]
                else:
                    text += Stroke(part).to_text(cap_state)
        print text
    else:
        # text -> steno.
        supported_chars = set()
        for part in WORD_PARTS:
            supported_chars.update(part)
            supported_chars.update(part.upper())
        assert not set('/[]') & supported_chars
        supported_chars -= set('|') # | is the special character for [cap].
        supported_chars = ''.join(sorted(supported_chars))
        rx = re.compile('([^' + supported_chars.replace('-', '\\-') + ']+)')
        steno = ''
        for text in sys.argv[1:]:
            for part in re.split(rx, text):
                if steno:
                    steno += '/'
                if part[0] in supported_chars:
                    steno += '/'.join(str(s) for s in strokes_from_text(part))
                else:
                    steno += '[' + ']/['.join(part) + ']'
        steno = steno.replace('_', '[ ]')
        print steno

if __name__ == '__main__':
    test()

# }}}

# vim: foldmethod=marker
