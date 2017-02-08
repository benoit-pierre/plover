# Copyright (c) 2010-2011 Joshua Harlan Lifton.
# See LICENSE.txt for details.

# TODO: unit test this file

"""Generic stenography data models.

This module contains the following class:

Stroke -- A data model class that encapsulates a sequence of steno keys.

"""

from plover import system


STROKE_DELIMITER = '/'

def normalize_steno(strokes_string):
    """Convert steno strings to one common form."""
    return tuple(system.Stroke.from_steno(stroke) for stroke
                 in strokes_string.split(STROKE_DELIMITER))

def sort_steno_keys(steno_keys):
    return sorted(steno_keys, key=lambda x: system.KEY_ORDER.get(x, -1))

def sort_steno_strokes(strokes_list):
    '''Return suggestions, sorted by fewest strokes, then fewest keys.'''
    return sorted(strokes_list, key=lambda x: (len(x), sum(map(len, x))))
