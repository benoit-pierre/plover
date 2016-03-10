# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

"""Unit tests for steno.py."""

from plover.steno import normalize_steno, Stroke

from . import PloverTest


class StenoTestCase(PloverTest):
    def test_normalize_steno(self):
        cases = (
        
        # TODO: More cases
        ('S', 'S'),
        ('S-', 'S'),
        ('-S', '-S'),
        ('ES', 'ES'),
        ('-ES', 'ES'),
        ('TW-EPBL', 'TWEPBL'),
        ('TWEPBL', 'TWEPBL'),
        ('19', '1-9'),
        ('14', '14'),
        ('146', '14-6'),
        ('67', '-67'),
        ('6', '-6'),
        ('9', '-9'),
        ('5', '5'),
        ('0', '0'),
        ('456', '456'),
        ('46', '4-6'),
        ('4*6', '4*6'),
        ('456', '456'),
        ('S46', 'S4-6'),
        )
        
        for arg, expected in cases:
            self.assertEqual('/'.join(normalize_steno(arg)), expected)
            
    def test_steno(self):
        self.assertEqual(Stroke(['S-']).rtfcre, 'S')
        self.assertEqual(Stroke(['S-', 'T-']).rtfcre, 'ST')
        self.assertEqual(Stroke(['T-', 'S-']).rtfcre, 'ST')
        self.assertEqual(Stroke(['-P', '-P']).rtfcre, '-P')
        self.assertEqual(Stroke(['-P', 'X-']).rtfcre, 'X-P')
        self.assertEqual(Stroke(['#', 'S-', '-T']).rtfcre, '1-9')
