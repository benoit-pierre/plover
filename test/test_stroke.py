import operator

import pytest

from plover.stroke import stroke_class

from . import parametrize


@pytest.fixture
def english_stroke_class():
    return stroke_class(
        '''
        #
        S- T- K- P- W- H- R-
        A- O-
        *
        -E -U
        -F -R -P -B -L -G -T -S -D -Z
        '''.split(),
        'A- O- * -E -U'.split(),
        '#', {
            'S-': '1-',
            'T-': '2-',
            'P-': '3-',
            'H-': '4-',
            'A-': '5-',
            'O-': '0-',
            '-F': '-6',
            '-P': '-7',
            '-L': '-8',
            '-T': '-9',
        }
    )

def test_setup_explicit():
    keys = '''
        #
        S- T- K- P- W- H- R-
        A- O-
        *
        -E -U
        -F -R -P -B -L -G -T -S -D -Z
    '''.split()
    implicit_hyphen_keys = 'A- O- * -E -U'.split()
    cls = stroke_class(keys, implicit_hyphen_keys)
    assert cls.KEYS == tuple(keys)
    assert cls.KEYS_IMPLICIT_HYPHEN == set(implicit_hyphen_keys)

def test_setup_explicit_with_numbers():
    keys = '''
        #
        S- T- K- P- W- H- R-
        A- O-
        *
        -E -U
        -F -R -P -B -L -G -T -S -D -Z
    '''.split()
    implicit_hyphen_keys = 'A- O- 5- 0- -E -U *'.split()
    number_key = '#'
    numbers = {
        'S-': '1-',
        'T-': '2-',
        'P-': '3-',
        'H-': '4-',
        'A-': '5-',
        'O-': '0-',
        '-F': '-6',
        '-P': '-7',
        '-L': '-8',
        '-T': '-9',
    }
    cls = stroke_class(keys, implicit_hyphen_keys, number_key, numbers)
    assert cls.KEYS == tuple(keys)
    assert cls.KEYS_IMPLICIT_HYPHEN == set(implicit_hyphen_keys)

def test_setup_implicit_hyphens():
    keys = '''
        #
        S- T- K- P- W- H- R-
        A- O-
        *
        -E -U
        -F -R -P -B -L -G -T -S -D -Z
    '''.split()
    cls = stroke_class(keys)
    assert cls.KEYS == tuple(keys)
    assert cls.KEYS_IMPLICIT_HYPHEN == {'A-', 'O-', '*', '-E', '-U', '-F'}

def test_setup_numbers():
    keys = '''
        #
        S- T- K- P- W- H- R-
        A- O-
        *
        -E -U
        -F -R -P -B -L -G -T -S -D -Z
    '''.split()
    implicit_hyphen_keys = 'A- O- * -E -U'.split()
    number_key = '#'
    numbers = {
        'S-': '1-',
        'T-': '2-',
        'P-': '3-',
        'H-': '4-',
        'A-': '5-',
        'O-': '0-',
        '-F': '-6',
        '-P': '-7',
        '-L': '-8',
        '-T': '-9',
    }
    cls = stroke_class(keys, implicit_hyphen_keys, number_key, numbers)
    assert cls.KEYS == tuple(keys)
    assert cls.KEYS_IMPLICIT_HYPHEN == set(implicit_hyphen_keys)
    assert cls.NUMBER_KEY == number_key

NEW_TESTS = (
    lambda: (
        '#',
        '#',
        '#',
        0b00000000000000000000001,
        False,
    ),
    lambda: (
        'T- -B -P S-',
        'S- T- -P -B',
        'ST-PB',
        0b00000011000000000000110,
        False,
    ),
    lambda: (
        'O- -E A-',
        'A- O- -E',
        'AOE',
        0b00000000000101100000000,
        False,
    ),
    lambda: (
        '-Z *',
        '* -Z',
        '*Z',
        0b10000000000010000000000,
        False,
    ),
    lambda: (
        '-R R-',
        'R- -R',
        'R-R',
        0b00000000100000010000000,
        False,
    ),
    lambda: (
        'S- -P O- # T-',
        '# S- T- O- -P',
        '120-7',
        0b00000001000001000000111,
        True,
    ),
    lambda: (
        '1- 2- 0- -7',
        '# S- T- O- -P',
        '120-7',
        0b00000001000001000000111,
        True,
    ),
    lambda: (
        '-L -F',
        '-F -L',
        '-FL',
        0b00000100010000000000000,
        False,
    ),
)

@parametrize(NEW_TESTS)
def test_new(english_stroke_class, in_keys, keys, rtfcre, value, isnumber):
    in_keys = in_keys.split()
    keys = keys.split()
    for init_arg in (in_keys, rtfcre, value):
        s = english_stroke_class(init_arg)
        msg = '%s [%u] %r' % (s, s, s.keys())
        assert s == value, msg
        assert s.keys() == keys, msg
        assert s.isnumber() == isnumber, msg
        assert str(s) == rtfcre, msg

HASH_TESTS = (
    lambda: ('#',    0b00000000000000000000001),
    lambda: ('ST',   0b00000000000000000000110),
    lambda: ('STK',  0b00000000000000000001110),
    lambda: ('*',    0b00000000000010000000000),
    lambda: ('-PB',  0b00000011000000000000000),
    lambda: ('AOE',  0b00000000000101100000000),
    lambda: ('R-R',  0b00000000100000010000000),
    lambda: ('R-F',  0b00000000010000010000000),
    lambda: ('APBD', 0b01000011000000100000000),
)

@parametrize(HASH_TESTS)
def test_hash(english_stroke_class, steno, hash_value):
    assert hash(english_stroke_class(steno)) == hash_value

CMP_TESTS = (
    lambda: ('#', '<', 'ST'),
    lambda: ('T', '>', 'ST'),
    lambda: ('PH', '>', 'TH'),
    lambda: ('SH', '<', 'STH'),
    lambda: ('ST', '<=', 'STK'),
    lambda: ('STK', '<=', 'STK'),
    lambda: ('STK', '==', 'STK'),
    lambda: ('*', '!=', 'R-R'),
    lambda: ('-PB', '>', 'AOE'),
    lambda: ('R-R', '>=', 'R-F'),
    lambda: ('APBD', '>=', 'APBD'),
)

@parametrize(CMP_TESTS)
def test_cmp(english_stroke_class, steno, op, other_steno):
    op = {
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        '>=': operator.ge,
        '>': operator.gt,
    }[op]
    assert op(english_stroke_class(steno), other_steno)

def test_sort(english_stroke_class):
    unsorted_strokes = [
        english_stroke_class(s)
        for s in '''
        AOE
        ST-PB
        *Z
        #
        R-R
        '''.split()
    ]
    sorted_strokes = [
        english_stroke_class(s)
        for s in '''
        #
        ST-PB
        R-R
        AOE
        *Z
        '''.split()
    ]
    assert list(sorted(unsorted_strokes)) == sorted_strokes

def test_xrange(english_stroke_class):
    expected = [
        english_stroke_class(s)
        for s in '''
        ST
        #ST
        K
        #K
        SK
        #SK
        TK
        #TK
        STK
        #STK
        P
        #P
        SP
        #SP
        '''.split()
    ]
    assert list(english_stroke_class.xrange('ST', 'TP')) == expected

def test_xsuffixes(english_stroke_class):
    expected = [
        english_stroke_class(s)
        for s in '''
        -TS
        -TD
        -TSD
        -TZ
        -TSZ
        -TDZ
        -TSDZ
        '''.split()
    ]
    assert list(english_stroke_class('-T').xsuffixes()) == expected
