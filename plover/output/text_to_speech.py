
import ctypes
import queue
import math
import threading
import sys

from pydub import AudioSegment
import simpleaudio as sa

from plover.output.delayed_keyboard_emulation import DelayedKeyboardEmulation


SILENCE_THRESHOLD = -55.0
CHUNK_SIZE = 5

def detect_leading_silence(sound, silence_threshold=SILENCE_THRESHOLD, chunk_size=CHUNK_SIZE):
    for trim_ms in range(0, len(sound), chunk_size):
        dbfs = sound[trim_ms:trim_ms+chunk_size].dBFS
        if dbfs >= silence_threshold:
            return max(0, trim_ms-chunk_size)
    return len(sound)

def detect_trailing_silence(sound, silence_threshold=SILENCE_THRESHOLD, chunk_size=CHUNK_SIZE):
    for trim_ms in range(len(sound)-chunk_size, -chunk_size, -chunk_size):
        dbfs = sound[trim_ms:trim_ms+chunk_size].dBFS
        if dbfs >= silence_threshold:
            return min(len(sound), trim_ms+chunk_size)
    return 0

def trim_silence(sound, silence_threshold=SILENCE_THRESHOLD, chunk_size=CHUNK_SIZE):
    return sound[detect_leading_silence(sound, silence_threshold, chunk_size):
                 detect_trailing_silence(sound, silence_threshold, chunk_size)]


if sys.platform.startswith('win32'):

    from pyttsx3.drivers import sapi5
    import comtypes.client
    import pythoncom

    class TTS:

        def __init__(self, rate=None, volume=None, voice=None):
            pythoncom.CoInitialize()
            self._tts = comtypes.client.CreateObject('SAPI.SPVoice')
            if voice is not None:
                for token in self._tts.GetVoices():
                    if token.Id == voice:
                        self._tts.Voice = token
                        break
                else:
                    raise ValueError('invalid voice: %s' % voice)
            if rate is not None:
                a, b = sapi5.E_REG.get(self._tts.Voice.Id, sapi5.E_REG[sapi5.MSMARY])
                self._tts.Rate = int(math.log(rate / a, b))
            if volume is not None:
                self._tts.Volume = int(round(volume * 100, 2))

        def available_voices(self):
            return {
                voice.GetDescription(): voice.Id
                for voice in self._tts.GetVoices()
            }

        def generate(self, text):
            vmemorystream = comtypes.client.CreateObject('SAPI.spMemoryStream')
            self._tts.AudioOutputStream = vmemorystream
            self._tts.Speak(text, 16)
            fmt = vmemorystream.Format.GetWaveFormatEx()
            data = vmemorystream.GetData()
            if not data:
                return None
            wav = AudioSegment(data=bytes(data),
                               sample_width=fmt.BitsPerSample // 8,
                               frame_rate=fmt.SamplesPerSec,
                               channels=fmt.Channels)
            return trim_silence(wav)

elif sys.platform.startswith('linux'):

    from pyttsx3.drivers import _espeak

    class TTS:

        _espeak_initialized = False

        def __init__(self, rate=None, volume=None, voice=None):
            if not TTS._espeak_initialized:
                if _espeak.Initialize(_espeak.AUDIO_OUTPUT_RETRIEVAL, 1000) == -1:
                    raise RuntimeError('could not initialize espeak')
                TTS._espeak_initialized = True
            _espeak.SetSynthCallback(self._on_synth)
            self._data_buffer = None
            if voice is not None:
                _espeak.SetVoiceByName(voice.encode('utf-8'))
            if rate is not None:
                _espeak.SetParameter(_espeak.RATE, rate, 0)
            if volume is not None:
                _espeak.SetParameter(_espeak.VOLUME, int(round(volume * 100, 2)), 0)
            self._generated = threading.Event()

        def _on_synth(self, wav, numsamples, events):
            for evt in events:
                if evt.type == _espeak.EVENT_LIST_TERMINATED:
                    break
                if evt.type == _espeak.EVENT_MSG_TERMINATED:
                    self._generated.set()
            if numsamples > 0:
                self._data_buffer += ctypes.string_at(wav, numsamples * ctypes.sizeof(ctypes.c_short))
            return 0

        def available_voices(self):
            return {
                voice.name.decode('utf-8'): voice.name.decode('utf-8')
                for voice in _espeak.ListVoices(None)
            }

        def generate(self, text):
            self._generated.clear()
            self._data_buffer = b''
            _espeak.Synth(text.encode('utf-8'), flags=_espeak.CHARS_UTF8)
            self._generated.wait()
            return AudioSegment(data=self._data_buffer, sample_width=2,
                                frame_rate=22050, channels=1)


def available_voices():
    return TTS().available_voices()


class SpeechOutput(threading.Thread):

    def __init__(self, text_output, rate=175, volume=1.0, voice=None):
        super().__init__()
        self._text_output = text_output
        self._queue = queue.Queue()
        self._rate = rate
        self._voice = voice
        self._volume = volume

    def run(self):
        tts = TTS(self._rate, self._volume, self._voice)
        while True:
            s = self._queue.get()
            if s is None:
                break
            s = s.strip()
            if not s:
                continue
            wav = tts.generate(s)
            if wav is None:
                continue
            # print('say', repr(s), len(wav), wav.channels,
            #       wav.frame_width, wav.frame_rate)
            play_obj = sa.play_buffer(wav.raw_data, wav.channels,
                                      wav.frame_width, wav.frame_rate)
            play_obj.wait_done()

    def start(self):
        self._text_output.start()
        super().start()

    def cancel(self):
        self._text_output.cancel()
        self._queue.put(None)
        self.join()

    def send_backspaces(self, n):
        pass

    def send_string(self, s):
        self._queue.put(s)

    def send_key_combination(self, c):
        self._text_output.send_key_combination(c)


class TextToSpeech(DelayedKeyboardEmulation):

    def __init__(self, params):
        super().__init__(params)
        rate = params['rate']
        volume = params['volume']
        voice = params['voice'] or None
        self._output = SpeechOutput(self._output, rate, volume, voice)

    @classmethod
    def get_option_info(cls):
        options = super().get_option_info()
        options['rate'] = (175, int)
        options['voice'] = ('', str)
        options['volume'] = (1.0, float)
        return options
