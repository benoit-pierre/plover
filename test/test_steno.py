# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

"""Unit tests for steno.py."""

from plover.steno import normalize_steno

from . import parametrize


NORMALIZE_TESTS = (
    # TODO: More cases
    lambda: ('S', 'S'),
    lambda: ('S-', 'S'),
    lambda: ('-S', '-S'),
    lambda: ('ES', 'ES'),
    lambda: ('-ES', 'ES'),
    lambda: ('TW-EPBL', 'TWEPBL'),
    lambda: ('TWEPBL', 'TWEPBL'),
    lambda: ('19', '1-9'),
    lambda: ('14', '14'),
    lambda: ('146', '14-6'),
    lambda: ('67', '-67'),
    lambda: ('6', '-6'),
    lambda: ('9', '-9'),
    lambda: ('5', '5'),
    lambda: ('0', '0'),
    lambda: ('456', '456'),
    lambda: ('46', '4-6'),
    lambda: ('4*6', '#H*F'),
    lambda: ('456', '456'),
    lambda: ('S46', '14-6'),
    # Number key.
    lambda: ('#S', '1'),
    lambda: ('#A', '5'),
    lambda: ('#0', '0'),
    lambda: ('#6', '-6'),
    # Implicit hyphens.
    lambda: ('SA-', 'SA'),
    lambda: ('SA-R', 'SAR'),
    lambda: ('-E', 'E'),
    # lambda: ('-O', 'O'),
    # lambda: ('S*-R', 'S*R'),
    # lambda: ('S-*R', 'S*R'),
)

@parametrize(NORMALIZE_TESTS)
def test_normalize_steno(steno, strokes):
    result = '/'.join(map(str, normalize_steno(steno)))
    msg = 'normalize_steno(%r)=%r != %r' % (
        steno, result, strokes,
    )
    assert result == strokes, msg


STROKE_TESTS = (
    lambda: (['S-'], ['S-'], 'S'),
    lambda: (['S-', 'T-'], ['S-', 'T-'], 'ST'),
    lambda: (['T-', 'S-'], ['S-', 'T-'], 'ST'),
    lambda: (['-P', '-P'], ['-P'], '-P'),
    lambda: (['-P', 'X-'], ['X-', '-P'], 'X-P'),
    lambda: (['#', 'S-', '-T'], ['1-', '-9'], '1-9'),
)
