import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from other import findAndReplace


class FindAndReplaceDlg(QDialog, findAndReplace.Ui_FindAndReplaceDlg):
    found = pyqtSignal(int)
    notfound = pyqtSignal(int)

    def __init__(self, text, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)
        self.__text = text
        self.__index = 0
        self.setupUi(self)
        # if not MAC:
        self.findButton.setFocusPolicy(Qt.NoFocus)
        self.replaceButton.setFocusPolicy(Qt.NoFocus)
        self.replaceAllButton.setFocusPolicy(Qt.NoFocus)
        self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.updateUi()

    @pyqtSlot(str)
    def on_findLineEdit_textEdited(self, text):
        self.__index = 0
        self.updateUi()

    def makeRegex(self):
        findText = self.findLineEdit.text()
        if findText == '*':
            findText = '.*'
        if self.syntaxComboBox.currentText() == "Literal":
            findText = re.escape(findText)
        flags = re.MULTILINE | re.DOTALL | re.UNICODE
        if not self.caseCheckBox.isChecked():
            flags |= re.IGNORECASE
        if self.wholeCheckBox.isChecked():
            findText = r"\b{}\b".format(findText)
        return re.compile(findText, flags)

    @pyqtSlot(bool)
    def on_findButton_clicked(self):
        regex = self.makeRegex()
        match = regex.search(self.__text, self.__index)
        if match is not None:
            self.__index = match.end()
            self.found.emit(match.start())
        else:
            self.notfound.emit(-1)

    @pyqtSlot(bool)
    def on_replaceButton_clicked(self):
        regex = self.makeRegex()
        self.__text = regex.sub(self.replaceLineEdit.text(),
                                self.__text, 1)

    @pyqtSlot(bool)
    def on_replaceAllButton_clicked(self):
        regex = self.makeRegex()
        self.__text = regex.sub(self.replaceLineEdit.text(),
                                self.__text)

    def updateUi(self):
        enable = bool(self.findLineEdit.text())
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)
        self.replaceAllButton.setEnabled(enable)

    def text(self):
        return self.__text

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    import sys

    text = """US experience shows that, unlike traditional patents,
    software patents do not encourage innovation and R&D, quite the
    contrary. In particular they hurt small and medium-sized enterprises
    and generally newcomers in the market. They will just weaken the market
    and increase spending on patents and litigation, at the expense of
    technological innovation and research. Especially dangerous are
    attempts to abuse the patent system by preventing interoperability as a
    means of avoiding competition with technological ability.
    --- Extract quoted from Linus Torvalds and Alan Cox's letter
    to the President of the European Parliament
    http://www.effi.org/patentit/patents_torvalds_cox.html"""


    def found(where):
        print("Found at {}".format(where))


    def nomore():
        print("No more found")


    app = QApplication(sys.argv)
    form = FindAndReplaceDlg(text)
    form.found.connect(found)
    form.notfound.connect(nomore)
    form.show()
    app.exec_()
    print(form.text())
