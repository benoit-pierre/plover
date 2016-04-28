
from ctypes import windll
import msvcrt
import atexit
import sys


_console_redirected = False


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12


def pause_console():
    print 'Press a key to continue...'
    msvcrt.getch()

def redirect_to_console():

    global _console_redirected
    if _console_redirected:
        return False

    for io in (sys.stdin,
               sys.stdout,
               sys.stderr):
        if not (
            io.__class__.__name__ == 'NullWriter' # No console, PyInstaller executable.
            or io.fileno() == -2                  # No console, e.g. with pythonw.exe.
        ):
            _console_redirected = True
            return False

    atexit.register(pause_console)

    windll.kernel32.FreeConsole()
    windll.kernel32.AllocConsole()
    windll.kernel32.SetConsoleCP(65001)

    sys.stdout = sys.__stdout__ = open('CONOUT$', 'wt', 0)
    sys.stderr = sys.__stderr__ = sys.__stdout__
    sys.stdin = sys.__stdin__ = open('CONIN$', 'rt')

    for stdhndl, fp in (
        (STD_INPUT_HANDLE, sys.stdin),
        (STD_OUTPUT_HANDLE, sys.stdout),
        (STD_ERROR_HANDLE, sys.stderr),
    ):
        hndl = msvcrt.get_osfhandle(fp.fileno())
        windll.kernel32.SetStdHandle(stdhndl, hndl)

    # Must be done after creating the console and fixing the standard handles.
    from win_unicode_console import streams
    sys.stdout = streams.stdout_text_str
    sys.stderr = streams.stderr_text_str
    sys.stdin = streams.stdin_text_fileobj

    _console_redirected = True

    return True
