
from plover.registry import registry

from collections import namedtuple
import re
import threading
import time


PART_RX = re.compile(r'(?:\d+(?:[.,]\d+)+|[\'\w]+[-\w\']*|[^\w\s]+|\s+)', re.UNICODE)

class DelayedKeyboardEmulation(threading.Thread):

    Combo = namedtuple('Combo', 'timestamp combo')

    class Output:

        Part = namedtuple('Part', 'timestamp text')

        def __init__(self, timestamp=None, replace=0, parts=None):
            self._timestamp = timestamp
            self._replace = replace
            self._parts = parts or []

        def __bool__(self):
            return bool(self._replace or self._parts)

        def __len__(self):
            return len(self._parts)

        def flush(self, deadline_timestamp):
            '''Remove parts and return (as a new output)
               all parts that are not after the deadline.
            '''
            if self._replace and self._timestamp <= deadline_timestamp:
                timestamp, replace = self._timestamp, self._replace
                self._timestamp, self._replace = None, 0
            else:
                timestamp, replace = None, None
            parts = []
            while self._parts and self._parts[0].timestamp <= deadline_timestamp:
                parts.append(self._parts.pop(0))
            return self.__class__(timestamp, replace, parts)

        @property
        def timestamp(self):
            if self._replace:
                return self._timestamp
            return self._parts[0].timestamp

        @property
        def replace(self):
            return self._replace

        @property
        def text(self):
            return ''.join(p.text for p in self._parts)

        def erase(self, timestamp, count):
            assert count > 0
            while count:
                if not self._parts:
                    self._replace += count
                    self._timestamp = timestamp
                    break
                last_part = self._parts.pop()
                if len(last_part.text) > count:
                    text = last_part.text[:-count]
                    if text.isspace():
                        timestamp = last_part.timestamp
                    self._parts.append(self.Part(timestamp, text))
                    break
                count -= len(last_part.text)

        def append(self, timestamp, text):
            assert text
            if self._parts:# and not self._parts[-1].text.isspace():
                last_part = self._parts.pop()
                text = last_part.text + text
            else:
                last_part = None
            parts = PART_RX.findall(text)
            if last_part is not None:
                if parts[0] == last_part.text:
                    self._parts.append(last_part)
                    parts.pop(0)
            self._parts.extend(self.Part(timestamp, p) for p in parts)

        def merge(self, another_output):
            if another_output._replace:
                self.erase(another_output._timestamp, another_output._replace)
            if another_output._parts:
                self._parts.extend(another_output._parts)

        def __repr__(self):
            return 'Output(%s:%s, %r)' % (self._timestamp, self._replace, self._parts)

    @classmethod
    def get_option_info(cls):
        return {
            'delay': (0.5, float),
            'output': ('Keyboard Emulation', str),
        }

    def __init__(self, params):
        super().__init__()
        self._stopping = False
        self._signal = threading.Semaphore(0)
        self._instructions = []
        self._lock = threading.Lock()
        self._delay = params['delay']
        output_class = registry.get_plugin('output', params['output']).obj
        output_options = {k: v[0] for k, v in output_class.get_option_info().items()}
        self._output = output_class(output_options)

    def _process(self, flush):
        if flush == 'all':
            instructions = self._instructions
            self._instructions = []
        elif flush == 'combo':
            instructions = []
            while self._instructions:
                i = self._instructions.pop(0)
                instructions.append(i)
                if isinstance(i, self.Combo):
                    break
            assert instructions
        elif flush == 'deadline':
            instructions = []
            deadline = time.time() - self._delay
            while self._instructions:
                i = self._instructions.pop(0)
                if isinstance(i, self.Combo):
                    instructions.append(i)
                    continue
                output = i.flush(deadline)
                if output:
                    instructions.append(output)
                if i:
                    self._instructions.insert(0, i)
                if not output:
                    break
        else:
            raise ValueError(flush)
        if not instructions:
            return
        # We'll merge contiguous outputs to optimize the final output.
        def flush():
            if flush.last_output is None:
                return
            replace = flush.last_output.replace
            text = flush.last_output.text
            if replace:
                self._output.send_backspaces(replace)
            if text:
                self._output.send_string(text)
            flush.last_output = None
        flush.last_output = None
        for i in instructions:
            if isinstance(i, self.Output):
                if flush.last_output is not None:
                    flush.last_output.merge(i)
                else:
                    flush()
                    flush.last_output = i
            else:
                flush()
                self._output.send_key_combination(i.combo)
        flush()

    def _timeout(self):
        # FIXME: handle zero delay.
        if not self._instructions:
            return self._delay
        return max(0, self._instructions[0].timestamp + self._delay - time.time())

    def _new_output(self, replace=0, text=''):
        assert bool(replace) ^ bool(text)
        timestamp = time.time()
        if self._instructions:
            last_output = self._instructions[-1]
            if not isinstance(last_output, self.Output):
                last_output = None
        else:
            last_output = None
        if last_output is None:
            # Previous instruction is not an output.
            last_output = self.Output()
            self._instructions.append(last_output)
        if replace:
            last_output.erase(timestamp, replace)
            if not last_output:
                self._instructions.pop()
        else:
            last_output.append(timestamp, text)

    def run(self):
        timeout = self._delay
        while True:
            signaled = self._signal.acquire(timeout=timeout)
            with self._lock:
                if self._stopping:
                    self._process('all')
                    return
                self._process('combo' if signaled else 'deadline')
                timeout = self._timeout()

    def start(self):
        self._output.start()
        super().start()

    def cancel(self):
        self._output.cancel()
        self._stopping = True
        self._signal.release()
        self.join()

    def send_backspaces(self, count):
        with self._lock:
            self._new_output(replace=count)

    def send_string(self, string):
        with self._lock:
            self._new_output(text=string)

    def send_key_combination(self, combo):
        with self._lock:
            self._instructions.append(self.Combo(time.time(), combo))
        self._signal.release()
