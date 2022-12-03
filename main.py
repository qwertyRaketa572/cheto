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
        self.new = False

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee WHERE id=?", (item_id := self.spinBox.text(),)).fetchall()
        self.tw.setRowCount(len(result))
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
            quer = "INSERT INTO coffee VALUES("
            quen = "UPDATE coffee SET\n"

            if self.new:
                que = quer + ", ".join([f"'{self.modified.get(key)}'"
                for key in self.modified.keys()])
                que += ")"
                print(que)
                res = cur.execute("""SELECT * FROM coffee""").fetchall()
                cur.execute(que)
            else:
                que = quen + ", ".join([f"{key}='{self.modified.get(key)}'"
                for key in self.modified.keys()])
                que += "WHERE id = ?"
                print(que)
                cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()

    def create_new(self):
        cur = self.con.cursor()
        self.tw.setColumnCount(7)
        self.tw.setRowCount(1)
        self.titles = ['ID', 'sort', 'degree_of_roasting', 'ground_in_grains', 'taste_description', 'price', 'packing_volume']
        for j in range(7):
            self.tw.setItem(1, j, QTableWidgetItem(''))
        self.new = True
        self.modified = {}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
