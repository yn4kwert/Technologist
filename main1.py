from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap
import resources_rc
import traceback
import math

from PyQt5.QtCore import pyqtSlot
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
MINIMUM_TUBE_LEN = 20
COMPR_PER_LEN_DICT = {'TPS-Line':
                          {'300CR':
                               {'0.5': '2.32', '1': '3.21',
                                '1.5': '4.32', '2': '6.21',
                                '2.5': '7.32', '3': '9.21',
                                '3.5': '10.32', '4': '12.21',
                                '4.5': '13.32', '5': '15.21',
                                '5.5': '16.32', '6': '18.21', }
                           }
                      }
'''
class - CamelCase
Method and func - lower_case_with_underscores or likeThatName
 global variable - _global_var_name
 Constants - CAP_WORDS'''

class CommonMethods():
    '''This class collects common methods across other classes for reusing'''

    def putLogo(self, ui):
        '''Puts a logo in left top corner of a window.'''
        pixmap = QPixmap(':/images/logo.png')  # resource path starts with ':'
        ui.putImageHere.setPixmap(pixmap)

    def showErrorDialog(self, type=QtWidgets.QMessageBox.Critical, title='Ошибка', text=''):
        '''shows simple error/warning window, return nothing'''
        if type == 'warning':
            type = QtWidgets.QMessageBox.Warning
        dialog = QtWidgets.QMessageBox(type,
                                       title,
                                       text,
                                       buttons=QtWidgets.QMessageBox.Ok,
                                       parent=self)
        dialog.exec_()


class MainWindow(QtWidgets.QMainWindow, CommonMethods):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)
        self.putLogo(self.ui_main)
        self.initMainWindowButtons()

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
        self.ui_main = PumpCalcWindow()
        self.ui_main.show()
        self.ui_main.closePumpCalcWindow()

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


class ClssDialog(QtWidgets.QDialog, CommonMethods):
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
            self.showErrorDialog(text="Вы ввели неправильный пароль!\nПопробуйте еще раз")


class ConstantWindow(QtWidgets.QMainWindow, CommonMethods): #class ConstantWindow(MainWindow, QtWidgets.QMainWindow):
    '''This class fully describes behavior of the window "Constant window"'''
    ''' Need to:
    Improve a function to save and load data?
    Right-click menu:
                    Edit item (open AddNewItemWindow)
                    smthg else?
    '''

    '''Design of constant window is created via QtDesigner and was transformed to .py file from .ui
    Method __init__ initialize this class from the ConstantWindow.py module
    AND put an image-logo from .png file (why .qrc?) I GUES IT SHOULD BE IMPLEMENTED AS A STAND ALONE METHOD for re-using'''
    all_tables = []
    incorrect_HB_data = dict()

    def __init__(self, parent=None):
        super(ConstantWindow, self).__init__(parent)
        self.ui = Ui_CheckConstantWindow()
        self.ui.setupUi(self)
        self.prod_line_cont = {'MT':
            {
                'is_hidden': False,
                'content': (self.ui.tableWidgetMTHousing,
                            self.ui.tableWidgetMTHB,
                            self.ui.tableWidgetMTDif,
                            self.ui.tableWidgetMTLDif,
                            self.ui.tableWidgetMTBearing,
                            self.ui.pushButtonHideMTHousing,
                            self.ui.pushButtonHideMTHB,
                            self.ui.pushButtonHideMTDif,
                            self.ui.pushButtonHideMTLDif,
                            self.ui.pushButtonHideMTBearing)
            },
            'EZLine':
            {
                'is_hidden': False,
                'content': (self.ui.tableWidgetEZLineHousing,
                            self.ui.tableWidgetEZLineHB,
                            self.ui.tableWidgetEZLineDif,
                            self.ui.tableWidgetEZLineLDif,
                            self.ui.tableWidgetEZLineBearing,
                            self.ui.pushButtonHideEZLineHousing,
                            self.ui.pushButtonHideEZLineHB,
                            self.ui.pushButtonHideEZLineDif,
                            self.ui.pushButtonHideEZLineLDif,
                            self.ui.pushButtonHideEZLineBearing)
            },
            'REDA':
            {
                'is_hidden': False,
                'content': (self.ui.tableWidgetREDAHousing,
                            self.ui.tableWidgetREDAHB,
                            self.ui.tableWidgetREDADif,
                            self.ui.tableWidgetREDALDif,
                            self.ui.tableWidgetREDABearing,
                            self.ui.pushButtonHideREDAHousing,
                            self.ui.pushButtonHideREDAHB,
                            self.ui.pushButtonHideREDADif,
                            self.ui.pushButtonHideREDALDif,
                            self.ui.pushButtonHideREDABearing)
            },
            'Other':
            {
                'is_hidden': False,
                'content': (self.ui.tableWidgetOtherHousing,
                            self.ui.tableWidgetOtherHB,
                            self.ui.tableWidgetOtherDif,
                            self.ui.tableWidgetOtherLDif,
                            self.ui.tableWidgetOtherBearing,
                            self.ui.pushButtonHideOtherHousing,
                            self.ui.pushButtonHideOtherHB,
                            self.ui.pushButtonHideOtherDif,
                            self.ui.pushButtonHideOtherLDif,
                            self.ui.pushButtonHideOtherBearing)
            }
        }
        self.putLogo(self.ui) #CommonMethods

        self.ui.labelCurrentUser.setText(user)
        self.expandColumnsWidth()
        self.clearTablesData() #after self.expandColumnsWidth!
        self.loadTablesData()
        '''UNCOMMENT THIS when releasing the program
        vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv'''
        if user != 'Главный технолог':
            self.disableTablesIfNotChiefTech()
        else:
            self.blockUneditableTablesVals()
            self.addRightClickMenu()
            self.ui.pushButtonRecalculate.clicked.connect(self.recalculateAllHousingLengthsValues)
            self.ui.pushButtonSaveChanges.clicked.connect(self.btnSaveChangesClicked)
            self.ui.pushButtonAddItem.clicked.connect(self.showAddNewItemWindow)
        '''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
        '''and comment this:
        vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv'''
        # self.addRightClickMenu()
        # self.ui.pushButtonRecalculate.clicked.connect(self.recalculateAllHousingLengthsValues)
        # self.ui.pushButtonSaveChanges.clicked.connect(self.btnSaveChangesClicked)
        # self.ui.pushButtonAddItem.clicked.connect(self.showAddNewItemWindow)
        '''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
        self.setupHideButtons()

    # def put_a_logo(self):
    def addRightClickMenu(self):
        '''apply right-click menu for all tables'''
        for table in self.all_tables:
            table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            table.customContextMenuRequested.connect(lambda point, table=table: self.initRightClickMenu(point, table))

    def initRightClickMenu(self, point, table):
        '''Initialization of right-click menu for current table.'''
        menu = QtWidgets.QMenu()
        if table.itemAt(point):
            '''vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv'''
            # edit_item = QtWidgets.QAction('edit_item', menu)
            # edit_item.triggered.connect(lambda: self.showAddNewItemWindow())
            # menu.addAction(edit_item)
            '''^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'''
            '''Adds additional action for housing tables'''
            if 'Housing' in str(table.objectName()):
                recalc_row = QtWidgets.QAction('recalculate_row', menu)
                row = table.itemAt(point).row()
                HB_table = getattr(self.ui, table.objectName()[:-6] + 'B', 'Check names of Housing and HB tables!!!')
                recalc_row.triggered.connect(lambda: self.tryRecalcCurrentRowHsgLenVal(row, table, HB_table))
                menu.addAction(recalc_row)

            del_item = QtWidgets.QAction('del_item', menu)
            del_item.triggered.connect(lambda: self.deleteChosenRow(table, point))
            menu.addAction(del_item)
        else:
            pass
        menu.exec(table.mapToGlobal(point))


    # def confirmDeleteRowDialog_decorated(self):
    #     dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
    #                                f"Уверен?",
    #                                f'Точно уверен???',
    #                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
    #                                parent=self)
    #     dialog.exec_()
    #
    #
    # #@are_you_sure
    # def deleteChosenRow_decorated(self, table, point):
    #
    #     deleted_row = table.itemAt(point).row()
    #     #print(self.confirmDeleteRowDialog())
    #     self.are_you_sure()
    #     table.removeRow(deleted_row)
    #     print(deleted_row)


    def confirmDeleteRowDialog(self, row, table):
        '''Open warning dialog prior deleting row. The result must be processed further'''
        dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                   f"Удалить деталь",
                                   f'Вы уверены, что хотите удалить ряд {row+1} в таблице {table.objectName()}?',
                                   buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                   parent=self)
        result = dialog.exec_()
        return result

    def deleteChosenRow(self, table, point):
        '''delete chosen row'''
        deleted_row = table.itemAt(point).row()
        if self.confirmDeleteRowDialog(deleted_row, table) == QtWidgets.QMessageBox.Yes:
            table.removeRow(deleted_row)
            print(deleted_row)

    def setupHideButtons(self):
        '''Set up all buttons in the Constant Window'''
        self.ui.pushButtonTPSLine.clicked.connect(lambda checked, prod_line='MT': self.hidePLContent(prod_line))
        self.ui.pushButtonEZLine.clicked.connect(lambda checked, prod_line='EZLine': self.hidePLContent(prod_line))
        self.ui.pushButtonREDA.clicked.connect(lambda checked, prod_line='REDA': self.hidePLContent(prod_line))
        self.ui.pushButtonOther.clicked.connect(lambda checked, prod_line='Other': self.hidePLContent(prod_line))

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
        '''Expands columns width to fill all spare space horisontally'''
        all_tables = self.ui.scrollAreaWidgetContents.findChildren(QtWidgets.QTableWidget)
        self.all_tables = all_tables
        for table in all_tables:
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def showAddNewItemWindow(self): #, is_edited=False
        self.ui_new = NewItemWindow(self) #NewItemWindow(self) - ссылка на self как раз позволяет прицепить дочерний класс к родительскому. Т.е. у NewItemWindow - родитель self (constant_window)
        #self.ui_new.is_edited = is_edited
        self.ui_new.open()
        self.ui_new.closeNewItemWindow()

    def recalculateAllHousingLengthsValues(self):
        '''Recalculates work length values in housing-tables'''
        self.incorrect_HB_data.clear()
        for table in self.all_tables[::5]:
            HB_table = getattr(self.ui, table.objectName()[:-6] + 'B', 'Check names of Housing and HB tables!!!')
            rows = table.rowCount()
            for row in range(rows):
                self.tryRecalcCurrentRowHsgLenVal(row, table, HB_table)
        self.blockUneditableTablesVals()
        self.showIncorrectDataInHBTable(self.incorrect_HB_data)

    def tryRecalcCurrentRowHsgLenVal(self, row, table, HB_table):
        '''recalculate constant values but only for one chosen row'''
        result_set, product_line, series, FL_or_CR = self.findHBRowsForRecalculatedValues(row, table, HB_table)
        if self.checkRelevantHBQuantityInHBTable(HB_table, result_set, product_line, series, FL_or_CR):
            head_sizes_list, base_sizes_list = self.getHeadAndBaseSizesFromHBTable(result_set, HB_table)
            self.recalcCurrentRowHsgLenVal(table, row, head_sizes_list, base_sizes_list)
        else:
            self.putWorkLengthValuesInHousingTablesAndBlock(table, row)

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

    def recalcCurrentRowHsgLenVal(self, table, row, head_sizes_list, base_sizes_list):
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
        self.putWorkLengthValuesInHousingTablesAndBlock(table,
                                                        row,
                                                        str(work_housing_len_nom),
                                                        str(work_housing_len_max),
                                                        str(work_housing_len_min)
                                                        )
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
        ''' This method gets size, up_dev and low_dev for head & base in HB_table with row_ids written in result_set'''
        head_sizes_list = []
        base_sizes_list = []

        res_list = list(result_set)

        if HB_table.item(res_list[0], 2).text() == 'Голова':
           head_sizes_list.extend((HB_table.item(res_list[0], 4).text(),
                                   HB_table.item(res_list[0], 5).text(),
                                   HB_table.item(res_list[0], 6).text()
                                   ))
           base_sizes_list.extend((HB_table.item(res_list[1], 4).text(),
                                   HB_table.item(res_list[1], 5).text(),
                                   HB_table.item(res_list[1], 6).text()
                                   ))
        else:
            base_sizes_list.extend((HB_table.item(res_list[0], 4).text(),
                                    HB_table.item(res_list[0], 5).text(),
                                    HB_table.item(res_list[0], 6).text()
                                    ))
            head_sizes_list.extend((HB_table.item(res_list[1], 4).text(),
                                    HB_table.item(res_list[1], 5).text(),
                                    HB_table.item(res_list[1], 6).text()
                                    ))
        return head_sizes_list, base_sizes_list

    def showIncorrectDataInHBTable(self, incorrect_HB_data):
        '''This method is responsible for showing pop-up window describing incorrect data in HB tables
        Invokes window after window for all PL where mistakes were found.
        It's more likely to make it more user-friendly'''
        for PL_type in incorrect_HB_data:
            self.showErrorDialog('warning',
                                 f"Ошибка в таблице {PL_type}",
                                 f'Ошибка в таблице Концевые Детали {PL_type}!\n {str(incorrect_HB_data[PL_type])}'
                                 )

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

        self.ui.pushButtonAddItem.hide()
        self.ui.pushButtonSaveChanges.hide()
        self.ui.pushButtonRecalculate.hide()

    def hidePLContent(self, prod_line):
        '''Hides all QTabWidgets and Buttons with product line names related to chosen product line '''
        for content_el in self.prod_line_cont[prod_line]['content']:
            content_el.setVisible(self.prod_line_cont[prod_line]['is_hidden'])
        self.prod_line_cont[prod_line]['is_hidden'] = not self.prod_line_cont[prod_line]['is_hidden']

    def buttonHide2Clicked(self, btn_name):
        '''This method allows to hide any Table widget dependantly on clicked button Hide/Unhide
        It is not safe to use eval() - needed to be replaced'''
        table = getattr(self.ui, 'tableWidget'+btn_name, 'smth_wrong_with_tab_name')
        if table.isVisible():
            table.hide()
        else:
            table.show()

    def closeConstantWindow(self):
        self.ui.pushButtonClose.clicked.connect(self.close)

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
        table.setItem(row_position, 8, QtWidgets.QTableWidgetItem(data_to_save[7]))

    def fillHBTable(self, table, new_item_product_line, data_to_save):
        '''This method fills in Head&Base table of chosen product line'''
        row_position = self.addNewRow(table)
        self.fillFirst6Cols(table, row_position, data_to_save, new_item_product_line)
        table.setItem(row_position, 6, QtWidgets.QTableWidgetItem(data_to_save[5]))

    def addNewItem(self, new_item_product_line, new_item_type, data_to_save):
        '''This method choose necessary table for new Item and fills chosen table with transmitted data'''
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
            self.showErrorDialog(text='Undefined Prodcuct Line')


class NewItemWindow(QtWidgets.QDialog, CommonMethods):
    '''Describes behaviour of NewItemWindow'''
    chosen_product_line = ''
    comboBoxItemType_activated = False
    #is_edited = False
    def __init__(self, parent=None):
        super(NewItemWindow, self).__init__(parent)
        self.parent = parent
        self.ui_new = Ui_DialogCreateNewItem()
        self.ui_new.setupUi(self)
        self.hideContent() #self.is_edited
        self.ui_new.comboBoxProductLine.currentTextChanged.connect(self.checkProductLine)
        self.ui_new.comboBoxItemType.currentTextChanged.connect(self.checkItemType)

        self.ui_new.pushButtonSave.clicked.connect(self.collectNewItemParamVals)
        '''Hides all lineEdits, comboBoxes and labels for new item parameters'''
        '''Как скрыть все элементы по нормальному?'''
        '''Запихнуть в контейнер?Написать функцию на строку из булевых значений?'''
        # all_QLineEdits = self.ui_new.findChildren(QtWidgets.QLabel) #Почему не работает?
        # print(all_QLineEdits)

    def hideContent(self): #, is_edited
        #if not is_edited:
            self.ui_new.labelItemType.hide()
            self.ui_new.comboBoxItemType.hide()
            self.ui_new.labelItemParameters.hide()
            self.hideAllParameters()
        # else:
        #     print('I dont hide')

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
        self.ui_new.labelBearingIsDif.hide()
        self.ui_new.comboBoxBearingIsDif.hide()

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
        param_properties = [self.ui_new.comboBoxSeriesRus,
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
                            self.ui_new.lineEditBearingMod,
                            self.ui_new.comboBoxBearingIsDif
                            ]#или в __init__ его?
        for param in param_properties:
            if param.isVisible():
                if isinstance(param, QtWidgets.QLineEdit):
                    data_to_save.append(f'{param.text()}')
                else:
                    data_to_save.append(f'{param.currentText()}')
        if new_item_product_line == '' or new_item_type == '':
            self.showErrorDialog(text="Пустые значения\nНе выбран производитель и/или тип детали")
        elif self.checkNoEmptyValues(data_to_save):
            self.close()
            self.parent.addNewItem(new_item_product_line, new_item_type, data_to_save)
        else:
            self.showErrorDialog(text="Пустые значения\nНе все необходимые поля заполнены")

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
        self.applyStyle(label_style)

    def applyStyle(self, label_style):
        self.ui_new.labelProductLine.setStyleSheet(label_style)
        self.ui_new.labelItemType.setStyleSheet(label_style)
        self.ui_new.labelItemParameters.setStyleSheet(label_style)

    def checkProductLine(self):
        ''' Checks chosen product line and hides all fields, if no product line is chosen and shows ItemTypeBoxes'''
        print(type(self.comboBoxItemType_activated))
        print(self.comboBoxItemType_activated)
        chosen_product_line = self.ui_new.comboBoxProductLine.currentText()
        print(chosen_product_line)
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
            self.ui_new.labelBearingIsDif.hide()
            self.ui_new.comboBoxBearingIsDif.hide()
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
            self.ui_new.labelBearingIsDif.hide()
            self.ui_new.comboBoxBearingIsDif.hide()
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
            self.ui_new.labelBearingIsDif.hide()
            self.ui_new.comboBoxBearingIsDif.hide()
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
            self.ui_new.labelBearingIsDif.show()##
            self.ui_new.comboBoxBearingIsDif.show()##

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
            self.ui_new.labelBearingIsDif.hide()
            self.ui_new.comboBoxBearingIsDif.hide()
        elif chosen_item_type == '':
            self.hideAllParameters()
            self.ui_new.labelItemParameters.hide()


class AboutWindow(QtWidgets.QMainWindow, CommonMethods):

    def __init__(self):
        super(AboutWindow, self).__init__()
        self.ui = Ui_AboutWindow()
        self.ui.setupUi(self)
        self.putLogo(self.ui)  # CommonMethods
        self.ui.labelCurrentUser.setText(user)

    def closeAboutWindow(self):
        self.ui.pushButtonClose.clicked.connect(self.close)


class PumpCalcWindow(QtWidgets.QMainWindow, CommonMethods):
    error_detected = False
    result_block_visible = False
    ds_dif, ds_hsg, ds_ldif, ds_brg, ds_hb = [], [], [], [], []
    result = {'min': {'dif': '', 'imp': '', 'brg': '', 'brg_imp': '', 'tube_len': '', 'len_btw_brg': ''},
              'nom': {'dif': '', 'imp': '', 'brg': '', 'brg_imp': '', 'tube_len': '', 'len_btw_brg': ''},
              'max': {'dif': '', 'imp': '', 'brg': '', 'brg_imp': '', 'tube_len': '', 'len_btw_brg': ''}
              }
    dict_PL_excel_names = {'TPS-Line': {'hsg': 'MTHousing', 'dif': 'MTDif', 'ldif': 'MTLDif', 'brg': 'MTBearing', 'hb': 'MTHB'},
                           'EZLine': {'hsg': 'EZLineHousing', 'dif': 'EZLineDif', 'ldif': 'EZLineLDif', 'brg': 'EZLineBearing', 'hb': 'EZLineHB'},
                           'REDA': {'hsg': 'REDAHousing', 'dif': 'REDADif', 'ldif': 'REDALDif', 'brg': 'REDABearing', 'hb': 'REDAHB'},
                           'другое': {'hsg': 'OtherHousing', 'dif': 'OtherDif', 'ldif': 'OtherLDif', 'brg': 'OtherBearing', 'hb': 'OtherHB'}}

    def __init__(self):
        super(PumpCalcWindow, self).__init__()
        self.ui_calc = Ui_PumpCalcWindow()
        self.ui_calc.setupUi(self)

        self.ui_new = Ui_DialogCreateNewItem()
        self.ui_new.setupUi(self)

        self.putLogo(self.ui_calc)  # CommonMethods

        self.ui_calc.labelCurrentUser.setText(user)
        self.initComboBoxInput()
        self.applyVisibilityResultBlock()
        self.ui_new.comboBoxProductLine.currentTextChanged.connect(self.checkProductLine)
        self.ui_calc.pushButtonCalculate.clicked.connect(self.onClickCalculate)

        self.ui_new.comboBoxCRFL.currentTextChanged.connect(self.grabDataForCombo)
        self.ui_new.comboBoxSeriesRus.currentTextChanged.connect(self.grabDataForCombo)
        self.ui_new.comboBoxSeriesEng.currentTextChanged.connect(self.grabDataForCombo)

    def initComboBoxInput(self):
        self.ui_calc.gridLayoutInput.addWidget(self.ui_new.comboBoxProductLine, 1, 1, 1, 1)
        self.ui_calc.gridLayoutInput.addWidget(self.ui_new.comboBoxCRFL, 1, 2, 1, 1)
        self.ui_calc.gridLayoutInput.addWidget(self.ui_new.comboBoxSeriesRus, 1, 3, 1, 1)
        self.ui_calc.gridLayoutInput.addWidget(self.ui_new.comboBoxSeriesEng, 1, 4, 1, 1)
        self.ui_calc.gridLayoutInput.addWidget(self.ui_new.comboBoxLengthCodeRus, 1, 5, 1, 1)
        self.ui_calc.gridLayoutInput.addWidget(self.ui_new.comboBoxLengthCodeEng, 1, 6, 1, 1)
        self.hideChangingContent()

    def hideChangingContent(self):
        self.ui_calc.labelSeriesRus.hide()
        self.ui_new.comboBoxSeriesRus.hide()
        self.ui_calc.labelHousingLengthRus.hide()
        self.ui_new.comboBoxLengthCodeRus.hide()

        self.ui_calc.labelSeriesEng.hide()
        self.ui_new.comboBoxSeriesEng.hide()
        self.ui_calc.labelHousingLengthEng.hide()
        self.ui_new.comboBoxLengthCodeEng.hide()

    def prepareDataSets(self, product_line):
        if len(self.ds_dif) > 0 or len(self.ds_brg) > 0:
            ds_dif = self.readSavedData_item(product_line, 'dif')
            ds_bearing = self.readSavedData_item(product_line, 'brg')
        else:
            ds_bearing = self.ds_brg
            ds_dif = self.ds_dif
        ds_housing = self.readSavedData_item(product_line, 'hsg')
        ds_ldif = self.readSavedData_item(product_line, 'ldif')
        return ds_housing, ds_dif, ds_ldif, ds_bearing

    def grabDataForCombo(self):
        '''COllects changed data and re-init comboboxes of bearing type and stages type'''
        product_line = self.ui_new.comboBoxProductLine.currentText()
        FL_CR = self.ui_new.comboBoxCRFL.currentText()
        series = self.ui_new.comboBoxSeriesRus.currentText() if self.ui_new.comboBoxSeriesRus.isVisible() \
            else self.ui_new.comboBoxSeriesEng.currentText()
        print(product_line, FL_CR, series)
        self.ds_dif = ds_dif = self.readSavedData_item(product_line, 'dif')
        self.ds_brg = ds_brg = self.readSavedData_item(product_line, 'brg')

        all_stg_types = self.findStgSizes(ds_dif, product_line, FL_CR, series)
        self.initChangingComboBoxes(self.ui_calc.comboBoxStageSize, all_stg_types)
        self.ui_calc.comboBoxStageSize.currentTextChanged.connect(self.gatherInfo)
        all_brg_types = self.findBrgSizes(ds_brg, product_line, series)
        self.initChangingComboBoxes(self.ui_calc.comboBoxBrgMod, all_brg_types)

    def gatherInfo(self):
        ds_brg = self.ds_brg
        product_line = self.ui_new.comboBoxProductLine.currentText()
        if product_line == 'REDA' or product_line == 'EZLine':
            series = self.ui_new.comboBoxSeriesEng.currentText()
        elif product_line == 'TPS-Line' or product_line == 'другое':
            series = self.ui_new.comboBoxSeriesRus.currentText()
        else:
            return
        all_brg_types = self.findBrgSizes(ds_brg, product_line, series)
        self.initChangingComboBoxes(self.ui_calc.comboBoxBrgMod, all_brg_types)

    def findBrgSizes(self, ds_brg, product_line, series):
        all_brg_types = []
        #print(self.ui_calc.comboBoxStageSize.currentText(), type(self.ui_calc.comboBoxStageSize.currentText()))
        for row in range(ds_brg.shape[0]):
            if ds_brg.iloc[row][0] == product_line and \
                    str(ds_brg.iloc[row][1]) == series and \
                    str(ds_brg.iloc[row][2]) == self.ui_calc.comboBoxStageSize.currentText():
                cur_brg_mod = str(ds_brg.iloc[row][7])
                if cur_brg_mod in all_brg_types:
                    self.showErrorDialog(text=f'Found dublicate of the same bearing'
                                              f' modification {cur_brg_mod} in table row {row} of {product_line}'
                                         )
                else:
                    all_brg_types.append(cur_brg_mod)
        return all_brg_types

    def findStgSizes(self, ds_dif, product_line, FL_CR, series):
        all_stg_types = []
        for row in range(ds_dif.shape[0]):
            if ds_dif.iloc[row][0] == product_line and \
                    str(ds_dif.iloc[row][1]) == series:# and \
                    #ds_dif.iloc[row][4] == FL_CR: ###UNCOMMENT FOR REDA
                all_stg_types.append(str(ds_dif.iloc[row][2]))
        return all_stg_types

    def initChangingComboBoxes(self, combo_box, values_list):
        if len(values_list) > 0:
            combo_box.clear()
            combo_box.addItems(values_list)

    def checkProductLine(self):
        ''' Checks chosen product line and hides all fields, if no product line is chosen and shows ItemTypeBoxes'''
        chosen_product_line = self.ui_new.comboBoxProductLine.currentText()
        print(chosen_product_line)
        if chosen_product_line == 'TPS-Line' or chosen_product_line == 'другое':
            self.ui_calc.labelSeriesRus.show()
            self.ui_new.comboBoxSeriesRus.show()
            self.ui_calc.labelHousingLengthRus.show()
            self.ui_new.comboBoxLengthCodeRus.show()

            self.ui_calc.labelSeriesEng.hide()
            self.ui_new.comboBoxSeriesEng.hide()
            self.ui_calc.labelHousingLengthEng.hide()
            self.ui_new.comboBoxLengthCodeEng.hide()

            self.grabDataForCombo()

        elif chosen_product_line == 'EZLine' or chosen_product_line == 'REDA':
            self.ui_calc.labelSeriesRus.hide()
            self.ui_new.comboBoxSeriesRus.hide()
            self.ui_calc.labelHousingLengthRus.hide()
            self.ui_new.comboBoxLengthCodeRus.hide()

            self.ui_calc.labelSeriesEng.show()
            self.ui_new.comboBoxSeriesEng.show()
            self.ui_calc.labelHousingLengthEng.show()
            self.ui_new.comboBoxLengthCodeEng.show()

            self.grabDataForCombo()
        else:
            self.hideChangingContent()

    def applyVisibilityResultBlock(self):
        self.ui_calc.widgetResultBlock.setVisible(self.result_block_visible)

    def showResultBlock(self):
        self.result_block_visible = True
        self.fillInResultBlock2(self.result)
        self.applyVisibilityResultBlock()

    def fillInResultBlock2(self, result):
        '''Fills all the result block with data from result dictionary'''
        self.ui_calc.labelDifNumMinVal.setText(str(result['min']['dif']))
        self.ui_calc.labelImpNumMinVal.setText(str(result['min']['imp']))
        self.ui_calc.labelBrgNumMinVal.setText(str(result['min']['brg']))
        self.ui_calc.labelBrgImpNumMinVal.setText(str(result['min']['brg_imp']))
        self.ui_calc.labelComprTubeLenMinVal.setText(str(result['min']['tube_len']))
        self.ui_calc.labelLenBetweenBrgMinVal.setText(str(result['min']['len_btw_brg']))

        self.ui_calc.labelDifNumNomVal.setText(str(result['nom']['dif']))
        self.ui_calc.labelImpNumNomVal.setText(str(result['nom']['imp']))
        self.ui_calc.labelBrgNumNomVal.setText(str(result['nom']['brg']))
        self.ui_calc.labelBrgImpNumNomVal.setText(str(result['nom']['brg_imp']))
        self.ui_calc.labelComprTubeLenNomVal.setText(str(result['nom']['tube_len']))
        self.ui_calc.labelLenBetweenBrgNomVal.setText(str(result['nom']['len_btw_brg']))

        self.ui_calc.labelDifNumMaxVal.setText(str(result['max']['dif']))
        self.ui_calc.labelImpNumMaxVal.setText(str(result['max']['imp']))
        self.ui_calc.labelBrgNumMaxVal.setText(str(result['max']['brg']))
        self.ui_calc.labelBrgImpNumMaxVal.setText(str(result['max']['brg_imp']))
        self.ui_calc.labelComprTubeLenMaxVal.setText(str(result['max']['tube_len']))
        self.ui_calc.labelLenBetweenBrgMaxVal.setText(str(result['max']['len_btw_brg']))

    def onClickCalculate(self):
        '''describes actions performed after button "pushButtonCalculate" clicked'''
        global HOUSING_LENGTH_CODE

        self.error_detected = False
        EXS_dist, product_line, FL_CR, stage_size, brg_mod, series, hsg_len_code = self.catchInputData()

        if not self.error_detected:
            ds_housing, ds_dif, ds_ldif, ds_bearing = self.prepareDataSets(product_line)

            #ds_housing, ds_dif, ds_ldif, ds_bearing = self.readSavedData(product_line)
            if not self.error_detected:
                sizes = self.getData(ds_housing, ds_dif,
                                     ds_ldif, ds_bearing,
                                     product_line, FL_CR,
                                     stage_size, brg_mod,
                                     series, hsg_len_code
                                     )
                print('sizes!', sizes)

                if not self.error_detected:
                    overall_hsg_len = HOUSING_LENGTH_CODE[hsg_len_code]
                    print(EXS_dist, type(EXS_dist))
                    quantity = self.defineValues(overall_hsg_len, EXS_dist, sizes)
                    print('quant', quantity)
                    self.calculateValues(sizes, quantity)
                    print('---------------------------------')
                    print(self.result)
                    print('---------------------------------')
                    self.showResultBlock()
                else:
                    self.showErrorDialog(text=f'Can\'t find find data in loaded dataset.'
                                              f'\n Obtaintng folloving data:\n {sizes}')
                    print(f'Can\'t find find data in loaded dataset. /n Obtaintng folloving data: {sizes}')
            else:
                self.showErrorDialog(text='Can\'t read file')
                print('Can\'t read file')
        else:
            self.showErrorDialog(text='Not enough input data')
            print('NoInputData')

    def calculateValues(self, sizes, quantity):
        '''MAX - когда влезет больше всего ступеней
        MIN - когда влезет меньше всего ступеней, т.е. когда длины РО максимальные, а корпуса - минимальные
        tube_min_len может быть больше tube_max_len'''
        self.result['min']['tube_len'] = self.calcTubeLength(quantity['dif']['min'],
                                           sizes['dif']['max'],
                                           sizes['ldif']['max'],
                                           quantity['brg'],
                                           sizes['brg']['max'],
                                           sizes['dif']['compr'],
                                           sizes['hsg']['min']
                                           )
        self.result['nom']['tube_len'] = self.calcTubeLength(quantity['dif']['nom'],
                                           sizes['dif']['nom'],
                                           sizes['ldif']['nom'],
                                           quantity['brg'],
                                           sizes['brg']['nom'],
                                           sizes['dif']['compr'],
                                           sizes['hsg']['nom']
                                           )
        self.result['max']['tube_len'] = self.calcTubeLength(quantity['dif']['max'],
                                           sizes['dif']['min'],
                                           sizes['ldif']['min'],
                                           quantity['brg'],
                                           sizes['brg']['min'],
                                           sizes['dif']['compr'],
                                           sizes['hsg']['max']
                                           )
        # Без учета компрессии!
        self.result['min']['len_btw_brg'] = self.calcLenBtwBrg(quantity['brg'],
                                             quantity['dif']['min'],
                                             sizes['dif']['max']
                                             )
        self.result['nom']['len_btw_brg'] = self.calcLenBtwBrg(quantity['brg'],
                                             quantity['dif']['nom'],
                                             sizes['dif']['max']
                                             )
        self.result['max']['len_btw_brg'] = self.calcLenBtwBrg(quantity['brg'],
                                             quantity['dif']['max'],
                                             sizes['dif']['max']
                                             )

    def catchInputData(self):
        '''Saves input data to variables'''
        EXS_dist = float(self.ui_calc.comboBoxEXSDistanse.currentText())
        product_line = self.ui_new.comboBoxProductLine.currentText()
        FL_CR = self.ui_new.comboBoxCRFL.currentText()
        stage_size = str(self.ui_calc.comboBoxStageSize.currentText())
        brg_mod = self.ui_calc.comboBoxBrgMod.currentText()

        if product_line == 'TPS-Line' or product_line == 'другое':
            series = self.ui_new.comboBoxSeriesRus.currentText()
            hsg_len_code = self.ui_new.comboBoxLengthCodeRus.currentText()
        elif product_line == 'EZLine' or product_line == 'REDA':
            series = self.ui_new.comboBoxSeriesEng.currentText()
            hsg_len_code = self.ui_new.comboBoxLengthCodeEng.currentText()
        else:
            series = ''
            hsg_len_code = ''
            self.error_detected = True
        if stage_size == '' or brg_mod == '':
            self.error_detected = True

        #Need to save this data for rare case, when compression per stage is not defined.
        #However, compression may be stated in a drawing, but for a whole pump.
        #In that case, we need to calculate compression per stage. Actually, we can not to calculate it and take
        #overall compression value, but it looks like more complicated.
        self.chosen_prod_line = product_line
        self.chosen_stg_size = str(stage_size)
        self.chosen_hsg_len = str(hsg_len_code)

        return EXS_dist, product_line, FL_CR, stage_size, brg_mod, series, hsg_len_code

    def closePumpCalcWindow(self):
        self.ui_calc.pushButtonClose.clicked.connect(self.close)

    def calcTubeLength (self, dif_num, dif_len, ldif_len, brg_num, brg_len, comp_per_stg, hsg_work_len):
        '''calculates compression tube length'''
        rotor_len = dif_num * dif_len + ldif_len + brg_num * brg_len
        pump_comp = (dif_num + brg_num + 1) * comp_per_stg
        tube_len = round(hsg_work_len - rotor_len + pump_comp, 2)

        print('rotor_len = dif_num * dif_len + ldif_len + brg_num * brg_len', rotor_len, dif_num, dif_len, ldif_len, brg_num , brg_len)
        print('pump_comp = (dif_num + brg_num + 1) * comp_per_stg', pump_comp, dif_num, brg_num, comp_per_stg)
        return tube_len

    def getBearingData(self, ds_bearing, product_line, series, stage_size, brg_mod):
        '''Gather bearing data from file'''
        print(1)
        found = False
        brg_min_len, brg_nom_len, brg_max_len, brg_is_dif, brg_imp_type = -1, -1, -1, -1, -1
        for row in range(ds_bearing.shape[0]):
            if ds_bearing.iloc[row][0] == product_line and \
                    str(ds_bearing.iloc[row][1]) == series and \
                    ds_bearing.iloc[row][2] == stage_size and \
                    str(ds_bearing.iloc[row][7]) == brg_mod:
                print('cond sucess')
                if not found:
                    print('if not found')
                    brg_nom_len = float(ds_bearing.iloc[row][3])
                    brg_max_len = round(brg_nom_len + float(ds_bearing.iloc[row][4]), 3)
                    brg_min_len = round(brg_nom_len - float(ds_bearing.iloc[row][5]), 3)
                    brg_is_dif = ds_bearing.iloc[row][8]
                    brg_imp_type = ds_bearing.iloc[row][6]
                    print(brg_nom_len, brg_max_len, brg_min_len,brg_is_dif, brg_is_dif )
                    found = True
                else:
                    self.showErrorDialog(type='warning',
                                          title='Дубликат',
                                          text=f'found dublicate in table "Bearing" of {product_line},'
                                               f' row {row}, please delete dublicate')
                    print(f'found dublicate in row {row}, please delete dublicate')

        self.found_brg = found
        return brg_min_len, brg_nom_len, brg_max_len, str(brg_is_dif), str(brg_imp_type)

    def getDifData(self, ds_dif, product_line, series, stage_size, FL_CR):
        '''Gather diffuser data from dataset'''
        found = False
        dif_min_len, dif_nom_len, dif_max_len, comp_per_stg = -1, -1, -1, -1
        for row in range(ds_dif.shape[0]):
            if ds_dif.iloc[row][0] == product_line and \
                    ds_dif.iloc[row][1] == series and \
                    ds_dif.iloc[row][2] == stage_size and \
                    ds_dif.iloc[row][4] == FL_CR:
                if not found:
                    dif_nom_len = float(ds_dif.iloc[row][5])
                    dif_min_len = round(dif_nom_len - float(ds_dif.iloc[row][7]), 3)
                    dif_max_len = round(dif_nom_len + float(ds_dif.iloc[row][6]), 3)
                    try:
                        comp_per_stg = round(float(ds_dif.iloc[row][3])/1000, 3)
                    except ValueError:
                        comp_per_stg = False
                        print('X' * 30)
                        print('need to find compression value in table!')
                        print('X' * 30)
                    found = True
                else:
                    self.showErrorDialog(type='warning',
                                          title='Дубликат',
                                          text=f'found dublicate in table "Diffusers" of {product_line},'
                                               f' row {row}, please delete dublicate')
                    print(f'found dublicate in row {row}, please delete dublicate')
        print('dif_min_len, dif_nom_len, dif_max_len, comp_per_stg : ', dif_min_len, dif_nom_len, dif_max_len, comp_per_stg)
        self.found_dif = found
        return dif_min_len, dif_nom_len, dif_max_len, comp_per_stg

    def getHousingData(self, ds_housing, product_line, series, hsg_len_code, FL_CR):
        '''Gather housing data from dataset'''
        found = False
        hsg_min_len, hsg_nom_len, hsg_max_len = -1, -1, -1
        print(product_line, series, hsg_len_code, FL_CR, type(product_line), type(series), type(hsg_len_code), type(FL_CR))
        for row in range(ds_housing.shape[0]):
            if ds_housing.iloc[row][0] == product_line and \
                    ds_housing.iloc[row][1] == series and \
                    ds_housing.iloc[row][2] == FL_CR and \
                    ds_housing.iloc[row][3] == float(hsg_len_code):
                if not found:
                    hsg_nom_len = float(ds_housing.iloc[row][7])
                    hsg_max_len = float(ds_housing.iloc[row][8])
                    hsg_min_len = float(ds_housing.iloc[row][9])
                    # print(hsg_nom_len, hsg_max_len, hsg_min_len)
                    found = True
                else:
                    self.showErrorDialog(type='warning',
                                          title='Дубликат',
                                          text=f'found dublicate in table "Housing" of {product_line},'
                                               f' row {row}, please delete dublicate')
                    print(f'found dublicate in row {row}, please delete dublicate')
        print('hsg_nom_len, hsg_max_len, hsg_min_len', hsg_nom_len, hsg_max_len, hsg_min_len)
        self.found_hsg = found
        print(str(self.found_hsg)*10)
        return hsg_min_len, hsg_nom_len, hsg_max_len

    def getLDifData(self, ds_ldif, product_line, series, stage_size):
        '''Gather lower diffuser data from dataset'''
        found = False
        ldif_min_len, ldif_nom_len, ldif_max_len = -1, -1, -1
        for row in range(ds_ldif.shape[0]):
            if ds_ldif.iloc[row][0] == product_line and \
                    ds_ldif.iloc[row][1] == series and \
                    ds_ldif.iloc[row][2] == stage_size:
                if not found:
                    ldif_nom_len = float(ds_ldif.iloc[row][3])
                    ldif_max_len = round(ldif_nom_len + float(ds_ldif.iloc[row][4]), 3)
                    ldif_min_len = round(ldif_nom_len - float(ds_ldif.iloc[row][5]), 3)
                    # print(hsg_nom_len, hsg_max_len, hsg_min_len)
                    found = True
                else:
                    self.showErrorDialog(type='warning',
                                          title='Дубликат',
                                          text=f'found dublicate in table "LowerDiffuser" of {product_line},'
                                               f' row {row}, please delete dublicate')
                    print(f'found dublicate in row {row}, please delete dublicate')
        print('ldif_min_len, ldif_nom_len, ldif_max_len', ldif_min_len, ldif_nom_len, ldif_max_len)
        self.found_ldif = found
        return ldif_min_len, ldif_nom_len, ldif_max_len

    def defineBearingNum(self, overall_hsg_len, EXS_dist):
        '''Defines amount of radial bearings depenantly on overall housing and EXS distance'''
        brg_num = math.ceil((overall_hsg_len + 0.1) / (1000 * EXS_dist)) - 1
        return brg_num

    def defineDifNum(self, brg_num, brg_len, hsg_len, dif_len, ldif_len, comp_per_stg):
        '''Calculate amount of diffusers in pump '''
        global MINIMUM_TUBE_LEN
        if self.no_compr_per_stg:
            try:
                pump_compr = float(COMPR_PER_LEN_DICT[self.chosen_prod_line][self.chosen_stg_size][self.chosen_hsg_len])
            except Exception:
                self.showErrorDialog(text='Compression per stage undefined.'
                                          ' Tried to find compression per pump in COMPR_PER_LEN_DICT, but unseccessful')

            dif_num = math.floor((hsg_len + pump_compr - MINIMUM_TUBE_LEN - brg_num * brg_len - ldif_len) / (dif_len))
        else:
            print(type(hsg_len), type(MINIMUM_TUBE_LEN), type(brg_num), type(brg_len), type(ldif_len), type(dif_len), type(comp_per_stg))
            dif_num = math.floor((hsg_len - MINIMUM_TUBE_LEN - brg_num * brg_len - ldif_len) / (dif_len - comp_per_stg))
        return dif_num

    def defineBrgImpNum(self, brg_num, brg_imp_type):
        '''Calculate amount of bearing-specific impellers in pump'''
        if brg_imp_type == 'Короткое':
            brg_imp_num = brg_num
        else:
            brg_imp_num = 0
        return brg_imp_num

    def defineImpNum(self, dif_num, brg_num, brg_is_dif, brg_imp_type):
        '''Calculate amount of  impellers in pump'''
        brg_imp_bot = brg_num if brg_imp_type != 'Обычное' else 0
        brg_imp_top = brg_num if brg_is_dif == '1' else 0
        imp_num = dif_num - brg_imp_bot + brg_imp_top
        print('*' * 20)
        print(imp_num, dif_num, brg_imp_bot, brg_imp_top)
        print('*' * 20)
        return imp_num

    def calcLenBtwBrg(self, brg_num, dif_num, dif_max_len):
        '''Calculate distance between bearings in pump. This should be the maximum possible distance
         without compression account! I.e. dif_len is always maximum value!'''
        len_btw_brg = round(math.ceil(dif_num / (brg_num + 1)) * dif_max_len, 2)
        return len_btw_brg

    # def readSavedData(self, product_line):
    #     dict_PL_excel_names = {'TPS-Line': ('MTHousing', 'MTDif', 'MTLDif', 'MTBearing', 'MTHB'),
    #                            'EZLine': ('EZLineHousing', 'EZLineDif', 'EZLineLDif', 'EZLineBearing', 'EZLineHB'),
    #                            'REDA': ('REDAHousing', 'REDADif', 'REDALDif', 'REDABearing', 'REDAHB'),
    #                            'Other': ('OtherHousing', 'OtherDif', 'OtherLDif', 'OtherBearing', 'OtherHB')}
    #     try:
    #         excel_hsg_sheet_name = dict_PL_excel_names[product_line][0]
    #         excel_dif_sheet_name = dict_PL_excel_names[product_line][1]
    #         excel_ldif_sheet_name = dict_PL_excel_names[product_line][2]
    #         excel_bearing_sheet_name = dict_PL_excel_names[product_line][3]
    #         ds_housing = pd.read_excel('./Data.xlsx', sheet_name=excel_hsg_sheet_name, header=0, index_col=0)
    #         ds_dif = pd.read_excel('./Data.xlsx', sheet_name=excel_dif_sheet_name, header=0, index_col=0)
    #         ds_ldif = pd.read_excel('./Data.xlsx', sheet_name=excel_ldif_sheet_name, header=0, index_col=0)
    #         ds_bearing = pd.read_excel('./Data.xlsx', sheet_name=excel_bearing_sheet_name, header=0, index_col=0)
    #         return ds_housing, ds_dif, ds_ldif, ds_bearing
    #     except Exception:
    #         self.error_detected = True
    #         print('No or wrong Data!')

    def readSavedData_item(self, product_line, item):
        try:
            sheet_name = self.dict_PL_excel_names[product_line][item]
            ds = pd.read_excel('./Data.xlsx', sheet_name=sheet_name, header=0, index_col=0)
            return ds
        except Exception:
            self.error_detected = True
            self.showErrorDialog(text=f'No or wrong Data! in table {product_line} {item}')
            print('No or wrong Data!')

    def getData(self,
                ds_housing, ds_dif, ds_ldif, ds_bearing, product_line,
                FL_CR, stage_size, brg_mod, series, hsg_len_code
                ):
        global COMPR_PER_LEN_DICT

        sizes = {'brg': {'min': '', 'nom': '', 'max': '', 'is_dif': '', 'imp_type': ''},
               'dif': {'min': '', 'nom': '', 'max': '', 'compr': ''},
               'ldif': {'min': '', 'nom': '', 'max': ''},
               'hsg': {'min': '', 'nom': '', 'max': ''}
               }

        sizes['brg']['min'], sizes['brg']['nom'], sizes['brg']['max'], sizes['brg']['is_dif'], sizes['brg']['imp_type'] = \
            self.getBearingData(ds_bearing, product_line, series, stage_size, brg_mod)

        sizes['hsg']['min'], sizes['hsg']['nom'], sizes['hsg']['max'] = \
            self.getHousingData(ds_housing, product_line, series, hsg_len_code, FL_CR)

        sizes['ldif']['min'], sizes['ldif']['nom'], sizes['ldif']['max'] = \
            self.getLDifData(ds_ldif, product_line, series, stage_size)

        sizes['dif']['min'], sizes['dif']['nom'], sizes['dif']['max'], sizes['dif']['compr'] = \
            self.getDifData(ds_dif, product_line, series, stage_size, FL_CR)

        if not sizes['dif']['compr']:
            self.no_compr_per_stg = True
        else:
            self.no_compr_per_stg = False

        if not self.found_ldif * self.found_dif * self.found_hsg * self.found_brg:
            self.error_detected = True
            print('NO DATA')
        return sizes

    def defineValues(self, overall_hsg_len, EXS_dist, sizes):

        quantity = {'brg': self.defineBearingNum(overall_hsg_len, EXS_dist),
                    'dif': {'min': '', 'nom': '', 'max': ''},
                    'imp': {'min': '', 'nom': '', 'max': ''},
                    'brg_imp': ''}

        self.result['min']['brg'] = quantity['brg']
        self.result['nom']['brg'] = quantity['brg']
        self.result['max']['brg'] = quantity['brg']

        quantity['dif']['min'] = self.defineDifNum(quantity['brg'],
                                                   sizes['brg']['max'],
                                                   sizes['hsg']['min'],
                                                   sizes['dif']['max'],
                                                   sizes['ldif']['max'],
                                                   sizes['dif']['compr']
                                                  )
        self.result['min']['dif'] = quantity['dif']['min']
        quantity['dif']['nom'] = self.defineDifNum(quantity['brg'],
                                                   sizes['brg']['nom'],
                                                   sizes['hsg']['nom'],
                                                   sizes['dif']['nom'],
                                                   sizes['ldif']['nom'],
                                                   sizes['dif']['compr']
                                                  )
        self.result['nom']['dif'] = quantity['dif']['nom']
        quantity['dif']['max'] = self.defineDifNum(quantity['brg'],
                                                  sizes['brg']['min'],
                                                  sizes['hsg']['max'],
                                                  sizes['dif']['min'],
                                                  sizes['ldif']['min'],
                                                  sizes['dif']['compr']
                                                  )
        self.result['max']['dif'] = quantity['dif']['max']

        quantity['brg_imp'] = self.defineBrgImpNum(quantity['brg'], sizes['brg']['imp_type'])
        self.result['min']['brg_imp'] = quantity['brg_imp']
        self.result['nom']['brg_imp'] = quantity['brg_imp']
        self.result['max']['brg_imp'] = quantity['brg_imp']

        quantity['imp']['min'] = self.defineImpNum(quantity['dif']['min'],
                                                   quantity['brg'],
                                                   sizes['brg']['is_dif'],
                                                   sizes['brg']['imp_type']
                                                   )
        self.result['min']['imp'] = quantity['imp']['min']
        quantity['imp']['nom'] = self.defineImpNum(quantity['dif']['nom'],
                                                   quantity['brg'],
                                                   sizes['brg']['is_dif'],
                                                   sizes['brg']['imp_type']
                                                   )
        self.result['nom']['imp'] = quantity['imp']['nom']
        quantity['imp']['max'] = self.defineImpNum(quantity['dif']['max'],
                                                   quantity['brg'],
                                                   sizes['brg']['is_dif'],
                                                   sizes['brg']['imp_type']
                                                   )
        self.result['max']['imp'] = quantity['imp']['max']
        return quantity


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)

sys.excepthook = excepthook

if __name__ == '__main__':
    import os
    print(os.getcwd())
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())