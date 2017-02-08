
from plover.translation import Translation
from plover import system


def toggle_asterisk(translator, stroke, cmdline):
    # Toggle asterisk of previous stroke
    translations = translator.get_state().translations
    if not translations:
        return
    t = translations[-1]
    translator.untranslate_translation(t)
    toggled_stroke = t.strokes[-1]
    if '*' in toggled_stroke:
        toggled_stroke -= '*'
    else:
        toggled_stroke += '*'
    translator.translate_stroke(toggled_stroke)

def delete_space(translator, stroke, cmdline):
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
        translator.translate_translation(t)

def insert_space(translator, stroke, cmdline):
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
        english.append(
            translator.lookup([lookup_stroke], system.SUFFIX_KEYS)
            or lookup_stroke.rtfcre
        )
        t = Translation([stroke], ' '.join(english))
        t.replaced = [replaced]
        t.is_retrospective_command = True
        translator.translate_translation(t)
