#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

from __future__ import print_function
from collections import namedtuple

import functools
import re

SUPPORTED_SUFFIXES = {
    'B': 'able',
    'D': 'ed',
    'G': 'ing',
    'L': 'ment',
    'P': 'ness',
    'R': 'er',
    'S': 's',
    'T': 'est',
    'V': 'ive',
    'Y': 'ly',
}

Word = namedtuple('Word', 'word compositions derivatives')

RootWord = namedtuple('RootWord', 'root flags forbidden')
AffixClass = namedtuple('AffixClass', 'prefix flag cross_product rules')
AffixRule = namedtuple('AffixRule', 'strip_chars affix affix_flags condition morpho_fields')


class AffReader(object):

    def __init__(self, filename):
        self._f = open(filename, 'rb')
        self._encoding = 'UTF-8'

    def set_encoding(self, encoding):
        self._encoding = encoding

    def next(self):
        while True:
            line = next(self._f).strip().decode(self._encoding)
            comment_start = line.find('#')
            if -1 != comment_start:
                line = line[:comment_start]
            if line:
                return line


def load_hunspell_dic(filename):
    word_list = []
    for n, line in enumerate(open(filename, 'rb')):
        if line.endswith(b'\n'):
            line = line[:-1]
        line = line.decode('UTF-8')
        if 1 == n and re.match('^[0-9]+$', line):
            # Ignore approximate word count.
            continue
        if line.startswith('/'):
            # Ignore comments.
            continue
        line = line.split('/', 1)
        if 1 == len(line):
            root, flags = line[0], ''
        else:
            root, flags = line
        if root.startswith('*'):
            forbidden = True
            root = root[1:]
        else:
            forbidden = False
        word = RootWord(root, set(flags), forbidden)
        word_list.append(word)
    return word_list

def load_hunspell_aff(filename):
    affix_classes = {}
    af = AffReader(filename)
    while True:
        try:
            line = af.next()
        except StopIteration:
            break
        line = line.split()
        cmd, args = line[0], line[1:]
        if 'SET' == cmd:
            assert 1 == len(args)
            af.set_encoding(args[0])
            continue
        if cmd in ('PFX', 'SFX'):
            assert 3 == len(args)
            prefix = 'PFX' == cmd
            flag, cross_product, count = args
            assert 1 == len(flag)
            assert cross_product in 'YN'
            cross_product = 'Y' == cross_product
            affix_class = AffixClass(prefix, flag, cross_product, [])
            for n in range(int(count)):
                rule = af.next().split()
                prefix = 'PFX' == rule[0]
                flag, strip_chars, affix, condition = rule[1:5]
                morpho_fields = rule[5:]
                assert '/' not in affix, 'not supported: affix with flags'
                assert not morpho_fields, 'not supported: morphological fields'
                assert prefix == affix_class.prefix
                assert flag == affix_class.flag
                if '0' == strip_chars:
                    strip_chars = None
                if '0' == affix:
                    affix = None
                if '.' == condition:
                    condition = None
                affix_rule = AffixRule(strip_chars, affix, set(), condition, morpho_fields)
                affix_class.rules.append(affix_rule)
            assert affix_class.flag #.encode('utf-8') not in affix_classes
            affix_classes[affix_class.flag] = affix_class
            continue
    return affix_classes


def load_hunspell_wordmap(dic_filename, aff_filename, supported_suffixes=None):
    if supported_suffixes is None:
        supported_suffixes = SUPPORTED_SUFFIXES
    word_list = load_hunspell_dic(dic_filename)
    affix_classes = load_hunspell_aff(aff_filename)
    wordmap = {}
    for root in word_list:
        prefixes = []
        suffixes = []
        for f in sorted(root.flags):
            afc = affix_classes.get(f)
            if afc is None or not afc.prefix:
                continue
            for r in afc.rules:
                assert r.condition is None, r
                assert r.strip_chars is None, r
                w = r.affix + root.root
                prefixes.append((w, r.affix, root.root, ''))
        for f in sorted(root.flags):
            afc = affix_classes.get(f)
            if afc is None or afc.prefix:
                continue
            suffix = supported_suffixes.get(f)
            if suffix is None:
                continue
            for r in afc.rules:
                if r.condition is not None and \
                   re.search(r.condition + '$', root.root) is None:
                    continue
                if r.strip_chars is not None and \
                   root.root.endswith(r.strip_chars):
                    strip = -len(r.strip_chars)
                else:
                    strip = None
                for w, prefix, base, __ in [(root.root, '', root.root, '')] + prefixes:
                    suffixes.append((w[:strip] + r.affix, prefix, base, suffix))
                break
        word = wordmap.get(root.root)
        if word is None:
            word = Word(root.root, [], [])
            wordmap[root.root] = word
        word.compositions.append(('', root.root, ''))
        derivatives = word.derivatives
        for w, prefix, base, suffix in prefixes + suffixes:
            word = wordmap.get(w)
            if word is None:
                word = Word(w, [], [])
                wordmap[w] = word
            word.compositions.append((prefix, base, suffix))
            derivatives.append(word)
    return wordmap


if __name__ == '__main__':

    import sys

    wordmap = load_hunspell_wordmap(sys.argv[1], sys.argv[2])

    for __, w in sorted(wordmap.items()):
        print(w.word)
        for prefix, base, suffix in w.compositions:
            print('=', '+'.join(p for p in (prefix, base, suffix) if p))
        if w.derivatives:
            print('->', ', '.join(d.word for d in w.derivatives))
