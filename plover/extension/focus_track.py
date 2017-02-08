
from threading import Lock, Thread
import select
import errno
import os

from Xlib import display, X, Xatom
from Xlib.error import BadWindow

from plover.engine import StartingStrokeState


class XEventLoop(Thread):

    def __init__(self, name='xev'):
        super(XEventLoop, self).__init__()
        self.name += '-' + name
        self._display = display.Display()
        self._pipe = os.pipe()

    def _on_event(self, event):
        pass

    def run(self):
        display_fileno = self._display.fileno()
        while True:
            if not self._display.pending_events():
                try:
                    rlist, wlist, xlist = select.select((self._pipe[0],
                                                         display_fileno),
                                                        (), ())
                except select.error as err:
                    if isinstance(err, OSError):
                        code = err.errno
                    else:
                        code = err[0]
                    if code != errno.EINTR:
                        raise
                    continue
                assert not wlist
                assert not xlist
                if self._pipe[0] in rlist:
                    break
                # If we're here, rlist should contains display_fileno,
                # trigger a new iteration to check for pending events.
                continue
            self._on_event(self._display.next_event())

    def cancel(self):
        # Wake up the capture thread...
        os.write(self._pipe[1], b'quit')
        # ...and wait for it to terminate.
        self.join()
        for fd in self._pipe:
            os.close(fd)


class FocusTrack(XEventLoop):

    def __init__(self, engine):
        super(FocusTrack, self).__init__(name='focus_track')
        self._states = {}
        self._lock = Lock()
        self._engine = engine
        self._root_window = None
        self._focus_window = None
        self._atom_active_window = None
        self._output_enabled = False

    def _get_state(self):
        with self._engine:
            return (
                self._engine.translator_state,
                self._engine.starting_stroke_state,
            )

    def _set_state(self, translator_state, starting_stroke_state):
        with self._engine:
            self._engine.translator_state = translator_state
            self._engine.starting_stroke_state = starting_stroke_state

    def _clear_state(self):
        with self._engine:
            config = self._engine.config
            self._engine.clear_translator_state()
            self._engine.starting_stroke_state = StartingStrokeState(
                config['start_attached'], config['start_capitalized']
            )

    def _switch_state(self):
        if not self._output_enabled:
            return
        if self._focus_window is None:
            print('reset state')
            self._clear_state()
        else:
            print('set state %x' % self._focus_window.id)
            state = self._states.get(self._focus_window.id)
            if state is None:
                self._clear_state()
                state = self._get_state()
                self._states[self._focus_window.id] = state
            else:
                self._set_state(*state)

    def _on_output_changed(self, enabled):
        print('output', 'enabled' if enabled else 'disabled')
        with self._lock:
            self._output_enabled = enabled
            if enabled:
                self._switch_state()

    def _update_focus(self):
        value = self._root_window.get_property(self._atom_active_window, Xatom.WINDOW, 0, 1).value
        if X.NONE == value[0]:
            # Focus lost.
            return
        # Focus gained.
        with self._lock:
            window = self._display.create_resource_object('window', value[0])
            try:
                wm_name = window.get_wm_name()
            except BadWindow:
                return
            # Ignore Plover's own "Add Translation" dialog.
            if wm_name == 'Plover: Add Translation':
                return
            print('focus %x' % window.id, wm_name)
            self._focus_window = window
            self._switch_state()

    def _on_event(self, event):
        if event.type == X.DestroyNotify:
            print('destroy %x' % event.window.id)
            with self._lock:
                if event.window == self._focus_window:
                    # Reset current state if focused.
                    self._focus_window = None
                    self._switch_state()
                # Destroy saved state if any.
                try:
                    del self._states[event.window.id]
                except KeyError:
                    pass
        elif event.type == X.PropertyNotify and \
           event.atom == self._atom_active_window and \
           event.state == X.PropertyNewValue:
            self._update_focus()

    def start(self):
        self._root_window = self._display.screen().root
        self._root_window.change_attributes(event_mask=X.PropertyChangeMask|X.SubstructureNotifyMask)
        self._atom_active_window = self._display.intern_atom('_NET_ACTIVE_WINDOW', only_if_exists=True)
        self._update_focus()
        self._engine.hook_connect('output_changed', self._on_output_changed)
        self._output_enabled = self._engine.output
        super(FocusTrack, self).start()

    def stop(self):
        self._engine.hook_disconnect('output_changed', self._on_output_changed)
        self.cancel()
        self.join()
