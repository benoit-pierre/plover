# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

# TODO: maybe move this code into the StenoDictionary itself. The current saver 
# structure is odd and awkward.
# TODO: write tests for this file

"""Common elements to all dictionary formats."""

from os.path import splitext
import shutil
import sys
import threading

from plover.exception import DictionaryLoaderException
from plover.registry import registry, ASSET_SCHEME


def _get_dictionary_module(format):
    dictionaries = registry.get_dictionaries()
    try:
        dictionary_module = dictionaries[format].load()
    except KeyError:
        raise DictionaryLoaderException(
            'Unsupported format for dictionary: %s. Supported formats: %s' %
            (format, ', '.join(sorted(dictionaries.keys()))))
    return dictionary_module

def create_dictionary(filename):
    '''Create a new dictionary.

    The format is inferred from the extension.

    Note: the file is not created! The resulting dictionary save
    method must be called to finalize the creation on disk.
    '''
    assert not filename.startswith(ASSET_SCHEME)
    extension = splitext(filename)[1].lower()
    dictionary_module = _get_dictionary_module(extension[1:])
    if dictionary_module.create_dictionary is None:
        raise DictionaryLoaderException('%s dictionaries don\'t support creation' % extension)
    try:
        d = dictionary_module.create_dictionary()
    except Exception as e:
        ne = DictionaryLoaderException('creating %s dictionary failed: %s' % (extension, str(e)))
        raise type(ne), ne, sys.exc_info()[2]
    d.set_path(filename)
    d.save = ThreadedSaver(d, filename, dictionary_module.save_dictionary)
    return d

def load_dictionary(filename):
    """Load a dictionary from a file."""
    extension = splitext(filename)[1].lower()
    dictionary_module = _get_dictionary_module(extension[1:])
    try:
        d = dictionary_module.load_dictionary(filename)
    except Exception as e:
        ne = DictionaryLoaderException('loading \'%s\' failed: %s' % (filename, str(e)))
        raise type(ne), ne, sys.exc_info()[2]
    d.set_path(filename)
    if dictionary_module.save_dictionary is None or filename.startswith(ASSET_SCHEME):
        d.save = None
    else:
        d.save = ThreadedSaver(d, filename, dictionary_module.save_dictionary)
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
