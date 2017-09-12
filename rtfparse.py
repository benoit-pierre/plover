#!/usr/bin/env python3

import io
import re
import sys

from plover import system
from plover.config import DEFAULT_SYSTEM_NAME
from plover.dictionary.base import create_dictionary
from plover.registry import registry
from plover.steno import normalize_steno


RTF_TOKEN_PARTS = (
    ('cchar' , r'\\([-_~\\{}*])'                        , (0,)  ),
    ('cword' , r'\\([A-Za-z]+-?[0-9]*) ?'               , (0,)  ),
    ('gstart', r'({)(?:(\\\*)?\\([A-Za-z]+-?[0-9]*) ?)?', (1, 2)),
    ('gend'  , r'(})'                                   , (0,)  ),
    ('text'  , r'([^\n\r\\{}]+)'                        , (0,)  ),
)
RTF_TOKEN_MATCH_RESULTS_FOR_LASTINDEX = [None]
for name, pattern, wanted in RTF_TOKEN_PARTS:
    num_groups = len(RTF_TOKEN_MATCH_RESULTS_FOR_LASTINDEX)
    groups = [n + num_groups
              for n in range(re.compile(pattern).groups)]
    wanted = tuple(w + num_groups for w in wanted)
    for n in range(len(groups)):
        RTF_TOKEN_MATCH_RESULTS_FOR_LASTINDEX.append((name, wanted))
RTF_TOKEN = re.compile('|'.join(p for n, p, w in RTF_TOKEN_PARTS))

def rtf_tokenize(input):
    for lnum, line in enumerate(input):
        cnum = 0
        for m in RTF_TOKEN.finditer(line):
            start, end = m.span()
            assert start == cnum
            name, wanted = RTF_TOKEN_MATCH_RESULTS_FOR_LASTINDEX[m.lastindex]
            yield name, m.group(*wanted)
            cnum = end
    yield None, None


class Parser(object):

    def __init__(self):
        pass

    def parse(self, input, normalize=normalize_steno):
        tokenizer = rtf_tokenize(input)
        kind, value = next(tokenizer)
        assert (kind, value) == ('gstart', (None, 'rtf1')), (kind, value)
        kind, value = next(tokenizer)
        group_stack = [('', None, False)]
        g_text, g_destination, g_ignoring = '', 'rtf1', False
        next_token = None
        steno = None
        while True:
            if next_token is not None:
                kind, value = next_token
                next_token = None
            else:
                kind, value = next(tokenizer)
            if kind is None:
                if steno is not None:
                    yield normalize(steno), g_text
                break
            # Group start.
            if kind == 'gstart':
                if g_ignoring:
                    ignoring = True
                    destination = None
                else:
                    destination = value[1]
                    if destination == 'cxs':
                        ignoring = False
                        assert len(group_stack) == 1, len(group_stack)
                        if steno is not None:
                            yield normalize(steno), g_text
                            steno = None
                        g_text = ''
                    else:
                        ignoring = bool(value[0])
                group_stack.append((g_text, g_destination, g_ignoring))
                g_text, g_destination, g_ignoring = '', destination, ignoring
                continue
            # Group end.
            if kind == 'gend':
                if g_ignoring:
                    text = ''
                else:
                    if g_destination == 'cxs':
                        steno = g_text
                        text = ''
                    elif g_destination == 'cxsvatdictflags':
                        if 'N' in g_text:
                            text = '{-|}'
                        else:
                            text = ''
                    elif g_destination == 'cxp':
                        text = g_text.strip()
                        if text in ('.', '!', '?', ',', ';', ':'):
                            text = '{' + text + '}'
                        elif text == "'":
                            text = "{^'}"
                        elif text in ('-', '/'):
                            text = '{^' + text + '^}'
                        elif text:
                            # Show unknown punctuation as given.
                            text = '{^' + text + '^}'
                    elif g_destination == 'cxfing':
                        text = '{&' + g_text + '}'
                    else:
                        text = g_text
                g_text, g_destination, g_ignoring = group_stack.pop()
                g_text += text
                continue
            # No need to process other token types when
            # ignoring one of the encapsulating groups.
            if g_ignoring:
                continue
            # Control char.
            if kind == 'cchar':
                if value == '*':
                    pass
                elif value == '~':
                    g_text += '{^ ^}'
                elif value == '_':
                    g_text += '{^-^}'
                elif value in ('\\r', '\\n'):
                    g_text += '{#Return}{#Return}'
                else:
                    g_text += value
                continue
            # Control word.
            if kind == 'cword':
                if value == 'par':
                    g_text += '{#Return}{#Return}'
                elif value == 'cxfc':
                    g_text += '{-|}'
                elif value == 'cxfing':
                    kind, value = next(tokenizer)
                    assert kind == 'text'
                    g_text += '{&' + value + '}'
                elif value == 'cxds':
                    next_token = next(tokenizer)
                    if next_token[0] == 'text':
                        text = next_token[1]
                        next_token = next(tokenizer)
                        if next_token == ('cword', 'cxds'):
                            # Infix
                            g_text += '{^' + text + '^}'
                            next_token = None
                        else:
                            # Prefix.
                            g_text += '{^' + text + '}'
                    else:
                        g_text += '{^}'
                continue
            # Text.
            if kind == 'text':
                next_token = next(tokenizer)
                if next_token == ('cword', 'cxds'):
                    # Suffix.
                    g_text += '{' + value + '^}'
                    next_token = None
                else:
                    g_text += value
                continue


registry.update()
system.setup(DEFAULT_SYSTEM_NAME)

input = io.open(sys.argv[1], encoding='cp1252')
output = create_dictionary(sys.argv[2])
output.update(Parser().parse(input))#, normalize=lambda s: tuple(s.split('/'))))
output.save()
