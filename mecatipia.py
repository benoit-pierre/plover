# vim: set fileencoding=utf-8 :

# SCPMTN*#LRiUEAOIRNSLs
LETTERS = (
    'S-', 'C-', 'P-', 'M-', 'T-', 'N-', '*-', '#-', 'L-', 'R-',
    'i',
    '-U', '-E', '-A', '-O', '-I', '-R', '-N', '-S', '-L', '-s',
)

IMPLICIT_HYPHENS = 'iUEAOI'

NUMBERS = {
    '-U' : 1,
    '-E' : 6,
    '-A' : 2,
    '-O' : 7,
    '-I' : 3,
    '-R' : 8,
    '-N' : 4,
    '-S' : 9,
    '-L' : 5,
    '-s' : 0,
}

COMBOS = {
    'SP' : u'ex',
    'S*' : u'z',
    'S'  : u's',
    'S#' : u'x',
    'CM' : u'cc',
    'C*' : u'qu',
    'C'  : u'c',
    'C#' : u'g',
    'P*' : u'b',
    'P'  : u'p',
    'P#' : u'ñ',
    'M*' : u'ch',
    'M'  : u'm',
    'M#' : u'f',
    'T*' : u'd',
    'T'  : u't',
    'T#' : u'h',
    'N*' : u'll',
    'N'  : u'n',
    'N#' : u'v',
    '*L' : u'k',
    '*R' : u'w',
    '*i' : u'j',
    '#L' : u'q',
    '#R' : u'rr',
    '#i' : u'y',
    'L'  : u'l',
    'R'  : u'r',
    'i'  : u'i',
    'U'  : u'u',
    'E'  : u'e',
    'A'  : u'a',
    'O'  : u'o',
    'I'  : u'i',
    '-R' : u'r',
    '-N' : u'n',
    '-NL': u'm',
    '-S' : u's',
    '-L' : u'l',
}
MAX_COMBO_LEN = 0

WORD_PARTS = {}
MAX_WORD_PART_LEN = 0


def strokes_to_steno(stroke):
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
        right_index = stroke_steno.find('-')
        if -1 == right_index:
            for implicit_hyphen_letter in IMPLICIT_HYPHENS:
                right_index = stroke_steno.find(implicit_hyphen_letter)
                if -1 != right_index:
                    break
        if -1 == right_index:
            left = steno
            right = ''
        else:
            left = stroke_steno[:right_index]
            right = stroke_steno[right_index:]
        stroke = []
        for letter in left:
            stroke.append(letter + '-')
        for letter in right:
            if '-' == letter:
                pass
            elif 'i' == letter:
                stroke.append(letter)
            else:
                stroke.append('-' + letter)
        stroke_list.append(tuple(stroke))
    return tuple(stroke_list)

def strokes_weight(stroke):
    if isinstance(stroke[0], (tuple, list)):
        return '/'.join(strokes_weight(s) for s in stroke)
    s = ''
    for l in stroke:
        s += chr(ord('a') + LETTERS.index(l))
    return s

def has_accent(text):
    for accent_letter in u'ÁÉÍÓÚáéíóú':
        if accent_letter in text:
            return True
    return False

def strip_accents(text):
    for accent_letter, base_letter in (
        (u'Á', u'A'),
        (u'É', u'E'),
        (u'Í', u'I'),
        (u'Ó', u'O'),
        (u'Ú', u'U'),
        (u'á', u'a'),
        (u'é', u'e'),
        (u'í', u'i'),
        (u'ó', u'o'),
        (u'ú', u'u'),
    ):
        text = text.replace(accent_letter, base_letter)
    return text

def list_vowels(text):
    vowel_list = []
    for c, char in enumerate(text):
        if char in u'áéíóúaeiou':
            vowel_list.append(c)
    # Don't count 'e'/'u' in 'ex'/'gu'/'qu' prefix if other vowels follow.
    if len(vowel_list) > 1:
        for prefix in (u'ex', u'gu', u'qu'):
            if text.startswith(prefix):
                return vowel_list[1:]
    return vowel_list

def add_accent(text, accent_index):
    text = list(text)
    text[accent_index] = {
        u'a': u'á',
        u'e': u'é',
        u'i': u'í',
        u'o': u'ó',
        u'u': u'ú',
    }[text[accent_index]]
    return ''.join(text)

def strokes_to_text(stroke):
    if isinstance(stroke[0], (tuple, list)):
        accent_stroke = None
        text = ''
        for s in stroke:
            if s in (('*-',), ('#-',)):
                accent_stroke = s[0]
                continue
            part = strokes_to_text(s)
            if accent_stroke is not None:
                vowel_list = list_vowels(part)
                nb_vowels = len(vowel_list)
                accent_index = None
                if 1 == nb_vowels:
                    # Monophthong: accent on the vowel.
                    if accent_stroke == '#-':
                        accent_index = vowel_list[0]
                elif 2 == nb_vowels:
                    # Diphtong: accent on the first or second vowel.
                    if accent_stroke == '#-':
                        accent_index = vowel_list[0]
                    elif accent_stroke == '*-':
                        accent_index = vowel_list[1]
                elif 3 == nb_vowels:
                    # Triphtong: accent on 'e' or 'a'.
                    if accent_stroke == '#-':
                        for vowel in u'ae':
                            vowel_index = part.find(vowel)
                            if -1 != vowel_index:
                                accent_index = vowel_index
                                break
                if accent_index is not None:
                    part = add_accent(part, accent_index)
                accent_stroke = None
            text += part
        return text
    # Numbers.
    if len(stroke) >= 2 and '*-' == stroke[0] and \
       LETTERS.index(stroke[1]) > LETTERS.index('i'):
        numbers = []
        for l in stroke[1:]:
            numbers.append(NUMBERS[l])
        # Sort based on weight.
        numbers.sort()
        # Fix 0: it has the highest weight.
        if 0 == numbers[0]:
            numbers = numbers[1:] + [0]
        text = ''.join(str(n) for n in numbers)
        return text
    text = ''
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
        # Strip accents.
        part = strip_accents(part)
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
    def optimize(n):
        assert n < len(stroke_list)
        assert len(stroke_list) == len(part_list)
        stroke = stroke_list[n]
        part = part_list[n]
        # "simplificar": SiN/PLi/M#i/CAR" -> SIN/PLI/M#I/CAR
        if 'i' == part[-1] and 'i' == stroke[-1]:
            stroke[-1] = '-I'
            return n
        if 0 == n:
            return n + 1
        prev_stroke = stroke_list[n - 1]
        prev_part = part_list[n - 1]
        if LETTERS.index(stroke[0]) >= LETTERS.index('i'):
            # "presentar": PRES/EN/TAR -> PRE/SEN/TAR
            for letter in 'RSNL':
                sl = letter.lower()
                ss = letter + '-'
                es = '-' + letter
                if prev_part[-1] != sl or prev_stroke[-1] != es:
                    continue
                stroke_list[n - 1] = prev_stroke[:-1]
                part_list[n - 1] = prev_part[:-1]
                stroke_list[n] = [ss] + stroke
                part_list[n] = sl + part
                return n - 1
            # "foguéame": M#O/#/C#UEANL/E -> M#O/#/C#UEA/ME
            if 'm' == prev_part[-1] and ['-N', '-L'] == prev_stroke[-2:]:
                stroke_list[n - 1] = prev_stroke[:-2]
                part_list[n - 1] = prev_part[:-1]
                stroke_list[n] = ['M-'] + stroke
                part_list[n] = u'm' + part
                return n - 1
        # "perro": "PER/RO" -> "PE/RRO"
        if 'r' == prev_part[-1] and 'r' == part[0]:
            stroke_list[n - 1] = prev_stroke[:-1]
            part_list[n - 1] = prev_part[:-1]
            stroke_list[n] = ['#-',] + stroke
            part_list[n] = 'r' + part
            return n - 1
        # "mejilla": "ME/*iIL/LA" -> "ME/*iI/N*A"
        if 'l' == prev_part[-1] and 'l' == part[0]:
            stroke_list[n - 1] = prev_stroke[:-1]
            part_list[n - 1] = prev_part[:-1]
            stroke_list[n] = ['N-', '*-'] + stroke[1:]
            part_list[n] = 'l' + part
            return n - 1
        return n + 1
    n = 0
    while n < len(stroke_list):
        n = optimize(n)
    # Add missing accents.
    stroke_num = -1
    text_pos = 0
    for part in part_list:
        stroke_num += 1
        stroke = stroke_list[stroke_num]
        original_part = text[text_pos:(text_pos+len(part))]
        original_part = original_part.lower()
        text_pos += len(part)
        if not has_accent(original_part):
            continue
        vowel_list = list_vowels(original_part)
        nb_vowels = len(vowel_list)
        accent_index = None
        for vowel_index in vowel_list:
            if has_accent(original_part[vowel_index]):
                # Only one accent is allowed.
                if accent_index is not None:
                    return ()
                accent_index = vowel_index
        assert accent_index in vowel_list
        accent_stroke = None
        if 1 == nb_vowels:
            # Monophthong: accent on the vowel.
            accent_stroke = '#-'
        elif 2 == nb_vowels:
            # Diphtong: accent on the first or second vowel.
            if accent_index == vowel_list[0]:
                accent_stroke = '#-'
            else:
                accent_stroke = '*-'
        elif 3 == nb_vowels:
            # Triphtong: accent on 'e' or 'a'.
            if part[accent_index] in u'ae':
                accent_stroke = '#-'
        if accent_stroke is None:
            return ()
        stroke_list.insert(stroke_num, (accent_stroke,))
        stroke_num += 1
    return tuple(tuple(s) for s in stroke_list)

combos = {}
for steno, translation in COMBOS.items():
    strokes = steno_to_strokes(steno)
    assert 1 == len(strokes)
    combos[strokes[0]] = translation
COMBOS = combos
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


# Required interface for Plover "Python" dictionary.

MAXIMUM_KEY_LENGTH = 2

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

