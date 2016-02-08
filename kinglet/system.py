# vim: set fileencoding=utf-8 :

# 1QA2WS3ED4RF5TG_XCVBNM,6YH7UJ8IK9OL0P;
#
# 123 45 67 890
# QWE RT YU IOP
# ASD FG HK KL;
#    XCVBNM,
#       _
#
KEYS = (
    # Left third and little fingers.
    '1', 'Q', 'A',
    '2', 'W', 'S',
    '3', 'E', 'D',
    # Left fore and middle fingers.
    '4', 'R', 'F',
    '5', 'T', 'G',
    # Thumbs.
    '_', # Space
    'X', 'C', 'V', 'B', 'N', 'M', ',',
    # Right fore and middle fingers.
    '6', 'Y', 'H',
    '7', 'U', 'J',
    # Right third and little fingers.
    '8', 'I', 'K',
    '9', 'O', 'L',
    '0', 'P', ';',
)

IMPLICIT_HYPHEN_KEYS = KEYS

SUFFIX_KEYS = ()

NUMBER_KEY = ''

NUMBERS = {}

UNDO_STROKE_STENO = ''

ORTHOGRAPHY_RULES = []

ORTHOGRAPHY_RULES_ALIASES = {}

ORTHOGRAPHY_WORDLIST = None

KEYBOARD_KEYMAP = (
    ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('0', '0'),
    ('Q', 'q'), ('W', 'w'), ('E', 'e'), ('R', 'r'), ('T', 't'), ('Y', 'y'), ('U', 'u'), ('I', 'i'), ('O', 'o'), ('P', 'p'),
    ('A', 'a'), ('S', 's'), ('D', 'd'), ('F', 'f'), ('G', 'g'), ('H', 'h'), ('J', 'j'), ('K', 'k'), ('L', 'l'), (';', ';'),
    ('X', 'x'), ('C', 'c'), ('V', 'v'), ('B', 'b'), ('N', 'n'), ('M', 'm'), (',', ','),
    ('_', ('space')),
    ('no-op', ()),
    ('arpeggiate', ()),
)

