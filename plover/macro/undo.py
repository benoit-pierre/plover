
import sys

from plover.translation import Translation


if sys.platform.startswith('darwin'):
    BACK_STRING = '{#Alt_L(BackSpace)}{^}'
else:
    BACK_STRING = '{#Control_L(BackSpace)}{^}'


def undo(translator, stroke):
    for t in reversed(translator.get_state().translations):
        translator._undo_last()
        if t.has_undo():
            translator._do_translations(*t.replaced)
            return
    # There is no more buffer to delete from -- remove undo and add a
    # stroke that removes last word on the user's OS, but don't add it
    # to the state history.
    translator._output([], [Translation([stroke], BACK_STRING)], None)
