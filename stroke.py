#!/usr/bin/env python2

from collections import namedtuple


KEYS = None
KEYS_MASK = None
KEYS_LETTERS = None
KEYS_IMPLICIT_HYPHEN = None
KEY_TO_MASK = None
KEY_FROM_MASK = None


def msb(x):
    x |= (x >> 1)
    x |= (x >> 2)
    x |= (x >> 4)
    x |= (x >> 8)
    x |= (x >> 16)
    x |= (x >> 32)
    return (x & ~(x >> 1))

def lsb(x):
    return (x & -x)

def popcount(x):
    # 0x5555555555555555: 0101...
    # 0x3333333333333333: 00110011..
    # 0x0f0f0f0f0f0f0f0f:  4 zeros,  4 ones ...
    # Put count of each 2 bits into those 2 bits.
    x -= (x >> 1) & 0x5555555555555555
    # Put count of each 4 bits into those 4 bits.
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
    # Put count of each 8 bits into those 8 bits.
    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f
    # Put count of each 16 bits into their lowest 8 bits.
    x += x >>  8
    # Put count of each 32 bits into their lowest 8 bits.
    x += x >> 16
    # Put count of each 64 bits into their lowest 8 bits.
    x += x >> 32
    return x & 0x7f


integer_type = long

class Stroke(integer_type):

    @classmethod
    def from_steno(cls, steno):
        n = 0
        keys = []
        for letter in steno:
            if '-' == letter:
                if n >= KEY_FIRST_RIGHT_INDEX:
                    raise ValueError
                n = KEY_FIRST_RIGHT_INDEX
                continue
            n = KEYS_LETTERS.find(letter, n)
            if -1 == n:
                raise ValueError
            keys.append(KEYS[n])
        return cls.from_keys(keys)

    @classmethod
    def from_keys(cls, keys):
        value = reduce(lambda x, y: x | y, [KEY_TO_MASK[k] for k in keys])
        return cls.from_integer(value)

    @classmethod
    def from_integer(cls, value):
        assert 0 == (value & ~KEYS_MASK)
        return integer_type.__new__(cls, value)

    def __new__(cls, value=None):
        if value is None:
            return cls.from_integer(0)
        if isinstance(value, Stroke):
            return value
        if isinstance(value, (int, long)):
            return cls.from_integer(value)
        if isinstance(value, str):
            return cls.from_steno(value)
        return cls.from_keys(value)

    def __or__(self, other):
        return self.from_integer(integer_type(self) | integer_type(Stroke(other)))

    def __and__(self, other):
        return self.from_integer(integer_type(self) & integer_type(Stroke(other)))

    def __add__(self, other):
        return self | other

    def __sub__(self, other):
        return self.from_integer(integer_type(self) & ~integer_type(Stroke(other)))

    def __len__(self):
        return popcount(integer_type(self))

    def __iter__(self):
        v = integer_type(self)
        while v:
            m = lsb(v)
            yield KEY_FROM_MASK[m]
            v &= ~m

    def __repr__(self):
        left = ''
        middle = ''
        right = ''
        for k in self:
            l = k.replace('-', '')
            if k in KEYS_IMPLICIT_HYPHEN:
                middle += l
            elif '-' == k[0]:
                right += l
            else:
                left += l
        s = left
        if not middle and right:
            s += '-'
        else:
            s += middle
        s += right
        return s

    def __str__(self):
        return self.__repr__()

    def first(self):
        return KEY_FROM_MASK[lsb(integer_type(self))]

    def last(self):
        return KEY_FROM_MASK[msb(integer_type(self))]

    def keys(self):
        return [k for k in self]

    def is_prefix(self, other):
        return msb(integer_type(self)) < lsb(integer_type(Stroke(other)))

    def is_suffix(self, other):
        return lsb(integer_type(self)) > msb(integer_type(Stroke(other)))

    @staticmethod
    def xrange(start, stop=None):
        start = integer_type(Stroke(start))
        if stop is None:
            start, stop = 0, start
        if -1 == stop:
            stop = (1 << len(KEYS)) - 1
        stop = integer_type(Stroke(stop))
        assert start <= stop
        for v in range(start, stop):
            yield Stroke(v)

    def xsuffixes(self, stop=None):
        """Generate all stroke prefixed by <self>
        (not included), until <stop> (included).
        """
        start_bit = msb(integer_type(self)) << 1
        end_bit = 1 << (1 + len(KEYS))
        assert start_bit <= end_bit
        count = popcount((end_bit - 1) & ~((start_bit << 1) - 1))
        prefix = integer_type(self)
        shift = popcount(start_bit - 1)
        if stop is None:
            stop = end_bit - 1
        stop = integer_type(Stroke(stop))
        for n in range(1, (1 << count)):
            v = n << shift
            assert 0 == (prefix & v)
            v |= prefix
            yield Stroke(v)
            if v == stop:
                break


def setup(keys, implicit_hyphen_keys=None):
    global KEYS, KEYS_MASK, KEYS_IMPLICIT_HYPHEN, KEYS_LETTERS
    global KEY_TO_MASK, KEY_FROM_MASK
    global KEY_FIRST_RIGHT_INDEX
    assert len(keys) <= 64
    KEYS = tuple(keys)
    KEYS_MASK = (1 << len(KEYS)) - 1
    KEY_TO_MASK = dict([(k, 1 << n) for n, k in enumerate(KEYS)])
    KEY_FROM_MASK = dict(zip(KEY_TO_MASK.values(), KEY_TO_MASK.keys()))
    # Find left and right letters.
    KEY_FIRST_RIGHT_INDEX = None
    KEYS_LETTERS = ''
    letters_left = {}
    letters_right = {}
    for n, k in enumerate(keys):
        assert len(k) <= 2
        if 1 == len(k):
            assert '-' != k
            l = k
            is_left = False
            is_right = False
        elif 2 == len(k):
            is_left = '-' == k[1]
            is_right = '-' == k[0]
            assert is_left != is_right
            l = k.replace('-', '')
        KEYS_LETTERS += l
        if KEY_FIRST_RIGHT_INDEX is None:
            if not is_right:
                assert k not in letters_left
                letters_left[l] = k
                continue
            KEY_FIRST_RIGHT_INDEX = n
        # Invalid: ['-R', '-L']
        assert not is_left
        # Invalid: ['-R', '-R']
        assert k not in letters_right
        # Invalid: ['#', '-R', '#']
        assert is_right or l not in letters_left
        letters_right[l] = k
    # Find implicit hyphen keys/letters.
    implicit_hyphen_letters = {}
    for k in reversed(keys[:KEY_FIRST_RIGHT_INDEX]):
        l = k.replace('-', '')
        if l in letters_right:
            break
        implicit_hyphen_letters[l] = k
    for k in keys[KEY_FIRST_RIGHT_INDEX:]:
        l = k.replace('-', '')
        if l in letters_left:
            break
        implicit_hyphen_letters[l] = k
    if implicit_hyphen_keys is not None:
        # Hyphen keys must be a continous block.
        hyphens_str = lambda l: ''.join(sorted(l, key=KEYS.index))
        all_hyphens = hyphens_str(implicit_hyphen_letters.values())
        hyphens = hyphens_str(implicit_hyphen_keys)
        assert hyphens in all_hyphens
        KEYS_IMPLICIT_HYPHEN = set(implicit_hyphen_keys)
    else:
        KEYS_IMPLICIT_HYPHEN = set(implicit_hyphen_letters.values())


# Prevent use of 'from stroke import *'.
__all__ = ()


if __name__ == '__main__':

    setup((
        '#',
        'S-', 'T-', 'K-', 'P-', 'W-', 'H-', 'R-',
        'A-', 'O-',
        '*',
        '-E', '-U',
        '-F', '-R', '-P', '-B', '-L', '-G', '-T', '-S', '-D', '-Z',
    ),
        ('A-', 'O-', '*', '-E', '-U')
    )

    s1 = Stroke(23)
    print s1
    s2 = Stroke(56)
    print s2
    s3 = Stroke(('-F', 'S-', '-S', 'A-', '*'))
    print s3
    s4 = Stroke('SAF')
    print s4
    s5 = Stroke('R-')
    print s5
    s6 = Stroke('-L')
    print s6
    s7 = Stroke('L-')
    print s7

