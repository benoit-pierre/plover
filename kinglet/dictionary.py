
from kinglet.theory import strokes_to_text, strokes_from_text, Stroke

# Required interface for Plover "Python" dictionary. {{{

MAXIMUM_KEY_LENGTH = 1

CAP_STATE = {
    'shift': False,
    'capslock': False,
}

def lookup_translation(key):
    assert len(key) <= MAXIMUM_KEY_LENGTH
    stroke_list = [Stroke(s) for s in key]
    return '{^%s}' % strokes_to_text(stroke_list,
                                     cap_state=CAP_STATE,
                                     use_keymap=True)

def reverse_lookup(text):
    stroke_list = strokes_from_text(text)
    if not stroke_list:
        return []
    return [tuple(str(s) for s in stroke_list)]

# }}}

# vim: foldmethod=marker
