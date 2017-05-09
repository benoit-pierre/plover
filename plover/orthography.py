# Copyright (c) 2010-2011 Joshua Harlan Lifton.
# See LICENSE.txt for details.

"""Functions that implement some English orthographic rules."""

from plover import system
from plover.hunspell import load_hunspell_wordmap

WORDMAP = load_hunspell_wordmap('plover/assets/en_US.dic',
                                'plover/assets/en_US.aff')

def make_candidates_from_rules(word, suffix):
    for r in system.ORTHOGRAPHY_RULES:
        m = r[0].match(word + " ^ " + suffix)
        if m:
            yield m.expand(r[1])

def _add_suffix(word, suffix):

    # First, check for a valid known derivative.
    hw = WORDMAP.get(word)
    if hw is not None:
        for hw in hw.derivatives:
            for compo in hw.compositions:
                if compo[0] or compo[2] != suffix:
                    continue
                return hw.word

    candidates = []

    # Then try orthographic rules.
    for c in make_candidates_from_rules(word, suffix):
        if c in WORDMAP:
            # If it's a valid word, return it.
            return c
        candidates.append(c)

    # If there's an alias, try the rules again.
    alias = system.ORTHOGRAPHY_RULES_ALIASES.get(suffix, None)
    if alias is not None:
        for c in make_candidates_from_rules(word, alias):
            if c in WORDMAP:
                # If it's a valid word, return it.
                return c
            candidates.append(c)

    # Try a simple join if it is in the dictionary.
    simple = word + suffix
    if simple in WORDMAP:
        return simple

    # Try the first result from the orthographic rules.
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
