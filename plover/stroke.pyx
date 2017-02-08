from libc.stdint cimport int64_t


cdef inline int64_t _msb(int64_t x):
    x |= (x >> 1)
    x |= (x >> 2)
    x |= (x >> 4)
    x |= (x >> 8)
    x |= (x >> 16)
    x |= (x >> 32)
    return (x + 1) >> 1

cdef inline int64_t _lsb(int64_t x):
    return x & -x

cdef inline int64_t _popcount(int64_t x):
    cdef:
        int64_t m1 = 0x5555555555555555 # 0101...
        int64_t m2 = 0x3333333333333333 # 00110011...
        int64_t m3 = 0x0f0f0f0f0f0f0f0f # 000011110001111...
        int64_t m4 = 0x7f
    # Put count of each 2 bits into those 2 bits.
    x -= (x >> 1) & m1
    # Put count of each 4 bits into those 4 bits.
    x = (x & m2) + ((x >> 2) & m2)
    # Put count of each 8 bits into those 8 bits.
    x = (x + (x >> 4)) & m3
    # Put count of each 16 bits into their lowest 8 bits.
    x += x >>  8
    # Put count of each 32 bits into their lowest 8 bits.
    x += x >> 16
    # Put count of each 64 bits into their lowest 8 bits.
    x += x >> 32
    return x & m4


cdef inline int64_t _cmp(int64_t si1, int64_t si2):
    cdef:
        int64_t m, lsb1, lsb2
    m = si1 ^ si2
    si1 = (si1 & m) or si1
    lsb1 = si1 & -si1
    si2 = (si2 & m) or si2
    lsb2 = si2 & -si2
    return lsb1 - lsb2


def stroke_class(keys, implicit_hyphen_keys=None,
                 number_key=None, numbers={}):

    assert len(keys) <= 63

    KEYS = tuple(keys)
    KEYS_MASK = (1 << len(KEYS)) - 1
    KEY_TO_MASK = dict([(k, 1 << n) for n, k in enumerate(KEYS)])
    KEY_FROM_MASK = dict(zip(KEY_TO_MASK.values(), KEY_TO_MASK.keys()))
    # Find left and right letters.
    KEYS_FIRST_RIGHT_INDEX = None
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
        if KEYS_FIRST_RIGHT_INDEX is None:
            if not is_right:
                assert k not in letters_left
                letters_left[l] = k
                continue
            KEYS_FIRST_RIGHT_INDEX = n
        # Invalid: ['-R', '-L']
        assert not is_left
        # Invalid: ['-R', '-R']
        assert k not in letters_right
        # Invalid: ['#', '-R', '#']
        assert is_right or l not in letters_left
        letters_right[l] = k
    # Find implicit hyphen keys/letters.
    implicit_hyphen_letters = {}
    for k in reversed(keys[:KEYS_FIRST_RIGHT_INDEX]):
        l = k.replace('-', '')
        if l in letters_right:
            break
        implicit_hyphen_letters[l] = k
    for k in keys[KEYS_FIRST_RIGHT_INDEX:]:
        l = k.replace('-', '')
        if l in letters_left:
            break
        implicit_hyphen_letters[l] = k
    if implicit_hyphen_keys is not None:
        # Hyphen keys must be a continous block.
        hyphens_str = lambda l: ''.join(sorted(l, key=KEYS.index))
        all_hyphens = hyphens_str(implicit_hyphen_letters.values())
        hyphens = hyphens_str(k for k in implicit_hyphen_keys
                              if k not in numbers.values())
        assert hyphens in all_hyphens
        KEYS_IMPLICIT_HYPHEN = set(implicit_hyphen_keys)
    else:
        KEYS_IMPLICIT_HYPHEN = set(implicit_hyphen_letters.values())
    NUMBERS_MASK = 0
    NUMBER_KEY = number_key
    NUMBER_KEY_MASK = 0
    KEY_TO_NUMBER = {}
    if number_key is not None:
        KEY_TO_NUMBER = dict(numbers)
        NUMBER_KEY = number_key
        NUMBER_KEY_MASK = KEY_TO_MASK[number_key]
        NUMBERS_MASK |= NUMBER_KEY_MASK
        for key, num in KEY_TO_NUMBER.items():
            KEY_TO_MASK[num] = NUMBER_KEY_MASK | KEY_TO_MASK[key]
            NUMBERS_MASK |= KEY_TO_MASK[key]
    LETTER_TO_INDEX_AND_MASK = {}
    for n, k in enumerate(KEYS):
        LETTER_TO_INDEX_AND_MASK.setdefault(k.strip('-'), []).extend((n, 1 << n))
        num = KEY_TO_NUMBER.get(k)
        if num is not None:
            LETTER_TO_INDEX_AND_MASK[num.strip('-')] = [n, (1 << n) | NUMBER_KEY_MASK]
    LETTER_TO_INDEX_AND_MASK = {
        l: tuple(indexes) if len(indexes) == 4 else tuple(indexes) + (-1, 0)
        for l, indexes in LETTER_TO_INDEX_AND_MASK.items()
    }
    if KEYS_FIRST_RIGHT_INDEX is not None:
        LETTER_TO_INDEX_AND_MASK['-'] = (KEYS_FIRST_RIGHT_INDEX - 1, 0, -1, 0)

    def __new__(cls, value=0):
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls.from_steno(value)
        if isinstance(value, int):
            return cls.from_integer(value)
        return cls.from_keys(value)

    @classmethod
    def from_integer(cls, value):
        assert value == (KEYS_MASK & value)
        return int.__new__(cls, value)

    @classmethod
    def from_steno(cls, steno):
        cdef:
            int64_t v, m, first_m, last_m
            int n, first_n, last_n
            Py_UNICODE letter
        n = 0
        v = 0
        for letter in steno:
            first_n, first_m, last_n, last_m = LETTER_TO_INDEX_AND_MASK.get(letter, (-1, 0, -1, 0))
            if n <= first_n:
                n, m = first_n, first_m
            elif n <= last_n:
                n, m = last_n, last_m
            else:
                raise ValueError('invalid letter %r in %r' % (letter, steno))
            v |= m
            n += 1
        return int.__new__(cls, v)

    @classmethod
    def from_keys(cls, keys):
        cdef:
            int64_t value = 0
            int64_t m
            unicode k
        for k in keys:
            m = KEY_TO_MASK[k]
            value |= m
        return int.__new__(cls, value)

    def __lt__(self, other):
        return _cmp(self, self.__class__(other)) < 0

    def __le__(self, other):
        return _cmp(self, self.__class__(other)) <= 0

    def __eq__(self, other):
        return long(self) == long(self.__class__(other))

    def __ne__(self, other):
        return long(self) != long(self.__class__(other))

    def __gt__(self, other):
        return _cmp(self, self.__class__(other)) > 0

    def __ge__(self, other):
        return _cmp(self, self.__class__(other)) >= 0

    def __contains__(self, other):
        cdef:
            int64_t v = self, ov = self.__class__(other)
        return v & ov == ov

    def __invert__(self):
        cdef:
            int64_t v = self
        return self.from_integer(~v & KEYS_MASK)

    def __or__(self, other):
        cdef:
            int64_t v = self, ov = self.__class__(other)
        return self.from_integer(v | ov)

    def __and__(self, other):
        cdef:
            int64_t v = self, ov = self.__class__(other)
        return self.from_integer(v & ov)

    def __add__(self, other):
        return self | other

    def __sub__(self, other):
        cdef:
            int64_t v = self, ov = self.__class__(other)
        return self.from_integer(v & ~ov)

    def __len__(self):
        cdef:
            int64_t v = self
        return _popcount(v)

    def __iter__(self):
        cdef:
            int64_t v = self, lsb
        while v:
            lsb = _lsb(v)
            yield KEY_FROM_MASK[lsb]
            v &= ~lsb

    def __str__(self):
        cdef:
            unicode left, middle, right, k, s
        isnumber = self.isnumber()
        left = ''
        middle = ''
        right = ''
        for k in self:
            if isnumber:
                if k == NUMBER_KEY:
                    continue
                k = KEY_TO_NUMBER[k]
            if k in KEYS_IMPLICIT_HYPHEN:
                middle += k
            elif '-' == k[0]:
                right += k
            else:
                left += k
        s = left.replace('-', '')
        if not middle and right:
            s += '-'
        else:
            s += middle.replace('-', '')
        s += right.replace('-', '')
        return s

    def __repr__(self):
        return 'Stroke(%s : %r)' % (str(self), self.keys())

    def isnumber(self):
        cdef:
            int64_t v = self
        return (
            v == (v & NUMBERS_MASK)
            and v & NUMBER_KEY_MASK
            and v != NUMBER_KEY_MASK
        )

    @property
    def rtfcre(self):
        return str(self)

    def first(self):
        cdef:
            int64_t v = self
        return KEY_FROM_MASK[_lsb(v)]

    def last(self):
        cdef:
            int64_t v = self
        return KEY_FROM_MASK[_msb(v)]

    def keys(self):
        return list(self)

    def is_prefix(self, other):
        cdef:
            int64_t v = self, ov = self.__class__(other)
        return _msb(v) < _lsb(ov)

    def is_suffix(self, other):
        cdef:
            int64_t v = self, ov = self.__class__(other)
        return _lsb(v) > _msb(ov)

    def startswith(self, other):
        cdef:
            int64_t v = self, ov = self.__class__(other)
        return v & ((_msb(ov) << 1) - 1) == ov

    @classmethod
    def xrange(cls, start, stop=None):
        start = int(cls(start))
        if stop is None:
            start, stop = 0, start
        if -1 == stop:
            stop = (1 << len(KEYS)) - 1
        stop = int(cls(stop))
        assert start <= stop
        for v in range(start, stop):
            yield cls(v)

    def xsuffixes(self, stop=None):
        """Generate all stroke prefixed by <self>
        (not included), until <stop> (included).
        """
        cdef:
            int64_t start_bit, end_bit, count, prefix, shift, s, n, v
        start_bit = _msb(int(self)) << 1
        end_bit = 1 << len(KEYS)
        assert start_bit <= end_bit
        count = _popcount((end_bit - 1) & ~(start_bit - 1))
        prefix = self
        shift = _popcount(start_bit - 1)
        if stop is None:
            s = end_bit - 1
        else:
            s = self.__class__(stop)
        for n in range(1, (1 << count)):
            v = n << shift
            assert 0 == (prefix & v)
            v |= prefix
            yield self.__class__(v)
            if v == s:
                break

    class_namespace = {
        '__new__': __new__,

        'from_integer': from_integer,
        'from_keys': from_keys,
        'from_steno': from_steno,

        '__hash__': int.__hash__,
        '__lt__': __lt__,
        '__le__': __le__,
        '__eq__': __eq__,
        '__ne__': __ne__,
        '__gt__': __gt__,
        '__ge__': __ge__,
        '__contains__': __contains__,
        '__invert__': __invert__,
        '__or__': __or__,
        '__and__': __and__,
        '__add__': __add__,
        '__sub__': __sub__,
        '__len__': __len__,
        '__iter__': __iter__,
        '__str__': __str__,
        '__repr__': __repr__,

        'isnumber': isnumber,
        'rtfcre': rtfcre,
        'first': first,
        'last': last,
        'keys': keys,
        'is_prefix': is_prefix,
        'is_suffix': is_suffix,
        'startswith': startswith,
        'xrange': xrange,
        'xsuffixes': xsuffixes,
    }

    cls = type('Stroke', (int,), class_namespace)

    cls.KEYS = KEYS
    cls.KEYS_MASK = KEYS_MASK
    cls.KEYS_IMPLICIT_HYPHEN = KEYS_IMPLICIT_HYPHEN
    cls.KEY_TO_MASK = KEY_TO_MASK
    cls.KEY_FROM_MASK = KEY_FROM_MASK
    cls.KEY_TO_NUMBER = KEY_TO_NUMBER
    cls.NUMBERS_MASK = NUMBERS_MASK
    cls.NUMBER_KEY = NUMBER_KEY

    return cls


# Prevent use of 'from stroke import *'.
__all__ = ()
