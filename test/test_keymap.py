
import unittest

from plover.machine.keymap import Keymap


def new_keymap():
    return Keymap(('k%u' % n for n in range(8)),
                  ('a%u' % n for n in range(4)))

BINDINGS_LIST = (
    ('k0', 'a0'),
    ('k1', 'a3'),
    ('k4', 'a1'),
    ('k5', 'a2'),
    ('k7', 'a1'),
)
BINDINGS_DICT = dict(BINDINGS_LIST)
MAPPINGS_LIST = (
    ('a0', ('k0',)),
    ('a1', ('k4', 'k7')),
    ('a2', ('k5',)),
    ('a3', ('k1',)),
)
MAPPINGS_DICT = dict(MAPPINGS_LIST)
MAPPINGS_FULL = dict(MAPPINGS_DICT)
MAPPINGS_FULL.update({'no-op': ()})


class KeymapTest(unittest.TestCase):

    def test_keymap_init(self):
        k = new_keymap()
        self.assertEqual(k.get_bindings(), {})
        self.assertEqual(k.get_mappings(), {})

    def test_keymap_set_bindings(self):
        # Set bindings from a dictionary.
        k = new_keymap()
        k.set_bindings(BINDINGS_DICT)
        self.assertEqual(k.get_bindings(), BINDINGS_DICT)
        self.assertEqual(k.get_mappings(), MAPPINGS_FULL)
        # Set bindings from a list of tuples.
        k = new_keymap()
        k.set_bindings(BINDINGS_LIST)
        self.assertEqual(k.get_bindings(), BINDINGS_DICT)
        self.assertEqual(k.get_mappings(), MAPPINGS_FULL)

    def test_keymap_set_mappings(self):
        # Set mappings from a dictionary.
        k = new_keymap()
        k.set_mappings(MAPPINGS_DICT)
        self.assertEqual(k.get_bindings(), BINDINGS_DICT)
        self.assertEqual(k.get_mappings(), MAPPINGS_FULL)
        # Set mappings from a list of tuples.
        k = new_keymap()
        k.set_mappings(MAPPINGS_LIST)
        self.assertEqual(k.get_bindings(), BINDINGS_DICT)
        self.assertEqual(k.get_mappings(), MAPPINGS_FULL)

    def test_keymap_setitem(self):
        bindings = dict(BINDINGS_DICT)
        mappings = dict(MAPPINGS_FULL)
        k = new_keymap()
        k.set_mappings(mappings)
        # Bind to one key.
        k['a3'] = 'k6'
        del bindings['k1']
        bindings['k6'] = 'a3'
        mappings['a3'] = ('k6',)
        self.assertEqual(k.get_bindings(), bindings)
        self.assertEqual(k.get_mappings(), mappings)
        # Bind to multiple keys.
        k['a3'] = ('k6', 'k1')
        bindings['k1'] = 'a3'
        bindings['k6'] = 'a3'
        mappings['a3'] = ('k1', 'k6',)
        self.assertEqual(k.get_bindings(), bindings)
        self.assertEqual(k.get_mappings(), mappings)
        # If a key is already mapped (k0), don't override it.
        k['a3'] = ('k0', 'k2')
        del bindings['k1']
        del bindings['k6']
        bindings['k2'] = 'a3'
        mappings['a3'] = ('k2',)
        self.assertEqual(k.get_bindings(), bindings)
        self.assertEqual(k.get_mappings(), mappings)
        # Assert on invalid action.
        with self.assertRaises(AssertionError):
            k['a9'] = 'k0'
