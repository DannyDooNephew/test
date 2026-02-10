"""
Maya script with a Qt GUI containing a blue button that creates locators.
Supports + and - buttons to adjust the quantity with a visual count display.
Uses Qt widgets with curved buttons and pressed-state shading.
"""

import maya.cmds as cmds

# Qt imports - Maya typically ships with PySide2
try:
    from PySide2 import QtWidgets, QtCore
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6 import QtWidgets, QtCore
    from shiboken6 import wrapInstance

try:
    from maya import OpenMayaUI as omui
except ImportError:
    omui = None

# Module-level count for locator quantity
_locator_count = 1

# Store reference to prevent garbage collection
_window_instance = None


def maya_main_window():
    """Get Maya's main window as a Qt widget for parenting."""
    if omui is None:
        return None
    main_window_ptr = omui.MQtUtil.mainWindow()
    if main_window_ptr is None:
        return None
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def create_locators():
    """Create locators at the origin. Quantity is determined by the current count."""
    global _locator_count
    for _ in range(_locator_count):
        cmds.spaceLocator()
    print(f"Created {_locator_count} locator(s).")


# Stylesheet for curved buttons with pressed-state shading
RED_BUTTON_STYLE = """
    QPushButton {
        background-color: #cc3333;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #e04040;
    }
    QPushButton:pressed {
        background-color: #992222;
    }
"""

BLUE_BUTTON_STYLE = """
    QPushButton {
        background-color: #3366cc;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #4080e0;
    }
    QPushButton:pressed {
        background-color: #224499;
    }
"""


class LocatorCreatorWindow(QtWidgets.QDialog):
    """Qt-based locator creator window with curved buttons and pressed-state feedback."""

    def __init__(self, parent=None):
        super(LocatorCreatorWindow, self).__init__(parent)
        global _locator_count
        _locator_count = 1
        self._count_label = None
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("Create Locator")
        self.setMinimumWidth(280)
        self.setMinimumHeight(180)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Instruction label
        instruction = QtWidgets.QLabel("Click the button to create locator(s) at the origin")
        instruction.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(instruction)

        # Counter row: [ - ] [ count ] [ + ]
        counter_layout = QtWidgets.QHBoxLayout()
        counter_layout.setSpacing(12)

        minus_btn = QtWidgets.QPushButton("-")
        minus_btn.setFixedSize(50, 40)
        minus_btn.setStyleSheet(RED_BUTTON_STYLE)
        minus_btn.clicked.connect(self._decrement_count)
        counter_layout.addWidget(minus_btn)

        self._count_label = QtWidgets.QLabel("1")
        self._count_label.setAlignment(QtCore.Qt.AlignCenter)
        self._count_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; min-width: 50px; padding: 8px;"
        )
        counter_layout.addWidget(self._count_label, alignment=QtCore.Qt.AlignCenter)

        plus_btn = QtWidgets.QPushButton("+")
        plus_btn.setFixedSize(50, 40)
        plus_btn.setStyleSheet(RED_BUTTON_STYLE)
        plus_btn.clicked.connect(self._increment_count)
        counter_layout.addWidget(plus_btn)

        layout.addLayout(counter_layout)

        # Create Locator button
        create_btn = QtWidgets.QPushButton("Create Locator")
        create_btn.setMinimumHeight(44)
        create_btn.setStyleSheet(BLUE_BUTTON_STYLE)
        create_btn.clicked.connect(create_locators)
        layout.addWidget(create_btn)

    def _increment_count(self):
        global _locator_count
        _locator_count += 1
        self._count_label.setText(str(_locator_count))

    def _decrement_count(self):
        global _locator_count
        _locator_count = max(1, _locator_count - 1)
        self._count_label.setText(str(_locator_count))


def show_window():
    """Create and display the locator creator window."""
    global _window_instance

    # Delete existing window if present
    if _window_instance is not None:
        try:
            _window_instance.close()
            _window_instance.deleteLater()
        except RuntimeError:
            pass
        _window_instance = None

    parent = maya_main_window()
    _window_instance = LocatorCreatorWindow(parent=parent)

    if parent is not None:
        _window_instance.setWindowFlags(_window_instance.windowFlags() | QtCore.Qt.Window)
        _window_instance.show()
    else:
        _window_instance.show()

    return _window_instance


if __name__ == "__main__":
    show_window()
