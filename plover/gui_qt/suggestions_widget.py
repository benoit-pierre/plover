from PyQt5.QtGui import (
    QFont,
    QTextCursor,
    QTextCharFormat,
    QTextFrameFormat,
    QTextListFormat,
)
from PyQt5.QtWidgets import QWidget

from plover.translation import escape_translation

from plover.gui_qt.suggestions_widget_ui import Ui_SuggestionsWidget


class SuggestionsWidget(QWidget, Ui_SuggestionsWidget):

    STYLE_TRANSLATION, STYLE_STROKES = range(2)

    # Anatomy of the text document:
    # - "root" frame:
    #  - 0+ "suggestions" frames
    #   - 1+ "translation" frames
    #    - 1-10 "strokes" frames

    def __init__(self):
        super(SuggestionsWidget, self).__init__()
        self.setupUi(self)
        self._suggestions_frame_format = QTextFrameFormat()
        self._suggestions_frame_format.setBorderStyle(QTextFrameFormat.BorderStyle_Inset)
        self._suggestions_frame_format.setBorder(1)
        self._suggestions_char_format = QTextCharFormat()
        self._translation_frame_format = QTextFrameFormat()
        self._translation_frame_format.setLeftMargin(4.0)
        self._translation_char_format = QTextCharFormat()
        self._strokes_char_format = QTextCharFormat()
        self._strokes_char_format.font().setStyleHint(QFont.Monospace)

    def prepend(self, suggestion_list):
        before_height = self.suggestions.document().size().height()
        cursor = self.suggestions.textCursor()
        cursor.movePosition(QTextCursor.Start)
        frame = cursor.insertFrame(self._suggestions_frame_format)
        for suggestion in suggestion_list:
            child_frame = frame.lastCursorPosition().insertFrame(self._translation_frame_format)
            cursor = child_frame.lastCursorPosition()
            cursor.setCharFormat(self._translation_char_format)
            cursor.block().setUserState(self.STYLE_TRANSLATION)
            cursor.insertText(escape_translation(suggestion.text) + u':')
            if not suggestion.steno_list:
                cursor.insertText(u' ' + _('no suggestions'))
                continue
            cursor.insertList(QTextListFormat.ListDisc)
            for strokes_list in suggestion.steno_list[:10]:
                cursor.setCharFormat(self._strokes_char_format)
                cursor.block().setUserState(self.STYLE_STROKES)
                cursor.insertText(u'/'.join(strokes_list) + u'\n')
            cursor.deletePreviousChar()
        # Keep current position when not at the top of the document.
        scrollbar_value = self.suggestions.verticalScrollBar().value()
        if scrollbar_value != 0:
            after_height = self.suggestions.document().size().height()
            delta_height = after_height - before_height
            self.suggestions.verticalScrollBar().setValue(scrollbar_value + delta_height)

    def clear(self):
        self.suggestions.clear()

    def _reformat(self):
        document = self.suggestions.document()
        cursor = self.suggestions.textCursor()
        block = document.begin()
        style_format = {
            self.STYLE_TRANSLATION: self._translation_char_format,
            self.STYLE_STROKES: self._strokes_char_format,
        }
        while block != document.end():
            style = block.userState()
            fmt = style_format.get(style)
            if fmt is not None:
                cursor.setPosition(block.position())
                cursor.select(QTextCursor.BlockUnderCursor)
                cursor.setCharFormat(fmt)
            block = block.next()

    @property
    def text_font(self):
        return self._translation_char_format.font()

    @text_font.setter
    def text_font(self, font):
        self._translation_char_format.setFont(font)
        self._reformat()

    @property
    def strokes_font(self):
        return self._strokes_char_format.font()

    @text_font.setter
    def strokes_font(self, font):
        self._strokes_char_format.setFont(font)
        self._reformat()
