# -*- coding: utf-8 -*-
# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

"Launch the plover application."

import os
import sys
import traceback
import argparse

WXVER = '3.0'
if not hasattr(sys, 'frozen'):
    import wxversion
    wxversion.ensureMinimal(WXVER)

import wx
import json
import pkg_resources

from collections import OrderedDict

import plover.gui.main
import plover.oslayer.processlock
from plover.oslayer.config import CONFIG_DIR
from plover.config import CONFIG_FILE, DEFAULT_DICTIONARIES, Config
from plover.registry import registry
from plover import log
from plover import __name__ as __software_name__
from plover import __version__

if sys.platform.startswith('win32'):
    from plover.oslayer import winconsole
    def redirect_to_console():
        if winconsole.redirect_to_console():
            log.update_stderr(sys.stderr)
else:
    redirect_to_console = lambda: None


def show_error(title, message):
    """Report error to the user.

    This shows a graphical error and prints the same to the terminal.
    """
    print message
    app = wx.App()
    alert_dialog = wx.MessageDialog(None,
                                    message,
                                    title,
                                    wx.OK | wx.ICON_INFORMATION)
    alert_dialog.ShowModal()
    alert_dialog.Destroy()

def init_config_dir():
    """Creates plover's config dir.

    This usually only does anything the first time plover is launched.
    """
    # Create the configuration directory if needed.
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    # Create a default configuration file if one doesn't already exist.
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'wb') as f:
            f.close()

class ArgumentParser(argparse.ArgumentParser):

    NEEDS_CONSOLE = set(
        '''
        print_usage
        print_help
        exit
        '''.split())

    def __getattribute__(self, name):
        if name in ArgumentParser.NEEDS_CONSOLE:
            redirect_to_console()
        return super(ArgumentParser, self).__getattribute__(name)

def main():
    """Launch plover."""
    description = "Run the plover stenotype engine. This is a graphical application."
    parser = ArgumentParser(description=description)
    parser.add_argument('--version', action='version', version='%s %s'
                        % (__software_name__.capitalize(), __version__))
    parser.add_argument('-s', '--script', default=None, nargs=argparse.REMAINDER,
                        help='use another plugin console script as main entrypoint, '
                        'passing in the rest of the command line arguments, '
                        'print list of available scripts when no argument is given')
    parser.add_argument('-l', '--log-level', choices=['debug', 'info', 'warning', 'error', 'critical'],
                        default=None, help='set log level')
    args = parser.parse_args(args=sys.argv[1:])

    try:
        if args.log_level is None:
            log_level = 'WARNING'
        else:
            redirect_to_console()
            log_level = args.log_level.upper()
        log.set_level(log_level)

        if args.script is not None:
            redirect_to_console()
            registry.load_plugins()
            registry.update()
            scripts = registry.get_scripts()
            if args.script:
                name = args.script[0]
                entrypoint = scripts.get(name)
                if entrypoint is None:
                    log.error('no such script: %s', name)
                    code = 1
                else:
                    sys.argv = args.script
                    code = entrypoint.load()()
                if code is None:
                    code = 0
            else:
                print 'available script(s):'
                for name, entrypoint in sorted(scripts.items()):
                    print '%s [%s]' % (name, entrypoint.dist.project_name)
                code = 0
            sys.exit(code)

        # Ensure only one instance of Plover is running at a time.
        with plover.oslayer.processlock.PloverLock():
            init_config_dir()
            # This must be done after calling init_config_dir, so
            # Plover's configuration directory actually exists.
            log.setup_logfile()
            config = Config()
            config.target_file = CONFIG_FILE
            gui = plover.gui.main.PloverGUI(config)
            gui.MainLoop()
            with open(config.target_file, 'wb') as f:
                config.save(f)
    except plover.oslayer.processlock.LockNotAcquiredException:
        show_error('Error', 'Another instance of Plover is already running.')
        sys.exit(1)
    except SystemExit:
        raise
    except:
        show_error('Unexpected error', traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
