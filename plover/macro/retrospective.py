
from plover.translation import Translation
from plover.steno import Stroke


def toggle_asterisk(translator, stroke):
    # Toggle asterisk of previous stroke
    translations = translator.get_state().translations
    if not translations:
        return
    t = translations[-1]
    translator._undo_last()
    translator._do_translations(*t.replaced)
    keys = set(t.strokes[-1].steno_keys)
    if '*' in keys:
        keys.remove('*')
    else:
        keys.add('*')
    translator._translate_stroke(Stroke(keys))
    return

def delete_space(translator, stroke):
    # Retrospective delete space
    translations = translator.get_state().translations
    if len(translations) < 2:
        return
    replaced = translations[-2:]
    if replaced[1].is_retrospective_command:
        return
    english = []
    for t in replaced:
        if t.english is not None:
            english.append(t.english)
        elif len(t.rtfcre) == 1 and t.rtfcre[0].isdigit():
            english.append('{&%s}' % t.rtfcre[0])
    if len(english) > 1:
        t = Translation([stroke], '{^~|^}'.join(english))
        t.replaced = replaced
        t.is_retrospective_command = True
        translator._translate_translation(t)
    return

def insert_space(translator, stroke):
    # Retrospective insert space
    translations = translator.get_state().translations
    if not translations:
        return
    replaced = translations[-1]
    if replaced.is_retrospective_command:
        return
    lookup_stroke = replaced.strokes[-1]
    english = [t.english or '/'.join(t.rtfcre)
               for t in replaced.replaced]
    if english:
        english.append(translator._lookup([lookup_stroke]) or lookup_stroke.rtfcre)
        t = Translation([stroke], ' '.join(english))
        t.replaced = [replaced]
        t.is_retrospective_command = True
        translator._translate_translation(t)
    return
