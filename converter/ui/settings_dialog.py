from __future__ import annotations
from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
)


def _form_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("FormLabel")
    return lbl


class SettingsDialog(QDialog):
    def __init__(self, settings: QSettings, max_concurrency: int, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(440)
        self._settings = settings

        title = QLabel("Preferences")
        title.setObjectName("SectionTitle")
        subtitle = QLabel("Personalize how Splash looks and runs.")
        subtitle.setObjectName("SectionSubtitle")

        self._theme = QComboBox()
        self._theme.addItems(["Dark", "Light"])
        self._theme.setCurrentText(
            "Dark" if settings.value("theme", "dark") == "dark" else "Light"
        )

        self._conc = QSpinBox()
        self._conc.setRange(1, max(1, max_concurrency))
        self._conc.setValue(int(settings.value("concurrency", max(1, max_concurrency // 2))))

        hint = QLabel(f"Up to {max_concurrency} concurrent conversions on this machine.")
        hint.setObjectName("Hint")

        theme_row = QVBoxLayout()
        theme_row.setSpacing(6)
        theme_row.addWidget(_form_label("Theme"))
        theme_row.addWidget(self._theme)

        conc_row = QVBoxLayout()
        conc_row.setSpacing(6)
        conc_row.addWidget(_form_label("Parallel conversions"))
        conc_row.addWidget(self._conc)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        ok = buttons.button(QDialogButtonBox.StandardButton.Ok)
        if ok is not None:
            ok.setObjectName("Primary")
            ok.setText("Save")
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addLayout(theme_row)
        layout.addLayout(conc_row)
        layout.addWidget(hint)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(buttons)
        layout.addLayout(btn_row)

    def _save(self) -> None:
        self._settings.setValue("theme", "dark" if self._theme.currentText() == "Dark" else "light")
        self._settings.setValue("concurrency", self._conc.value())
        self.accept()
