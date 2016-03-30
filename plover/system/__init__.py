
from plover.registry import registry
from plover import resource
from plover import log

from io import open
import os
import re


def _load_wordlist(filename):
    if filename is None:
        return {}
    with resource.resource_stream(filename, encoding='utf-8') as fp:
        pairs = [word.strip().rsplit(' ', 1) for word in fp]
        pairs.sort(reverse=True, key=lambda x: int(x[1]))
        words = {p[0].lower(): int(p[1]) for p in pairs}
    return words

_EXPORTS = {
    'KEY_ORDER'                : lambda mod: dict((l, n) for n, l in enumerate(mod.KEYS)),
    'NUMBER_KEY'               : lambda mod: mod.NUMBER_KEY,
    'NUMBERS'                  : lambda mod: dict(mod.NUMBERS),
    'SUFFIX_KEYS'              : lambda mod: set(mod.SUFFIX_KEYS),
    'UNDO_STROKE_STENO'        : lambda mod: mod.UNDO_STROKE_STENO,
    'IMPLICIT_HYPHEN_KEYS'     : lambda mod: set(mod.IMPLICIT_HYPHEN_KEYS),
    'IMPLICIT_HYPHENS'         : lambda mod: set(l.replace('-', '')
                                                 for l in mod.IMPLICIT_HYPHEN_KEYS),
    'ORTHOGRAPHY_WORDS'        : lambda mod: _load_wordlist(mod.ORTHOGRAPHY_WORDLIST),
    'ORTHOGRAPHY_RULES'        : lambda mod: [(re.compile(pattern, re.I), replacement)
                                              for pattern, replacement in mod.ORTHOGRAPHY_RULES],
    'ORTHOGRAPHY_RULES_ALIASES': lambda mod: dict(mod.ORTHOGRAPHY_RULES_ALIASES),
    'KEYMAPS'                  : lambda mod: mod.KEYMAPS,
}

def setup(name):
    log.info('loading system: %s', name)
    systems = registry.get_systems()
    mod = systems[name].load()
    globs = globals()
    for symbol, init in _EXPORTS.items():
        globs[symbol] = init(mod)
    globs['NAME'] = name

