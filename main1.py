from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap
import resources_rc
import traceback

from constant_window import Ui_CheckConstantWindow
from main_window import Ui_MainWindow
from pumpCalc_window import Ui_PumpCalcWindow
from about_window import Ui_AboutWindow
from new_item_window import Ui_DialogCreateNewItem

import sys
import pandas as pd

flag = ''
PASSWORD = '123'
user = 'Технолог'
MT_hidden = False
EZLine_hidden = False
REDA_hidden = False
Other_hidden = False

HOUSING_LENGTH_CODE = {
    '#10': 450, '#20': 850, '#30': 1230,
    '#40': 1555, '#50': 1930, '#60': 2210,
    '#70': 2650, '#80': 2930, '#90': 3600,
    '#100': 4000, '#110': 4590, '#120': 4950,
    '#130': 5620, '#140': 6020, '#150': 7500,
    '#160': 9000, '0.5' : 500, '1' : 1000,
    '1.5': 1500, '2': 2000, '2.5': 2500,
    '3' : 3000, '3.5': 3500, '4': 4000,
    '4.5': 4500, '5': 5000, '5.5': 5500,
    '6': 6000, '6.5': 6500, '7': 7000,
    '7.5': 7500, '8': 8000, '8.5': 8500,
    '9': 9000, '9.5': 9500, '10': 10000,
    }

'''
class - CamelCase
Method and func - lower_case_with_underscores or likeThatName
 global variable - _global_var_name
 Constants - CAP_WORDS'''

# class all_windows(QtWidgets.QMainWindow):
#
#     def __init__(self):
#         super(all_windows, self).__init__()
#         self.ui = Ui_PumpCalcWindow()   # Создать ui файл с шаблонным оформлением?
#         self.ui.setupUi(self)
#         #Как применить этот участок кода для всех окон?:
#         pixmap = QPixmap(':/images/logo.png')  # resource path starts with ':'
#         self.ui.putImageHere.setPixmap(pixmap)
#         self.ui.labelCurrentUser.setText(user)

class PutLogo():
    pass

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)

        self.put_a_logo(self.ui_main)
        self.initMainWindowButtons()
        # pixmap = QPixmap(':/images/logo.png')  # resource path starts with ':'
        # self.ui_main.putImageHere.setPixmap(pixmap)

    def put_a_logo(self, chosen_ui):
        '''Puts a logo in left top corner of a window.'''
        pixmap = QPixmap(':/images/logo.png')  # resource path starts with ':'
        chosen_ui.putImageHere.setPixmap(pixmap)

    def initMainWindowButtons(self):
        self.ui_main.pushButtonChekConstValues.clicked.connect(self.showConstantWindow)
        self.ui_main.pushButtonPumpCalc.clicked.connect(self.showPumpCalcWindow)
        self.ui_main.pushButtonAboutProg.clicked.connect(self.showAboutWindow)
        self.ui_main.pushButtonChiefTech.clicked.connect(self.changeUser)

    def showConstantWindow(self):
        '''Create and show ConstantWindow'''
        self.ui = ConstantWindow()
        self.ui.show()
        self.ui.closeConstantWindow()

    def showAboutWindow(self):
        '''Create and show About Window'''
        self.ui = AboutWindow()
        self.ui.show()
        self.ui.closeAboutWindow()

    def showPumpCalcWindow(self):
        '''Create and show PumpCalcWindow'''
        self.ui = PumpCalcWindow()
        self.ui.show()
        self.ui.closePumpCalcWindow()

    def changeUser(self):
        '''checks flag value and changes current user label in MainWindow'''
        global user
        global flag
        if self.ui_main.labelCurrentUser.text() == 'Технолог':
            self.dialog_password = ClssDialog()
            self.dialog_password.exec_()
            if flag == "Canceled":
                print('Canceled')
            elif flag == "Empty":
                print('Empty')
            elif flag == "Invalid Password":
                print('Access denied')
                # print(user)
            elif flag == "Valid Password":
                print('Ok')
                user = 'Главный технолог'
                self.ui_main.labelCurrentUser.setText('Главный технолог')
                flag = "Empty"
            else:
                print('smth went wrong when chek user flags. Current flag: ', flag )
        elif self.ui_main.labelCurrentUser.text() == 'Главный технолог':
            user = 'Технолог'
            self.ui_main.labelCurrentUser.setText('Технолог')
        else:
            print('smth went wrong. Wrong user type. Current user: ', user)


class ClssDialog(QtWidgets.QDialog):
    '''This class is responsible for password input dialog box operation
    Description of this dialog box is implemented 'on place' and not imported from other modules'''
    global flag

    def __init__(self, parent=None):
        super(ClssDialog, self).__init__(parent)
        #зачем здесь параметры ClssDialog, self; parent=none; parent?

        self.setWindowTitle("Авторизация")
        self.resize(508, 114)

        self.pushButtonCancel = QtWidgets.QPushButton(self)
        self.pushButtonCancel.setGeometry(QtCore.QRect(70, 80, 80, 25))
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.pushButtonCancel.setText("Отмена")
        self.pushButtonCancel.clicked.connect(self.btnClosed)

        self.pushButtonOk = QtWidgets.QPushButton(self)
        self.pushButtonOk.setGeometry(QtCore.QRect(340, 80, 80, 25))
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.pushButtonOk.setText("Ок")
        self.pushButtonOk.clicked.connect(self.btnOk)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(70, 20, 451, 17))
        self.label.setObjectName("label")
        self.label.setText("Введите пароль, чтобы получить права Главного технолога")

        self.lineEditPassword = QtWidgets.QLineEdit(self)
        self.lineEditPassword.setGeometry(QtCore.QRect(70, 50, 351, 23))
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)

    def btnClosed(self):
        '''This method describes what should happen if button Cancel is pressed in INputPassword window'''
        global flag
        flag = 'Canceled'
        self.close()

    def btnOk(self):
        '''This method describes what should happen if button OK is pressed in INputPassword window'''
        global flag
        if self.lineEditPassword.text() == PASSWORD:
            flag = 'Valid Password'
            self.close()
        else:
            flag = 'Invalid Password'
            dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                           "Неправильный пароль",
                                           "Вы ввели неправильный пароль!\nПопробуйте еще раз",
                                           buttons=QtWidgets.QMessageBox.Ok,
                                           parent=self)
            dialog.exec_()

    # def closeEvent(self, event):
    #     global flag
    #     # Переопределить colseEvent
    #     print('closed')
    #     flag = 'Canceled'
    #     event.accept()

        # if reply == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()


class ConstantWindow(QtWidgets.QMainWindow): #class ConstantWindow(MainWindow, QtWidgets.QMainWindow):
    '''This class fully describes behavior of the window "Constant window"'''
    ''' Need to:
    Improve a function to save and load data!
   
    Right-click menu:
                    Delete item
                    Edit item (open AddNewItemWindow)
                    Recalculate current row
                    smthg else?
    '''

    '''Design of constant window is created via QtDesigner and was transformed to .py file from .ui
    Method __init__ initialize this class from the ConstantWindow.py module
    AND put an image-logo from .png file (why .qrc?) I GUES IT SHOULD BE IMPLEMENTED AS A STAND ALONE METHOD for re-using'''
    all_tables = []
    incorrect_HB_data = dict()

    def __init__(self, parent=None):
        global MT_hidden

        super(ConstantWindow, self).__init__(parent)
        self.ui = Ui_CheckConstantWindow()
        self.ui.setupUi(self)
        self.MT_content = [self.ui.tableWidgetMTHousing,
                           self.ui.tableWidgetMTHB,
                           self.ui.tableWidgetMTDif,
                           self.ui.tableWidgetMTLDif,
                           self.ui.tableWidgetMTBearing,
                           self.ui.pushButtonHideMTHousing,
                           self.ui.pushButtonInitTableMTHousing,
                           self.ui.pushButtonHideMTHB,
                           self.ui.pushButtonInitTableMTHB,
                           self.ui.pushButtonHideMTDif,
                           self.ui.pushButtonInitTableMTDif,
                           self.ui.pushButtonHideMTLDif,
                           self.ui.pushButtonInitTableMTLDif,
                           self.ui.pushButtonHideMTBearing,
                           self.ui.pushButtonInitTableMTBearing
        ]
        '''Put a logo'''
        #self.put_a_logo(self, self.ui)             HOW TO INHERIT?
        pixmap = QPixmap(':/images/logo.png')  # resource path starts with ':' #@staticmethod??? Mixin?
        self.ui.putImageHere.setPixmap(pixmap)

        self.ui.labelCurrentUser.setText(user)
        self.expandColumnsWidth()
        self.clearTablesData() #after self.expandColumnsWidth!
        self.loadTablesData()
        '''UNCOMMENT THIS when releasing the program
        vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv'''
        # if user != 'Главный технолог':
        #     self.disableTablesIfNotChiefTech()
        # else:
        #     self.blockUneditableTablesVals()
        '''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
        self.ui.pushButtonInitTableMTHousing.clicked.connect(self.upload_xlsx_file)
        self.ui.pushButtonRecalculate.clicked.connect(self.recalculateAllHousingLengthsValues)
        #self.ui.pushButtonHideMTHousing.clicked.connect(self.button_hide_clicked) #replaced with universal method ''buttonHide2Clicked''

        self.ui.pushButtonSaveChanges.clicked.connect(self.btnSaveChangesClicked)
        self.ui.pushButtonAddItem.clicked.connect(self.showAddNewItemWindow)
        self.ui.TestButton.clicked.connect(self.blockUneditableTablesVals)
        self.addRightClickMenu(self.ui.tableWidgetMTHousing)

        self.setupHideButtons()

    # def put_a_logo(self):
    def addRightClickMenu(self, table):
        table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.initRightClickMenu)

    def initRightClickMenu(self, point):
        menu = QtWidgets.QMenu()
        if self.ui.tableWidgetMTHousing.itemAt(point):
            edit_item = QtWidgets.QAction('edit_item', menu)
            edit_item.triggered.connect(self.showAddNewItemWindow)

            del_item = QtWidgets.QAction('del_item', menu)
            del_item.triggered.connect(lambda: print("Текст в первой ячейке: " +
                                                      self.ui.tableWidgetMTHousing.objectName()))
            menu.addAction(edit_item)
            menu.addAction(del_item)
        else:
            pass
        menu.exec(self.ui.tableWidgetMTHousing.mapToGlobal(point))

    def setupHideButtons(self):
        self.ui.pushButtonTPSLine.clicked.connect(self.hideAllMT, MT_hidden)
        self.ui.pushButtonEZLine.clicked.connect(self.hideAllEZLine, EZLine_hidden)
        self.ui.pushButtonREDA.clicked.connect(self.hideAllREDA, REDA_hidden)
        self.ui.pushButtonOther.clicked.connect(self.hideAllOther, Other_hidden)

        self.ui.pushButtonHideMTHousing.clicked.connect(
            lambda checked, btn_name='MTHousing': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideMTHB.clicked.connect(lambda checked, btn_name='MTHB': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideMTDif.clicked.connect(lambda checked, btn_name='MTDif': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideMTLDif.clicked.connect(
            lambda checked, btn_name='MTLDif': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideMTBearing.clicked.connect(
            lambda checked, btn_name='MTBearing': self.buttonHide2Clicked(btn_name))

        self.ui.pushButtonHideEZLineHousing.clicked.connect(
            lambda checked, btn_name='EZLineHousing': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideEZLineHB.clicked.connect(
            lambda checked, btn_name='EZLineHB': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideEZLineDif.clicked.connect(
            lambda checked, btn_name='EZLineDif': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideEZLineLDif.clicked.connect(
            lambda checked, btn_name='EZLineLDif': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideEZLineBearing.clicked.connect(
            lambda checked, btn_name='EZLineBearing': self.buttonHide2Clicked(btn_name))

        self.ui.pushButtonHideREDAHousing.clicked.connect(
            lambda checked, btn_name='REDAHousing': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideREDAHB.clicked.connect(
            lambda checked, btn_name='REDAHB': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideREDADif.clicked.connect(
            lambda checked, btn_name='REDADif': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideREDALDif.clicked.connect(
            lambda checked, btn_name='REDALDif': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideREDABearing.clicked.connect(
            lambda checked, btn_name='REDABearing': self.buttonHide2Clicked(btn_name))

        self.ui.pushButtonHideOtherHousing.clicked.connect(
            lambda checked, btn_name='OtherHousing': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideOtherHB.clicked.connect(
            lambda checked, btn_name='OtherHB': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideOtherDif.clicked.connect(
            lambda checked, btn_name='OtherDif': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideOtherLDif.clicked.connect(
            lambda checked, btn_name='OtherLDif': self.buttonHide2Clicked(btn_name))
        self.ui.pushButtonHideOtherBearing.clicked.connect(
            lambda checked, btn_name='OtherBearing': self.buttonHide2Clicked(btn_name))

    def expandColumnsWidth(self):
        all_tables = self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QTableWidget)
        self.all_tables = all_tables
        for table in all_tables:
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # self.ui.tableWidgetMTHousing.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetMTDif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetMTLDif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetMTBearing.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetMTHB.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        #
        # self.ui.tableWidgetEZLineHousing.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetEZLineDif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetEZLineLDif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetEZLineBearing.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetEZLineHB.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        #
        # self.ui.tableWidgetREDAHousing.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetREDADif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetREDALDif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetREDABearing.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetREDAHB.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        #
        # self.ui.tableWidgetOtherHousing.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetOtherDif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetOtherLDif.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetOtherBearing.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # self.ui.tableWidgetOtherHB.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def showAddNewItemWindow(self):
        self.ui_new = NewItemWindow(self) #NewItemWindow(self) - ссылка на self как раз позволяет прицепить дочерний класс к родительскому. Т.е. у NewItemWindow - родитель self (constant_window)
        self.ui_new.open()
        self.ui_new.closeNewItemWindow()

    def recalculateAllHousingLengthsValues(self):
        '''Recalculates work length values in housing-tables'''
        self.incorrect_HB_data.clear()
        for table in self.all_tables[::5]:
            HB_table = getattr(self.ui, table.objectName()[:-6] + 'B', 'Check names of Housing and HB tables!!!')
            rows = table.rowCount()
            for row in range(rows):
                result_set, product_line, series, FL_or_CR = self.findHBRowsForRecalculatedValues(row, table, HB_table)
                if self.checkRelevantHBQuantityInHBTable(HB_table, result_set, product_line, series, FL_or_CR):
                    head_sizes_list, base_sizes_list = self.getHeadAndBaseSizesFromHBTable(result_set, HB_table)
                    self.recalculateCurrentRowHousingLengthsValues(table, row, head_sizes_list, base_sizes_list)
                else:
                    self.putWorkLengthValuesInHousingTablesAndBlock(table, row)
        self.blockUneditableTablesVals()
        #print(self.incorrect_HB_data)
        self.showIncorrectDataInHBTable(self.incorrect_HB_data)

    def putWorkLengthValuesInHousingTablesAndBlock(self, table, row, nom_len='-1', max_len='-1', min_len='-1'):
        item = table.setItem(row, 7, QtWidgets.QTableWidgetItem(nom_len))
        item = table.item(row, 7)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        item = table.setItem(row, 8, QtWidgets.QTableWidgetItem(max_len))
        item = table.item(row, 8)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        item = table.setItem(row, 9, QtWidgets.QTableWidgetItem(min_len))
        item = table.item(row, 9)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def findHBRowsForRecalculatedValues(self, row, table, HB_table):
        '''Finds all rows in HB tables for current product_line, series and FL_or_CR'''

        product_line = table.item(row, 0).text()
        series = table.item(row, 1).text()
        FL_or_CR = table.item(row, 2).text()

        find_series_in_HB = HB_table.findItems(series, QtCore.Qt.MatchExactly)
        find_product_line_in_HB = HB_table.findItems(product_line, QtCore.Qt.MatchExactly)
        find_FL_or_CR_in_HB = HB_table.findItems(FL_or_CR, QtCore.Qt.MatchExactly)

        find_series_in_HB_set = set()
        find_product_line_in_HB_set = set()
        find_FL_or_CR_in_HB_set = set()

        for element in find_series_in_HB:
            find_series_in_HB_set.add(element.row())

        for element in find_product_line_in_HB:
            find_product_line_in_HB_set.add(element.row())

        for element in find_FL_or_CR_in_HB:
            find_FL_or_CR_in_HB_set.add(element.row())
        # find_series_in_HB_set = set(tuple(find_series_in_HB)) #Почему не работает?
        return find_series_in_HB_set & find_product_line_in_HB_set & find_FL_or_CR_in_HB_set,\
               product_line, series, FL_or_CR

    def recalculateCurrentRowHousingLengthsValues(self, table, row, head_sizes_list, base_sizes_list):
        '''Recalculates min, max and nominal work length of the housing in the table "table" at row "row"'''
        head_size_nom = float(head_sizes_list[0])
        head_size_up_dev = float(head_sizes_list[1])
        head_size_low_dev = float(head_sizes_list[2])

        base_size_nom = float(base_sizes_list[0])
        base_size_up_dev = float(base_sizes_list[1])
        base_size_low_dev = float(base_sizes_list[2])

        hosing_size_up_dev = float(table.item(row, 5).text())
        hosing_size_low_dev = float(table.item(row, 6).text())

        work_housing_len_nom = round(float(table.item(row, 4).text())
                                     - head_size_nom
                                     - base_size_nom
                                     , 3
                                     )
        work_housing_len_max = round(work_housing_len_nom
                                     + hosing_size_up_dev
                                     + base_size_low_dev
                                     + head_size_low_dev
                                     , 3
                                     )
        work_housing_len_min = round(work_housing_len_nom
                                     - hosing_size_low_dev
                                     - base_size_up_dev
                                     - head_size_up_dev
                                     , 3
                                     )
        self.putWorkLengthValuesInHousingTablesAndBlock(table, row, str(work_housing_len_nom), str(work_housing_len_max), str(work_housing_len_min))
        # item = table.setItem(row, 7, QtWidgets.QTableWidgetItem(str(work_housing_len_nom)))
        # item = table.item(row, 7)
        # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        #
        # item = table.setItem(row, 8, QtWidgets.QTableWidgetItem(str(work_housing_len_max)))
        # item = table.item(row, 8)
        # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        #
        # item = table.setItem(row, 9, QtWidgets.QTableWidgetItem(str(work_housing_len_min)))
        # item = table.item(row, 9)
        # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def getHeadAndBaseSizesFromHBTable(self, result_set, HB_table):
        ''' This method gets size, up_dev and low_dev for head and base in HB_table with row_ids written in result_set'''
        head_sizes_list = []
        base_sizes_list = []

        res_list = list(result_set)

        if HB_table.item(res_list[0], 2).text() == 'Голова':
           head_sizes_list.extend((HB_table.item(res_list[0], 4).text(), HB_table.item(res_list[0], 5).text(), HB_table.item(res_list[0], 6).text()))
           base_sizes_list.extend((HB_table.item(res_list[1], 4).text(), HB_table.item(res_list[1], 5).text(), HB_table.item(res_list[1], 6).text()))
        else:
            base_sizes_list.extend((HB_table.item(res_list[0], 4).text(), HB_table.item(res_list[0], 5).text(), HB_table.item(res_list[0], 6).text()))
            head_sizes_list.extend((HB_table.item(res_list[1], 4).text(), HB_table.item(res_list[1], 5).text(), HB_table.item(res_list[1], 6).text()))
        return head_sizes_list, base_sizes_list

    def showIncorrectDataInHBTable(self, incorrect_HB_data):
        '''This method is responsible for showing pop-up window describing incorrect data in HB tables
        Invokes window after window for all PL where mistakes were found.
        It's more likely to make it more user-friendly'''
        for PL_type in incorrect_HB_data:
            dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                           f"Ошибка в таблице {PL_type}",
                                           f'Ошибка в таблице Концевые Детали {PL_type}!\n {str(incorrect_HB_data[PL_type])}',
                                           buttons=QtWidgets.QMessageBox.Ok,
                                           parent=self)
            dialog.exec_()

    def checkRelevantHBQuantityInHBTable(self, HB_table, evaluated_set, product_line, series, FL_or_CR):
        '''Checks if there are only 1 Head and 1 Base suitable for current PL, series and FL_CR
        if no - returns False and save mistake info in self.incorrect_HB_data dict'''
        set_length = len(evaluated_set)
        evaluated_list = list(evaluated_set)
        if set_length < 2:
            self.incorrect_HB_data.setdefault(product_line, []).append((series, FL_or_CR, set_length, 'missing'))
            return False

        elif set_length > 2:
            self.incorrect_HB_data.setdefault(product_line, []).append((series, FL_or_CR, set_length, 'more'))
            return False

        else: #len=2
            if HB_table.item(evaluated_list[0], 2).text() == HB_table.item(evaluated_list[1], 2).text():
                self.incorrect_HB_data.setdefault(product_line, []).append((series, FL_or_CR, set_length, 'multiple'))
                return False
            else:
                return True

    def blockUneditableTablesVals(self):
        '''This method blocks all calculated values, thus even ChiefTechnologist can't change them directly'''

        for table in self.all_tables[0::5]: #Only housning tables
            rows = table.rowCount()
            for row in range(rows):

                for col_id in (4, 7, 8, 9):
                    item = table.item(row, col_id)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                print(f'{row} succes')
                break

    def disableTablesIfNotChiefTech(self):
        '''This method blocks TableWidgets and hides some buttons
         in constant_window if current user is not chief technologist'''
        for table in self.all_tables:
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # self.ui.tableWidgetMTHousing.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetMTHB.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetMTDif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetMTLDif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetMTBearing.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #
        # self.ui.tableWidgetEZLineHousing.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetEZLineHB.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetEZLineDif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetEZLineLDif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetEZLineBearing.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #
        # self.ui.tableWidgetREDAHousing.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetREDAHB.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetREDADif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetREDALDif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetREDABearing.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #
        # self.ui.tableWidgetOtherHousing.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetOtherHB.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetOtherDif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetOtherLDif.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidgetOtherBearing.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.ui.pushButtonAddItem.hide()
        self.ui.pushButtonSaveChanges.hide()

    def hideAllMT(self):
        '''This method allows to hide all data about MT equipment by clicking TPS-line nameline (button)
        I changed it from if-else statement, but this invoked a bug: when hide a single TabWidget and clicking TPS-line nameline twice,
        TabWidget becomes visible with button labeled "Unhide"
        NEED TO FIX IT -- button 'hide/unhide' will be removed and replaced by button with name of item type '''
        global MT_hidden
        for content_element in self.MT_content:
                content_element.setVisible(MT_hidden)
        # self.ui.tableWidgetMTHousing.setVisible(MT_hidden)
        # self.ui.tableWidgetMTHB.setVisible(MT_hidden)
        # self.ui.tableWidgetMTDif.setVisible(MT_hidden)
        # self.ui.tableWidgetMTLDif.setVisible(MT_hidden)
        # self.ui.tableWidgetMTBearing.setVisible(MT_hidden)
        #
        # self.ui.pushButtonHideMTHousing.setVisible(MT_hidden)
        # self.ui.pushButtonInitTableMTHousing.setVisible(MT_hidden)
        #
        # self.ui.pushButtonHideMTHB.setVisible(MT_hidden)
        # self.ui.pushButtonInitTableMTHB.setVisible(MT_hidden)
        #
        # self.ui.pushButtonHideMTDif.setVisible(MT_hidden)
        # self.ui.pushButtonInitTableMTDif.setVisible(MT_hidden)
        #
        # self.ui.pushButtonHideMTLDif.setVisible(MT_hidden)
        # self.ui.pushButtonInitTableMTLDif.setVisible(MT_hidden)
        #
        # self.ui.pushButtonHideMTBearing.setVisible(MT_hidden)
        # self.ui.pushButtonInitTableMTBearing.setVisible(MT_hidden)
        MT_hidden = not MT_hidden

    def hideAllEZLine(self):
        '''hides all EZLine content
        I'm not sure if it is necessary to do like hideAllMT or how to do it in another way.
        Also, not sure if it is necessary to merge this 4 similar methods in one (gues, it's likely) and
        how to implement it without "eval"'''
        global EZLine_hidden

        self.ui.tableWidgetEZLineHousing.setVisible(EZLine_hidden)
        self.ui.tableWidgetEZLineHB.setVisible(EZLine_hidden)
        self.ui.tableWidgetEZLineDif.setVisible(EZLine_hidden)
        self.ui.tableWidgetEZLineLDif.setVisible(EZLine_hidden)
        self.ui.tableWidgetEZLineBearing.setVisible(EZLine_hidden)

        self.ui.pushButtonHideEZLineHousing.setVisible(EZLine_hidden)
        self.ui.pushButtonInitTableEZLineHousing.setVisible(EZLine_hidden)

        self.ui.pushButtonHideEZLineHB.setVisible(EZLine_hidden)
        self.ui.pushButtonInitTableEZLineHB.setVisible(EZLine_hidden)

        self.ui.pushButtonHideEZLineDif.setVisible(EZLine_hidden)
        self.ui.pushButtonInitTableEZLineDif.setVisible(EZLine_hidden)

        self.ui.pushButtonHideEZLineLDif.setVisible(EZLine_hidden)
        self.ui.pushButtonInitTableEZLineLDif.setVisible(EZLine_hidden)

        self.ui.pushButtonHideEZLineBearing.setVisible(EZLine_hidden)
        self.ui.pushButtonInitTableEZLineBearing.setVisible(EZLine_hidden)

        EZLine_hidden = not EZLine_hidden

    def hideAllREDA(self):
        '''hides all REDA content'''
        global REDA_hidden

        self.ui.tableWidgetREDAHousing.setVisible(REDA_hidden)
        self.ui.tableWidgetREDAHB.setVisible(REDA_hidden)
        self.ui.tableWidgetREDADif.setVisible(REDA_hidden)
        self.ui.tableWidgetREDALDif.setVisible(REDA_hidden)
        self.ui.tableWidgetREDABearing.setVisible(REDA_hidden)

        self.ui.pushButtonHideREDAHousing.setVisible(REDA_hidden)
        self.ui.pushButtonInitTableREDAHousing.setVisible(REDA_hidden)

        self.ui.pushButtonHideREDAHB.setVisible(REDA_hidden)
        self.ui.pushButtonInitTableREDAHB.setVisible(REDA_hidden)

        self.ui.pushButtonHideREDADif.setVisible(REDA_hidden)
        self.ui.pushButtonInitTableREDADif.setVisible(REDA_hidden)

        self.ui.pushButtonHideREDALDif.setVisible(REDA_hidden)
        self.ui.pushButtonInitTableREDALDif.setVisible(REDA_hidden)

        self.ui.pushButtonHideREDABearing.setVisible(REDA_hidden)
        self.ui.pushButtonInitTableREDABearing.setVisible(REDA_hidden)

        REDA_hidden = not REDA_hidden

    def hideAllOther(self):
        '''hides all Other PL content'''
        global Other_hidden

        self.ui.tableWidgetOtherHousing.setVisible(Other_hidden)
        self.ui.tableWidgetOtherHB.setVisible(Other_hidden)
        self.ui.tableWidgetOtherDif.setVisible(Other_hidden)
        self.ui.tableWidgetOtherLDif.setVisible(Other_hidden)
        self.ui.tableWidgetOtherBearing.setVisible(Other_hidden)

        self.ui.pushButtonHideOtherHousing.setVisible(Other_hidden)
        self.ui.pushButtonInitTableOtherHousing.setVisible(Other_hidden)

        self.ui.pushButtonHideOtherHB.setVisible(Other_hidden)
        self.ui.pushButtonInitTableOtherHB.setVisible(Other_hidden)

        self.ui.pushButtonHideOtherDif.setVisible(Other_hidden)
        self.ui.pushButtonInitTableOtherDif.setVisible(Other_hidden)

        self.ui.pushButtonHideOtherLDif.setVisible(Other_hidden)
        self.ui.pushButtonInitTableOtherLDif.setVisible(Other_hidden)

        self.ui.pushButtonHideOtherBearing.setVisible(Other_hidden)
        self.ui.pushButtonInitTableOtherBearing.setVisible(Other_hidden)

        Other_hidden = not Other_hidden

    # def button_hide_clicked(self):
    #'''This method allows to hide Table widget of MT Housings by clicking Hide/Unhide button'''
    #     if self.ui.pushButtonHideMTHousing.text() == 'Hide':
    #         self.ui.tableWidgetMTHousing.setVisible(False)
    #         self.ui.pushButtonHideMTHousing.setText('Unhide')
    #     else:
    #         self.ui.tableWidgetMTHousing.setVisible(True)
    #         self.ui.pushButtonHideMTHousing.setText('Hide')

    # def buttonHide3Clicked(self, btn_name):
    #     '''This method allows to hide any Table widget dependantly on clicked button Hide/Unhide
    #     It is not safe to use eval() - needed to be replaced'''
    #     if eval('self.ui.pushButtonHide'+btn_name+'.text()') == 'Hide':
    #         eval('self.ui.tableWidget'+btn_name+'.setVisible(False)')
    #         eval('self.ui.pushButtonHide'+btn_name+'.setText(\'Unhide\')')
    #     else:
    #         eval('self.ui.tableWidget'+btn_name+'.setVisible(True)')
    #         eval('self.ui.pushButtonHide'+btn_name+'.setText(\'Hide\')')

    def buttonHide2Clicked(self, btn_name):
        '''This method allows to hide any Table widget dependantly on clicked button Hide/Unhide
        It is not safe to use eval() - needed to be replaced'''
        table = getattr(self.ui, 'tableWidget'+btn_name, 'smth_wrong_with_tab_name')
        print(table, type(table))
        if table.isVisible():
            table.hide()
        else:
            table.show()

    def closeConstantWindow(self):
        self.ui.pushButtonClose.clicked.connect(self.close)
        #self.ui.pushButton_backToMainWindow.clicked.connect(self.showMainWindow)

    def upload_xlsx_file(self):
        ''' This method allows to upload all cells values from xslx table to program. I.e. initialize the table.
        I guess, it's better to transform it into the func or to think how to reuse this method'''
        self.ui.tableWidgetMTHousing.clearContents()
        xl = pd.read_excel('./MT_housing.xlsx', header=0, index_col=0)
        #self.ui.tableWidgetMTHousing.clear()
        rows, cols = xl.shape
        self.ui.tableWidgetMTHousing.setRowCount(rows)
        for row in range(rows):
            for col in range(cols):
                self.ui.tableWidgetMTHousing.setItem(row, col, QtWidgets.QTableWidgetItem(str(xl.iloc[row][col])))
        #self.calculateAndBlockUneditableMTHousingTableValues()

    def clearTablesData(self):
        '''Clears all tableWidgets content'''
        for table in self.all_tables:
            table.clearContents()

    def loadTablesData(self):
        '''loads tables data from the disk to tableWidgets'''
        try:
            for table in self.all_tables:
                excel_sheet_name = str(table.objectName())[11:]  # RegEx?
                xl = pd.read_excel('./Data.xlsx', sheet_name=excel_sheet_name, header=0, index_col=0)
                rows, cols = xl.shape
                table.setRowCount(rows)
                for row in range(rows):
                    for col in range(cols):
                        table.setItem(row, col, QtWidgets.QTableWidgetItem(str(xl.iloc[row][col])))
        except Exception:
            print('No or wrong Data!')

    def btnSaveChangesClicked(self):
        '''This method should save all changes to the memory'''
        print('Saving your data')
        missing_data_presist = False
        #Перезаписывает таблицы с нуля. Нужно подумать над частичной перезаписью
        #Возможно стоит отмечать каким-то цветом измененные поля, собирать данные об измененной ячейке
        #в формате table_name, row, col и осуществлять перезапись в файл чисто по собранным данным
        with pd.ExcelWriter('./Data.xlsx') as writer:
            for table in self.all_tables:
                excel_sheet_name = str(table.objectName())[11:] #RegEx?
                rows = table.rowCount()
                cols = table.columnCount()
                table_values = []
                for row in range(rows):
                    col_vals = []
                    for col in range(cols):
                        try:
                            col_vals.append(table.item(row, col).text())
                        except Exception:
                            missing_data_presist = True
                            col_vals.append('-1')
                    table_values.append(col_vals)
                table_df = pd.DataFrame(table_values)
                table_df.to_excel(writer, sheet_name=excel_sheet_name)
        if missing_data_presist:
            print('Missing data were found and replaced with \'-1\' value!\n Data were saved')
        else:
            print('Your data saved successfully')

    def btnSaveChangesClicked_TEST(self):
        '''This method should save all changes to the memory'''
        print('Saving your data')
        #Перезаписывает таблицы с нуля. Нужно подумать над частичной перезаписью
        #Возможно стоит отмечать каким-то цветом измененные поля, собирать данные об измененной ячейке
        #в формате table_name, row, col и осуществлять перезапись в файл чисто по собранным данным

        for table in self.all_tables:
            rows = table.rowCount()
            cols = table.columnCount()
            table_values = []
            for row in range(rows):
                col_vals = []
                for col in range(cols):
                    try:
                        col_vals.append(table.item(row, col).text())
                    except Exception:
                        print('empty?', row, col)
                table_values.append(col_vals)

            print(table_values)
        print('Your data saved successfully')

    def addNewRow(self, table):
        '''This method add new empty row to the "table"'''
        row_position = table.rowCount()
        table.insertRow(row_position)
        return row_position

    def fillFirst6Cols(self, table, row_position, data_to_save, new_item_product_line):
        '''This method fills in first 6 cols values in "row_position"  in "table" '''
        table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(new_item_product_line))
        table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(data_to_save[0]))
        table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(data_to_save[1]))
        table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(data_to_save[2]))
        table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(data_to_save[3]))
        table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(data_to_save[4]))

    def fillHousingTable(self, table, new_item_product_line, data_to_save):
        '''This method fills in Housing table of chosen product line'''
        row_position = self.addNewRow(table)
        table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(new_item_product_line))
        table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(data_to_save[0]))
        table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(data_to_save[1]))
        table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(data_to_save[2]))
        table.setItem(row_position, 4, QtWidgets.QTableWidgetItem(str(HOUSING_LENGTH_CODE[data_to_save[2]])))
        table.setItem(row_position, 5, QtWidgets.QTableWidgetItem(data_to_save[3]))
        table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(data_to_save[4]))
        table.setItem(row_position, 7, QtWidgets.QTableWidgetItem('Calculate!')) #Рабочая номинальная
        table.setItem(row_position, 8, QtWidgets.QTableWidgetItem('Calculate!')) #Раб макс
        table.setItem(row_position, 9, QtWidgets.QTableWidgetItem('Calculate!')) #Раб мин

    def fillDifTable(self, table, new_item_product_line, data_to_save):
        '''This method fills in Diffuser table of chosen product line'''
        row_position = self.addNewRow(table)
        self.fillFirst6Cols(table, row_position, data_to_save, new_item_product_line)
        table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(data_to_save[5]))
        table.setItem(row_position, 7, QtWidgets.QTableWidgetItem(data_to_save[6]))

    def fillLDifTable(self, table, new_item_product_line, data_to_save):
        '''This method fills in Lower Diffuser table of chosen product line'''
        row_position = self.addNewRow(table)
        self.fillFirst6Cols(table, row_position, data_to_save, new_item_product_line)

    def fillBearingTable(self, table, new_item_product_line, data_to_save):
        '''This method fills in Bearing table of chosen product line'''
        row_position = self.addNewRow(table)
        self.fillFirst6Cols(table, row_position, data_to_save, new_item_product_line)
        table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(data_to_save[5]))
        table.setItem(row_position, 7, QtWidgets.QTableWidgetItem(data_to_save[6]))

    def fillHBTable(self, table, new_item_product_line, data_to_save):
        '''This method fills in Head&Base table of chosen product line'''
        row_position = self.addNewRow(table)
        self.fillFirst6Cols(table, row_position, data_to_save, new_item_product_line)
        table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(data_to_save[5]))

    def addNewItem(self, new_item_product_line, new_item_type, data_to_save):
        '''This method choose neccessary table for new Item and fills chosen table with transmitted data'''
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #Как это реализовать? Через условия? Через eval? Через словари?
        #[MT, EZLine, REDA, Other]
        #[Housing, Dif, LDif, Bearing, HB]
        print(new_item_product_line, new_item_type, data_to_save)
        if new_item_product_line == 'TPS-Line':
            if new_item_type == 'Корпус':
                self.fillHousingTable(self.ui.tableWidgetMTHousing, new_item_product_line, data_to_save)
            elif new_item_type == 'Направляющий аппарат':
                self.fillDifTable(self.ui.tableWidgetMTDif, new_item_product_line, data_to_save)

            elif new_item_type == 'Нижний направляющий аппарат':
                self.fillLDifTable(self.ui.tableWidgetMTLDif, new_item_product_line, data_to_save)

            elif new_item_type == 'Подшипник':
                self.fillBearingTable(self.ui.tableWidgetMTBearing, new_item_product_line, data_to_save)

            else: #head&base
                self.fillHBTable(self.ui.tableWidgetMTHB, new_item_product_line, data_to_save)

        elif new_item_product_line == 'EZLine':
            if new_item_type == 'Корпус':
                self.fillHousingTable(self.ui.tableWidgetEZLineHousing, new_item_product_line, data_to_save)

            elif new_item_type == 'Направляющий аппарат':
                self.fillDifTable(self.ui.tableWidgetEZLineDif, new_item_product_line, data_to_save)

            elif new_item_type == 'Нижний направляющий аппарат':
                self.fillLDifTable(self.ui.tableWidgetEZLineLDif, new_item_product_line, data_to_save)

            elif new_item_type == 'Подшипник':
                self.fillBearingTable(self.ui.tableWidgetEZLineBearing, new_item_product_line, data_to_save)

            else:  # head&base
                self.fillHBTable(self.ui.tableWidgetEZLineHB, new_item_product_line, data_to_save)

        elif new_item_product_line == 'REDA':
            if new_item_type == 'Корпус':
                self.fillHousingTable(self.ui.tableWidgetREDAHousing, new_item_product_line, data_to_save)

            elif new_item_type == 'Направляющий аппарат':
                self.fillDifTable(self.ui.tableWidgetREDADif, new_item_product_line, data_to_save)

            elif new_item_type == 'Нижний направляющий аппарат':
                self.fillLDifTable(self.ui.tableWidgetREDALDif, new_item_product_line, data_to_save)

            elif new_item_type == 'Подшипник':
                self.fillBearingTable(self.ui.tableWidgetREDABearing, new_item_product_line, data_to_save)

            else:  # head&base
                self.fillHBTable(self.ui.tableWidgetREDAHB, new_item_product_line, data_to_save)

        elif new_item_product_line == 'другое':
            if new_item_type == 'Корпус':
                self.fillHousingTable(self.ui.tableWidgetOtherHousing, new_item_product_line, data_to_save)

            elif new_item_type == 'Направляющий аппарат':
                self.fillDifTable(self.ui.tableWidgetOtherDif, new_item_product_line, data_to_save)

            elif new_item_type == 'Нижний направляющий аппарат':
                self.fillLDifTable(self.ui.tableWidgetOtherLDif, new_item_product_line, data_to_save)

            elif new_item_type == 'Подшипник':
                self.fillBearingTable(self.ui.tableWidgetOtherBearing, new_item_product_line, data_to_save)

            else:  # head&base
                self.fillHBTable(self.ui.tableWidgetOtherHB, new_item_product_line, data_to_save)
        else:
                print('New ProductLine?')


class NewItemWindow(QtWidgets.QDialog):
    '''Describes behaviour of NewItemWindow'''
    chosen_product_line = ''
    comboBoxItemType_activated = False
    def __init__(self, parent=None):
        super(NewItemWindow, self).__init__(parent)
        self.parent = parent
        self.ui_new = Ui_DialogCreateNewItem()
        self.ui_new.setupUi(self)

        self.ui_new.labelItemType.hide()
        self.ui_new.comboBoxItemType.hide()

        self.ui_new.labelItemParameters.hide()

        self.hideAllParameters()
        self.ui_new.comboBoxProductLine.currentTextChanged.connect(self.checkProductLine)
        self.ui_new.comboBoxItemType.currentTextChanged.connect(self.checkItemType)

        self.ui_new.pushButtonSave.clicked.connect(self.collectNewItemParamVals)
        '''Hides all lineEdits, comboBoxes and labels for new item parameters'''
        '''Как скрыть все элементы по нормальному?'''
        '''Запихнуть в контейнер?Написать функцию на строку из булевых значений?'''
        # all_QLineEdits = self.ui_new.findChildren(QtWidgets.QLabel) #Почему не работает?
        # print(all_QLineEdits)

    def hideAllParameters(self):
        '''This method hides all labels, comboboxes and linedits'''
        self.ui_new.labelSeriesRus.hide()
        self.ui_new.comboBoxSeriesRus.hide()
        self.ui_new.labelSeriesEng.hide()
        self.ui_new.comboBoxSeriesEng.hide()
        self.ui_new.labelHorB.hide()
        self.ui_new.comboBoxHorB.hide()
        self.ui_new.labelStagSize.hide()
        self.ui_new.lineEditStagSize.hide()
        self.ui_new.labelCompression.hide()
        self.ui_new.lineEditCompression.hide()
        self.ui_new.labelCRFL.hide()
        self.ui_new.comboBoxCRFL.hide()

        self.ui_new.labelLengthCodeRus.hide()
        self.ui_new.comboBoxLengthCodeRus.hide()
        self.ui_new.labelLengthCodeEng.hide()
        self.ui_new.comboBoxLengthCodeEng.hide()

        self.ui_new.labelHeight.hide()
        self.ui_new.lineEditHeight.hide()

        self.ui_new.labelUpDev.hide()
        self.ui_new.lineEditUpDev.hide()
        self.ui_new.labelLowDev.hide()
        self.ui_new.lineEditLowDev.hide()

        self.ui_new.labelBearingImp.hide()
        self.ui_new.comboBoxBearingImp.hide()
        self.ui_new.labelBearingMod.hide()
        self.ui_new.lineEditBearingMod.hide()

    def closeNewItemWindow(self):
        '''Defines what to do on close button push'''
        self.ui_new.pushButtonCancel.clicked.connect(self.close)

    def checkNoEmptyValues(self, list):
        '''CHecks that all available blanks don't have empty vals'''
        if '' not in list:
            return True
        else:
            return False

    def collectNewItemParamVals(self):
        '''Collects all values from available comboBoxes and lineEdits and pass data to constant_window.
        It also will raise an error message if there any missing data'''
        new_item_product_line = self.ui_new.comboBoxProductLine.currentText()
        new_item_type = self.ui_new.comboBoxItemType.currentText()
        data_to_save = []
        #-----------------------------------------------------------------------
        '''all_QLineEdits = self.ui_new.findChildren(QtWidgets.QLineEdit)
        print(all_QLineEdits)''' #Почему не работает?!
        # for item in all_QLineEdits:
        #     print(item)
            # if item.isVisible():
            #     line_edits.append(f'{item.text()}')
        #-----------------------------------------------------------------------
        param_properties = [
                                self.ui_new.comboBoxSeriesRus,
                                self.ui_new.comboBoxSeriesEng,
                                self.ui_new.comboBoxHorB,
                                self.ui_new.lineEditStagSize,
                                self.ui_new.lineEditCompression,
                                self.ui_new.comboBoxCRFL,
                                self.ui_new.comboBoxLengthCodeRus,
                                self.ui_new.comboBoxLengthCodeEng,
                                self.ui_new.lineEditHeight,
                                self.ui_new.lineEditUpDev,
                                self.ui_new.lineEditLowDev,
                                self.ui_new.comboBoxBearingImp,
                                self.ui_new.lineEditBearingMod
                            ]#или в __init__ его?
        for param in param_properties:
            if param.isVisible():
                if isinstance(param, QtWidgets.QLineEdit):
                    data_to_save.append(f'{param.text()}')
                else:
                    data_to_save.append(f'{param.currentText()}')
        if self.checkNoEmptyValues(data_to_save):
            self.close()
            self.parent.addNewItem(new_item_product_line, new_item_type, data_to_save)
        else:
            dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
                                           "Пустые значения",
                                           "Не все необходимые поля заполнены",
                                           buttons=QtWidgets.QMessageBox.Ok,
                                           parent=self)
            dialog.exec_()

        '''def collectNewItemParamVals(self):
        print('hi')
        new_item_product_line = self.ui_new.comboBoxProductLine.currentText()
        new_item_type = self.ui_new.comboBoxItemType.currentText()
        if new_item_type == 'Корпус':
            combo_box_data = [f'{item.currentText()}' for item in
                          self.ui_new.groupBoxHousing.findChildren(QtWidgets.QComboBox)]
            line_edit_data = [f'{item.text()}' for item in self.ui_new.groupBoxHousing.findChildren(QtWidgets.QLineEdit)]
            # output_data = [line_edit_data[-1], *combo_box_data[:], *line_edit_data[:2]]
            # print(output_data)
        elif new_item_type == 'Направляющий аппарат':
            combo_box_data = [f'{item.currentText()}' for item in
                          self.ui_new.groupBoxDif.findChildren(QtWidgets.QComboBox)]
            line_edit_data = [f'{item.text()}' for item in self.ui_new.groupBoxDif.findChildren(QtWidgets.QLineEdit)]
        elif new_item_type == 'Нижний направляющий аппарат':
            combo_box_data = [f'{item.currentText()}' for item in
                          self.ui_new.groupBoxLDif.findChildren(QtWidgets.QComboBox)]
            line_edit_data = [f'{item.text()}' for item in self.ui_new.groupBoxLDif.findChildren(QtWidgets.QLineEdit)]
        elif new_item_type == 'Подшипник':
            combo_box_data = [f'{item.currentText()}' for item in
                          self.ui_new.groupBoxBearing.findChildren(QtWidgets.QComboBox)]
            line_edit_data = [f'{item.text()}' for item in self.ui_new.groupBoxBearing.findChildren(QtWidgets.QLineEdit)]
        elif new_item_type == 'Концевая деталь':
            combo_box_data = [f'{item.currentText()}' for item in
                          self.ui_new.groupBoxHB.findChildren(QtWidgets.QComboBox)]
            line_edit_data = [f'{item.text()}' for item in self.ui_new.groupBoxHB.findChildren(QtWidgets.QLineEdit)]
        else:
            print('Unknown item type')

        #combo_box_data = [f'{item.currentText()}' for item in self.ui_new.groupBoxHousing.findChildren(QtWidgets.QComboBox)]
        # line_edit_data = [f'{item.text()}' for item in self.findChildren(QLineEdit)]
        #combo_box_data = self.ui_new.groupBoxHousing.findChildren(QtWidgets.QComboBox)
        print(combo_box_data,line_edit_data)
        #Нужно передать сюда chosen_item_type и chosen_product_line, чтобы на основании этого можно было добвить новую строку в табилцу
        new_item_type = 'chosen_item_type'
        new_item_product_type = 'Product_line'
        self.close()
        self.parent.addNewItem(new_item_product_type, new_item_type)'''

    def changeWindowColor(self, chosen_product_line):
        '''This method changes color design of the NewItemWindow dependantly on chosen product line'''
        #self.ui_new.DialogCreateNewItem.setStyleSheet("background-color: rgb(255, 220, 220);") Почему не работает?
        #print(self.checkProductLine.chosen_product_line) Почему не работает?
        if chosen_product_line == 'TPS-Line':
            label_style = str("background-color: rgb(255, 181, 181);\n"
                              "color: rgb(255, 0, 0);\n"
                                                  "font: 75 15pt \"MS Sans Serif\";")
            #self.ui_new.DialogCreateNewItem.setStyleSheet("background-color: rgb(255, 220, 220);")

        elif chosen_product_line == 'EZLine':
            label_style = str("background-color: rgb(255, 255, 110);\n"
                              "color: rgb(181, 181, 0);\n"
                                                  "font: 75 15pt \"MS Sans Serif\";")
            #self.ui_new.DialogCreateNewItem.setStyleSheet("background-color: rgb(255, 255, 220);")
        elif chosen_product_line == 'REDA':
            label_style = str("background-color: rgb(144, 144, 255);\n"
                              "color: rgb(0, 0, 255);\n"
                                                  "font: 75 15pt \"MS Sans Serif\";")
            #self.ui_new.DialogCreateNewItem.setStyleSheet("background-color: rgb(220, 220, 255);")

        elif chosen_product_line == 'другое':
            label_style = str("background-color: rgb(181, 255, 181);\n"
                              "color: rgb(0, 181, 0);\n"
                                                  "font: 75 15pt \"MS Sans Serif\";")
        elif chosen_product_line == '':
            label_style = str("background-color: rgb(181, 181, 181);\n"
                          "color: rgb(255, 255, 255);\n"
                          "font: 75 15pt \"MS Sans Serif\";")
            #self.ui_new.DialogCreateNewItem.setStyleSheet("background-color: rgb(220, 255, 220);")


        self.ui_new.labelProductLine.setStyleSheet(label_style)
        self.ui_new.labelItemType.setStyleSheet(label_style)
        self.ui_new.labelItemParameters.setStyleSheet(label_style)

    def checkProductLine(self):
        ''' Checks chosen product line and hides all fields, if no product line is chosen and shows ItemTypeBoxes'''
        print(self.comboBoxItemType_activated)
        chosen_product_line = self.ui_new.comboBoxProductLine.currentText()
        self.changeWindowColor(chosen_product_line)
        if chosen_product_line == '':
            self.ui_new.labelItemType.hide()
            self.ui_new.comboBoxItemType.hide()
            self.ui_new.labelItemParameters.hide()
            self.hideAllParameters()
        else:
            self.chosen_product_line = chosen_product_line #for conditional branch in checkItemType
            self.ui_new.labelItemType.show()
            self.ui_new.comboBoxItemType.show()

            '''This condition is written for not showing spare part specific labels/lineEdits and comboBoxes when changing 
            product line comboBox value when comboBoxItemType is not activated yet and for changing spare part specific 
            labels/lineEdits and comboBoxes when comboBoxItemType is activated'''
            if self.comboBoxItemType_activated == True:
                self.checkItemType()

    def clearLineEditFields(self):
        '''clears all lineEdit's data in NewItemWindow'''
        self.ui_new.lineEditStagSize.setText('')
        self.ui_new.lineEditCompression.setText('')
        self.ui_new.lineEditHeight.setText('')
        self.ui_new.lineEditUpDev.setText('')
        self.ui_new.lineEditLowDev.setText('')
        self.ui_new.lineEditBearingMod.setText('')

    def checkItemType(self):
        '''checks chosen item type and shows corresponding fields and labels of item parameters'''
        self.comboBoxItemType_activated = True
        self.clearLineEditFields()
        chosen_item_type = self.ui_new.comboBoxItemType.currentText()
        self.ui_new.labelItemParameters.show()
        #ДНФ, КНФ?
        self.ui_new.labelUpDev.show()
        self.ui_new.lineEditUpDev.show()
        self.ui_new.labelLowDev.show()
        self.ui_new.lineEditLowDev.show()
        '''Условние ветвление скрывает-показывает нужные поля label/lineEdit/comboBox в зависимости от выбранной детали'''
        '''Переписать по нормальному!'''
        if chosen_item_type == 'Корпус':
            if self.chosen_product_line == 'REDA' or self.chosen_product_line == 'EZLine':
                self.ui_new.labelSeriesRus.hide()
                self.ui_new.comboBoxSeriesRus.hide()
                self.ui_new.labelSeriesEng.show()
                self.ui_new.comboBoxSeriesEng.show()

                self.ui_new.labelLengthCodeRus.hide()
                self.ui_new.comboBoxLengthCodeRus.hide()
                self.ui_new.labelLengthCodeEng.show()
                self.ui_new.comboBoxLengthCodeEng.show()
            else:
                self.ui_new.labelSeriesRus.show()
                self.ui_new.comboBoxSeriesRus.show()
                self.ui_new.labelSeriesEng.hide()
                self.ui_new.comboBoxSeriesEng.hide()

                self.ui_new.labelLengthCodeRus.show()
                self.ui_new.comboBoxLengthCodeRus.show()
                self.ui_new.labelLengthCodeEng.hide()
                self.ui_new.comboBoxLengthCodeEng.hide()

            self.ui_new.labelHorB.hide()
            self.ui_new.comboBoxHorB.hide()
            self.ui_new.labelStagSize.hide()
            self.ui_new.lineEditStagSize.hide()
            self.ui_new.labelCompression.hide()
            self.ui_new.lineEditCompression.hide()
            self.ui_new.labelCRFL.show()                        ##
            self.ui_new.comboBoxCRFL.show()                     ##
            self.ui_new.labelHeight.hide()
            self.ui_new.lineEditHeight.hide()
            self.ui_new.labelBearingImp.hide()
            self.ui_new.comboBoxBearingImp.hide()
            self.ui_new.labelBearingMod.hide()
            self.ui_new.lineEditBearingMod.hide()
        elif chosen_item_type == 'Направляющий аппарат':
            if self.chosen_product_line == 'REDA' or self.chosen_product_line == 'EZLine':
                self.ui_new.labelSeriesRus.hide()
                self.ui_new.comboBoxSeriesRus.hide()
                self.ui_new.labelSeriesEng.show()
                self.ui_new.comboBoxSeriesEng.show()
            else:
                self.ui_new.labelSeriesRus.show()
                self.ui_new.comboBoxSeriesRus.show()
                self.ui_new.labelSeriesEng.hide()
                self.ui_new.comboBoxSeriesEng.hide()

            self.ui_new.labelLengthCodeRus.hide()
            self.ui_new.comboBoxLengthCodeRus.hide()
            self.ui_new.labelHorB.hide()
            self.ui_new.comboBoxHorB.hide()
            self.ui_new.labelStagSize.show()##
            self.ui_new.lineEditStagSize.show()##
            self.ui_new.labelCompression.show()##
            self.ui_new.lineEditCompression.show()##
            self.ui_new.labelCRFL.show()  ##
            self.ui_new.comboBoxCRFL.show()  ##
            self.ui_new.labelHeight.show()##
            self.ui_new.lineEditHeight.show()##
            self.ui_new.labelBearingImp.hide()
            self.ui_new.comboBoxBearingImp.hide()
            self.ui_new.labelBearingMod.hide()
            self.ui_new.lineEditBearingMod.hide()
        elif chosen_item_type == 'Нижний направляющий аппарат':
            if self.chosen_product_line == 'REDA' or self.chosen_product_line == 'EZLine':
                self.ui_new.labelSeriesRus.hide()
                self.ui_new.comboBoxSeriesRus.hide()
                self.ui_new.labelSeriesEng.show()
                self.ui_new.comboBoxSeriesEng.show()
            else:
                self.ui_new.labelSeriesRus.show()
                self.ui_new.comboBoxSeriesRus.show()
                self.ui_new.labelSeriesEng.hide()
                self.ui_new.comboBoxSeriesEng.hide()

            self.ui_new.labelLengthCodeRus.hide()
            self.ui_new.comboBoxLengthCodeRus.hide()
            self.ui_new.labelHorB.hide()
            self.ui_new.comboBoxHorB.hide()
            self.ui_new.labelStagSize.show()##
            self.ui_new.lineEditStagSize.show()##
            self.ui_new.labelCompression.hide()
            self.ui_new.lineEditCompression.hide()
            self.ui_new.labelCRFL.hide()
            self.ui_new.comboBoxCRFL.hide()
            self.ui_new.labelHeight.show()##
            self.ui_new.lineEditHeight.show()##
            self.ui_new.labelBearingImp.hide()
            self.ui_new.comboBoxBearingImp.hide()
            self.ui_new.labelBearingMod.hide()
            self.ui_new.lineEditBearingMod.hide()
        elif chosen_item_type == 'Подшипник':
            if self.chosen_product_line == 'REDA' or self.chosen_product_line == 'EZLine':
                self.ui_new.labelSeriesRus.hide()
                self.ui_new.comboBoxSeriesRus.hide()
                self.ui_new.labelSeriesEng.show()
                self.ui_new.comboBoxSeriesEng.show()
            else:
                self.ui_new.labelSeriesRus.show()
                self.ui_new.comboBoxSeriesRus.show()
                self.ui_new.labelSeriesEng.hide()
                self.ui_new.comboBoxSeriesEng.hide()

            self.ui_new.labelLengthCodeRus.hide()
            self.ui_new.comboBoxLengthCodeRus.hide()
            self.ui_new.labelHorB.hide()
            self.ui_new.comboBoxHorB.hide()
            self.ui_new.labelStagSize.show()##
            self.ui_new.lineEditStagSize.show()##
            self.ui_new.labelCompression.hide()
            self.ui_new.lineEditCompression.hide()
            self.ui_new.labelCRFL.hide()
            self.ui_new.comboBoxCRFL.hide()
            self.ui_new.labelHeight.show()##
            self.ui_new.lineEditHeight.show()##
            self.ui_new.labelBearingImp.show()##
            self.ui_new.comboBoxBearingImp.show()##
            self.ui_new.labelBearingMod.show()##
            self.ui_new.lineEditBearingMod.show()##
        elif chosen_item_type == 'Концевая деталь':
            if self.chosen_product_line == 'REDA' or self.chosen_product_line == 'EZLine':
                self.ui_new.labelSeriesRus.hide()
                self.ui_new.comboBoxSeriesRus.hide()
                self.ui_new.labelSeriesEng.show()
                self.ui_new.comboBoxSeriesEng.show()
            else:
                self.ui_new.labelSeriesRus.show()
                self.ui_new.comboBoxSeriesRus.show()
                self.ui_new.labelSeriesEng.hide()
                self.ui_new.comboBoxSeriesEng.hide()

            self.ui_new.labelLengthCodeRus.hide()
            self.ui_new.comboBoxLengthCodeRus.hide()
            self.ui_new.labelHorB.show()##
            self.ui_new.comboBoxHorB.show()##
            self.ui_new.labelStagSize.hide()
            self.ui_new.lineEditStagSize.hide()
            self.ui_new.labelCompression.hide()
            self.ui_new.lineEditCompression.hide()
            self.ui_new.labelCRFL.show()##
            self.ui_new.comboBoxCRFL.show()##
            self.ui_new.labelHeight.show()##
            self.ui_new.lineEditHeight.show()##
            self.ui_new.labelBearingImp.hide()
            self.ui_new.comboBoxBearingImp.hide()
            self.ui_new.labelBearingMod.hide()
            self.ui_new.lineEditBearingMod.hide()
        elif chosen_item_type == '':
            self.hideAllParameters()
            self.ui_new.labelItemParameters.hide()


class AboutWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(AboutWindow, self).__init__()
        self.ui = Ui_AboutWindow()
        self.ui.setupUi(self)
        pixmap = QPixmap(':/images/logo.png')  # resource path starts with ':'
        self.ui.putImageHere.setPixmap(pixmap)
        self.ui.labelCurrentUser.setText(user)

    def closeAboutWindow(self):
        self.ui.pushButtonClose.clicked.connect(self.close)
        #self.ui.pushButton_backToMainWindow.clicked.connect(self.showMainWindow)

    # def showMainWindow(self):
    #     self.ui = MainWindow()
    #     self.ui.show()
    #     self.ui.showMainWindow()


class PumpCalcWindow(QtWidgets.QMainWindow):#QtWidgets.QMainWindow):

    def __init__(self):
        super(PumpCalcWindow, self).__init__()
        self.ui = Ui_PumpCalcWindow()
        self.ui.setupUi(self)

        pixmap = QPixmap(':/images/logo.png')  # resource path starts with ':'
        self.ui.putImageHere.setPixmap(pixmap)
        self.ui.labelCurrentUser.setText(user)

    def closePumpCalcWindow(self):
        self.ui.pushButtonClose.clicked.connect(self.close)


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)
#    QtWidgets.QApplication.quit()             # !!! если вы хотите, чтобы событие завершилось

sys.excepthook = excepthook

if __name__ == '__main__':
    import os
    print(os.getcwd())
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    #w.showMainWindow()
    #w.back_to_main_window()
    sys.exit(app.exec_())