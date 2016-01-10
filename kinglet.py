# vim: set fileencoding=utf-8 :

# Required theory constants. {{{

# _XCVBNM,4RF5TG6YH7UJ2WS3ED8IK9OL
LETTERS = (
    # Thumbs.
    '_', # Space
    'X', 'C', 'V', 'B', 'N', 'M', ',',
    # Left fore and middle fingers.
    '4', 'R', 'F',
    '5', 'T', 'G',
    # Right fore and middle fingers.
    '6', 'Y', 'H',
    '7', 'U', 'J',
    # Left third and little fingers.
    '2', 'W', 'S',
    '3', 'E', 'D',
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

# Default keymap for Plover, which can be changed/customized in the GUI configuration.
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

IMPLICIT_HYPHENS = ''.join(l.replace('-', '') for l in IMPLICIT_HYPHEN_LETTERS)

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
    '24  ': u'', # [cap]
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
    '126 ': u'', # [cap]
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
    # Thumbs.
    (8, THUMB_CLUSTER_COMBOS),
    # Left fore and middle fingers.
    (6, LEFT_CLUSTER_COMBOS),
    # Right fore and middle fingers.
    (6, RIGHT_CLUSTER_COMBOS),
    # Left third and little fingers.
    (6, LEFT_CLUSTER_COMBOS),
    # Right third and little fingers.
    (6, RIGHT_CLUSTER_COMBOS),
)

COMBOS = {}
MAX_COMBO_LEN = 0

WORD_PARTS = {}
MAX_WORD_PART_LEN = 0


def strokes_to_steno(stroke):
    if () == stroke:
        return ''
    if isinstance(stroke[0], (tuple, list)):
        return '/'.join(strokes_to_steno(s) for s in stroke)
    s = ''.join(stroke)
    if '--' in s:
        part1, part2 = s.split('--', 2)
        return strokes_to_steno(part1 + '-') + strokes_to_steno('-' + part2)
    if '-' == s[0]:
        s = s.replace('-', '')
        if s[0] in IMPLICIT_HYPHENS:
            return s
        return '-' + s
    return s.replace('-', '')

def steno_to_strokes(steno):
    stroke_list = []
    for stroke_steno in steno.split('/'):
        stroke = [l for l in stroke_steno]
        stroke_list.append(tuple(stroke))
    return tuple(stroke_list)

def strokes_weight(stroke):
    if isinstance(stroke[0], (tuple, list)):
        return '/'.join(strokes_weight(s) for s in stroke)
    s = ''
    for l in stroke:
        s += chr(ord('a') + LETTERS.index(l))
    return s

def strokes_to_text(stroke):
    if () == stroke:
        return u''
    if isinstance(stroke[0], (tuple, list)):
        text = u''
        for s in stroke:
            part = strokes_to_text(s)
            text += part
        return text
    # Single letter stroke: use keymap.
    if len(stroke) == 1:
        return SYSTEM_KEYMAP[stroke[0]]
    text = u''
    while len(stroke) > 0:
        combo = stroke[0:MAX_COMBO_LEN]
        while len(combo) > 0:
            if combo in COMBOS:
                part = COMBOS[combo]
                text += part
                break
            combo = combo[:-1]
        if 0 == len(combo):
            raise ValueError
        assert len(combo) > 0
        stroke = stroke[len(combo):]
    return text

def text_to_strokes(text):
    leftover_text = text
    stroke_list = []
    part_list = []
    stroke = []
    while len(leftover_text) > 0:
        # Find candidate parts (by decreasing length).
        combo_list = []
        part = leftover_text[0:MAX_WORD_PART_LEN]
        while len(part) > 0:
            if part in WORD_PARTS:
                combo_list.extend(WORD_PARTS[part])
            part = part[:-1]
        if 0 == len(combo_list):
            return ()
        assert len(combo_list) > 0
        # First try to extend current stroke.
        part = None
        if len(stroke) > 0:
            stroke_last_letter_weight = LETTERS.index(stroke[-1])
            for combo in combo_list:
                if stroke_last_letter_weight < LETTERS.index(combo[0]):
                    # Check if we're not changing the translation.
                    wanted = strokes_to_text(tuple(stroke) + combo)
                    result = strokes_to_text(tuple(stroke)) + COMBOS[combo]
                    if wanted != result:
                        continue
                    stroke.extend(combo)
                    part = COMBOS[combo]
                    part_list[-1] += part
                    break
        # Start a new stroke
        if part is None:
            combo = combo_list[0]
            stroke = list(combo)
            stroke_list.append(stroke)
            part = COMBOS[combo]
            part_list.append(part)
        assert len(part) > 0
        leftover_text = leftover_text[len(part):]
    assert len(stroke_list) == len(part_list)
    return tuple(tuple(s) for s in stroke_list)


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
        strokes = steno_to_strokes(steno)
        assert 1 == len(strokes)
        assert strokes[0] not in COMBOS
        COMBOS[strokes[0]] = translation
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
    combo_list = sorted(combo_list, key=lambda s: strokes_weight(s))
    WORD_PARTS[part] = combo_list
MAX_WORD_PART_LEN = max(len(part) for part in WORD_PARTS.keys())

# }}}

# Required interface for Plover "Python" dictionary. {{{

MAXIMUM_KEY_LENGTH = 1

def lookup_translation(key):
    strokes = []
    for steno in key:
        strokes.extend(steno_to_strokes(steno))
    if len(strokes) > 2:
        raise KeyError()
    if len(strokes) == 2 and strokes[0] not in (('*-',), ('#-',)):
        raise KeyError()
    strokes = tuple(strokes)
    try:
        text = strokes_to_text(strokes)
    except ValueError:
        raise KeyError
    return '{^%s}' % text
    raise KeyError()

def reverse_lookup(text):
    strokes = text_to_strokes(text)
    if () == strokes:
        return None
    steno = [strokes_to_steno(s) for s in strokes]
    return (steno,)

# }}}

# Main entry-point for testing. {{{

# if __name__ == '__main__':
#     import sys
#     import re
#     if '/' == sys.argv[1]:
#         text = u''
#         # steno -> text.
#         for steno in sys.argv[2:]:
#             steno = steno.replace('[ ]', '_')
#             for part in steno.split('/'):
#                 if not part:
#                     continue
#                 if '[' == part[0]:
#                     assert ']' == part[-1]
#                     text += part[1:-2]
#                 else:
#                     strokes = steno_to_strokes(part)
#                     text += strokes_to_text(strokes)
#         print text
#     else:
#         # text -> steno.
#         supported_chars = set()
#         for part in WORD_PARTS:
#             supported_chars.update(part)
#         assert not set('/[]') & supported_chars
#         supported_chars = ''.join(sorted(supported_chars))
#         rx = re.compile('([^' + supported_chars.replace('-', '\\-') + ']+)')
#         steno = ''
#         for text in sys.argv[1:]:
#             # No case support for now.
#             text = text.lower()
#             for part in re.split(rx, text):
#                 if steno:
#                     steno += '/'
#                 if part[0] in supported_chars:
#                     strokes = text_to_strokes(part)
#                     steno += strokes_to_steno(strokes)
#                 else:
#                     steno += '[' + ']/['.join(part) + ']'
#         steno = steno.replace('_', '[ ]')
#         print steno

# }}}

# vim: foldmethod=marker
