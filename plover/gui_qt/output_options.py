from copy import copy

from PyQt5.QtCore import QVariant, pyqtSignal
from PyQt5.QtWidgets import QLabel, QFormLayout, QDoubleSpinBox, QWidget

from plover.gui_qt.i18n import get_gettext


_ = get_gettext()


class DelayedKeyboardEmulationOption(QWidget):

    valueChanged = pyqtSignal(QVariant)

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
