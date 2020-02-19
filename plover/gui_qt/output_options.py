from copy import copy

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QComboBox, QFormLayout, QDoubleSpinBox, QSpinBox, QWidget

from plover.gui_qt.i18n import get_gettext
from plover.output.text_to_speech import available_voices


_ = get_gettext()


class DelayedKeyboardEmulationOption(QWidget):

    valueChanged = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._value = {}
        self._layout = QFormLayout(self)
        self._delay_label = QLabel(_('Delay (seconds)'))
        self._delay = QDoubleSpinBox()
        self._delay.setMinimum(0.0)
        self._delay.valueChanged.connect(self._on_delay_changed)
        self._layout.addRow(self._delay_label, self._delay)

    def setValue(self, value):
        self._value = copy(value)
        self._delay.setValue(self._value['delay'])

    def _update(self, option, value):
        self._value[option] = value
        self.valueChanged.emit(self._value)

    def _on_delay_changed(self, delay):
        self._update('delay', delay)
        self._value['delay'] = delay


class TextToSpeechOption(DelayedKeyboardEmulationOption):

    def __init__(self):
        super().__init__()
        self._rate_label = QLabel(_('Rate (WPM)'))
        self._rate = QSpinBox()
        self._rate.setMinimum(50)
        self._rate.setMaximum(500)
        self._rate.valueChanged.connect(self._on_rate_changed)
        self._layout.addRow(self._rate_label, self._rate)
        self._volume_label = QLabel(_('Volume'))
        self._volume = QDoubleSpinBox()
        self._volume.setMinimum(0.0)
        self._volume.setMaximum(1.0)
        self._volume.setSingleStep(0.1)
        self._volume.valueChanged.connect(self._on_volume_changed)
        self._layout.addRow(self._volume_label, self._volume)
        self._voice_label = QLabel(_('Voice'))
        self._voice = QComboBox()
        self._voice.addItem(_('Use default'), '')
        self._voice.insertSeparator(1)
        for voice_name, voice_id in sorted(available_voices().items()):
            self._voice.addItem(voice_name, voice_id)
        self._voice.currentIndexChanged.connect(self._on_voice_changed)
        self._layout.addRow(self._voice_label, self._voice)

    def setValue(self, value):
        super().setValue(value)
        self._rate.setValue(self._value['rate'])
        self._volume.setValue(self._value['volume'])
        voice_index = self._voice.findData(self._value['voice'])
        if voice_index <= 0:
            voice_index == 0
        self._voice.setCurrentIndex(voice_index)

    def _on_rate_changed(self, rate):
        self._update('rate', rate)

    def _on_volume_changed(self, volume):
        self._update('volume', volume)

    def _on_voice_changed(self, voice_index):
        voice = self._voice.itemData(voice_index)
        self._update('voice', voice)
