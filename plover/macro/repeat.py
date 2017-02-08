def last_stroke(translator, stroke, cmdline):
    # Repeat last stroke
    translations = translator.get_state().translations
    if not translations:
        return
    translator.translate_stroke(translations[-1].strokes[-1])
