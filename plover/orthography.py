# Copyright (c) 2010-2011 Joshua Harlan Lifton.
# See LICENSE.txt for details.

"""Functions that implement some English orthographic rules."""

import os.path
import re
from plover.config import ASSETS_DIR

word_list_file_name = os.devnull
WORDS = dict()
try:
    with open(word_list_file_name) as f:
        pairs = [word.strip().rsplit(' ', 1) for word in f]
        pairs.sort(reverse=True, key=lambda x: int(x[1]))
        WORDS = {p[0].lower(): int(p[1]) for p in pairs}
except IOError as e:
    print e

RULES = [
]


def make_candidates_from_rules(word, suffix, check=lambda x: True):
    candidates = []
    for r in RULES:
        m = r[0].match(word + " ^ " + suffix)
        if m:   
            expanded = m.expand(r[1])
            if check(expanded):
                candidates.append(expanded)
    return candidates

def _add_suffix(word, suffix):
    in_dict_f = lambda x: x in WORDS

    candidates = []
    
    # Try a simple join if it is in the dictionary.
    simple = word + suffix
    if in_dict_f(simple):
        candidates.append(simple)
    
    # Try rules with dict lookup.
    candidates.extend(make_candidates_from_rules(word, suffix, in_dict_f))

    # For all candidates sort by prominence in dictionary and, since sort is
    # stable, also by the order added to candidates list.
    if candidates:
        candidates.sort(key=lambda x: WORDS[x])
        return candidates[0]
    
    # Try rules without dict lookup.
    candidates = make_candidates_from_rules(word, suffix)
    if candidates:
        return candidates[0]
    
    # If all else fails then just do a simple join.
    return simple

def add_suffix(word, suffix):
    """Add a suffix to a word by applying the rules above
    
    Arguments:
        
    word -- A word
    suffix -- The suffix to add
    
    """
    suffix, sep, rest = suffix.partition(' ')
    expanded = _add_suffix(word, suffix)
    return expanded + sep + rest
