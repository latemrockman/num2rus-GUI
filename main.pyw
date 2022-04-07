import sys
from num2rus import num2rus
from PyQt5 import QtCore, QtGui, QtWidgets
from form import *

class MyWin(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.lib_val1 = {
            "a": ("целых", "рублей", "долларов", "евро"),
            "b": ("целая", "рубль", "доллар", "евро"),
            "c": ("целых", "рубля", "доллара", "евро"),
            "d": ("целых", "рублей", "долларов", "евро")}
        self.lib_sot = {
            "a": ("десятых", "сотых", "тысячных", "десятитысячных", "стотысячных"),
            "b": ("десятая", "сотая", "тысячная", "десятитысячная", "стотысячная"),
            "c": ("десятых", "сотых", "тысячных", "десятитысячных", "стотысячных"),
            "d": ("десятых", "сотых", "тысячных", "десятитысячных", "стотысячных")}

        self.whole = ""
        self.fractional = ""
        self.val1 = "val1"
        self.val2 = "val2"

        self.ui.lineEdit.textEdited.connect(self.Check)
        self.ui.comboCurrency.currentIndexChanged.connect(self.Currency)
        self.ui.comboDischarge.currentIndexChanged.connect(self.Check)

    # устанавливает соотношение комбобоксов:
    def Currency(self):
        # если не "простые числа", то установить разрядность "сотые" и заблокировать комбо
        if self.ui.comboCurrency.currentText() == "Просто число":
            self.ui.comboDischarge.setCurrentIndex(0)
            self.ui.comboDischarge.setEnabled(True)
        else:
            self.ui.comboDischarge.setCurrentIndex(2)
            self.ui.comboDischarge.setEnabled(False)
        self.Check()
    # все проверки, приводит текст к нужному формату:
    def Check(self):
        self.text = self.ui.lineEdit.text()

        # блокирует все кроме цифр и точек/запятых
        if self.text:
            for i in self.text:
                if i not in "0123456789.,":
                    self.text = self.text.replace(i, "")
                    self.ui.lineEdit.setText(self.text)
        else:
            self.ui.plainTextEdit.clear()


        # заменяем все точки на запятые
        if "." in self.text:
            self.text = self.text.replace(".",",")
            self.ui.lineEdit.setText(self.text)

        # если ограничение только целые числа, то не даем ставить запятую
        if self.ui.comboDischarge.currentIndex() == 0:
            self.text = self.text.replace(",","")
            self.ui.lineEdit.setText(self.text)

        # не даем поставить вторую запятую
        while self.text.count(",") > 1:
            self.text = self.text[::-1].replace(",", "", 1)
            self.text = self.text[::-1]
            self.ui.lineEdit.setText(self.text)

        # если первый символ запятая, то поставить ноль в начало строки
        if len(self.text) != 0 and self.text[0] == ",":
            self.text = "0" + self.text
            self.ui.lineEdit.setText(self.text)

        # если пусто то ничего не делает
        if self.text != "":
            self.transfer()
    # контролирует кол-во знаков после запятой:
    def CheckDischarge(self):
        self.text = self.ui.lineEdit.text()
        if "," in self.text:
            self.comma = self.text.find(",") + 1
            self.after_comma = self.ui.comboDischarge.currentIndex()

            self.text = self.text[:self.comma+self.after_comma]
            self.ui.lineEdit.setText(self.text)
    # исключения одна/две
    def exception(self):
        self.res_text = self.ui.plainTextEdit.toPlainText().lower()
        self.lib_exc = {
            1: ("целая", "десятая", "сотая", "тысячная", "десятитысячная", "стотысячная", "копейка"),
            2: ("целых", "десятых", "сотых", "тысячных", "десятитысячных", "стотысячных", "копейки")}

        for i in self.lib_exc[1]:
            self.exc1 = "один " + i
            if self.exc1 in self.res_text:
                self.res_text = self.res_text.replace(self.exc1, "одна " + i)
        for i in self.lib_exc[2]:
            self.exc2 = "два " + i
            if self.exc2 in self.res_text:
                self.res_text = self.res_text.replace(self.exc2, "две " + i)

        if "," in self.text and self.text[::-1].find(",") == 1 and self.ui.comboCurrency.currentIndex() != 0:
            self.mlist[1] = self.mlist[1] + "0"

        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.appendPlainText(self.res_text.capitalize())
    # перевод цифр в текст и вывод результата:
    def transfer(self):
        self.ui.plainTextEdit.clear()
        self.text = self.ui.lineEdit.text()

        self.unit_m()

        if "," in self.text:
            self.CheckDischarge()
            self.nlist = self.text.split(",")
            if self.nlist[1] == "":
                self.nlist[1] = "0"
            if self.text[::-1].find(",") == 1 and self.ui.comboCurrency.currentIndex() != 0:
                self.nlist[1] = self.nlist[1] + "0"

            self.whole = num2rus(int(self.nlist[0]))
            self.fractional = num2rus(int(self.nlist[1]))
            self.ui.plainTextEdit.appendPlainText(f"{self.whole.capitalize()} {self.val1} {self.fractional} {self.val2}")
        else:
            self.whole = int(self.ui.lineEdit.text())
            self.whole = num2rus(self.whole).capitalize()
            self.ui.plainTextEdit.appendPlainText(f"{self.whole} {self.val1}")

        self.exception()

        if "," in self.text and self.text[::-1].find(",") == 1 and self.ui.comboCurrency.currentIndex() != 0:
            self.text = self.text + "0"
            self.ui.lineEdit.setText(self.text)
            self.ui.lineEdit.setCursorPosition(self.comma+1)

        if "," in self.text and self.text[::-1].find(",") == 2 and self.ui.comboCurrency.currentIndex() != 0 and self.text[-2:] == "00":
            self.text = self.text[:-1]
            self.ui.lineEdit.setText(self.text)
    # склонение:
    def unit_m(self):
        self.CheckDischarge()
        self.text = self.ui.lineEdit.text()
        self.mlist = []

        # создание списка mlist
        if "," in self.text:
            self.mlist = self.text.split(",")
            if len(self.mlist[1]) == 0:
                self.mlist[1] = "0"
            if self.text[::-1].find(",") == 1 and self.ui.comboCurrency.currentIndex() != 0:
                self.mlist[1] = self.mlist[1] + "0"
        else:
            self.mlist.append(self.text)

        self.end1 = int(self.mlist[0][-1])   # последняя цифра целой части
        self.end2 = int(self.mlist[0][-2:])  # последние 2 цифры целой части
        self.ed = self.ui.comboCurrency.currentIndex()
        self.ed1 = self.ui.comboDischarge.currentIndex()

        # склонение целой части
        if self.end1 == 1:
            self.group_ed1 = "b"
        if self.end1 >= 2 and self.end1 <= 4:
            self.group_ed1 = "c"
        if self.end1 >= 5 and self.end1 <= 9 or self.end1 == 0:
            self.group_ed1 = "d"
        if self.end2 >= 10 and self.end2 <= 20:
            self.group_ed1 = "a"

        # результат склонения целой части
        if self.ui.comboDischarge.currentIndex() == 0:
            self.val1 = ""
        else:
            self.val1 = self.lib_val1[self.group_ed1][self.ed]

        # склонение дробной части:
        if "," in self.text:
            self.end11 = int(self.mlist[1][-1])  # последняя цифра дробной части
            self.end22 = int(self.mlist[1][-2:])  # последние 2 цифры дробной части

            if self.end11 == 1:
                self.group_ed2 = "b"
            if self.end11 >= 2 and self.end11 <= 4:
                self.group_ed2 = "c"
            if self.end11 >= 5 and self.end11 <= 9 or self.end11 == 0:
                self.group_ed2 = "d"
            if len(self.mlist[1]) >= 2 and self.end22 >= 10 and self.end22 <= 20:
                self.group_ed2 = "a"

            self.lib_val2 = {
                "a": (self.lib_sot["a"][len(self.mlist[1])-1], "копеек", "центов", "евроцентов"),
                "b": (self.lib_sot["b"][len(self.mlist[1])-1], "копейка", "цент", "евроцент"),
                "c": (self.lib_sot["c"][len(self.mlist[1])-1], "копейки", "цента", "евроцента"),
                "d": (self.lib_sot["d"][len(self.mlist[1])-1], "копеек", "центов", "евроцентов")}

            self.val2 = self.lib_val2[self.group_ed2][self.ed]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())

