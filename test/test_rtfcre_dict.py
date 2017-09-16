# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

import ast
import inspect

import pytest

from plover.dictionary.rtfcre_dict import RtfDictionary, format_translation
from plover.steno import normalize_steno

from .utils import make_dict


def parametrize(tests):
    ids = []
    argvalues = []
    for n, t in enumerate(tests):
        line = inspect.getsourcelines(t)[1]
        ids.append('%u.%u' % (n+1, line))
        argvalues.append(t())
    # ids = list(map(str, range(1, len(argvalues)+1)))
    def decorator(fn):
        parameters = list(inspect.signature(fn).parameters.keys())
        if 'self' == parameters[0]:
            parameters.pop(0)
        argnames = ','.join(parameters)
        return pytest.mark.parametrize(argnames, argvalues, ids=ids)(fn)
    return decorator


RTF_LOAD_TESTS = (

    # Empty dictionary.
    lambda: '''



    ''',

    # Only one translation.
    lambda: r'''
    {\*\cxs SP}translation

    'SP': 'translation',
    ''',

    # One translation on multiple lines.
    lambda: '''
    {\\*\\cxs SP}\r\ntranslation

    'SP': 'translation'
    ''',

    # Multiple translations no newlines.
    lambda: r'''
    {\*\cxs SP}translation{\*\cxs S}translation2

    'SP': 'translation',
    'S': 'translation2',
    ''',

    # Multiple translations on separate lines.
    lambda: '''
    {\\*\\cxs SP}translation\r\n{\\*\\cxs S}translation2

    'SP': 'translation',
    'S': 'translation2',
    ''',
    lambda: '''
    {\\*\\cxs SP}translation\n{\\*\\cxs S}translation2

    'SP': 'translation',
    'S': 'translation2',
    ''',

    # Escaped \r and \n handled
    lambda: '''
    {\\*\\cxs SP}trans\\\r\\\n

    'SP': 'trans{#Return}{#Return}{#Return}{#Return}',
    ''',

    # Escaped \r\n handled in mid translation
    lambda: '''
    {\\*\\cxs SP}trans\\\r\\\nlation

    'SP': 'trans{#Return}{#Return}{#Return}{#Return}lation',
    ''',

    # Whitespace is preserved in various situations.
    lambda: r'''
    {\*\cxs S}t  

    'S': 't{^  ^}',
    ''',
    lambda: r'''
    {\*\cxs S}  t

    'S': '{^  ^}t',
    ''',
    lambda: r'''
    {\*\cxs S}t   {\*\cxs T}t    

    'S': 't{^   ^}',
    'T': 't{^    ^}',
    ''',
    lambda: '''
    {\\*\\cxs S}t   \r\n{\\*\\cxs T}t    

    'S': 't{^   ^}',
    'T': 't{^    ^}',
    ''',
    lambda: '''
    {\\*\\cxs S}t  \r\n{\\*\\cxs T} t \r\n

    'S': 't{^  ^}',
    'T': ' t ',
    ''',
    lambda: r'''
    {\*\cxs T}t t t  

    'T': 't t t{^  ^}',
    ''',

    # Translations are ignored if converter returns None
     lambda: pytest.mark.xfail(r'''
     {\*\cxs S}return_none

     '''),

    # Conflicts result on only the last one kept.
    lambda: r'''
    {\*\cxs T}t
    {\*\cxs T}g

    'T': 'g',
    ''',
    lambda: pytest.mark.xfail(r'''
    {\*\cxs T}t
    {\*\cxs T}return_none

    'T': 't',
    '''),

    # Translation conversion tests.

    lambda: ('', ''),
    lambda: (r'\-', '-'),
    lambda: (r'\\ ', '\\ '),
    lambda: (r'\\', '\\'),
    lambda: (r'\{', '{'),
    lambda: (r'\}', '}'),
    lambda: (r'\~', '{^ ^}'),
    lambda: (r'\_', '{^-^}'),
    lambda: ('\\\r', '{#Return}{#Return}'),
    lambda: ('\\\n', '{#Return}{#Return}'),
    lambda: (r'\cxds', '{^}'),
    lambda: (r'pre\cxds ', '{pre^}'),
    lambda: (r'pre\cxds  ', '{pre^} '),
    lambda: (r'pre\cxds', '{pre^}'),
    lambda: (r'\cxds post', '{^post}'),
    lambda: (r'\cxds in\cxds', '{^in^}'),
    lambda: (r'\cxds in\cxds ', '{^in^}'),
    lambda: (r'\cxfc', '{-|}'),
    lambda: (r'\cxfl', '{>}'),
    lambda: (r'pre\cxfl', 'pre{>}'),
    # Stenovations extensions...
    lambda: pytest.mark.xfail((r'{\*\cxsvatdictflags N}', '{-|}')),
    lambda: pytest.mark.xfail((r'{\*\cxsvatdictflags LN1}', '{-|}')),
    lambda: (r'\par', '{#Return}{#Return}'),
    # caseCATalyst declares new styles without a preceding \par so we treat
    # it as an implicit par.
    lambda: pytest.mark.xfail((r'\s1', '{#Return}{#Return}')),
    # But if the \par is present we don't treat \s as an implicit par.
    lambda: (r'\par\s1', '{#Return}{#Return}'),
    # Continuation styles are indented too.
    lambda: pytest.mark.xfail((r'\par\s4', '{#Return}{#Return}{^    ^}')),
    # caseCATalyst punctuation.
    lambda: (r'.', '{.}'),
    lambda: (r'. ', '{.} '),
    lambda: (r' . ', ' . '),
    lambda: (r'{\cxa Q.}.', 'Q..'),
    # Don't mess with period that is part of a word.
    lambda: (r'Mr.', 'Mr.'),
    lambda: (r'.attribute', '.attribute'),
    lambda: (r'{\cxstit contents}', 'contents'),
    lambda: (r'{\cxfing c}', '{&c}'),
    lambda: (r'{\cxp.}', '{.}'),
    lambda: (r'{\cxp .}', '{.}'),
    lambda: (r'{\cxp . }', '{.}'),
    lambda: (r'{\cxp .  }', '{.}'),
    lambda: (r'{\cxp !}', '{!}'),
    lambda: (r'{\cxp ?}', '{?}'),
    lambda: (r'{\cxp ,}', '{,}'),
    lambda: (r'{\cxp ;}', '{;}'),
    lambda: (r'{\cxp :}', '{:}'),
    lambda: ('{\\cxp \'}', '{^\'}'),
    lambda: ('{\\cxp -}', '{^-^}'),
    lambda: ('{\\cxp /}', '{^/^}'),
    lambda: pytest.mark.xfail(('{\\cxp...  }', '{^...  ^}')),
    lambda: pytest.mark.xfail(('{\\cxp ") }', '{^") ^}')),
    lambda: ('{\\nonexistant }', ''),
    lambda: ('{\\nonexistant contents}', 'contents'),
    lambda: ('{\\nonexistant cont\\_ents}', 'cont{^-^}ents'),
    lambda: ('{\\*\\nonexistant }', ''),
    lambda: ('{\\*\\nonexistant contents}', ''),
    lambda: pytest.mark.xfail(('{eclipse command}', '{eclipse command}')),
    lambda: ('test text', 'test text'),
    lambda: ('test  text', 'test  text'),
    lambda: (r'{\cxconf [{\cxc abc}]}', '[abc]'),
    lambda: (r'{\cxconf [{\cxc abc}|{\cxc def}]}', '[abc|def]'),
    lambda: (r'{\cxconf [{\cxc abc}|{\cxc def}|{\cxc ghi}]}', '[abc|def|ghi]'),
    lambda: pytest.mark.xfail((r'{\cxconf [{\cxc abc}|{\cxc {\cxp... }}]}', '{^... ^}')),
    lambda: (r'be\cxds{\*\cxsvatdictentrydate\yr2006\mo5\dy10}', '{be^}'),
    lambda: (r'{\nonexistant {\cxp .}}', '{.}'),
    lambda: (r'{\*\nonexistant {\cxp .}}', ''),
)

@parametrize(RTF_LOAD_TESTS)
def test_rtf_load(test_case):
    if isinstance(test_case, tuple):
        # Translation conversion test.
        rtf_entries = '{\*\cxs S}' + test_case[0]
        dict_entries = { normalize_steno('S'): test_case[1] }
    else:
        rtf_entries, dict_entries = test_case.rsplit('\n\n', 1)
        dict_entries = {
            normalize_steno(k): v
            for k, v in ast.literal_eval('{' + dict_entries + '}').items()
        }
    rtf_styles = {
        0: 'Normal',
        1: 'Question',
        2: 'Answer',
        3: 'Colloquy',
        4: 'Continuation Q',
        5: 'Continuation A',
        6: 'Continuation Col',
        7: 'Paren',
        8: 'Centered',
    }
    rtf = (
        '\r\n'.join(
            [r'{\rtf1\ansi\cxdict{\*\cxrev100}{\*\cxsystem Fake Software}'] +
            [r'{\s%d %s;}' % (k, v) for k, v in rtf_styles.items()] +
            ['}'])
        + rtf_entries
        + '\r\n}'
    )
    with make_dict(rtf.encode('cp1252')) as filename:
        d = RtfDictionary.load(filename)
        assert dict(d.items()) == dict_entries



@pytest.mark.parametrize('before, expected', (
    ('', ''),
    ('{^in^}', r'\cxds in\cxds '),
    ('{pre^}', r'pre\cxds '),
    ('{pre^} ', r'pre\cxds '),
    ('{pre^}  ', r'pre\cxds '),
))
def test_format_translation(before, expected):
    result = format_translation(before)
    assert result == expected


@pytest.mark.parametrize('contents, expected', (
    ({'S/T': '{pre^}'},
     b'{\\rtf1\\ansi{\\*\\cxrev100}\\cxdict{\\*\\cxsystem Plover}'
     b'{\\stylesheet{\\s0 Normal;}}\r\n'
     b'{\\*\\cxs S///T}pre\\cxds \r\n}\r\n'
    ),
))
def test_save_dictionary(contents, expected):
    with make_dict(b'foo') as filename:
        d = RtfDictionary.create(filename)
        d.update(contents)
        d.save()
        with open(filename, 'rb') as fp:
            contents = fp.read()
    assert contents == expected
