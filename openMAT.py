#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import scipy.io
import re


pattern=r'([+-]?[0-9]+?[0-9]*)'

drec = []


# 最初のファイルを開く画面
class FirstWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.statusBar()
        
        # メニューバーのアイコン設定
        openFile = QAction('Open', self)
        # ショートカット設定
        openFile.setShortcut('Ctrl+O')
        # ステータスバー設定
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        # メニューバー作成
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        # 開くボタン
        obtn = QPushButton('Open', self)
        # Quitボタンをクリックしたら画面を閉じる
        obtn.clicked.connect(self.showDialog)
        obtn.resize(obtn.sizeHint())
        obtn.move(90, 50)

        # 終了ボタン
        qbtn = QPushButton('Quit', self)
        # Quitボタンをクリックしたら画面を閉じる
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(90, 110)

        self.setGeometry(200, 200, 250, 250)
        self.setWindowTitle('openMAT beta')
        # self.show()

        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        # fname[0]は選択したファイルのパス（ファイル名を含む）
        if fname[0]:
            global drec
            drec = fname[0]
            all_windows = allWindows()
            all_windows.show()

    def showDialog(self):

        # 第二引数はダイアログのタイトル、第三引数は表示するパス
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        # fname[0]は選択したファイルのパス（ファイル名を含む）
        if fname[0]:
            global drec
            drec = fname[0]
            all_windows = allWindows()
            all_windows.show()


# 最初の変数を表示するウインドウ
class allWindows(QWidget):
    def __init__(self, parent=None):
        super(allWindows, self).__init__(parent)
        self.w = QDialog(parent)
        # self.q = QDialog(parent)
        self.parent = parent

        matfile = scipy.io.loadmat(drec)
        data = list(matfile.keys())

        colcnt = 1
        rowcnt = len(data)-3
        self.tablewidget = QTableWidget(rowcnt, colcnt)
        self.tablewidget.move(100, 100)

        # ヘッダー設定
        horHeaders = ["variables"]
        self.tablewidget.setHorizontalHeaderLabels(horHeaders)
        verHeaders = []
        self.tablewidget.setVerticalHeaderLabels(verHeaders)

        # print(colcnt)
        # print(rowcnt)

        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)


        for m in range(rowcnt):
            item = QTableWidgetItem(str(data[m+3]))
            self.tablewidget.setItem(m, 0, item)

        # レイアウト
        layout = QHBoxLayout()
        layout.addWidget(self.tablewidget)
        self.w.setGeometry(300, 300, 1000, 500)
        self.w.setLayout(layout)
        self.w.setWindowTitle('openMAT bata - variables view')

        self.tablewidget.doubleClicked.connect(self.click)
        # self.tablewidget.horizontalHeader().sectionDoubleClicked.connect(self.click)

    @pyqtSlot()
    def click(self):
        print("\n")
        for currentQTableWidgetItem in self.tablewidget.selectedItems():
            # print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            fname = currentQTableWidgetItem.text()
            other_window = valWindow(currentQTableWidgetItem.text())
            other_window.show()

    def dc(self):
        print("ok")

    def show(self):
        self.w.exec_()


# 変数表示
class valWindow(QWidget):

    def __init__(self, arg, parent=None):
        self.w = QDialog(parent)
        self.parent = parent

        matfile = scipy.io.loadmat(drec)
        data = matfile[arg] # classに変数渡せてない

        colcnt = len(data[0])
        rowcnt = len(data)
        self.tablewidget = QTableWidget(rowcnt, colcnt)
        self.tablewidget.move(100, 100)

        #ヘッダー設定
        horHeaders = []
        self.tablewidget.setHorizontalHeaderLabels(horHeaders)
        verHeaders = []
        self.tablewidget.setVerticalHeaderLabels(verHeaders)


        #テーブルの中身作成
        for n in range(rowcnt):
            for m in range(colcnt):
                item = QTableWidgetItem(str(data[n][m]))
                self.tablewidget.setItem(n, m, item)

        # self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)


        #レイアウト
        layout = QHBoxLayout()
        layout.addWidget(self.tablewidget)
        self.w.setGeometry(500, 500, 1000, 500)
        self.w.setLayout(layout)
        self.w.setWindowTitle('openMAT')

    def show(self):
        self.w.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = FirstWidget()
    main_window.show()
    sys.exit(app.exec_())