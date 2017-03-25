# Copyright (c) 2011 Joshua Harlan Lifton.
# See LICENSE.txt for details.

"""Custom exceptions used by Plover.

The exceptions in this module are typically caught in the main GUI
loop and displayed to the user as an alert dialog.

"""

class InvalidConfigurationError(Exception):
    "Raised when there is something wrong in the configuration."
    pass

class DictionaryLoaderException(Exception):
    """Dictionary file could not be loaded."""

    def __init__(self, filename, exception):
        super(DictionaryLoaderException, self).__init__(filename, exception)
        self.filename = filename
        self.exception = exception

    def get_path(self):
        return self.filename

    def __str__(self):
        return 'loading dictionary `%s` failed: %s' % (self.filename, self.exception)
