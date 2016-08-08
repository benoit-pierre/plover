
from PyQt5.QtCore import QSettings, QSize
from PyQt5.QtWidgets import (
    QMainWindow,
    QMenu,
    QToolBar,
    QToolButton,
)


def ToolButton(action):
    button = QToolButton()
    button.setDefaultAction(action)
    return button


def ToolBar(*action_list):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(16, 16))
    for action in action_list:
        toolbar.addWidget(ToolButton(action))
    return toolbar


class WindowState(object):

    ROLE = None

    def _save_state(self, settings):
        pass

    def save_state(self):
        assert self.ROLE
        settings = QSettings()
        settings.beginGroup(self.ROLE)
        settings.setValue('geometry', self.saveGeometry())
        if isinstance(self, QMainWindow):
            settings.setValue('state', self.saveState())
        self._save_state(settings)
        settings.endGroup()

    def _restore_state(self, settings):
        pass

    def restore_state(self):
        assert self.ROLE
        settings = QSettings()
        settings.beginGroup(self.ROLE)
        geometry = settings.value('geometry')
        if geometry is not None:
            self.restoreGeometry(geometry)
        if isinstance(self, QMainWindow):
            state = settings.value('state')
            if state is not None:
                self.restoreState(state)
        self._restore_state(settings)
        settings.endGroup()


def find_menu_actions(menu, root=''):
    '''Recursively find and return a menu actions.'''
    actions_dict = {}
    for action in menu.actions():
        if not action.text():
            continue
        action_id = root
        if action_id:
            action_id += '.'
        action_id += action.text().replace('&', '')
        actions_dict[action_id] = action
    for sub_menu in menu.findChildren(QMenu):
        sub_root = root
        if sub_root:
            sub_root += '.'
        sub_root += sub_menu.title().replace('&', '')
        actions_dict.update(find_menu_actions(sub_menu, sub_root))
    return actions_dict
