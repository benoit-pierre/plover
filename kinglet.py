#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :

# Required theory constants. {{{

# 1QA2WS3ED4RF5TG_XCVBNM,6YH7UJ8IK9OL0P;
#
# 123 45 67 890
# QWE RT YU IOP
# ASD FG HK KL;
#    XCVBNM,
#       _
#
LETTERS = (
    # Left third and little fingers.
    '1', 'Q', 'A',
    '2', 'W', 'S',
    '3', 'E', 'D',
    # Left fore and middle fingers.
    '4', 'R', 'F',
    '5', 'T', 'G',
    # Thumbs.
    '_', # Space
    'X', 'C', 'V', 'B', 'N', 'M', ',',
    # Right fore and middle fingers.
    '6', 'Y', 'H',
    '7', 'U', 'J',
    # Right third and little fingers.
    '8', 'I', 'K',
    '9', 'O', 'L',
    '0', 'P', ';',
)

IMPLICIT_HYPHEN_LETTERS = LETTERS

SUFFIX_LETTERS = ()

NUMBER_LETTER = ''

NUMBERS = {}

UNDO_STROKE_STENO = ''

ORTHOGRAPHY_RULES = []

ORTHOGRAPHY_RULES_ALIASES = {}

ORTHOGRAPHY_WORDLIST = None

KEYBOARD_KEYMAP = (
    ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('0', '0'),
    ('Q', 'Q'), ('W', 'w'), ('E', 'e'), ('R', 'r'), ('T', 't'), ('Y', 'y'), ('U', 'u'), ('I', 'i'), ('O', 'o'), ('P', 'P'),
    ('A', 'A'), ('S', 's'), ('D', 'd'), ('F', 'f'), ('G', 'g'), ('H', 'h'), ('J', 'j'), ('K', 'k'), ('L', 'l'), (';', ';'),
    ('X', 'x'), ('C', 'c'), ('V', 'v'), ('B', 'b'), ('N', 'n'), ('M', 'm'), (',', ','),
    ('_', ('space')),
    ('no-op', ()),
    ('arpeggiate', ()),
)

# }}}

# Theory implementation. {{{

import re

import stroke

stroke.setup(LETTERS, IMPLICIT_HYPHEN_LETTERS)

# System keymap, used for one letter strokes.
SYSTEM_KEYMAP = {
    '1': u'1', '2': u'2', '3': u'3', '4': u'4', '5': u'5', '6': u'6', '7': u'7', '8': u'8', '9': u'9', '0': u'0',
    'Q': u'q', 'W': u'w', 'E': u'e', 'R': u'r', 'T': u't', 'Y': u'y', 'U': u'u', 'I': u'i', 'O': u'o', 'P': u'p',
    'A': u'a', 'S': u's', 'D': u'd', 'F': u'f', 'G': u'g', 'H': u'h', 'J': u'j', 'K': u'k', 'L': u'l', ';': u';',
    'X': u'x', 'C': u'c', 'V': u'v', 'B': u'b', 'N': u'n', 'M': u'm', ',': u',',
    '_': u' ',
}

KEY_PRESSED = u'■'
KEY_RELEASED = u'□'

SPACE_CHAR = u'_'

def parse_combos(cluster, key_mapping):
    key_mapping = ''.join(key_mapping.strip().split())
    combo_text = None
    combo_keys = u''
    combos = {}
    for row in cluster.strip().split('\n') + ['\n',]: # Extra empty line to finish last combo.
        row = row.strip()
        if row:
            cells = row.split()
            assert 1 <= len(cells) <= 2
            if len(cells) > 1:
                assert combo_text is None
                combo_text = cells[1]#.strip()
            combo_keys += cells[0]
            continue
        assert len(combo_keys) == len(key_mapping)
        keys = []
        for n, char in enumerate(combo_keys):
            assert char in (KEY_PRESSED, KEY_RELEASED)
            if char == KEY_PRESSED:
                keys.append(key_mapping[n])
        keys.sort()
        keys = u''.join(keys)
        assert keys, u'invalid empty combo for %s' % combo_text
        text = combo_text.replace(SPACE_CHAR, u' ')
        assert text not in combos, u'combo mapped multiple times: %s and %s' % (text, combos[keys])
        combos[keys] = text
        combo_text = None
        combo_keys = []
    return combos

'''
Use the following in VIM to make editing clusters easier:

pyfile toggle_on_off.py
nmap <buffer> <space> :python toggle_on_off()<CR>
nnoremap <buffer> <RightMouse> <LeftMouse>:python toggle_on_off()<CR>
'''

# Thumbs clusters.
THUMB_CLUSTER_MAPPING = u'''
2345678
   1
'''
THUMB_CLUSTER_COMBOS = parse_combos(
u'''

□□□■□□□  a
   □

□■■■■□□  b
   □

□□■■□□□  c
   □

□■□□□■□  d
   □

□□■□□□□  e
   □

□■■■□□□  f
   □

□□■□■■□  g
   □

□□■□□■□  h
   □

□□□□□■□  i
   □

□□□□■■■  j
   □

■□□■■□□  k
   □

□□□■□■□  l
   □

□□□□■■□  m
   □

□□■□■□□  n
   □

□■□□□□□  o
   □

□□□■■■□  p
   □

■□□□■■□  q
   □

□■□■□□□  r
   □

□■□□■□□  s
   □

□□□□■□□  t
   □

□■■□□□□  u
   □

□□□□■□■  v
   □

□■□■■□□  w
   □

■■■□□□□  x
   □

□□■■□■□  y
   □

□■■□□□■  z
   □

□■■□□■□  an
   □

■□□□□□□  at
   □

□□□□□□■  en
   □

□■□□■■□  er
   □

□□■■■□□  he
   □

□■■□■□□  in
   □

■□□□■□□  nd
   □

□■■□■■□  on
   □

■□□□□■□  or
   □

□□■■■■□  re
   □

□■□□□□■  te
   □

□□□■■□□  th
   □

□□■□□□■  ti
   □

□□□■■□■  -
   □

■■□□□□□  !
   □

■□■■□□□  "
   □

■□□■□□□  ,
   □

□□□■□□■  .
   □

□□□□□■■  ?
   □

□□■■□□■  '
   □

■□■□□□□  |
   □

□□□□□□□  _
   ■

''', THUMB_CLUSTER_MAPPING)

# Left hand outer cluster: third and little fingers.
LEFT_OUTER_CLUSTER_MAPPING = u'''
147
258
369
'''
LEFT_OUTER_CLUSTER_COMBOS = parse_combos(
u'''

□□□
□■■  a
□□□

□■□
□■□  b
□□□

□□■
□□■  c
□□□

□■■
□■□  d
□□□

□□■
□□□  e
□□□

□□□
□■□  f
□□□

□□□
□■□  g
■□□

□□■
□■■  h
□□□

□□□
□□□  i
□■■

□□□
■□□  j
□□□

□□□
□□■  k
■□■

□□□
□□■  l
□■■

□□□
□■■  m
□■■

□□□
□□■  n
□■□

□■■
□□□  o
□□□

□■□
□□□  p
□□□

■□□
□□□  q
□□□

□□□
□■■  r
□■□

□□■
□■□  s
□□□

□□□
□□□  t
□□■

□■■
□■■  u
□□□

□□■
■□□  v
□□□

□■□
■□□  w
□□□

□□□
□□□  x
■□■

□□□
■■□  y
□□□

□□□
□□□  z
■□□

■■□
□□□  an
□□□

□■□
■■□  at
□□□

□□□
□■□  en
■■□

□□□
□□□  er
■■□

□□■
□■■  he
□■□

□□□
□□□  in
□■□

■■□
■□□  nd
□□□

□□□
■■□  on
■□□

□□□
■□■  or
■□□

□□□
□■□  re
□■□

□□■
■□■  te
□□□

□□□
□□■  th
□□■

□■□
■■□  ti
■□□

□□□
■□■  -
□□□

■□□
■□□  !
□□□

□□■
■□■  "
■□□

■■□
■■□  ,
□□□

□□□
■■□  .
■■□

□□□
■□□  ?
■□□

■□■
■□□  '
□□□

□□□
□□■  |
■□□

□□□
□□■  _
□□□

''', LEFT_OUTER_CLUSTER_MAPPING)

# Left hand inner cluster: fore and middle fingers.
LEFT_INNER_CLUSTER_MAPPING = u'''
14
25
36
'''
LEFT_INNER_CLUSTER_COMBOS = parse_combos(
u'''

■□
□□  a
□□

■■
■□  b
■■

■■
□□  c
□□

□□
■□  d
□■

□□
■□  e
□□

□□
■■  f
□■

■□
■□  g
□■

□□
□□  h
■□

■□
■□  i
□□

□■
□■  j
■□

□□
■■  k
■□

■□
□■  l
□□

■■
■■  m
□□

□□
□■  n
□■

□■
□■  o
□□

■□
□■  p
□■

□■
□■  q
■■

□□
□□  r
□■

□□
■□  s
■□

□■
□□  t
□□

■■
□■  u
□□

□■
■□  v
□□

□□
□□  w
■■

■■
■□  x
■□

□□
■□  y
■■

□■
□□  z
■□

■■
□■  an
□■

■□
□□  at
■■

■□
■□  en
■□

□□
■■  er
■■

■□
■■  he
□□

■□
■■  in
□■

□■
□■  nd
□■

■■
□□  on
□■

□■
■■  or
□□

■□
□□  re
□■

□□
□■  te
■□

□□
■■  th
□□

■□
□□  ti
■□

□■
■□  -
■□

■■
□□  !
■□

□■
■■  "
■□

□■
□□  ,
□■

■■
□□  .
■■

□■
□□  ?
■■

□□
□■  '
■■

■■
■□  |
□□

□□
□■  _
□□

''', LEFT_INNER_CLUSTER_MAPPING)

# Right hand clusters are mirrored from the left hand.
def mirror_combos(base_combos, mapping):
    transform = {}
    for row in mapping.strip().split('\n'):
        for n, k in enumerate(row.strip()):
            transform[k] = row[len(row) - (n + 1)]
    mirrored_combos = {}
    for combo, translation in base_combos.items():
        combo = [transform[c] for c in combo]
        combo.sort()
        combo = ''.join(combo)
        mirrored_combos[combo] = translation
    return mirrored_combos
# 147 14    41 741
# 258 25 -> 52 852
# 369 36    63 963
RIGHT_INNER_CLUSTER_COMBOS = mirror_combos(LEFT_INNER_CLUSTER_COMBOS, LEFT_INNER_CLUSTER_MAPPING)
RIGHT_OUTER_CLUSTER_COMBOS = mirror_combos(LEFT_OUTER_CLUSTER_COMBOS, LEFT_OUTER_CLUSTER_MAPPING)

# Final list of all clusters.
CLUSTERS = (
    # Left third and little fingers.
    (9, LEFT_OUTER_CLUSTER_COMBOS),
    # Left fore and middle fingers.
    (6, LEFT_INNER_CLUSTER_COMBOS),
    # Thumbs.
    (8, THUMB_CLUSTER_COMBOS),
    # Right fore and middle fingers.
    (6, RIGHT_INNER_CLUSTER_COMBOS),
    # Right third and little fingers.
    (9, RIGHT_OUTER_CLUSTER_COMBOS),
)

COMBOS = {}
MAX_COMBO_LEN = 0

WORD_PARTS = {}
MAX_WORD_PART_LEN = 0


class Stroke(stroke.Stroke):

    def to_text(self, cap_state=None, use_keymap=False):
        keys = self.keys()
        # Single letter stroke: use keymap.
        if use_keymap and len(keys) == 1:
            return SYSTEM_KEYMAP[keys[0]]
        text = u''
        while keys:
            combo = Stroke(keys[0:MAX_COMBO_LEN])
            while combo:
                if combo in COMBOS:
                    part = COMBOS[combo]
                    text += part
                    break
                combo -= combo.last()
            if not combo:
                raise KeyError
            keys = keys[len(combo):]
        # [cap] support.
        if cap_state is None:
            final_text = text
        else:
            final_text = u''
            for part in re.split(r'(\|+)', text):
                if not part:
                    continue
                if u'||' == part:
                    cap_state['capslock'] = True
                elif u'|' == part:
                    if cap_state['capslock']:
                        assert not cap_state['shift']
                        cap_state['capslock'] = False
                    else:
                        cap_state['shift'] = True
                else:
                    if cap_state['shift']:
                        assert not cap_state['capslock']
                        cap_state['shift'] = False
                        final_text += part.capitalize()
                    elif cap_state['capslock']:
                        final_text += part.upper()
                    else:
                        final_text += part
        return final_text

def strokes_to_text(stroke_list, cap_state=None):
    return u''.join(s.to_text(cap_state) for s in stroke_list)

def strokes_from_text(text):
    leftover_text = text
    # [cap] support.
    leftover_text = re.sub(r'([A-Z][A-Z]+)', lambda m: '||' + m.group(1).lower() + '|', leftover_text)
    leftover_text = re.sub(r'([A-Z])', lambda m: '|' + m.group(1).lower(), leftover_text)
    stroke_list = []
    part_list = []
    stroke = Stroke()
    while len(leftover_text) > 0:
        # Find candidate parts.
        combo_list = []
        part = leftover_text[0:MAX_WORD_PART_LEN]
        while len(part) > 0:
            combo_list.extend(WORD_PARTS.get(part, ()))
            part = part[:-1]
        if 0 == len(combo_list):
            return ()
        # First try to extend current stroke.
        part = None
        if stroke:
            for combo in combo_list:
                if stroke.is_prefix(combo):
                    # Check if we're not changing the translation.
                    wanted = stroke.to_text(use_keymap=False) + COMBOS[combo]
                    result = (stroke + combo).to_text()
                    if wanted != result:
                        continue
                    stroke += combo
                    part = COMBOS[combo]
                    part_list[-1] += part
                    break
        # Start a new stroke
        if part is None:
            if stroke:
                stroke_list.append(stroke)
            combo = combo_list[0]
            stroke = combo
            part = COMBOS[combo]
            part_list.append(part)
        assert len(part) > 0
        leftover_text = leftover_text[len(part):]
    if stroke:
        stroke_list.append(stroke)
    assert len(stroke_list) == len(part_list)
    return stroke_list


n = 0
for cluster_size, cluster_combos in CLUSTERS:
    cluster = LETTERS[n:n+cluster_size]
    assert len(cluster) == cluster_size
    n += cluster_size
    for combo, translation in cluster_combos.items():
        keys = []
        for k in combo.strip():
            k = int(k)
            assert 1 <= k <= cluster_size, '%u/%u' % (k, cluster_size)
            keys.append(cluster[k-1])
        stroke = Stroke(keys)
        assert stroke not in COMBOS
        COMBOS[stroke] = translation
assert n == len(LETTERS)
MAX_COMBO_LEN = max(len(combo) for combo in COMBOS)

for combo, part in COMBOS.items():
    if part in WORD_PARTS:
        WORD_PARTS[part] += (combo,)
    else:
        WORD_PARTS[part] = (combo,)
for part, combo_list in WORD_PARTS.items():
    # We want left combos to be given priority over right ones,
    # e.g. 'R-' over '-R' for 'r'.
    WORD_PARTS[part] = sorted(combo_list)
MAX_WORD_PART_LEN = max(len(part) for part in WORD_PARTS.keys())

# }}}

# Required interface for Plover "Python" dictionary. {{{

MAXIMUM_KEY_LENGTH = 1

CAP_STATE = {
    'shift': False,
    'capslock': False,
}

def lookup_translation(key):
    assert len(key) <= MAXIMUM_KEY_LENGTH
    stroke_list = [Stroke(s) for s in key]
    return '{^%s}' % strokes_to_text(stroke_list, cap_state=CAP_STATE)

def reverse_lookup(text):
    stroke_list = strokes_from_text(text)
    if not stroke_list:
        return []
    return [tuple(str(s) for s in stroke_list)]

# }}}

# Main entry-point for testing. {{{

if __name__ == '__main__':
    import sys
    import re
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

# }}}

# vim: foldmethod=marker
