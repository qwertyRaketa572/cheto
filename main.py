import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.sqlite')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('coffee')
        model.select()

        self.pushButton.clicked.connect(self.nw)

        self.table.setModel(model)
        self.table.move(10, 10)
        self.table.resize(617, 315)

        self.show()

    def nw(self):
        self.nw = MyWidget2(self)
        self.nw.show()


class MyWidget2(QMainWindow):
    def __init__(self, ow):
        super().__init__()
        self.ow = ow
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.update_result)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.create_new)
        self.pushButton_4.clicked.connect(self.close)
        self.tw.itemChanged.connect(self.item_changed)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee WHERE id=?", (item_id := self.spinBox.text(),)).fetchall()
        self.tw.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tw.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tw.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
            for key in self.modified.keys()])
            que += "WHERE id = ?"
            print(que)
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()

    def create_new(self):
        cur = self.con.cursor()
        cur.execute("""INSERT INTO coffee VALUES (input(), input(), input(), input(), input(), input(), input())""")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
