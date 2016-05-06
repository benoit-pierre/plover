# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

"""Parsing a json formatted dictionary.

"""

try:
    import simplejson as json
except ImportError:
    import json

from plover.steno_dictionary import StenoDictionary
from plover.steno import normalize_steno
from plover import resource

def create_dictionary():
    return StenoDictionary()

def load_dictionary(filename):

    for encoding in ('utf-8', 'latin-1'):
        try:
            with resource.resource_stream(filename, encoding=encoding) as fp:
                d = json.load(fp)
                break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError('\'%s\' encoding could not be determined' % (filename,))

    return StenoDictionary((normalize_steno(x[0]), x[1])
                           for x in dict(d).iteritems())


# TODO: test this
def save_dictionary(d, fp):
    contents = json.dumps(dict(('/'.join(k), v) for k, v in d.iteritems()),
                          ensure_ascii=False, sort_keys=True,
                          indent=0, separators=(',', ': '))
    fp.write(contents.encode('utf-8'))
