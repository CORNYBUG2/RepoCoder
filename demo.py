import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QTextCursor, QFont

# ---- IMPORT YOUR SYSTEM ----
from iterative.iteration_controller import IterationController
from generator.prompt_builder import PromptBuilder
from generator.llm_generator import LLMGenerator

retriever = None
builder = PromptBuilder()
generator = LLMGenerator()

controller = IterationController(
    retriever,
    builder,
    generator,
    mode="completion"
)
# ----------------------------------


class CodeEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---- BIGGER FONT (REAL FIX) ----
        font = QFont("Consolas")
        font.setPointSize(18)
        self.setFont(font)
        self.setCursorWidth(3)

        # ---- ghost tracking ----
        self.ghost_text = ""
        self.ghost_start = None
        self.ghost_end = None
        self.is_inserting_ghost = False

        # ---- timer ----
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.generate)

        self.textChanged.connect(self.on_text_change)

    # -------- typing --------
    def on_text_change(self):
        if self.is_inserting_ghost:
            return

        self.timer.start(1200)

    # -------- generate --------
    def generate(self):
        code = self.toPlainText()

        if not code.strip():
            return

        self.clear_ghost()

        suggestion = controller.run(code)

        if suggestion:
            self.insert_ghost(suggestion)

    # -------- insert ghost --------
    def insert_ghost(self, text):
        self.is_inserting_ghost = True

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)

        self.ghost_start = cursor.position()

        original_fmt = cursor.charFormat()

        ghost_fmt = cursor.charFormat()
        ghost_fmt.setForeground(QColor("#6a9955"))  # VS Code green
        ghost_fmt.setFontItalic(True)

        cursor.setCharFormat(ghost_fmt)
        cursor.insertText(text)

        self.ghost_end = cursor.position()
        self.ghost_text = text

        cursor.setCharFormat(original_fmt)

        self.is_inserting_ghost = False

    # -------- clear ghost --------
    def clear_ghost(self):
        if self.ghost_start is not None and self.ghost_end is not None:
            self.is_inserting_ghost = True

            cursor = self.textCursor()
            cursor.setPosition(self.ghost_start)
            cursor.setPosition(self.ghost_end, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()

            self.ghost_start = None
            self.ghost_end = None
            self.ghost_text = ""

            self.is_inserting_ghost = False

    # -------- key handling --------
    def keyPressEvent(self, event):
        # ACCEPT
        if event.key() == Qt.Key_Tab and self.ghost_text:
            cursor = self.textCursor()

            cursor.setPosition(self.ghost_start)
            cursor.setPosition(self.ghost_end, QTextCursor.KeepAnchor)

            fmt = cursor.charFormat()
            fmt.setForeground(QColor("#d4d4d4"))
            fmt.setFontItalic(False)

            cursor.setCharFormat(fmt)

            self.ghost_start = None
            self.ghost_end = None
            self.ghost_text = ""
            return

        # ignore control keys
        ignore_keys = {
            Qt.Key_Shift,
            Qt.Key_Control,
            Qt.Key_Alt,
            Qt.Key_CapsLock,
            Qt.Key_Left,
            Qt.Key_Right,
            Qt.Key_Up,
            Qt.Key_Down,
            Qt.Key_Escape,
        }

        if self.ghost_text and event.key() not in ignore_keys:
            self.clear_ghost()

        super().keyPressEvent(event)


class AIEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Code Assistant")

        # ---- VS CODE STYLE ----
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas;
            }

            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                padding: 12px;
                selection-background-color: #264f78;
            }

            QLabel {
                color: #569cd6;
                font-size: 22px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel("AI Code Assistant")
        layout.addWidget(title)

        self.editor = CodeEditor()
        self.editor.setPlaceholderText("Start typing your code...")
        layout.addWidget(self.editor)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIEditor()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())