# vim: set fileencoding=utf-8 :

import re

from kinglet.system import *
from kinglet import stroke

from text_table import parse_text_table


stroke.setup(KEYS, IMPLICIT_HYPHEN_KEYS)

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
    combos = {}
    for row in parse_text_table(cluster):
        assert 0 == (len(row) % 2)
        for c in range(0, len(row), 2):
            text = row[c].strip().replace(SPACE_CHAR, u' ')
            keys = []
            for n, char in enumerate(u''.join(l.strip() for l in row[c + 1])):
                assert char in (u'\n', u' ', KEY_PRESSED, KEY_RELEASED)
                if char == KEY_PRESSED:
                    keys.append(key_mapping[n])
            keys.sort()
            keys = u''.join(keys)
            assert keys, u'invalid empty combo for %s' % text
            assert text not in combos, u'combo mapped multiple times: %s and %s' % (text, combos[keys])
            combos[keys] = text
    return combos

'''
Use the following in VIM to make editing clusters easier:

pyfile misc/vim_toggle_on_off.py
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

    a  □□□■□□□    q  ■□□□■■□    nd ■□□□■□□
          □             □             □

    b  □■■■■□□    r  □■□■□□□    on □■■□■■□
          □             □             □

    c  □□■■□□□    s  □■□□■□□    or ■□□□□■□
          □             □             □

    d  □■□□□■□    t  □□□□■□□    re □□■■■■□
          □             □             □

    e  □□■□□□□    u  □■■□□□□    te □■□□□□■
          □             □             □

    f  □■■■□□□    v  □□□□■□■    th □□□■■□□
          □             □             □

    g  □□■□■■□    w  □■□■■□□    ti □□■□□□■
          □             □             □

    h  □□■□□■□    x  ■■■□□□□    -  □□□■■□■
          □             □             □

    i  □□□□□■□    y  □□■■□■□    !  ■■□□□□□
          □             □             □

    j  □□□□■■■    z  □■■□□□■    "  ■□■■□□□
          □             □             □

    k  ■□□■■□□    an □■■□□■□    ,  ■□□■□□□
          □             □             □

    l  □□□■□■□    at ■□□□□□□    .  □□□■□□■
          □             □             □

    m  □□□□■■□    en □□□□□□■    ?  □□□□□■■
          □             □             □

    n  □□■□■□□    er □■□□■■□    '  □□■■□□■
          □             □             □

    o  □■□□□□□    he □□■■■□□    |  ■□■□□□□
          □             □             □

    p  □□□■■■□    in □■■□■□□    _  □□□□□□□
          □             □             ■

''', THUMB_CLUSTER_MAPPING)

# Left hand outer cluster: third and little fingers.
LEFT_OUTER_CLUSTER_MAPPING = u'''
147
258
369
'''
LEFT_OUTER_CLUSTER_COMBOS = parse_combos(
u'''

    a  □□□    b  □■□    c  □□■    d  □■■    e  □□■    f  □□□    g  □□□    h  □□■
       □■■       □■□       □□■       □■□       □□□       □■□       □■□       □■■
       □□□       □□□       □□□       □□□       □□□       □□□       ■□□       □□□

    i  □□□    j  □□□    k  □□□    l  □□□    m  □□□    n  □□□    o  □■■    p  □■□
       □□□       ■□□       □□■       □□■       □■■       □□■       □□□       □□□
       □■■       □□□       ■□■       □■■       □■■       □■□       □□□       □□□

    q  ■□□    r  □□□    s  □□■    t  □□□    u  □■■    v  □□■    w  □■□    x  □□□
       □□□       □■■       □■□       □□□       □■■       ■□□       ■□□       □□□
       □□□       □■□       □□□       □□■       □□□       □□□       □□□       ■□■

    y  □□□    z  □□□    an ■■□    at □■□    en □□□    er □□□    he □□■    in □□□
       ■■□       □□□       □□□       ■■□       □■□       □□□       □■■       □□□
       □□□       ■□□       □□□       □□□       ■■□       ■■□       □■□       □■□

    nd ■■□    on □□□    or □□□    re □□□    te □□■    th □□□    ti □■□    -  □□□
       ■□□       ■■□       ■□■       □■□       ■□■       □□■       ■■□       ■□■
       □□□       ■□□       ■□□       □■□       □□□       □□■       ■□□       □□□

    !  ■□□    "  □□■    ,  ■■□    .  □□□    ?  □□□    '  ■□■    |  □□□    _  □□□
       ■□□       ■□■       ■■□       ■■□       ■□□       ■□□       □□■       □□■
       □□□       ■□□       □□□       ■■□       ■□□       □□□       ■□□       □□□

''', LEFT_OUTER_CLUSTER_MAPPING)

# Left hand inner cluster: fore and middle fingers.
LEFT_INNER_CLUSTER_MAPPING = u'''
14
25
36
'''
LEFT_INNER_CLUSTER_COMBOS = parse_combos(
u'''

    a  ■□    b  ■□    c  ■■    d  □□    e  □□    f  □□    g  ■□    h  □□
       □□       ■□       □□       ■□       ■□       ■■       ■□       □□
       □□       ■■       □□       □■       □□       □■       □■       ■□

    i  ■□    j  □■    k  □□    l  ■□    m  ■■    n  □□    o  □■    p  ■□
       ■□       □■       ■■       □■       ■■       □■       □■       □■
       □□       ■□       ■□       □□       □□       □■       □□       □■

    q  □■    r  □□    s  □□    t  □■    u  ■■    v  □■    w  □□    x  ■■
       □■       □□       ■□       □□       □■       ■□       □□       ■□
       ■■       □■       ■□       □□       □□       □□       ■■       ■□

    y  □□    z  □■    an ■■    at ■□    en ■□    er □□    he ■□    in ■□
       ■□       □□       □■       □□       ■□       ■■       ■■       ■■
       ■■       ■□       □■       ■■       ■□       ■■       □□       □■

    nd □■    on ■■    or □■    re ■□    te □□    th □□    ti ■□    -  □■
       □■       □□       ■■       □□       □■       ■■       □□       ■□
       □■       □■       □□       □■       ■□       □□       ■□       ■□

    !  ■■    "  □■    ,  □■    .  ■■    ?  □■    '  □□    |  ■■    _  □□
       □□       ■■       □□       □□       □□       □■       ■□       □■
       ■□       ■□       □■       ■■       ■■       ■■       □□       □□

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

def strokes_to_text(stroke_list, cap_state=None, use_keymap=False):
    return u''.join(s.to_text(cap_state, use_keymap) for s in stroke_list)

def strokes_from_text(text):
    leftover_text = text
    # [cap] support.
    leftover_text = re.sub(r'([A-Z][A-Z]+)', lambda m: '||' + m.group(1).lower() + '|', leftover_text)
    leftover_text = re.sub(r'([A-Z])', lambda m: '|' + m.group(1).lower(), leftover_text)
    stroke_list = []
    part_list = []
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
        if stroke_list:
            stroke = stroke_list[-1]
            for combo in combo_list:
                if stroke.is_prefix(combo):
                    # Check if we're not changing the translation.
                    wanted = stroke.to_text(use_keymap=False) + COMBOS[combo]
                    result = (stroke + combo).to_text()
                    if wanted != result:
                        continue
                    stroke_list[-1] += combo
                    part = COMBOS[combo]
                    part_list[-1] += part
                    break
        # Start a new stroke
        if part is None:
            combo = combo_list[0]
            stroke_list.append(combo)
            part = COMBOS[combo]
            part_list.append(part)
        assert len(part) > 0
        leftover_text = leftover_text[len(part):]
    assert len(stroke_list) == len(part_list)
    return stroke_list


n = 0
for cluster_size, cluster_combos in CLUSTERS:
    cluster = KEYS[n:n+cluster_size]
    assert len(cluster) == cluster_size
    n += cluster_size
    for combo, translation in cluster_combos.items():
        steno = ''
        for k in combo.strip():
            k = int(k)
            assert 1 <= k <= cluster_size, '%u/%u' % (k, cluster_size)
            steno += cluster[k-1]
        stroke = Stroke(steno)
        assert stroke not in COMBOS
        COMBOS[stroke] = translation
assert n == len(KEYS)
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

# vim: foldmethod=marker
