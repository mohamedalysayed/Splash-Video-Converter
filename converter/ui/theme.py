from __future__ import annotations

# Cast — iOS-inspired theme.
# Palette mirrors Apple's current system colors (iOS 17/18):
#   systemBlue  dark #0A84FF / light #007AFF
#   systemIndigo dark #5E5CE6 / light #5856D6
#   systemBackground, secondarySystemBackground, tertiarySystemBackground
#   label, secondaryLabel, tertiaryLabel, separator

_FONT_STACK = (
    '"SF Pro Display", "SF Pro Text", "-apple-system", '
    '"Inter", "Segoe UI Variable", "Segoe UI", '
    '"Helvetica Neue", "Cantarell", "Ubuntu", sans-serif'
)


DARK_QSS = f"""
* {{
    font-family: {_FONT_STACK};
    font-size: 17px;
    outline: 0;
}}

QMainWindow, QDialog {{
    background-color: #000000;
    color: #FFFFFF;
}}

QWidget#AppRoot {{
    background-color: #000000;
}}

QWidget#HeroBar {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #1C1C1E, stop:1 #0E0E10
    );
    border-bottom: 1px solid #2C2C2E;
}}
QLabel#AppWordmark {{
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
}}
QLabel#AppTagline {{
    color: #8E8E93;
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 0.1px;
}}
QLabel#AccentDot {{
    color: #0A84FF;
    font-size: 28px;
    font-weight: 800;
}}

QMenuBar {{
    background-color: #1C1C1E;
    color: #F2F2F7;
    padding: 4px 8px;
    border: none;
}}
QMenuBar::item {{
    padding: 6px 12px;
    background: transparent;
    border-radius: 8px;
    color: #F2F2F7;
}}
QMenuBar::item:selected {{ background-color: #2C2C2E; }}
QMenu {{
    background-color: #1C1C1E;
    color: #F2F2F7;
    border: 1px solid #2C2C2E;
    border-radius: 12px;
    padding: 6px;
}}
QMenu::item {{ padding: 8px 22px 8px 16px; border-radius: 8px; margin: 1px; }}
QMenu::item:selected {{ background-color: #0A84FF; color: #FFFFFF; }}
QMenu::separator {{ height: 1px; background: #2C2C2E; margin: 6px 4px; }}

QLabel {{ color: #F2F2F7; }}
QLabel#SectionTitle {{
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.2px;
}}
QLabel#SectionSubtitle {{
    color: #8E8E93;
    font-size: 15px;
    font-weight: 500;
}}
QLabel#Hint {{ color: #8E8E93; font-size: 15px; font-weight: 500; }}
QLabel#FormLabel {{
    color: #98989E;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}}

QFrame#Card {{
    background-color: #1C1C1E;
    border: 1px solid #2C2C2E;
    border-radius: 18px;
}}
QFrame#Card[elevated="true"] {{
    background-color: #2C2C2E;
    border: 1px solid #3A3A3C;
}}

QPushButton {{
    background-color: #2C2C2E;
    color: #F2F2F7;
    border: 1px solid #3A3A3C;
    border-radius: 12px;
    padding: 11px 22px;
    font-weight: 600;
    font-size: 17px;
    min-height: 22px;
}}
QPushButton:hover {{ background-color: #3A3A3C; border-color: #48484A; }}
QPushButton:pressed {{ background-color: #1C1C1E; }}
QPushButton:disabled {{ color: #48484A; background-color: #1C1C1E; border-color: #2C2C2E; }}

QPushButton#Primary {{
    background-color: #0A84FF;
    color: #FFFFFF;
    border: 1px solid #0A84FF;
    padding: 14px 30px;
    border-radius: 14px;
    font-size: 18px;
    font-weight: 700;
}}
QPushButton#Primary:hover {{ background-color: #1F94FF; border-color: #1F94FF; }}
QPushButton#Primary:pressed {{ background-color: #006FE6; border-color: #006FE6; }}
QPushButton#Primary:disabled {{
    background-color: #1C3E68; border-color: #1C3E68; color: #6C94C4;
}}

QPushButton#Danger {{
    background-color: #FF453A;
    color: #FFFFFF;
    border: 1px solid #FF453A;
}}
QPushButton#Danger:hover {{ background-color: #FF6259; border-color: #FF6259; }}
QPushButton#Danger:pressed {{ background-color: #E53729; border-color: #E53729; }}

QPushButton#Ghost {{
    background-color: transparent;
    color: #0A84FF;
    border: none;
    font-weight: 600;
}}
QPushButton#Ghost:hover {{ color: #1F94FF; background-color: #14243A; border-radius: 10px; }}

QComboBox, QLineEdit, QSpinBox {{
    background-color: #1C1C1E;
    color: #F2F2F7;
    border: 1px solid #2C2C2E;
    border-radius: 12px;
    padding: 11px 16px;
    min-height: 24px;
    selection-background-color: #0A84FF;
    selection-color: #FFFFFF;
}}
QComboBox:hover, QLineEdit:hover, QSpinBox:hover {{ border-color: #3A3A3C; }}
QComboBox:focus, QLineEdit:focus, QSpinBox:focus {{ border-color: #0A84FF; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox::down-arrow {{
    image: none;
    width: 0px; height: 0px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #8E8E93;
    margin-right: 10px;
}}
QComboBox QAbstractItemView {{
    background-color: #1C1C1E;
    color: #F2F2F7;
    border: 1px solid #2C2C2E;
    border-radius: 12px;
    padding: 6px;
    selection-background-color: #0A84FF;
    selection-color: #FFFFFF;
}}
QSpinBox::up-button, QSpinBox::down-button {{ width: 18px; border: none; background: transparent; }}

QCheckBox {{ color: #F2F2F7; spacing: 10px; font-weight: 500; }}
QCheckBox::indicator {{
    width: 22px; height: 22px;
    border-radius: 11px;
    border: 1px solid #3A3A3C;
    background-color: #2C2C2E;
}}
QCheckBox::indicator:hover {{ border-color: #48484A; }}
QCheckBox::indicator:checked {{
    background-color: #0A84FF;
    border: 1px solid #0A84FF;
}}
QCheckBox::indicator:checked:hover {{ background-color: #1F94FF; border-color: #1F94FF; }}

QTableView {{
    background-color: #1C1C1E;
    alternate-background-color: #1C1C1E;
    gridline-color: transparent;
    border: none;
    border-radius: 14px;
    selection-background-color: #0A84FF;
    selection-color: #FFFFFF;
    color: #F2F2F7;
}}
QHeaderView::section {{
    background-color: transparent;
    color: #98989E;
    padding: 10px 12px;
    border: none;
    border-bottom: 1px solid #2C2C2E;
    font-weight: 600;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1.1px;
}}
QTableView::item {{ padding: 10px 6px; border-bottom: 1px solid #2C2C2E; }}
QTableCornerButton::section {{ background: transparent; border: none; }}

QProgressBar {{
    background-color: #2C2C2E;
    border: none;
    border-radius: 7px;
    text-align: center;
    color: #FFFFFF;
    font-weight: 600;
    font-size: 13px;
    height: 18px;
}}
QProgressBar::chunk {{
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #0A84FF, stop:1 #5E5CE6
    );
    border-radius: 7px;
}}

QFrame#DropZone {{
    background-color: #1C1C1E;
    border: 2px dashed #3A3A3C;
    border-radius: 20px;
}}
QFrame#DropZone[dragover="true"] {{
    border: 2px dashed #0A84FF;
    background-color: #0E2444;
}}
QLabel#DropIcon {{
    color: #0A84FF;
    font-size: 56px;
    font-weight: 300;
}}
QLabel#DropTitle {{
    color: #FFFFFF;
    font-size: 23px;
    font-weight: 700;
    letter-spacing: -0.3px;
}}
QLabel#DropHint {{ color: #8E8E93; font-size: 16px; font-weight: 500; }}

QScrollBar:vertical {{ background: transparent; width: 10px; margin: 4px 2px; }}
QScrollBar::handle:vertical {{
    background: #48484A;
    border-radius: 5px;
    min-height: 28px;
}}
QScrollBar::handle:vertical:hover {{ background: #636366; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px 4px; }}
QScrollBar::handle:horizontal {{
    background: #48484A; border-radius: 5px; min-width: 28px;
}}
QScrollBar::handle:horizontal:hover {{ background: #636366; }}
QScrollBar::add-line, QScrollBar::sub-line {{
    height: 0px; width: 0px; border: none; background: transparent;
}}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}

QStatusBar {{
    background-color: #0E0E10;
    color: #8E8E93;
    border-top: 1px solid #2C2C2E;
    font-size: 14px;
    font-weight: 500;
    padding: 5px 12px;
}}
QStatusBar::item {{ border: none; }}

QToolTip {{
    background-color: #2C2C2E;
    color: #F2F2F7;
    border: 1px solid #3A3A3C;
    border-radius: 8px;
    padding: 7px 12px;
    font-size: 14px;
}}

QLabel#Pill {{
    background: #2C2C2E;
    color: #F2F2F7;
    padding: 5px 14px;
    border-radius: 11px;
    font-weight: 600;
    font-size: 14px;
}}
"""


LIGHT_QSS = f"""
* {{
    font-family: {_FONT_STACK};
    font-size: 17px;
    outline: 0;
}}

QMainWindow, QDialog {{
    background-color: #F2F2F7;
    color: #000000;
}}

QWidget#AppRoot {{
    background-color: #F2F2F7;
}}

QWidget#HeroBar {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFFFFF, stop:1 #F2F2F7
    );
    border-bottom: 1px solid #D1D1D6;
}}
QLabel#AppWordmark {{
    color: #000000;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
}}
QLabel#AppTagline {{
    color: #6D6D72;
    font-size: 16px;
    font-weight: 500;
}}
QLabel#AccentDot {{
    color: #007AFF;
    font-size: 28px;
    font-weight: 800;
}}

QMenuBar {{
    background-color: #FFFFFF;
    color: #1C1C1E;
    padding: 4px 8px;
    border: none;
}}
QMenuBar::item {{ padding: 6px 12px; background: transparent; border-radius: 8px; }}
QMenuBar::item:selected {{ background-color: #E5E5EA; }}
QMenu {{
    background-color: #FFFFFF;
    color: #1C1C1E;
    border: 1px solid #D1D1D6;
    border-radius: 12px;
    padding: 6px;
}}
QMenu::item {{ padding: 8px 22px 8px 16px; border-radius: 8px; margin: 1px; }}
QMenu::item:selected {{ background-color: #007AFF; color: #FFFFFF; }}
QMenu::separator {{ height: 1px; background: #D1D1D6; margin: 6px 4px; }}

QLabel {{ color: #1C1C1E; }}
QLabel#SectionTitle {{
    color: #000000;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.2px;
}}
QLabel#SectionSubtitle {{ color: #6D6D72; font-size: 15px; font-weight: 500; }}
QLabel#Hint {{ color: #6D6D72; font-size: 15px; font-weight: 500; }}
QLabel#FormLabel {{
    color: #3A3A3C;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}}

QFrame#Card {{
    background-color: #FFFFFF;
    border: 1px solid #E5E5EA;
    border-radius: 18px;
}}
QFrame#Card[elevated="true"] {{
    background-color: #FFFFFF;
    border: 1px solid #D1D1D6;
}}

QPushButton {{
    background-color: #FFFFFF;
    color: #1C1C1E;
    border: 1px solid #D1D1D6;
    border-radius: 12px;
    padding: 11px 22px;
    font-weight: 600;
    font-size: 17px;
    min-height: 22px;
}}
QPushButton:hover {{ background-color: #F2F2F7; border-color: #B0B0B5; }}
QPushButton:pressed {{ background-color: #E5E5EA; }}
QPushButton:disabled {{ color: #AEAEB2; background-color: #F2F2F7; border-color: #E5E5EA; }}

QPushButton#Primary {{
    background-color: #007AFF;
    color: #FFFFFF;
    border: 1px solid #007AFF;
    padding: 14px 30px;
    border-radius: 14px;
    font-size: 18px;
    font-weight: 700;
}}
QPushButton#Primary:hover {{ background-color: #1C88FF; border-color: #1C88FF; }}
QPushButton#Primary:pressed {{ background-color: #0066D6; border-color: #0066D6; }}
QPushButton#Primary:disabled {{
    background-color: #B9D8FF; border-color: #B9D8FF; color: #FFFFFF;
}}

QPushButton#Danger {{
    background-color: #FF3B30;
    color: #FFFFFF;
    border: 1px solid #FF3B30;
}}
QPushButton#Danger:hover {{ background-color: #FF5148; border-color: #FF5148; }}
QPushButton#Danger:pressed {{ background-color: #D9291F; border-color: #D9291F; }}

QPushButton#Ghost {{
    background-color: transparent;
    color: #007AFF;
    border: none;
    font-weight: 600;
}}
QPushButton#Ghost:hover {{ color: #1C88FF; background-color: #E5F0FF; border-radius: 10px; }}

QComboBox, QLineEdit, QSpinBox {{
    background-color: #FFFFFF;
    color: #1C1C1E;
    border: 1px solid #D1D1D6;
    border-radius: 12px;
    padding: 11px 16px;
    min-height: 24px;
    selection-background-color: #007AFF;
    selection-color: #FFFFFF;
}}
QComboBox:hover, QLineEdit:hover, QSpinBox:hover {{ border-color: #B0B0B5; }}
QComboBox:focus, QLineEdit:focus, QSpinBox:focus {{ border-color: #007AFF; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox::down-arrow {{
    image: none;
    width: 0px; height: 0px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #6D6D72;
    margin-right: 10px;
}}
QComboBox QAbstractItemView {{
    background-color: #FFFFFF;
    color: #1C1C1E;
    border: 1px solid #D1D1D6;
    border-radius: 12px;
    padding: 6px;
    selection-background-color: #007AFF;
    selection-color: #FFFFFF;
}}

QCheckBox {{ color: #1C1C1E; spacing: 10px; font-weight: 500; }}
QCheckBox::indicator {{
    width: 22px; height: 22px;
    border-radius: 11px;
    border: 1px solid #C7C7CC;
    background-color: #FFFFFF;
}}
QCheckBox::indicator:hover {{ border-color: #B0B0B5; }}
QCheckBox::indicator:checked {{
    background-color: #007AFF;
    border: 1px solid #007AFF;
}}

QTableView {{
    background-color: #FFFFFF;
    alternate-background-color: #FFFFFF;
    gridline-color: transparent;
    border: none;
    border-radius: 14px;
    selection-background-color: #007AFF;
    selection-color: #FFFFFF;
    color: #1C1C1E;
}}
QHeaderView::section {{
    background-color: transparent;
    color: #6D6D72;
    padding: 10px 12px;
    border: none;
    border-bottom: 1px solid #E5E5EA;
    font-weight: 600;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1.1px;
}}
QTableView::item {{ padding: 10px 6px; border-bottom: 1px solid #E5E5EA; }}

QProgressBar {{
    background-color: #E5E5EA;
    border: none;
    border-radius: 7px;
    text-align: center;
    color: #1C1C1E;
    font-weight: 600;
    font-size: 13px;
    height: 18px;
}}
QProgressBar::chunk {{
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #007AFF, stop:1 #5856D6
    );
    border-radius: 7px;
}}

QFrame#DropZone {{
    background-color: #FFFFFF;
    border: 2px dashed #C7C7CC;
    border-radius: 20px;
}}
QFrame#DropZone[dragover="true"] {{
    border: 2px dashed #007AFF;
    background-color: #E5F0FF;
}}
QLabel#DropIcon {{
    color: #007AFF;
    font-size: 56px;
    font-weight: 300;
}}
QLabel#DropTitle {{
    color: #000000;
    font-size: 23px;
    font-weight: 700;
    letter-spacing: -0.3px;
}}
QLabel#DropHint {{ color: #6D6D72; font-size: 16px; font-weight: 500; }}

QScrollBar:vertical {{ background: transparent; width: 10px; margin: 4px 2px; }}
QScrollBar::handle:vertical {{
    background: #C7C7CC; border-radius: 5px; min-height: 28px;
}}
QScrollBar::handle:vertical:hover {{ background: #AEAEB2; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px 4px; }}
QScrollBar::handle:horizontal {{
    background: #C7C7CC; border-radius: 5px; min-width: 28px;
}}
QScrollBar::handle:horizontal:hover {{ background: #AEAEB2; }}
QScrollBar::add-line, QScrollBar::sub-line {{
    height: 0px; width: 0px; border: none; background: transparent;
}}
QScrollBar::add-page, QScrollBar::sub-page {{ background: transparent; }}

QStatusBar {{
    background-color: #FFFFFF;
    color: #6D6D72;
    border-top: 1px solid #E5E5EA;
    font-size: 14px;
    font-weight: 500;
    padding: 5px 12px;
}}
QStatusBar::item {{ border: none; }}

QToolTip {{
    background-color: #FFFFFF;
    color: #1C1C1E;
    border: 1px solid #D1D1D6;
    border-radius: 8px;
    padding: 7px 12px;
    font-size: 14px;
}}

QLabel#Pill {{
    background: #E5E5EA;
    color: #1C1C1E;
    padding: 5px 14px;
    border-radius: 11px;
    font-weight: 600;
    font-size: 14px;
}}
"""


def qss(theme: str) -> str:
    return DARK_QSS if theme == "dark" else LIGHT_QSS
