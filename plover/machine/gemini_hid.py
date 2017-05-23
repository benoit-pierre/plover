
import hid

from plover import log
from plover.machine.base import ThreadedStenotypeBase
from plover.machine.geminipr import GeminiPr


STENO_KEY_CHART = (
    "Fn", "#1", "#2", "#3", "#4", "#5", "#6", "S1-",
    "S2-", "T-", "K-", "P-", "W-", "H-", "R-", "A-",
    "O-", "*1", "*2", "res1", "res2", "pwr", "*3", "*4",
    "-E", "-U", "-F", "-R", "-P", "-B", "-L", "-G",
    "-T", "-S", "-D", "#7", "#8", "#9", "#A", "#B",
    "#C", "-Z",
)

class GeminiHid(ThreadedStenotypeBase):

    KEYMAP_MACHINE_TYPE = 'Gemini PR'
    KEYS_LAYOUT = GeminiPr.KEYS_LAYOUT

    def __init__(self, params):
        super(GeminiHid, self).__init__()
        self._dev = None

    def start_capture(self):
        self.finished.clear()
        self._initializing()
        self._dev = hid.device()
        for dev_info in hid.enumerate(0xFEED, 0x6061):
            print(dev_info)
            # if dev_info['usage_page'] == 0xFF60 and \
            #    dev_info['usage'] == 0x0061:
            #     dev_path = dev_info['path']
            #     break
            if dev_info['interface_number'] == 2:
                dev_path = dev_info['path']
                break
        else:
            raise Exception('interface not found')
            self._error()
            return
        self._dev = hid.device()
        try:
            self._dev.open_path(dev_path)
        except OSError:
            self._error()
            return
        self.start()

    def run(self):
        self._ready()
        while not self.finished.isSet():
            data = self._dev.read(32, 100)
            if not data:
                continue
            keys = []
            for i, b in enumerate(data):
                for j in range(8):
                    if (b & (1 << j)):
                        keys.append(STENO_KEY_CHART[i * 8 + j])
            steno_keys = self.keymap.keys_to_actions(keys)
            if steno_keys:
                self._notify(steno_keys)

    def stop_capture(self):
        self.finished.set()
        try:
            self.join()
        except RuntimeError:
            pass
        if self._dev is not None:
            self._dev.close()
            self._dev = None
        self._stopped()
