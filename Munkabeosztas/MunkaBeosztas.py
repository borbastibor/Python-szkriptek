# -*- coding: <utf-8> -*-
#------------------------------------------------------------------------------#
# MunkaBeosztas
# Egy OneDrive-on tárolt excel állományból kinyert adatokat jelenít meg
# táblázatos formában. Az adatokat beállított időközönként és időintervallumban
# frissíti.
#
# Felhasznált függvénykönyvátrak:
# PyQt5 - felhasználói felület, időzítő
# openpyxl - .xlsx állományok kezelése
#
# Borbás Tibor
# 2019. augusztus 15.
#------------------------------------------------------------------------------#

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime
from openpyxl import load_workbook
from enum import Enum

# Hány sort és oszlopot jelenítsen meg?
ROW_COUNT = 49
COL_COUNT = 8

# Milyen sűrűn frissítse az adatokat?
# percet kell megadni
UPD_INTERVAL = 1

# Milyen idő intervallumon frissítsen egy napon belül?
# Órát kell megadni
# Az érték intervalluma: 0 <= érték < 24
UPD_START = 6
UPD_END = 23

# Mutassa a horizontális és vertikális fejlécet?
SHOW_HHEADER = True
SHOW_VHEADER = False

# Font stílusok
FONT_SIZE = 9

NORMAL_FONT = QFont()
NORMAL_FONT.setFamily("Arial")
NORMAL_FONT.setPixelSize(FONT_SIZE)

COLHEAD_FONT = QFont()
COLHEAD_FONT.setFamily("Arial")
COLHEAD_FONT.setPixelSize(FONT_SIZE)
COLHEAD_FONT.setBold(True)
COLHEAD_FONT.setItalic(True)

ROWHEAD_FONT = QFont()
ROWHEAD_FONT.setFamily("Arial")
ROWHEAD_FONT.setPixelSize(FONT_SIZE)
ROWHEAD_FONT.setBold(True)

# Színek
SATDAY_BRUSH = QBrush(QColor(0,180,0,255),Qt.SolidPattern)
SUNDAY_BRUSH = QBrush(QColor(180,0,0,255),Qt.SolidPattern)

# Az applikáció osztálya
class App(QWidget):
    # Az osztály inicializálása
    def __init__(self):
        super().__init__()
        self.title = "Munka beosztás"
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.timer = QTimer()
        self.initUI()

    # Felhasználói felület létrehozása
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.createTable()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.showFullScreen()
        self.update()
        self.timer.setInterval(UPD_INTERVAL * 60000)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    # Táblázat létrehozása
    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(ROW_COUNT)
        self.tableWidget.setColumnCount(COL_COUNT)
        hHeader = self.tableWidget.horizontalHeader()
        hHeader.setFont(NORMAL_FONT)
        hHeader.setStretchLastSection(True)
        hHeader.setVisible(SHOW_HHEADER)
        self.tableWidget.setHorizontalHeader(hHeader)
        vHeader = self.tableWidget.verticalHeader()
        vHeader.setFont(NORMAL_FONT)
        vHeader.setVisible(SHOW_VHEADER)
        self.tableWidget.setVerticalHeader(vHeader)
        self.tableWidget.move(0,0)
    
    # Táblázatban lévő adatok frissítése és formázása
    def refreshData(self):
        wbook = load_workbook("munkabeosztas.xlsm",read_only=True,keep_vba=True,data_only=True)
        wsheet = wbook["07.15-21"]
        i = 0
        for row in wsheet.values:
            j = 0
            for value in row:
                item = QTableWidgetItem(value)
                if i == 0:
                    item.setFont(COLHEAD_FONT)
                    item.setTextAlignment(Qt.AlignCenter)
                if j == 0:
                    item.setFont(ROWHEAD_FONT)
                    item.setTextAlignment(Qt.AlignCenter)
                if i!=0 and j!=0: item.setFont(NORMAL_FONT)
                if j == 6 and i < 44: item.setBackground(SATDAY_BRUSH)
                if j == 7 and i < 44: item.setBackground(SUNDAY_BRUSH)
                self.tableWidget.setItem(i,j,item)
                j = j + 1
            i = i + 1
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    # Frissítést vezérlő eljárás - az időzítő hívja meg
    def update(self):
        tick = datetime.now()
        if tick.hour >= UPD_START or tick.hour < UPD_END:
            self.refreshData()
            self.setWindowTitle(self.title + " - Frissítve: " + tick.strftime("%Y-%m-%d %H:%M"))

# A főprogram
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
