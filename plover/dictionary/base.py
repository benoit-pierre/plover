# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

# TODO: maybe move this code into the StenoDictionary itself. The current saver 
# structure is odd and awkward.
# TODO: write tests for this file

"""Common elements to all dictionary formats."""

from os.path import splitext
import shutil
import threading

from plover.exception import DictionaryLoaderException
from plover.registry import registry, ASSET_SCHEME


def load_dictionary(filename):
    """Load a dictionary from a file."""
    extension = splitext(filename)[1].lower()
    dictionaries = registry.get_dictionaries()

    try:
        dict_type = dictionaries[extension[1:]].load()
    except KeyError:
        raise DictionaryLoaderException(
            'Unsupported extension for dictionary: %s. Supported extensions: %s' %
            (extension, ', '.join(sorted(dictionaries.keys()))))

    try:
        d = dict_type.load_dictionary(filename)
    except Exception as e:
        raise DictionaryLoaderException('loading \'%s\' failed: %s' % (filename, str(e)))
    d.set_path(filename)
    if dict_type.save_dictionary is None or filename.startswith(ASSET_SCHEME):
        d.save = None
    else:
        d.save = ThreadedSaver(d, filename, dict_type.save_dictionary)
    return d

def save_dictionary(d, filename, saver):
    # Write the new file to a temp location.
    tmp = filename + '.tmp'
    with open(tmp, 'wb') as fp:
        saver(d, fp)

    # Then move the new file to the final location.
    shutil.move(tmp, filename)
    
class ThreadedSaver(object):
    """A callable that saves a dictionary in the background.
    
    Also makes sure that there is only one active call at a time.
    """
    def __init__(self, d, filename, saver):
        self.d = d
        self.filename = filename
        self.saver = saver
        self.lock = threading.Lock()
        
    def __call__(self):
        t = threading.Thread(target=self.save)
        t.start()
        
    def save(self):
        with self.lock:
            save_dictionary(self.d, self.filename, self.saver)
