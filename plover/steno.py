# Copyright (c) 2010-2011 Joshua Harlan Lifton.
# See LICENSE.txt for details.

# TODO: unit test this file

"""Generic stenography data models.

This module contains the following class:

Stroke -- A data model class that encapsulates a sequence of steno keys.

"""

import re
import mecatipia

STROKE_DELIMITER = '/'
IMPLICIT_HYPHENS = set(mecatipia.IMPLICIT_HYPHENS)

def normalize_steno(strokes_string):
    """Convert steno strings to one common form."""
    strokes = strokes_string.split(STROKE_DELIMITER)
    normalized_strokes = []
    for stroke in strokes:
        has_implicit_dash = bool(set(stroke) & IMPLICIT_HYPHENS)
        if has_implicit_dash:
            stroke = stroke.replace('-', '')
        if stroke.endswith('-'):
            stroke = stroke[:-1]
        normalized_strokes.append(stroke)
    return tuple(normalized_strokes)

STENO_KEY_NUMBERS = {}

STENO_KEY_ORDER = dict((l, n) for n, l in enumerate(mecatipia.LETTERS))

class Stroke:
    """A standardized data model for stenotype machine strokes.

    This class standardizes the representation of a stenotype chord. A stenotype
    chord can be any sequence of stenotype keys that can be simultaneously
    pressed. Nearly all stenotype machines offer the same set of keys that can
    be combined into a chord, though some variation exists due to duplicate
    keys. This class accounts for such duplication, imposes the standard
    stenographic ordering on the keys, and combines the keys into a single
    string (called RTFCRE for historical reasons).

    """

    IMPLICIT_HYPHEN = set(mecatipia.steno_to_strokes(mecatipia.IMPLICIT_HYPHENS)[0])

    def __init__(self, steno_keys) :
        """Create a steno stroke by formatting steno keys.

        Arguments:

        steno_keys -- A sequence of pressed keys.

        """
        # Remove duplicate keys and save local versions of the input 
        # parameters.
        steno_keys_set = set(steno_keys)
        steno_keys = list(steno_keys_set)

        # Order the steno keys so comparisons can be made.
        steno_keys.sort(key=lambda x: STENO_KEY_ORDER.get(x, -1))
         
        # Convert strokes involving the number bar to numbers.
        if '#' in steno_keys:
            numeral = False
            for i, e in enumerate(steno_keys):
                if e in STENO_KEY_NUMBERS:
                    steno_keys[i] = STENO_KEY_NUMBERS[e]
                    numeral = True
            if numeral:
                steno_keys.remove('#')
        
        if steno_keys_set & self.IMPLICIT_HYPHEN:
            self.rtfcre = ''.join(key.strip('-') for key in steno_keys)
        else:
            pre = ''.join(k.strip('-') for k in steno_keys if k[-1] == '-' or 
                          k == '#')
            post = ''.join(k.strip('-') for k in steno_keys if k[0] == '-')
            self.rtfcre = '-'.join([pre, post]) if post else pre

        self.steno_keys = steno_keys

        # Determine if this stroke is a correction stroke.
        self.is_correction = (self.rtfcre == '#U')

    def __str__(self):
        if self.is_correction:
            prefix = '*'
        else:
            prefix = ''
        return '%sStroke(%s : %s)' % (prefix, self.rtfcre, self.steno_keys)

    def __eq__(self, other):
        return (isinstance(other, Stroke)
                and self.steno_keys == other.steno_keys)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self)

