import sys
import pymorphy2
import random
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow

morph = pymorphy2.MorphAnalyzer()

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('wordleGUI.ui', self)
        self.addButton.clicked.connect(self.add_word)
        self.step = 0
        spisok = ["ангел", "понос","лодка","остов","кошка","химия","физик","совет","свеча","поток","пенал","бебра","ножны","бобёр","живот","ложка","отдел","право","устой","обувь", ]
        self.zagadka = spisok[random.randint(0, len(spisok) - 1)]
    
    def add_word(self):
        word = self.wordLine.text()
        if self.check_word(word):
            self.write_word(word)
            if self.check_win(word):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Игра закончена!")
                msg.setText("Победа! Молодец, возьми с полки пирожок")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
                self.close()
            if self.next_step():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Игра закончена")
                msg.setText("Ваши попытки закончились")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec()
                self.close()
        
    def check_word(self, word):
        analyz = str(morph.parse(word))
        if 'FakeDictionary()' in analyz or 'UnknownPrefixAnalyzer' in analyz :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Ошибка")
            msg.setText("Такого слова не существует!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        elif len(word) != 5:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Ошибка")
            msg.setText("Слово не из 5 букв!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        elif 'NOUN' not in analyz:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Ошибка")
            msg.setText("Это не существительное!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        else:
            return True
    def write_word(self, word):
        for ind, char in enumerate(word):
            if char.lower() in self.zagadka:
                if char.lower() == self.zagadka[ind]:
                    eval("""self.letterbutton_{0}.setStyleSheet("background-color: yellow; font: 75 22pt 'MS Shell Dlg 2'")""".format(self.step * 5 + ind + 1))
                    eval("self.letterbutton_{0}.setText(char.upper())".format((self.step * 5 + ind + 1)))
                else:
                    eval("""self.letterbutton_{0}.setStyleSheet("background-color: lime; font: 75 22pt 'MS Shell Dlg 2'")""".format(self.step * 5 + ind + 1))
                    eval("self.letterbutton_{0}.setText(char.upper())".format((self.step * 5 + ind + 1)))
            else:
                eval("""self.letterbutton_{0}.setStyleSheet("background-color: gray; font: 75 22pt 'MS Shell Dlg 2'; color: white")""".format(self.step * 5 + ind + 1))
                eval("self.letterbutton_{0}.setText(char.upper())".format((self.step * 5 + ind + 1)))
    
    def next_step(self):
        for i in range(1,6):
            eval("self.letterbutton_{0}.setEnabled(False)".format(self.step * 5 + i))
        self.step += 1
        if self.step >= 6:
            return True
        for i in range(1,6):
            eval("self.letterbutton_{0}.setEnabled(True)".format(self.step * 5 + i))
    
    def check_win(self, word):
        for ind, char in enumerate(word.lower()):
            if char != self.zagadka[ind]:
                return False
        else:
            return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
 