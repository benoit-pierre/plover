#!/usr/bin/env python3
# Copyright (c) 2010 Joshua Harlan Lifton.
# See LICENSE.txt for details.
#
# keyboardcontrol.py - Abstracted keyboard control.
#
# Uses OS appropriate module.

"""Keyboard capture and control.

This module provides an interface for basic keyboard event capture and
emulation. Set the key_up and key_down functions of the
KeyboardCapture class to capture keyboard input. Call the send_string
and send_backspaces functions of the KeyboardEmulation class to
emulate keyboard input.

"""

import sys
import importlib

KEYBOARDCONTROL_NOT_FOUND_FOR_OS = \
        "No keyboard control module was found for os %s" % sys.platform


class KeyboardCaptureBase(object):
    """Listen to keyboard press and release events."""

    # Callbacks for keyboard press/release events.
    key_down = lambda key: None
    key_up = lambda key: None

    def start(self):
        pass

    def cancel(self):
        pass

    def suppress_keys(self, suppressed_keys=()):
        raise NotImplementedError()


class KeyboardEmulationBase(object):
    """Emulate keyboard events."""

    def send_backspaces(self, number_of_backspaces):
        raise NotImplementedError()

    def send_string(self, s):
        raise NotImplementedError()

    def send_key_combination(self, combo_string):
        raise NotImplementedError()


if sys.platform.startswith('linux'):
    module_name = 'xkeyboardcontrol'
elif sys.platform.startswith('win32'):
    module_name = 'winkeyboardcontrol'
elif sys.platform.startswith('darwin'):
    module_name = 'osxkeyboardcontrol'
else:
    raise Exception(KEYBOARDCONTROL_NOT_FOUND_FOR_OS)

keyboardcontrol = importlib.import_module('.' + module_name, __package__)

KeyboardCapture = keyboardcontrol.KeyboardCapture
KeyboardEmulation = keyboardcontrol.KeyboardEmulation


if __name__ == '__main__':

    import time

    kc = KeyboardCapture()
    ke = KeyboardEmulation()

    pressed = set()
    status = u'pressed: '

    def test(key, action):
        global status
        print(key, action)
        if u'pressed' == action:
            pressed.add(key)
        elif key in pressed:
            pressed.remove(key)
        new_status = u'pressed: ' + u'+'.join(pressed)
        if status != new_status:
            ke.send_backspaces(len(status))
            ke.send_string(new_status)
            status = new_status

    kc.key_down = lambda k: test(k, u'pressed')
    kc.key_up = lambda k: test(k, u'released')
    kc.suppress_keyboard('a s d f'.split())
    kc.start()
    print('Press CTRL-c to quit.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        kc.cancel()
