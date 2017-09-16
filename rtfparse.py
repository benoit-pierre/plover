#!/usr/bin/env python3

import re

from plover.steno import normalize_steno
from plover import log


RTF_TOKEN_PARTS = (
    ('cchar' , '\\\\([-_~\\\\{}*\n\r])'                 , (0,)  ),
    ('cword' , r'\\([A-Za-z]+-?[0-9]*) ?'               , (0,)  ),
    ('gstart', r'({)(?:(\\\*)?\\([A-Za-z]+-?[0-9]*) ?)?', (1, 2)),
    ('gend'  , r'(})'                                   , (0,)  ),
    ('text'  , '([^\n\r\\\\{}]+)'                       , (0,)  ),
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
            yield (name, m.group(*wanted)), (lnum, cnum)
            cnum = end
    yield (None, None), (lnum, cnum)


class ParseError(Exception):

    def __init__(self, position, fmt, *fmt_args):
        lnum, cnum = position
        msg = 'line %u, column %u: %s' % (
            lnum + 1, cnum + 1,
            fmt % fmt_args,
        )
        super(ParseError, self).__init__(msg)


class Parser(object):

    def __init__(self):
        pass

    def parse(self, input, normalize=normalize_steno, skip_errors=True):
        def finalize_translation(text):
            left_ws = len(text) - len(text.lstrip())
            if left_ws > 1:
                text = '{^' + text[:left_ws] + '^}' + text[left_ws:]
            right_ws = len(text) - len(text.rstrip())
            if right_ws > 1:
                text = text[:-right_ws] + '{^' + text[-right_ws:] + '^}'
            return text
        tokenizer = rtf_tokenize(input)
        token, position = next(tokenizer)
        if token != ('gstart', (None, 'rtf1')):
            raise ParseError(position, 'expected rtf group, got: %r', token)
        token, position = next(tokenizer)
        group_stack = []
        g_text, g_destination, g_ignoring = '', 'rtf1', False
        next_token, next_position = None, None
        steno = None
        while True:
            if next_token is not None:
                token, position = next_token, next_position
                next_token, next_position = None, None
            else:
                token, position = next(tokenizer)
            kind, value = token
            if kind is None:
                if steno is not None:
                    yield normalize(steno), finalize_translation(g_text)
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
                        if group_stack:
                            err = ParseError(position, 'group stack depth is %u', len(group_stack))
                            if skip_errors:
                                log.error('%s', err)
                                g_text, g_destination, g_ignoring = group_stack[0]
                                assert g_destination == 'rtf1'
                                group_stack.clear()
                            else:
                                raise err
                        if steno is not None:
                            yield normalize(steno), finalize_translation(g_text)
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
                if g_destination == 'rtf1':
                    next_token, next_position = next(tokenizer)
                    if next_token != (None, None):
                        err = ParseError(next_position, 'expected end of file, got: %r', next_token)
                        if skip_errors:
                            log.error('%s', err)
                            # Skip to next \cxs group.
                            while next_token != ('gstart', ('\\*', 'cxs')):
                                next_token, next_position = next(tokenizer)
                        else:
                            raise err
                    g_text = text
                    continue
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
                elif value in ('\r', '\n'):
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
                elif value == 'cxfl':
                    g_text += '{>}'
                elif value == 'cxfing':
                    token, position = next(tokenizer)
                    if token[0] != 'text':
                        raise ParseError(position, 'expected text, got: %r', token)
                    g_text += '{&' + token[1] + '}'
                elif value == 'cxds':
                    next_token, next_position = next(tokenizer)
                    if next_token[0] == 'text':
                        text = next_token[1]
                        next_token, next_position = next(tokenizer)
                        if next_token == ('cword', 'cxds'):
                            # Infix
                            g_text += '{^' + text + '^}'
                            next_token, next_position = None, None
                        else:
                            # Prefix.
                            g_text += '{^' + text + '}'
                    else:
                        g_text += '{^}'
                continue
            # Text.
            if kind == 'text':
                next_token, next_position = next(tokenizer)
                if next_token == ('cword', 'cxds'):
                    # Suffix.
                    g_text += '{' + value + '^}'
                    next_token, next_position = None, None
                else:
                    g_text += value
                continue


if __name__ == '__main__':

    import io
    import sys

    from plover import system
    from plover.config import DEFAULT_SYSTEM_NAME
    from plover.dictionary.base import create_dictionary
    from plover.registry import registry

    registry.update()
    system.setup(DEFAULT_SYSTEM_NAME)

    input = io.open(sys.argv[1], encoding='cp1252')
    output = create_dictionary(sys.argv[2])
    output.update(Parser().parse(input))#, normalize=lambda s: tuple(s.split('/'))))
    output.save()
