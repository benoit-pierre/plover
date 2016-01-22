#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :

# Required theory constants. {{{

# 2WS3ED4RF5TG_XCVBNM,6YH7UJ8IK9OL
LETTERS = (
    # Left third and little fingers.
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
    ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
    ('W', 'w'), ('E', 'e'), ('R', 'r'), ('T', 't'), ('Y', 'y'), ('U', 'u'), ('I', 'i'), ('O', 'o'),
    ('S', 's'), ('D', 'd'), ('F', 'f'), ('G', 'g'), ('H', 'h'), ('J', 'j'), ('K', 'k'), ('L', 'l'),
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
    '2': u'2', '3': u'3', '4': u'4', '5': u'5', '6': u'6', '7': u'7', '8': u'8', '9': u'9',
    'W': u'w', 'E': u'e', 'R': u'r', 'T': u't', 'Y': u'y', 'U': u'u', 'I': u'i', 'O': u'o',
    'S': u's', 'D': u'd', 'F': u'f', 'G': u'g', 'H': u'h', 'J': u'j', 'K': u'k', 'L': u'l',
    'X': u'x', 'C': u'c', 'V': u'v', 'B': u'b', 'N': u'n', 'M': u'm', ',': u',',
    '_': u' ',
}

# Thumbs clusters.
THUMB_CLUSTER_COMBOS = {
    # 2345678
    #    1
    '1   ': u' ',
    '5   ': u'a',
    '3456': u'b',
    '45  ': u'c',
    '37  ': u'd',
    '4   ': u'e',
    '345 ': u'f',
    '467 ': u'g',
    '47  ': u'h',
    '7   ': u'i',
    '678 ': u'j',
    '256 ': u'k',
    '57  ': u'l',
    '67  ': u'm',
    '46  ': u'n',
    '3   ': u'o',
    '567 ': u'p',
    '267 ': u'q',
    '35  ': u'r',
    '36  ': u's',
    '6   ': u't',
    '34  ': u'u',
    '68  ': u'v',
    '356 ': u'w',
    '234 ': u'x',
    '457 ': u'y',
    '348 ': u'z',
    '347 ': u'an',
    '2   ': u'at',
    '8   ': u'en',
    '367 ': u'er',
    '456 ': u'he',
    '346 ': u'in',
    '26  ': u'nd',
    '3467': u'on',
    '27  ': u'or',
    '4567': u're',
    '38  ': u'te',
    '56  ': u'th',
    '48  ': u'ti',
    '568 ': u'-',
    '23  ': u'!',
    '245 ': u'"',
    '25  ': u',',
    '58  ': u'.',
    '78  ': u'?',
    '458 ': u'\'',
    '24  ': u'|', # [cap]
}
# Left hand clusters.
LEFT_CLUSTER_COMBOS = {
    # 14
    # 25
    # 36
    '6   ': u'a',
    '235 ': u'b',
    '26  ': u'c',
    '24  ': u'd',
    '2   ': u'e',
    '1245': u'f',
    '145 ': u'g',
    '35  ': u'h',
    '3   ': u'i',
    '134 ': u'j',
    '1236': u'k',
    '15  ': u'l',
    '12  ': u'm',
    '25  ': u'n',
    '1   ': u'o',
    '2356': u'p',
    '146 ': u'q',
    '36  ': u'r',
    '14  ': u's',
    '4   ': u't',
    '56  ': u'u',
    '1234': u'v',
    '356 ': u'w',
    '16  ': u'x',
    '256 ': u'y',
    '346 ': u'z',
    '125 ': u'an',
    '1256': u'at',
    '123 ': u'en',
    '124 ': u'er',
    '23  ': u'he',
    '245 ': u'in',
    '456 ': u'nd',
    '2345': u'on',
    '1456': u'or',
    '236 ': u're',
    '3456': u'te',
    '45  ': u'th',
    '234 ': u'ti',
    '34  ': u'-',
    '136 ': u'!',
    '46  ': u'"',
    '156 ': u',',
    '345 ': u'.',
    '1346': u'?',
    '13  ': u'\'',
    '126 ': u'|', # [cap]
    '5   ': u' ',
}
# Right hand clusters are mirrored from the left hand.
# 14    41
# 25 -> 52
# 36    63
RIGHT_CLUSTER_COMBOS = {}
for combo, translation in LEFT_CLUSTER_COMBOS.items():
    combo = [' ' if ' ' == c else
             str((int(c) - 1 + 3) % 6 + 1)
             for c in combo]
    combo.sort()
    combo = ''.join(combo)
    RIGHT_CLUSTER_COMBOS[combo] = translation
# Final list of all clusters.
CLUSTERS = (
    # Left third and little fingers.
    (6, LEFT_CLUSTER_COMBOS),
    # Left fore and middle fingers.
    (6, LEFT_CLUSTER_COMBOS),
    # Thumbs.
    (8, THUMB_CLUSTER_COMBOS),
    # Right fore and middle fingers.
    (6, RIGHT_CLUSTER_COMBOS),
    # Right third and little fingers.
    (6, RIGHT_CLUSTER_COMBOS),
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
        steno = ''
        for k in combo.strip():
            k = int(k)
            assert 1 <= k <= cluster_size, '%u/%u' % (k, cluster_size)
            steno += cluster[k-1]
        stroke = Stroke(steno)
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
