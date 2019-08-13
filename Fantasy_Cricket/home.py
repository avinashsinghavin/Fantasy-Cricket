from modules.fantasy import *
from modules.create import *
from modules.evaluate import *
from modules.openteam import *
from modules.database import *
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


# Class of CREATE Team menu item
class CreateWindow(QDialog, Ui_createteam):
    def __init__(self, parent=None):
        global _teamname
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.obj = main_obj()  # main_obj() returning object of MainWindow class
        self.createteam_button.clicked.connect(self.close)
        self.createteam_button.clicked.connect(self.fetch_name)
        self.createteam_button.clicked.connect(self.obj._handleTextUpdate)
        self.createteam_button.clicked.connect(self.obj.radio_true)  # Enabling the radio button if team is created

    # Function to reinitialize all batsmen, bowlers, etc. when new team is created
    def fetch_name(self):
        global _teamname, list_bat, list_bwl, list_ar, list_wk, _list_bwl, _list_bat, _list_wk, _list_ar, \
            sel_players, cnt_ar, cnt_bat, cnt_bwl, cnt_wk, avail_pnt, used_pnt
        _teamname = self.team_name.toPlainText()
        if _teamname.strip() == "":
            _teamname = "Default_Name"
        self.obj = main_obj()
        self.obj.teamname.setText(f"Team Name: {_teamname}")
        list_bat = DataBase.bat_player()
        list_bwl = DataBase.bwl_player()
        list_ar = DataBase.ar_player()
        list_wk = DataBase.wk_player()
        _list_bat = defaultdict(int)
        _list_bwl = defaultdict(int)
        _list_ar = defaultdict(int)
        _list_wk = defaultdict(int)
        sel_players = defaultdict(int)
        cnt_bwl = 0
        cnt_ar = 0
        cnt_bat = 0
        cnt_wk = 0
        avail_pnt = 1000
        used_pnt = 0
        self.obj.selected_player.clear()
        self.obj.available_player.clear()


# Class of OPEN Team menu item
class OpenWindow(QDialog, Ui_openteamwindow):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.comboBox.addItems(DataBase.open())
        self.obj = main_obj()
        self.pushButton.clicked.connect(self.open_team)
        self.pushButton.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.obj.radio_true)  # Enabling radio button when an existing team is opened
        self.pushButton.clicked.connect(self.obj.selected_list)
        self.pushButton.clicked.connect(self.obj._handleTextUpdate)

    # Function to initialize listWidget of available and selected team area
    def open_team(self):
        global _teamname, list_bat, list_bwl, list_ar, list_wk, _list_bwl, _list_bat, _list_wk, _list_ar, \
            sel_players, cnt_ar, cnt_bat, cnt_bwl, cnt_wk, avail_pnt, used_pnt
        _teamname = str(self.comboBox.currentText())
        list_bat = DataBase.bat_player()
        list_bwl = DataBase.bwl_player()
        list_ar = DataBase.ar_player()
        list_wk = DataBase.wk_player()
        avail_pnt = 1000
        used_pnt = 0
        _list_bat = DataBase._bat_player(_teamname)
        _list_bwl = DataBase._bwl_player(_teamname)
        _list_ar = DataBase._ar_player(_teamname)
        _list_wk = DataBase._wk_player(_teamname)
        for i in _list_bat:
            used_pnt += _list_bat[i]
            del list_bat[i]
        for i in _list_wk:
            used_pnt += _list_wk[i]
            del list_wk[i]
        for i in _list_bwl:
            used_pnt += _list_bwl[i]
            del list_bwl[i]
        for i in _list_ar:
            used_pnt += _list_ar[i]
            del list_ar[i]
        cnt_bat = len(_list_bat)
        cnt_bwl = len(_list_bwl)
        cnt_ar = len(_list_ar)
        cnt_wk = len(_list_wk)
        avail_pnt = 1000 - used_pnt


# Class of EVALUATE Team menu item
class EvaluateWindow(QDialog, Ui_Form):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.comboBox.addItems(DataBase.open())  # Populating the scrollable area with saved teams in database
        self.comboBox_2.addItem("match1")
        self.pushButton.clicked.connect(self.calculate)

    # Function to calculate scores and overall scores
    def calculate(self):
        _teamname = str(self.comboBox.currentText())
        _matchname = str(self.comboBox_2.currentText())
        score = DataBase._evaluate_(_teamname, _matchname)  # Returns the scores of individual players
        name = DataBase._teamname_(_teamname)
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.listWidget.addItems([str(i) for i in score])
        self.listWidget_2.addItems([i for i in name])
        self.listWidget_2.update()
        self.listWidget.update()
        self.point.clear()
        self.point.appendPlainText(f"Points: {sum(score)}")


# MainWindow Class
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.radio_check(False)  # Disabling the radio button at the start
        self.new_team.triggered.connect(self.new_fun)
        self.open_team.triggered.connect(self.open_fun)
        self.save_team.triggered.connect(self.save_fun)
        self.evaluate_team.triggered.connect(self.eval_fun)
        self.radio_bat.toggled.connect(self.bat_list)
        self.radio_bow.toggled.connect(self.bwl_list)
        self.radio_ar.toggled.connect(self.ar_list)
        self.radio_wk.toggled.connect(self.wk_list)
        self.available_player.itemDoubleClicked.connect(self._handledoubleclick_availplayer)
        self.selected_player.itemDoubleClicked.connect(self._handledoubleclick_selplayer)

    # Populating batsman radio button
    def bat_list(self):
        self.available_player.clear()
        global list_bat
        self.available_player.addItems([i for i in list_bat])
        self.available_player.update()

    # Populating bowler radio button
    def bwl_list(self):
        self.available_player.clear()
        global list_bwl
        self.available_player.addItems([i for i in list_bwl])
        self.available_player.update()

    # Populating all-rounder radio button
    def ar_list(self):
        self.available_player.clear()
        global list_ar
        self.available_player.addItems([i for i in list_ar])
        self.available_player.update()

    # Populating wicket-keeper radio button
    def wk_list(self):
        self.available_player.clear()
        global list_wk
        self.available_player.addItems([i for i in list_wk])
        self.available_player.update()

    # Populating the selected players list
    def selected_list(self):
        self.selected_player.clear()
        global sel_players
        self.selected_player.addItems([i for i in _list_bat])
        self.selected_player.addItems([i for i in _list_bwl])
        self.selected_player.addItems([i for i in _list_ar])
        self.selected_player.addItems([i for i in _list_wk])
        self.selected_player.update()

    # Function to handle double click event for available players list by updating the values
    def _handledoubleclick_availplayer(self, item):

        global sel_players, list_wk, list_bwl, list_bat, list_ar, cnt_ar, cnt_bat, cnt_bwl, cnt_wk, \
            used_pnt, avail_pnt
        if cnt_ar + cnt_bat + cnt_bwl + cnt_wk > 10:
            QMessageBox.about(self, "Invalid Selection", "Players can't be more than 11")
            return 0
        if item.text() in list_bat:
            if cnt_bat > 4:
                QMessageBox.about(self, "Invalid Selection", "Batsman can't be more than 5")
                return 0
            if avail_pnt < list_bat[item.text()]:
                QMessageBox.about(self, "Insufficient Amount", "Insufficient points to purchase!")
                return 0
            used_pnt += list_bat[item.text()]
            _list_bat[item.text()] = list_bat[item.text()]
            del list_bat[item.text()]
            cnt_bat += 1
            self.bat_list()
            self.selected_list()
        elif item.text() in list_bwl:
            if cnt_bwl > 4:
                QMessageBox.about(self, "Invalid Selection", "Bowlers can't be more than 5")
                return 0
            if avail_pnt < list_bwl[item.text()]:
                QMessageBox.about(self, "Insufficient Amount", "Insufficient points to purchase!")
                return 0
            used_pnt += list_bwl[item.text()]
            _list_bwl[item.text()] = list_bwl[item.text()]
            del list_bwl[item.text()]
            cnt_bwl += 1
            self.bwl_list()
            self.selected_list()
        elif item.text() in list_ar:
            if avail_pnt < list_ar[item.text()]:
                QMessageBox.about(self, "Insufficient Amount", "Insufficient points to purchase!")
                return 0
            used_pnt += list_ar[item.text()]
            _list_ar[item.text()] = list_ar[item.text()]
            del list_ar[item.text()]
            cnt_ar += 1
            self.ar_list()
            self.selected_list()
        else:
            if avail_pnt < list_wk[item.text()]:
                QMessageBox.about(self, "Insufficient Amount", "Insufficient points to purchase!")
                return 0
            if cnt_wk > 0:
                QMessageBox.about(self, "Invalid Selection", "Wicket-Keeper can't be more than 1")
                return 0
            used_pnt += list_wk[item.text()]
            _list_wk[item.text()] = list_wk[item.text()]
            del list_wk[item.text()]
            cnt_wk += 1
            self.wk_list()
            self.selected_list()
        avail_pnt = 1000 - used_pnt
        self._handleTextUpdate()  # Calling function _handleTextUpdate() to refresh values

    # Function to handle double click event for selected players list by updating the values
    def _handledoubleclick_selplayer(self, item):
        global sel_players, list_wk, list_bwl, list_bat, list_ar, cnt_ar, cnt_bat, cnt_bwl, cnt_wk, \
            used_pnt, avail_pnt
        if item.text() in _list_bat:
            list_bat[item.text()] = _list_bat[item.text()]
            used_pnt -= list_bat[item.text()]
            del _list_bat[item.text()]
            cnt_bat -= 1
            if self.radio_bat.isChecked():
                self.bat_list()
            self.selected_list()
        elif item.text() in _list_bwl:
            list_bwl[item.text()] = _list_bwl[item.text()]
            used_pnt -= list_bwl[item.text()]
            del _list_bwl[item.text()]
            cnt_bwl -= 1
            if self.radio_bow.isChecked():
                self.bwl_list()
            self.selected_list()
        elif item.text() in _list_ar:
            list_ar[item.text()] = _list_ar[item.text()]
            used_pnt -= list_ar[item.text()]
            del _list_ar[item.text()]
            cnt_ar -= 1
            if self.radio_ar.isChecked():
                self.ar_list()
            self.selected_list()
        else:
            list_wk[item.text()] = _list_wk[item.text()]
            used_pnt -= list_wk[item.text()]
            del _list_wk[item.text()]
            cnt_wk -= 1
            if self.radio_wk.isChecked():
                self.wk_list()
            self.selected_list()
        avail_pnt = 1000 - used_pnt
        self._handleTextUpdate()  # Calling function _handleTextUpdate() to refresh values

    # Function for updating the count of players, available points and used points
    def _handleTextUpdate(self):
        global cnt_bwl, cnt_wk, cnt_bat, cnt_ar, avail_pnt, used_pnt
        self.batsman.clear()
        self.bowler.clear()
        self.allrounder.clear()
        self.wicketkeeper.clear()
        self.pointused.clear()
        self.pointavailable.clear()
        self.batsman.appendPlainText(f"Batsman (BAT): {cnt_bat}")
        self.bowler.appendPlainText(f"Bowler (BOW): {cnt_bwl}")
        self.wicketkeeper.appendPlainText(f"WicketKeeper (WK): {cnt_wk}")
        self.allrounder.appendPlainText(f"Allrounder (AR): {cnt_ar}")
        self.pointavailable.appendPlainText(f"Point Available: {avail_pnt}")
        self.pointused.appendPlainText(f"Point Used: {used_pnt}")

    # Function to enable radio button
    def radio_true(self):
        self.radio_check(True)
        self.radio_bat.setChecked(True)
        self.bat_list()

    # Action Listener for CREATE Team menu item
    def new_fun(self):
        newobj = CreateWindow()  # Creating an object of CreateWindow class
        newobj.exec_()

    # Action Listener for OPEN Team menu item
    def open_fun(self):
        openobj = OpenWindow()  # Creating an object of OpenWindow class
        openobj.exec_()

    # Action Listener for SAVE Team menu item which in-turn will directly add the selected players to database
    def save_fun(self):
        global sel_players
        sel_players = [str(self.selected_player.item(i).text()) for i in range(self.selected_player.count())]
        if len(sel_players) != 11:
            QMessageBox.about(self, "Error", "Invalid Selection! (Choose 11 players)")
        elif cnt_wk == 0:
            QMessageBox.about(self, "Error", "There must be atleast one wicketkeeper")
        else:
            DataBase.add(_teamname, sel_players)
            QMessageBox.about(self, "Information", "Team saved successfully!")

    # Action Listener for EVALUATE Team menu item
    def eval_fun(self):
        evalobj = EvaluateWindow()  # Creating an object of EvaluateWindow class
        evalobj.exec_()

    # Final function being called for enabling or disabling (individual) radio button
    def radio_check(self, flag):
        self.radio_bat.setEnabled(flag)
        self.radio_bow.setEnabled(flag)
        self.radio_ar.setEnabled(flag)
        self.radio_wk.setEnabled(flag)


DataBase = DBConnect()  # Object/Instance of DBConnect class in database module
'''All Global variables initialized here'''
_teamname = ""
list_bat = DataBase.bat_player()
list_bwl = DataBase.bwl_player()
list_ar = DataBase.ar_player()
list_wk = DataBase.wk_player()
_list_bat = defaultdict(int)
_list_bwl = defaultdict(int)
_list_ar = defaultdict(int)
_list_wk = defaultdict(int)
sel_players = defaultdict(int)
cnt_bwl = 0
cnt_ar = 0
cnt_bat = 0
cnt_wk = 0
avail_pnt = 1000
used_pnt = 0
'''End of initialization of variables'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()  # Creating an instance of MainWindow to start the UI

    # Function for returning the object of MainWindow()
    def main_obj():
        return win

    win.show()  # Displaying the UI using show()
    sys.exit(app.exec_())
