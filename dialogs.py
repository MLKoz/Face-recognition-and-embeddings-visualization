from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QGridLayout, QGroupBox, QVBoxLayout, QLineEdit, QHBoxLayout, QRadioButton, QCheckBox, QDateEdit, QComboBox, QFileDialog, QTextEdit
from PyQt5.QtWidgets import QLabel, QTableWidgetItem, QTableWidget, QMessageBox, QStyleFactory, QSlider, QSpinBox
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5 import QtCore
import sqlite3
from database import Database
from fsystem import Fsystem
from aimodule import AI
import tarfile
from PIL.ImageQt import ImageQt
from PIL import Image
import cv2
import os
from datetime import datetime

from races import lista_ras
from countries import lista_panstw

#from PyQt5.Qt import QWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap

fsystem=Fsystem()
AIModule=AI()

class Window(QDialog):
    def __init__(self):
        self.dialog123 = QDialog()
        self.dialog456 = QDialog()
        self.dialog789 = QDialog()
        self.currentRowTarget=-1
        self.photo_imagePath=""
        self.photo_imagePath2=""
        self.photo_imagePathFace2=""
        self.photo_imagePathFace1=""
        self.video_file_path=""
        self.poprzednie_zaznaczenie = -1
        self.baza=Database()
        self.baza.__init__()
        super().__init__()
        self.title = "Face Recognition Application"
        self.top = 200
        self.left = 400
        self.width = 600
        self.height = 150
        self.iconName = "icon.png"
        self.InitWindow()
        fsystem.check_or_create_the_system_file()


    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.CreateLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)
        self.show()

    def CreateLayout(self):
        self.groupBox = QGroupBox("Main menu")
        gridLayout = QGridLayout()

        self.buttonDatabaseManagement = QPushButton("Database management", self)
        self.buttonDatabaseManagement.setIconSize(QtCore.QSize(40, 40))
        self.buttonDatabaseManagement.setMinimumHeight(40)
        self.buttonDatabaseManagement.clicked.connect(lambda: self.DialogDatabaseManagement(self.baza.get_number_of_people_in_database()))
        gridLayout.addWidget(self.buttonDatabaseManagement, 0, 0)

        self.buttonRecognition = QPushButton("Face recognition in the picture", self)
        self.buttonRecognition.setMinimumHeight(40)
        self.buttonRecognition.clicked.connect(self.DialogSearchPeoplesFromPhoto)
        gridLayout.addWidget(self.buttonRecognition, 1, 0)

        self.buttonSearchInMovie = QPushButton("Face recognition on the video", self)
        self.buttonSearchInMovie.setIconSize(QtCore.QSize(40, 40))
        self.buttonSearchInMovie.setMinimumHeight(40)
        self.buttonSearchInMovie.clicked.connect(self.DialogVideoAnalysis)
        gridLayout.addWidget(self.buttonSearchInMovie, 2, 0)

        self.buttonPorownanieDwochOsob = QPushButton("Compare two people using photos")
        self.buttonPorownanieDwochOsob.setMinimumHeight(40)
        self.buttonPorownanieDwochOsob.clicked.connect(self.DialogCompareTwoGroupFaces)
        gridLayout.addWidget(self.buttonPorownanieDwochOsob, 3, 0)

        self.buttonCameraSettings = QPushButton("Camera module", self)
        self.buttonCameraSettings.setIconSize(QtCore.QSize(40, 40))
        self.buttonCameraSettings.setMinimumHeight(40)
        self.buttonCameraSettings.clicked.connect(self.DialogCameraMainWindow)
        gridLayout.addWidget(self.buttonCameraSettings, 4, 0)

        self.buttonAIModuleMenu = QPushButton("AI module", self)
        self.buttonAIModuleMenu.setIconSize(QtCore.QSize(40, 40))
        self.buttonAIModuleMenu.setMinimumHeight(40)
        self.buttonAIModuleMenu.clicked.connect(self.DialogAIModuleMenu)
        gridLayout.addWidget(self.buttonAIModuleMenu, 5, 0)

        self.buttonAnalizaBazy = QPushButton("Database analysis and visualization module", self)
        self.buttonAnalizaBazy.setMinimumHeight(40)
        self.buttonAnalizaBazy.clicked.connect(self.DialogAnalysisDatabase)
        gridLayout.addWidget(self.buttonAnalizaBazy, 6, 0)

        self.groupBox.setLayout(gridLayout)


    def DialogDatabaseManagement(self, x):
        self.gender_result = 0
        dialog = QDialog(self)
        self.dialog456 = dialog
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Database Management")
        dialog.setGeometry(400, 200, 870, 450)
        groupBox = QGroupBox("Database Management")
        gridLayout = QGridLayout()
        tableWidget = QTableWidget()
        tableWidget.clear()
        tableWidget.setRowCount(0)
        self.do_testu=tableWidget
        tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        tableWidget.setRowCount(x)
        tableWidget.setColumnCount(8)
        tableWidget.setHorizontalHeaderLabels(["ID", "Firstname", "Lastname", "Gender", "DoB", "Nationality", "Race", "Number of photos"])
        liczba = self.baza.get_number_of_people_in_database()
        tab = self.baza.view_date()
        plec = ["Women","Men"]
        rasy = lista_ras
        kraje = lista_panstw
        for x in range(liczba):
            for y in [z for z in range(0,8) if z!=3 and z!=5 and z!=6]:
                item = QTableWidgetItem(str(tab[x][y]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                tableWidget.setItem(x, y, item)
            item = QTableWidgetItem(str( plec[int(tab[x][3])] ) )
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 3, item)
            item = QTableWidgetItem(str(kraje[int(tab[x][5])]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 5, item)
            item = QTableWidgetItem(str(rasy[int(tab[x][6])]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 6, item)
        tableWidget.clicked.connect(lambda: self.db_management_cell_click(tableWidget,tableWidget.currentRow(), tableWidget.item(tableWidget.currentRow(), 0).text()))
        tableWidget.resizeColumnsToContents()
        gridLayout.addWidget(tableWidget, 0, 0)
        groupBoxWew = QGroupBox("")
        gridLayoutWew = QGridLayout()
        buttonAddPerson = QPushButton("Add new person", self)
        gridLayoutWew.addWidget(buttonAddPerson, 0, 0)
        buttonAddPerson.clicked.connect(self.DialogAddNewPerson)
        buttonAddPhotos = QPushButton("Add Photos",self)
        gridLayoutWew.addWidget(buttonAddPhotos,1,0)
        buttonAddPhotos.clicked.connect(lambda: self.DialogAddPhotos(int(tableWidget.item(tableWidget.currentRow(), 0).text())))
        buttonDeletePhotos = QPushButton("Delete Photos", self)
        gridLayoutWew.addWidget(buttonDeletePhotos, 2, 0)
        buttonDeletePhotos.clicked.connect(lambda: self.DialogDeletePhotos(int(tableWidget.item(tableWidget.currentRow(), 0).text())))
        buttonModifyPersonalData = QPushButton("Modify personal data", self)
        gridLayoutWew.addWidget(buttonModifyPersonalData, 3, 0)
        buttonModifyPersonalData.clicked.connect(lambda: self.DialogModifyPersonalData((int(tableWidget.item(tableWidget.currentRow(), 0).text()))))
        buttonDeletePerson = QPushButton("Delete person", self)
        gridLayoutWew.addWidget(buttonDeletePerson, 4, 0)
        buttonDeletePerson.clicked.connect(lambda: self.DialogDeletePerson(int(tableWidget.item(tableWidget.currentRow(), 0).text())))
        buttonSearchPerson = QPushButton("Search person", self)
        gridLayoutWew.addWidget(buttonSearchPerson, 5, 0)
        buttonSearchPerson.clicked.connect(self.DialogSearchPersonByPersonalData)
        groupBoxWew.setLayout(gridLayoutWew)
        gridLayout.addWidget(groupBoxWew,0,1)
        groupBoxWewx = QGroupBox("")
        gridLayoutWewx = QGridLayout()
        buttonExportDatabase = QPushButton("Export database", self)
        gridLayoutWewx.addWidget(buttonExportDatabase, 0, 0)
        buttonExportDatabase.clicked.connect(self.DialogExportDatabase)
        buttonImportDatabase = QPushButton("Import database", self)
        gridLayoutWewx.addWidget(buttonImportDatabase, 0, 1)
        buttonImportDatabase.clicked.connect(self.DialogImportDatabase)
        groupBoxWewx.setLayout(gridLayoutWewx)
        gridLayout.addWidget(groupBoxWewx, 1, 0)
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.exec_()

    #dodawanie nowej osoby w db management
    def DialogAddNewPerson(self):
        self.gender_result=0
        dialog = QDialog(self)
        self.dialog000=dialog
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Add new person to the database")
        dialog.setGeometry(400, 200, 300, 300)
        groupBox = QGroupBox("New person personal data")
        gridLayout = QGridLayout()
        lineFirstName = QLineEdit(self)
        lineFirstName.setPlaceholderText("Firstname:")
        gridLayout.addWidget(lineFirstName, 0, 0)
        lineLastName = QLineEdit(self)
        lineLastName.setPlaceholderText("Lastname:")
        gridLayout.addWidget(lineLastName, 1, 0)
        boxGender = QGroupBox("Person gender:")
        hboxlayout = QHBoxLayout()
        buttonMen = QRadioButton("Men")
        buttonMen.toggled.connect(lambda: self.btngenderstate(buttonMen))
        buttonWomen = QRadioButton("Women")
        buttonWomen.setChecked(True)
        boxGender.setLayout(hboxlayout)
        hboxlayout.addWidget(buttonMen)
        hboxlayout.addWidget(buttonWomen)
        gridLayout.addWidget(boxGender, 2, 0)
        boxDate = QGroupBox("Born Date")
        hboxlayout2 = QHBoxLayout()
        date1 = QDateEdit()
        boxDate.setLayout(hboxlayout2)
        hboxlayout2.addWidget(date1)
        gridLayout.addWidget(boxDate,3,0)
        boxNationality = QGroupBox("Born Place")
        hboxlayout3 = QHBoxLayout()
        nationalityCBox = QComboBox()
        boxNationality.setLayout(hboxlayout3)
        for i in lista_panstw:
            nationalityCBox.addItem(i)
        hboxlayout3.addWidget(nationalityCBox)
        gridLayout.addWidget(boxNationality, 4, 0)
        boxRace = QGroupBox("Race")
        hboxlayout4 = QHBoxLayout()
        raceCBox = QComboBox()
        boxRace.setLayout(hboxlayout4)
        for i in lista_ras:
            raceCBox.addItem(i)
        hboxlayout4.addWidget(raceCBox)
        gridLayout.addWidget(boxRace, 5, 0)
        buttonChoosePhoto = QPushButton("Choose photo file",self)
        buttonChoosePhoto.clicked.connect(self.choose_photo_to_add_new_person)
        gridLayout.addWidget(buttonChoosePhoto, 6, 0)
        box_label1 = QGroupBox("Face image:")
        vbox_label1 = QVBoxLayout()
        label = QLabel("")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.label = label
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        vbox_label1.addWidget(self.label)
        box_label1.setLayout(vbox_label1)
        gridLayout.addWidget(box_label1, 7, 0)
        self.AddPersonPhotoIsChoosen = False
        buttonAddNewPerson = QPushButton("Add to the database", self)
        buttonAddNewPerson.clicked.connect(lambda: self.DialogAddNewPersonResponse(lineFirstName.text(),lineLastName.text(),self.gender_result,date1.text(),nationalityCBox.currentIndex(), raceCBox.currentIndex()))
        gridLayout.addWidget(buttonAddNewPerson, 8, 0)
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.exec_()


    def DialogAddNewPersonResponse(self,firstname,lastname,gender,born_date,born_place,race):
        if firstname=="" or lastname=="":
            msg = QMessageBox.information(self, "Komunikat zwrotny", "Provide personal details.", QMessageBox.Yes)
            return
        elif self.AddPersonPhotoIsChoosen==False:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "You must select a photo.", QMessageBox.Yes)
            return
        else:
            self.dialog000.accept()
            id = self.baza.add_person_record(firstname, lastname, gender, born_date, born_place, race)
            fsystem.add_photo_for_person(id, self.PhotoNr1, 1)
            msg = QMessageBox.information(self, "Komunikat zwrotny", "The person was successfully added to the database", QMessageBox.Yes)
            self.dialog456.accept()
            self.DialogDatabaseManagement(self.baza.get_number_of_people_in_database())


    def DialogAddPhotos(self,currentRow):
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Add new photos")
        dialog.setGeometry(400, 200, 300, 300)
        groupBox = QGroupBox("Select photos in the file system")
        gridLayout = QGridLayout()
        buttonChoosePhoto = QPushButton("Select files", self)
        buttonChoosePhoto.clicked.connect(self.choose_person_face_files_to_add)
        gridLayout.addWidget(buttonChoosePhoto, 0, 0)
        self.editAmountPhotos = QLineEdit(self)
        self.editAmountPhotos.setEnabled(False)
        gridLayout.addWidget(self.editAmountPhotos,1,0)
        buttonChoosePhoto = QPushButton("Accept", self)
        buttonChoosePhoto.clicked.connect(lambda: self.DialogAddPhotosResponse(currentRow))
        gridLayout.addWidget(buttonChoosePhoto, 2, 0)
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        self.dialog123=dialog
        dialog.exec_()


    def DialogAddPhotosResponse(self, id):
        id_osoby = id
        ilosc_dodawanych_zdjec = len(self.photo_imagePath2)
        if ilosc_dodawanych_zdjec ==0:
            info = QMessageBox.information(self, "Komunikat zwrotny",
                                           "Invalid number of photos selected.",
                                           QMessageBox.Yes)
            return
        ilosc_w_bazie_przed=self.baza.get_photos_amount_for_person(id_osoby)
        tablica_nazw_zdjec=fsystem.return_list_files_for_person_id(id)
        aktualne_id_zdjecia=1
        if len(tablica_nazw_zdjec) != 0:
            aktualne_id_zdjecia=(int(sorted(fsystem.return_list_files_for_person_id(id), key=lambda x: int(x[:-4]))[-1][:-4]) + 1)
        ilosc_nie_ok = 0
        tab_error = ""
        for x in range(ilosc_dodawanych_zdjec):
            results = AIModule.extract_mtcnn_result_from_photo(self.photo_imagePath2[x])
            if len(results) > 1:
                tab_error = tab_error + " " + self.photo_imagePath2[x]
                ilosc_nie_ok+=1
                continue
            if len(results) == 0:
                tab_error = tab_error + " " + self.photo_imagePath2[x]
                ilosc_nie_ok += 1
                continue
            else:
                zdjecie_samej_twarzy = AIModule.extract_face_file_to_save(self.photo_imagePath2[x], results)
                fsystem.add_photo_for_person(id, zdjecie_samej_twarzy, aktualne_id_zdjecia)
                aktualne_id_zdjecia+=1
        self.baza.update_photos_amount(id_osoby, ilosc_w_bazie_przed+ilosc_dodawanych_zdjec-ilosc_nie_ok)
        if ilosc_nie_ok >0:
            info = QMessageBox.information(self, "Komunikat zwrotny", "Failed to add all photos to base, invalid number of faces detected in photos: " +tab_error, QMessageBox.Yes)
        else:
            info = QMessageBox.information(self, "Komunikat zwrotny",
                                           "Photos successfully added",
                                           QMessageBox.Yes)
        self.dialog123.accept()
        self.dialog456.accept()
        self.DialogDatabaseManagement(self.baza.get_number_of_people_in_database())


    def DialogDeletePhotos(self, id):
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Database Management")
        dialog.setGeometry(400, 200, 160*5+200, 350+320+40)
        groupBox = QGroupBox("Database Management")
        gridLayout = QGridLayout()
        photos_amount = self.baza.get_photos_amount_for_person(id)
        tableWidget = TableWidget(photos_amount, id)
        tableWidget.clicked.connect(lambda: self.DialogDeletePhotosResponse(tableWidget, dialog, tableWidget.currentColumn(), tableWidget.currentRow(), id, photos_amount))
        self.do_testu = tableWidget
        tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        gridLayout.addWidget(tableWidget, 0, 0)
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.close
        dialog.exec_()


    def DialogDeletePhotosResponse(self, tableWidget, dialog, x, y, id, liczba_zdjec):
        if x+y*5 >=liczba_zdjec:
            return
        message = QMessageBox.question(dialog,"Warning!","Are you sure you want to delete this photo?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            poprawka = 0
            if id > 9 and id <100:
                poprawka+=1
            elif id >99 and id <1000:
                poprawka+=2
            elif id > 999 and id < 10000:
                poprawka+=3
            elif id > 9999 and id < 100000:
                poprawka+=4
            elif id > 99999 and id < 1000000:
                poprawka+=5
            elif id > 999999 and id < 10000000:
                poprawka+=6

            z=int(tableWidget.cellWidget(y, x).get_text()[11 + poprawka:-4])
            fsystem.delete_photo(id,z)
            self.baza.update_photos_amount(id, self.baza.get_photos_amount_for_person(id) - 1)
            dialog.accept()
            self.dialog456.accept()
            self.DialogDeletePhotos(id)


    def DialogModifyPersonalData(self, id):
        row = self.baza.get_all_data_about_person(id)
        self.gender_result = 0
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Modify person data")
        dialog.setGeometry(400, 200, 300, 300)
        groupBox = QGroupBox("Enter new data")
        gridLayout = QGridLayout()
        lineFirstName = QLineEdit(self)
        lineFirstName.setPlaceholderText("Firstname:")
        gridLayout.addWidget(lineFirstName, 0, 0)
        lineLastName = QLineEdit(self)
        lineLastName.setPlaceholderText("Lastname:")
        gridLayout.addWidget(lineLastName, 1, 0)
        boxGender = QGroupBox("Person gender:")
        hboxlayout = QHBoxLayout()
        buttonMen = QRadioButton("Men")
        buttonMen.toggled.connect(lambda: self.btngenderstate(buttonMen))
        buttonWomen = QRadioButton("Women")
        boxGender.setLayout(hboxlayout)
        hboxlayout.addWidget(buttonMen)
        hboxlayout.addWidget(buttonWomen)
        gridLayout.addWidget(boxGender, 2, 0)
        boxRace = QGroupBox("Race")
        hboxlayout4 = QHBoxLayout()
        raceCBox = QComboBox()
        boxRace.setLayout(hboxlayout4)
        for i in lista_ras:
            raceCBox.addItem(i)
        hboxlayout4.addWidget(raceCBox)
        gridLayout.addWidget(boxRace, 3, 0)
        boxDate = QGroupBox("Born Date")
        hboxlayout2 = QHBoxLayout()
        date1 = QDateEdit()
        boxDate.setLayout(hboxlayout2)
        hboxlayout2.addWidget(date1)
        gridLayout.addWidget(boxDate, 4, 0)
        boxNationality = QGroupBox("Born Place")
        hboxlayout3 = QHBoxLayout()
        nationalityCBox = QComboBox()
        boxNationality.setLayout(hboxlayout3)
        for i in lista_panstw:
            nationalityCBox.addItem(i)
        hboxlayout3.addWidget(nationalityCBox)
        gridLayout.addWidget(boxNationality, 5, 0)
        buttonEditPersonData = QPushButton("Change", self)
        buttonEditPersonData.clicked.connect(
            lambda: self.DialogModifyPersonalDataResponse(id, lineFirstName.text(), lineLastName.text(), self.gender_result,
                                             date1.text(), nationalityCBox.currentIndex(), raceCBox.currentIndex(), dialog))
        gridLayout.addWidget(buttonEditPersonData,6, 0)
        lineFirstName.setText(row[1])
        lineLastName.setText(row[2])
        if row[3] == 1:
            buttonMen.setChecked(True)
        else:
            buttonWomen.setChecked(True)
        date1.setDate(QtCore.QDate(int(row[4][6:10]),int(row[4][3:5]),int(row[4][0:2])))
        nationalityCBox.setCurrentIndex(row[5])
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.exec_()


    def DialogModifyPersonalDataResponse(self, id, firstname, lastname, gender, born_date, born_place, race, dialog):
        if firstname == "" or lastname == "":
            msg = QMessageBox.information(self, "Komunikat zwrotny", "Provide personal details.",
                                          QMessageBox.Yes)
            return
        self.baza.update_personal_data(id, firstname, lastname, gender, born_date, born_place, race)
        msg = QMessageBox.information(self, "Komunikat zwrotny", "Changes saved.",
                                      QMessageBox.Yes)
        dialog.accept()
        self.dialog456.accept()
        self.DialogDatabaseManagement(self.baza.get_number_of_people_in_database())


    def DialogDeletePerson(self,id):
        message = QMessageBox.question(self.dialog456, "Komunikat zwrotny", "Are you sure you want to remove the selected person from the database?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            self.baza.delete_record(id)
            fsystem.delete_directory_and_photos(id)
            self.dialog456.accept()
            self.DialogDatabaseManagement(self.baza.get_number_of_people_in_database())


    def DialogSearchPersonByPersonalData(self):
        self.gender_result = 0
        dialog = QDialog(self)
        self.dialog456 = dialog
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Searching for a person by their personal data")
        dialog.setGeometry(400, 200, 559, 390)
        groupBox = QGroupBox("People found")
        gridLayout = QGridLayout()
        tableWidget = QTableWidget()
        self.do_testu = tableWidget
        gridLayout.addWidget(tableWidget, 0, 0)
        groupBoxWew = QGroupBox("Provide at least one information about the person you want to find")
        gridLayoutWew = QGridLayout()
        lineFirstName = QLineEdit(self)
        lineFirstName.setPlaceholderText("Firstname:")
        gridLayoutWew.addWidget(lineFirstName, 0, 0)
        lineLastName = QLineEdit(self)
        lineLastName.setPlaceholderText("Lastname:")
        gridLayoutWew.addWidget(lineLastName, 1, 0)
        lineNationality = QLineEdit(self)
        lineNationality.setPlaceholderText("Nationality:")
        gridLayoutWew.addWidget(lineNationality, 2, 0)
        boxDate = QGroupBox("DoB")
        hboxlayout2 = QHBoxLayout()
        date1 = QDateEdit()
        boxDate.setLayout(hboxlayout2)
        hboxlayout2.addWidget(date1)
        gridLayoutWew.addWidget(boxDate, 3, 0)
        boxRace = QGroupBox("Race")
        hboxlayout4 = QHBoxLayout()
        raceCBox = QComboBox()
        boxRace.setLayout(hboxlayout4)
        for i in lista_ras:
            raceCBox.addItem(i)
        hboxlayout4.addWidget(raceCBox)
        gridLayoutWew.addWidget(boxRace, 4, 0)
        buttonSearchPerson = QPushButton("Search", self)
        gridLayoutWew.addWidget(buttonSearchPerson, 5, 0)
        buttonSearchPerson.clicked.connect(lambda: self.DialogSearchPersonByPersonalDataShowResults(tableWidget, lineFirstName.text(), lineLastName.text(), lineNationality.text(), date1.text(), raceCBox.currentIndex()))
        groupBoxWew.setLayout(gridLayoutWew)
        gridLayout.addWidget(groupBoxWew, 1, 0)
        groupBoxWewx = QGroupBox("")
        gridLayoutWewx = QGridLayout()
        buttonExportDatabase = QPushButton("Export database", self)
        gridLayoutWewx.addWidget(buttonExportDatabase, 0, 0)
        buttonImportDatabase = QPushButton("Import database", self)
        gridLayoutWewx.addWidget(buttonImportDatabase, 0, 1)
        groupBoxWewx.setLayout(gridLayoutWewx)
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.exec_()


    def DialogSearchPersonByPersonalDataShowResults(self,tableWidget, firstname, lastname, nationality, dob, race):
        tableWidget.clear()
        tableWidget.setRowCount(0)
        tab = self.baza.search_person_via_data(firstname, lastname, nationality, dob, race)
        liczba = len(tab)
        tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        tableWidget.setRowCount(liczba)
        tableWidget.setColumnCount(8)
        tableWidget.setHorizontalHeaderLabels(
            ["ID", "Firstname", "Lastname", "Gender", "DoB", "Nationality", "Race", "Number of photos"])
        plec = ["Women", "Men"]
        kraje = lista_panstw
        rasy = lista_ras
        for x in range(liczba):
            for y in [z for z in range(0, 8) if z != 3 and z != 5 and z!=6]:
                item = QTableWidgetItem(str(tab[x][y]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                tableWidget.setItem(x, y, item)
            item = QTableWidgetItem(str(plec[int(tab[x][3])]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 3, item)
            item = QTableWidgetItem(str(kraje[int(tab[x][5])]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 5, item)
            item = QTableWidgetItem(str(rasy[int(tab[x][6])]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 6, item)
        tableWidget.resizeColumnsToContents()


    def DialogExportDatabase(self):
        fname = QFileDialog.getSaveFileName(self,"Save file",
                                            'c:\\',".gz files (*.gz )")
        if fname[0] != "":
            with tarfile.open(fname[0], mode='w') as archive:
                archive.add('photos', recursive=True)
                archive.add("camera", recursive=True)
                archive.add("models", recursive=True)
                archive.add("gen_time", recursive=True)
                archive.add("gen_data", recursive=True)
                archive.add("db.db")
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny",
                                          "You must select a file path.",
                                          QMessageBox.Yes)


    def DialogImportDatabase(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', ".gz files (*.gz )")
        if fname[0] != "":
            tar = tarfile.open(fname[0])
            tar.extractall()
            tar.close()
            self.dialog456.accept()
            self.DialogDatabaseManagement(self.baza.get_number_of_people_in_database())
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny",
                                          "You must select a file.",
                                          QMessageBox.Yes)


    def DialogSearchPeoplesFromPhoto(self):
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Search people in database")
        dialog.setGeometry(400, 200, 300, 300)
        groupBox = QGroupBox("Choose option")
        gridLayout = QGridLayout()
        buttonChoosePhoto = QPushButton("Choose photo file", self)
        buttonChoosePhoto.clicked.connect(self.choose_face_photo_to_find)
        gridLayout.addWidget(buttonChoosePhoto, 0, 0)
        self.labelSearch = QLabel("")
        gridLayout.addWidget(self.labelSearch, 1, 0)
        textResult = QTextEdit(self)
        buttonStartSearching = QPushButton("Start searching", self)
        gridLayout.addWidget(buttonStartSearching, 2, 0)
        buttonStartSearching.clicked.connect(lambda: self.DialogSearchPeoplesFromPhotoCalculations(textResult))
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.exec()
        dialog.show()


    def DialogSearchPeoplesFromPhotoCalculations(self, resultText):
        if self.photo_imagePathSearch == "":
            msg = QMessageBox.information(self, "Komunikat zwrotny", "You must select a photo.",
                                          QMessageBox.Yes)
            return
        result = AIModule.extract_mtcnn_result_from_photo(self.photo_imagePathSearch)
        ilosc_twarzy_na_zdjeciu=len(result)
        if ilosc_twarzy_na_zdjeciu <1:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "No face detected in the picture.",
                                          QMessageBox.Yes)
            return
        macierz_wynikow = list()
        textAnalizy = ""
        textList = list()
        lista_osob = list()
        macierz_wynikow_generalna=list()
        if ilosc_twarzy_na_zdjeciu > 0:
            for i in range(ilosc_twarzy_na_zdjeciu):
                id, prob, face, class_proba = AIModule.find_person_from_photo_and_extract_face2(self.photo_imagePathSearch,result, required_size=(160,160), position=i)
                wyniki = list(enumerate(class_proba[0]))
                wyniki2 = sorted(wyniki, key=lambda l: l[1], reverse=True)
                text = ""
                lista_osob_pre = list()
                if len(wyniki2) > 1:
                    if len(wyniki) > 10:
                        for k in range(10):
                            rows = self.baza.get_data_about_person(int(AIModule.get_id_from_svm(int(wyniki2[k][0]))[0]))
                            text += ("ID=" + str(rows[0][2]) + " " + rows[0][0] + " " + rows[0][
                                1] + " z prawdopodobieństwem:" + str(wyniki2[k][1] * 100) + " %\n")
                            lista_osob_pre.append(
                                (rows[0][2], rows[0][0], rows[0][1], rows[0][3], rows[0][4], wyniki2[k][1] * 100))
                    else:
                        for k in range(len(wyniki2)):
                            rows = self.baza.get_data_about_person(int(AIModule.get_id_from_svm(int(wyniki2[k][0]))[0]))
                            text += ("ID=" + str(rows[0][2]) + " " + rows[0][0] + " " + rows[0][
                                1] + " z prawdopodobieństwem:" + str(wyniki2[k][1] * 100) + " %\n")
                            lista_osob_pre.append(
                                (rows[0][2], rows[0][0], rows[0][1], rows[0][3], rows[0][4], wyniki2[k][1] * 100))
                else:
                    msg = QMessageBox.information(self, "Komunikat zwrotny", "Unknown error during calculate face recognition analysis.",
                                                  QMessageBox.Yes)
                id = wyniki2[0][0]
                prob = round(wyniki2[0][1]*100, 2)
                rows = self.baza.get_data_about_person(int(AIModule.get_id_from_svm(int(id))[0]))
                macierz_wynikow.append((rows[0][0]+" "+rows[0][1], prob, face))
                textList.append(text)
                macierz_wynikowx = list()
                macierz_wynikowx.append(cv2.cvtColor(cv2.resize(face, (160, 160)), cv2.COLOR_BGR2RGB))
                macierz_wynikowx.append(wyniki2)
                macierz_wynikowx.append(lista_osob_pre)
                macierz_wynikow_generalna.append(macierz_wynikowx)
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "No face detected in the photo.",
                                          QMessageBox.Yes)
            return

        resultText.setText(textAnalizy)
        self.DialogSearchPeoplesFromPhotoShowResults(macierz_wynikow, textList, macierz_wynikow_generalna)


    def DialogSearchPeoplesFromPhotoShowResults(self, macierz_wynikow, textList, macierz_generalna):
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Recognition results")
        dialog.setGeometry(400, 200, 160 * 5 + 200, 320 + 20)
        groupBox = QGroupBox("Recognition results, detected faces with results")
        gridLayout = QGridLayout()
        photos_amount = len(macierz_wynikow)
        tableWidget = QTableWidget()
        qteaat = QTextEdit("")
        tableWidget.clicked.connect(lambda: self.DialogSearchPeoplesFromPhotoShowResultAnalysis(macierz_generalna, tableWidget.currentColumn()+tableWidget.currentRow()*5, qteaat))
        if photos_amount >=5:
            liczba_kolumn = 5
            if photos_amount%5==0:
                liczba_wierszy = int(photos_amount/5)
            else:
                liczba_wierszy=int(photos_amount / 5)+1
        else:
            liczba_kolumn = int(photos_amount%5)
            liczba_wierszy=1
        tableWidget.setRowCount(liczba_wierszy)
        tableWidget.setColumnCount(liczba_kolumn)
        tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        x = 0
        y = 0
        for i in range(photos_amount):
            item = CustomWidget2(macierz_wynikow[i][0] + " " + str(macierz_wynikow[i][1]) + "%", macierz_wynikow[i][2])
            tableWidget.setCellWidget(y, x, item)
            x += 1
            if x == 5:
                y += 1
                x = 0
        tableWidget.resizeColumnsToContents()
        tableWidget.resizeRowsToContents()
        gridLayout.addWidget(tableWidget, 0, 0)
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.close
        dialog.exec_()


    def DialogSearchPeoplesFromPhotoShowResultAnalysis(self, macierz_wynikow, index, text_analizy):
        if index >= len(macierz_wynikow):
            return
        macierz_wynikow=macierz_wynikow[index]
        face = macierz_wynikow[0]
        idClassifier_and_probability = macierz_wynikow[1]
        idDatabase_and_name_and_lastname = macierz_wynikow[2]
        nr_os1 = idDatabase_and_name_and_lastname[0][0]
        nr_os2 = idDatabase_and_name_and_lastname[1][0]
        nr_os3 = idDatabase_and_name_and_lastname[2][0]
        if len(os.listdir("./photos/"+str(nr_os1))) != 0:
            file_name = os.listdir("./photos/"+str(nr_os1))[0]
            face_one= cv2.imread("photos/"+str(nr_os1)+"/"+file_name)
        if len(os.listdir("./photos/"+str(nr_os2))) != 0:
            file_name = os.listdir("./photos/"+str(nr_os2))[0]
            face_two= cv2.imread("photos/"+str(nr_os2)+"/"+file_name)
        if len(os.listdir("./photos/"+str(nr_os3))) != 0:
            file_name = os.listdir("./photos/"+str(nr_os3))[0]
            face_three= cv2.imread("photos/"+str(nr_os3)+"/"+file_name)
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "Error during load face file.",
                                          QMessageBox.Yes)
        font = QtGui.QFont()
        font.setPointSize(10)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Face recognition among people from the database")
        dialog.setGeometry(400, 200, 110, 110)

        groupBox = QGroupBox("Recognition results")
        gridLayout = QGridLayout()

        label_face0_text = QTextEdit(self)
        label_face0_text.setEnabled(False)
        label_face0_text.setText("Face photo analyzed - ")
        gridLayout.addWidget(label_face0_text, 0, 0)

        label_face0 = QLabel("0")
        label_face0.setPixmap(get_QPixmap_from_frame(face))
        label_face0_text.setFont(font)
        gridLayout.addWidget(label_face0, 0, 1)

        label_face1_text = QTextEdit(self)
        label_face1_text.setEnabled(False)
        label_face1_text.setFont(font)
        label_face1_text.setText("The most likely person:\n"+"ID:"+str(idDatabase_and_name_and_lastname[0][0])+
                                 "\nName:"+idDatabase_and_name_and_lastname[0][1]+"\nSurname:"+idDatabase_and_name_and_lastname[0][2]+
                                 "\nConfidence level:"+str(round(idClassifier_and_probability[0][1]*100, 2))+str("%"))
        gridLayout.addWidget(label_face1_text, 1, 0)
        label_face1 = QLabel("1")
        label_face1.setPixmap(get_QPixmap_from_frame(face_one))
        gridLayout.addWidget(label_face1, 1, 1)

        label_face2_text = QTextEdit(self)
        label_face2_text.setEnabled(False)
        label_face2_text.setFont(font)
        label_face2_text.setText("The second most likely person:\n"+"ID:"+str(idDatabase_and_name_and_lastname[1][0])+
                                 "\nName:"+idDatabase_and_name_and_lastname[1][1]+"\nSurname:"+idDatabase_and_name_and_lastname[1][2]+
                                 "\nConfidence level:"+str(round(idClassifier_and_probability[1][1]*100, 2))+str("%"))
        gridLayout.addWidget(label_face2_text, 2, 0)
        label_face2 = QLabel("2")
        label_face2.setPixmap(get_QPixmap_from_frame(face_two))
        gridLayout.addWidget(label_face2, 2, 1)

        label_face3_text = QTextEdit(self)
        label_face3_text.setEnabled(False)
        label_face3_text.setFont(font)
        label_face3_text.setText("The third most likely person:\n"+"ID:"+str(idDatabase_and_name_and_lastname[2][0])+
                                 "\nName:"+idDatabase_and_name_and_lastname[2][1]+"\nSurname:"+idDatabase_and_name_and_lastname[2][2]+
                                 "\nConfidence level:"+str(round(idClassifier_and_probability[2][1]*100, 2))+str("%"))
        gridLayout.addWidget(label_face3_text, 3, 0)
        label_face3 = QLabel("3")
        label_face3.setPixmap(get_QPixmap_from_frame(face_three))
        gridLayout.addWidget(label_face3, 3, 1)

        label_info_text = QLabel("If the recognition is correct you can\nadd mst. correct photo to database",self)
        label_info_text.setFont(font2)
        gridLayout.addWidget(label_info_text, 4, 0)

        button_ok1 = QPushButton("Add a face photo", self)
        button_ok1.setMinimumHeight(40)
        button_ok1.clicked.connect(lambda: self.add_found_photo(face, idClassifier_and_probability[0][0], idDatabase_and_name_and_lastname[0][0]))
        gridLayout.addWidget(button_ok1, 4, 1)

        label_info_text = QLabel(
            "You can generate a search analysis",
            self)
        label_info_text.setFont(font2)
        gridLayout.addWidget(label_info_text, 5, 0)

        button_ok1 = QPushButton("Show search analysis", self)
        button_ok1.setMinimumHeight(40)
        button_ok1.clicked.connect(lambda: self.DialogShowRecognitionAnalysis(macierz_wynikow[2], text_analizy=text_analizy))
        gridLayout.addWidget(button_ok1, 5, 1)

        groupBox.setLayout(gridLayout)
        groupBox.adjustSize()
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.exec_()


    def DialogShowRecognitionAnalysis(self, dane, text_analizy ):
        liczba_kobiet = 0
        liczba_mezczyzn = 0
        for i in range(len(dane)):
            if dane[i][3] == 0:
                liczba_kobiet+=1
            elif dane[i][3] == 1:
                liczba_mezczyzn+=1

        liczba_bialych = 0
        liczba_czarnych = 0
        liczba_azjatow = 0
        for i in range(len(dane)):
            if dane[i][4] == 0:
                liczba_bialych += 1
            elif dane[i][4] == 1:
                liczba_czarnych += 1
            elif dane[i][4] == 2:
                liczba_azjatow += 1

        imiona_i_nazwiska = list()
        procenty = list()
        for i in range(len(dane)):
            imiona_i_nazwiska.append(dane[i][1]+" "+dane[i][2])
            procenty.append(dane[i][5])

        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Analysis of person search in the database")
        dialog.setGeometry(50, 50, 1800, 900)

        groupBox = QGroupBox("Diagrams showing individual distributions")
        gridLayout = QGridLayout()

        import stats
        canvas = stats.Canvas(self, width=6, height=4, title="Gender distribution")
        canvas2 = stats.Canvas(self, width=6, height=4, title="Race distribution")
        from numpy import array as NParray
        canvas.plot(NParray([liczba_mezczyzn, liczba_kobiet]), ["Men", "Women"])
        canvas2.plot(NParray([liczba_bialych, liczba_czarnych, liczba_azjatow]), lista_ras)
        gridLayout.addWidget(canvas, 0, 0)
        gridLayout.addWidget(canvas2, 0, 1)

        canvas3 = stats.Canvas2(self, width=12, height=4, title="Probability distribution for 10 most likely people", ylabel="Probability (%)")
        canvas3.plot(tuple(procenty), imiona_i_nazwiska)
        gridLayout.addWidget(canvas3, 1, 0, 1, 2)

        groupBox.setLayout(gridLayout)

        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)

        dialog.exec_()


    def DialogVideoAnalysis(self):
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Video Analysis")
        dialog.setGeometry(400, 100, 500, 400)

        groupBox = QGroupBox("Analyze video file")
        gridLayout = QGridLayout()

        boxFramesSelect = QGroupBox("Choose frames selection")
        hboxlayout3 = QHBoxLayout()
        FramesSelectCBox = QComboBox()
        boxFramesSelect.setLayout(hboxlayout3)
        FramesSelectCBox.addItem("All frames")
        FramesSelectCBox.addItem("1 frame = 1 sec")
        FramesSelectCBox.addItem("5 frame = 1 sec")
        hboxlayout3.addWidget(FramesSelectCBox)
        gridLayout.addWidget(boxFramesSelect, 0, 0)

        boxFaceDetectionSelect = QGroupBox("Specify the minimum % of face detection precision")
        hboxlayout4 = QHBoxLayout()
        confidenceFaceDetectionSpin = QSpinBox()
        boxFaceDetectionSelect.setLayout(hboxlayout4)
        confidenceFaceDetectionSpin.setMinimum(0)
        confidenceFaceDetectionSpin.setMaximum(99)
        confidenceFaceDetectionSpin.setValue(95)
        hboxlayout4.addWidget(confidenceFaceDetectionSpin)
        gridLayout.addWidget(boxFaceDetectionSelect, 1, 0)

        boxFaceRecognitionSelect = QGroupBox("Specify the minimum % of face recognition precision")
        hboxlayout5 = QHBoxLayout()
        confidenceFaceRecognitionSpin = QSpinBox()
        boxFaceRecognitionSelect.setLayout(hboxlayout5)
        confidenceFaceRecognitionSpin.setMinimum(0)
        confidenceFaceRecognitionSpin.setMaximum(99)
        confidenceFaceRecognitionSpin.setValue(95)
        hboxlayout5.addWidget(confidenceFaceRecognitionSpin)
        gridLayout.addWidget(boxFaceRecognitionSelect, 2, 0)

        faceRatioSelect = QGroupBox("Min face size, percentage ratio to the whole photo")
        hboxlayout6 = QHBoxLayout()
        faceRatioSpin = QSpinBox()
        faceRatioSelect.setLayout(hboxlayout6)
        faceRatioSpin.setMinimum(0)
        faceRatioSpin.setMaximum(95)
        faceRatioSpin.setValue(10)
        hboxlayout6.addWidget(faceRatioSpin)
        gridLayout.addWidget(faceRatioSelect, 3, 0)
        box1 = QGroupBox("Select the option to search the movie")
        hbox1 = QVBoxLayout()
        self.zwrotne_id = -1
        self.zwrotne_id_opcja_video = 3
        qspinbox_id = QPushButton("Select person from DB", self)
        button_face = QPushButton("Choose photo file", self)
        radiobutton = QRadioButton("Compare only face from image")
        radiobutton.country = "0"
        radiobutton.clicked.connect(lambda: self.radio_option_video_search(button_face, qspinbox_id))
        hbox1.addWidget(radiobutton)
        radiobutton = QRadioButton("Select person from db")
        radiobutton.clicked.connect(lambda: self.radio_option_video_search(button_face, qspinbox_id))
        radiobutton.country = "2"
        hbox1.addWidget(radiobutton)
        radiobutton = QRadioButton("Check the database for each face photo in the video")
        radiobutton.clicked.connect(lambda: self.radio_option_video_search(button_face, qspinbox_id))
        radiobutton.setChecked(True)
        radiobutton.country = "3"
        hbox1.addWidget(radiobutton)
        box1.setLayout(hbox1)
        gridLayout.addWidget(box1, 4, 0)
        box2 = QGroupBox("Select person from database")
        vbox2 = QVBoxLayout()
        label_id = QLabel("Person ID from db - (None)", self)
        vbox2.addWidget(label_id)
        qspinbox_id.clicked.connect(lambda: self.DialogDatabaseManagementForVideo(self.baza.get_number_of_people_in_database(), label_id))
        vbox2.addWidget(qspinbox_id)
        box2.setLayout(vbox2)
        gridLayout.addWidget(box2, 5, 0)

        box3 = QGroupBox("Select face photo")
        hbox3 = QVBoxLayout()
        button_face.setMinimumHeight(20)
        self.label_face = QLabel()
        self.label_face.setAlignment(QtCore.Qt.AlignCenter)
        hbox3.addWidget(button_face)
        self.testPhotoPath = QTextEdit("")
        self.testPhotoPath.setEnabled(False)
        self.testPhotoPath.setMinimumHeight(28)
        self.testPhotoPath.setMaximumHeight(28)
        hbox3.addWidget(self.testPhotoPath)
        # hbox3.addWidget(self.label_face)
        box3.setLayout(hbox3)
        button_face.clicked.connect(lambda: self.choose_photo_to_find_on_video(self.label_face))
        gridLayout.addWidget(box3, 6, 0)

        #####################################
        # ustawienia przelaczania#
        qspinbox_id.setEnabled(False)
        button_face.setEnabled(False)
        box33 = QGroupBox("Select face photo")
        hbox33 = QVBoxLayout()
        buttonChoosePhoto = QPushButton("Choose video file", self)
        buttonChoosePhoto.setMinimumHeight(20)
        buttonChoosePhoto.clicked.connect(self.choose_video_file)
        hbox33.addWidget(buttonChoosePhoto)
        self.testVideoPath = QTextEdit("")
        self.testVideoPath.setEnabled(False)
        self.testVideoPath.setMinimumHeight(28)
        self.testVideoPath.setMaximumHeight(28)
        hbox33.addWidget(self.testVideoPath)
        box33.setLayout(hbox33)
        gridLayout.addWidget(box33, 7, 0)

        buttonStartSearchingMtcnn = QPushButton("Start the analysis", self)
        buttonStartSearchingMtcnn.setMinimumHeight(20)
        buttonStartSearchingMtcnn.clicked.connect(
            lambda: self.DialogVideoAnalysisCalculate(self.video_file_path, FramesSelectCBox.currentIndex(),
                                              0, confidenceFaceDetectionSpin.value(),
                                              confidenceFaceRecognitionSpin.value(), faceRatioSpin.value()))
        gridLayout.addWidget(buttonStartSearchingMtcnn, 8, 0)

        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.exec_()


    def DialogDatabaseManagementForVideo(self, x, label_id):
        label_id.setText("Person ID from db - (None)")
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Database Management")
        dialog.setGeometry(400, 200, 939, 340)

        groupBox = QGroupBox("Database Management")
        gridLayout = QGridLayout()

        tableWidget = QTableWidget()
        tableWidget.clear()
        tableWidget.setRowCount(0)
        self.do_testu=tableWidget
        tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        tableWidget.setRowCount(x)
        tableWidget.setColumnCount(8)
        tableWidget.setHorizontalHeaderLabels(["ID", "Firstname", "Lastname", "Gender", "DoB", "Nationality", "Rasy", "Number of photos"])
        liczba = self.baza.get_number_of_people_in_database()
        tab = self.baza.view_date_order_by_firstname_and_lastname()

        plec = ["Women","Men"]
        kraje = lista_panstw
        rasy = lista_ras

        for x in range(liczba):
            for y in [z for z in range(0,8) if z!=3 and z!=5 and z!=6]:
                item = QTableWidgetItem(str(tab[x][y]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                tableWidget.setItem(x, y, item)

            item = QTableWidgetItem(str( plec[int(tab[x][3])] ) )
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 3, item)

            item = QTableWidgetItem(str(kraje[int(tab[x][5])]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 5, item)

            item = QTableWidgetItem(str(rasy[int(tab[x][6])]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 6, item)

        tableWidget.resizeColumnsToContents()

        gridLayout.addWidget(tableWidget, 0, 0)

        groupBoxWew = QGroupBox("Face")
        gridLayoutWew = QGridLayout()

        etykieta_zdjecia = QLabel(self)
        etykieta_zdjecia.setMinimumSize(160,160)
        etykieta_zdjecia.setMaximumSize(160,160)
        gridLayoutWew.addWidget(etykieta_zdjecia, 0, 0)

        etykieta_zdjecia2 = QLabel(self)
        etykieta_zdjecia2.setMinimumSize(160, 160)
        etykieta_zdjecia2.setMaximumSize(160, 160)
        gridLayoutWew.addWidget(etykieta_zdjecia2, 0, 1)

        etykieta_zdjecia3 = QLabel(self)
        etykieta_zdjecia3.setMinimumSize(160, 160)
        etykieta_zdjecia3.setMaximumSize(160, 160)
        gridLayoutWew.addWidget(etykieta_zdjecia3, 1, 0)

        etykieta_zdjecia4 = QLabel(self)
        etykieta_zdjecia4.setMinimumSize(160, 160)
        etykieta_zdjecia4.setMaximumSize(160, 160)
        gridLayoutWew.addWidget(etykieta_zdjecia4, 1, 1)
        groupBoxWew.setLayout(gridLayoutWew)
        gridLayout.addWidget(groupBoxWew,0,1)
        groupBoxWewx = QGroupBox("")
        gridLayoutWewx = QGridLayout()
        self.zwrotne_id = -1
        zatwierdz_zdjecie = QPushButton("Accept")
        zatwierdz_zdjecie.setMinimumHeight(20)
        zatwierdz_zdjecie.clicked.connect(lambda: self.DialogDatabaseManagementForVideoSelectPerson(dialog, label_id))
        gridLayoutWewx.addWidget(zatwierdz_zdjecie)
        groupBoxWewx.setLayout(gridLayoutWewx)
        gridLayout.addWidget(groupBoxWewx, 1,0)
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)

        tableWidget.clicked.connect(lambda: self.db_management_for_video_cell_click(tableWidget, tableWidget.currentRow(),
                                                                  tableWidget.item(tableWidget.currentRow(),
                                                                                   0).text(), etykieta_zdjecia, etykieta_zdjecia2, etykieta_zdjecia3, etykieta_zdjecia4))
        dialog.exec_()


    def DialogDatabaseManagementForVideoSelectPerson(self, dialog, label_id):
        if self.zwrotne_id != -1:
            dialog.accept()
            label_id.setText("Person ID from db = (" + str(self.zwrotne_id) + ")")
            msg = QMessageBox.information(self, "Komunikat zwrotny", "The person from the base was correctly selected.", QMessageBox.Yes)
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "Select a person from the database or close the window.",
                                          QMessageBox.Yes)


    def DialogVideoAnalysisCalculate(self, video_path, divider, option, confidenceFaceDetection=95, confidenceFaceClasification=90, face_size=10):
        if self.zwrotne_id_opcja_video ==0:
            if self.testPhotoPath.toPlainText() == "" or self.video_file_path=="":
                msg = QMessageBox.information(self, "Komunikat zwrotny", "You must first select a movie and photo.",
                                              QMessageBox.Yes)
                return
        elif self.zwrotne_id_opcja_video == 2:
            if self.zwrotne_id == -1:
                msg = QMessageBox.information(self, "Komunikat zwrotny", "You must select a person from the database.",
                                              QMessageBox.Yes)
                return
            if self.video_file_path =="":
                msg = QMessageBox.information(self, "Komunikat zwrotny", "You must select a video.",
                                              QMessageBox.Yes)
                return
        elif self.zwrotne_id_opcja_video == 3:
            if self.video_file_path =="":
                msg = QMessageBox.information(self, "Komunikat zwrotny", "You must select a video.",
                                              QMessageBox.Yes)
                return

        if option == 0:
            from video import getFacesFromVideoWithMtcnn
            faces, prob = getFacesFromVideoWithMtcnn(video_path, divider, confidenceFaceDetection, face_size)
        """elif option == 1:
            from video_module import getFacesFromVideoWithDlib
            faces, prob = getFacesFromVideoWithDlib(video_path, divider)
        elif option == 2:
            from video_module import getFacesFromVideoWithOpenCvDnn
            faces, prob = getFacesFromVideoWithOpenCvDnn(video_path, divider, confidenceFaceDetection, 160, 160)"""
        if len(faces) == 0:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "No face detected in the movie",
                                          QMessageBox.Yes)
            return

        macierz_wynikow = list()
        for i in range(len(faces)):
            macierz_wynikow.append(("xxx",prob[i],faces[i]))
        self.DialogVideoAnalysisShowResults(faces, prob, self.zwrotne_id, self.zwrotne_id_opcja_video, wymagana_dokladnosc_klasyfikacji=confidenceFaceClasification)


    def DialogVideoAnalysisShowResults(self, lista_zdjec_twarzy, lista_prob, id_osoby_z_bazy, opcja_wyszukiwania,
                                       wymagana_dokladnosc_klasyfikacji):
        if self.zwrotne_id_opcja_video == 0:
            from numpy import asarray
            foto = asarray(self.PhotoNr2)
            wektor = AIModule.get_embedding(foto)
            lista_resized = list()
            for i in lista_zdjec_twarzy:
                lista_resized.append(cv2.resize(i, (160, 160)))
            lista_zdjec_wektory = list()
            for i in lista_resized:
                lista_zdjec_wektory.append(AIModule.get_embedding(i))
            from comparison import l2_normalize
            from scipy.spatial import distance
            lista_zdjec_wektory_po_normalizacji = list()
            for i in lista_zdjec_wektory:
                lista_zdjec_wektory_po_normalizacji.append(l2_normalize(i))
            lista_dystansow = list()
            wektor_po_normalizacji = l2_normalize(wektor)
            for i in lista_zdjec_wektory_po_normalizacji:
                lista_dystansow.append(distance.euclidean(wektor_po_normalizacji, i))
            lista_do_wyswietlenia = list()
            for i in range(len(lista_dystansow)):
                prob = AIModule.return_probability_from_distance(lista_dystansow[i])
                if prob > wymagana_dokladnosc_klasyfikacji:
                    lista_do_wyswietlenia.append((prob, lista_zdjec_twarzy[i]))
            if len(lista_do_wyswietlenia) != 0:
                self.DialogVideoAnalysisFromFaceShowResults(lista_do_wyswietlenia)
            else:
                msg = QMessageBox.information(self, "Komunikat zwrotny",
                                              "This person was not found in the movie.",
                                              QMessageBox.Yes)
                return
        else:
            ilosc_twarzy = len(lista_zdjec_twarzy)
            macierz_wynikow = list()
            textAnalizy = ""
            textList = list()
            macierz_wynikow_generalna = list()
            if ilosc_twarzy > 0:
                for i in range(ilosc_twarzy):
                    face = lista_zdjec_twarzy[i]
                    class_proba = AIModule.find_person_from_face_image_to_video_search(face)
                    positions_and_probs = list(enumerate(class_proba[0]))
                    sorted_positions_and_probs = sorted(positions_and_probs,
                                                        key=lambda l: l[1], reverse=True)
                    text = ""
                    lista_osob_pre = list()
                    if len(sorted_positions_and_probs) > 1:
                        if len(positions_and_probs) > 10:
                            for k in range(10):
                                row = self.baza.get_data_about_person(
                                    int(AIModule.get_id_from_svm
                                        (int(sorted_positions_and_probs[k][0]))[0]))
                                text += ("ID=" + str(row[0][2]) + " " + row[0][0] + " " + row[0][
                                    1] + " z prawdopodobieństwem:" + str(sorted_positions_and_probs[k][1] * 100) + " %\n")
                                lista_osob_pre.append(
                                    (row[0][2], row[0][0], row[0][1], row[0][3], row[0][4], sorted_positions_and_probs[k][1] * 100))
                        else:
                            for k in range(len(sorted_positions_and_probs)):
                                row = self.baza.get_data_about_person(
                                    int(AIModule.get_id_from_svm(int(sorted_positions_and_probs[k][0]))[0]))
                                text += ("ID=" + str(row[0][2]) + " " + row[0][0] + " " + row[0][
                                    1] + " z prawdopodobieństwem:" + str(sorted_positions_and_probs[k][1] * 100) + " %\n")
                                lista_osob_pre.append(
                                    (row[0][2], row[0][0], row[0][1], row[0][3], row[0][4], sorted_positions_and_probs[k][1] * 100))
                    else:
                        msg = QMessageBox.information(self, "Komunikat zwrotny", "Unknown error during video analysis.",
                                                      QMessageBox.Yes)
                    id = sorted_positions_and_probs[0][0]
                    prob = round(sorted_positions_and_probs[0][1] * 100, 2)
                    row = self.baza.get_data_about_person(
                        int(AIModule.get_id_from_svm(int(id))[0]))
                    macierz_wynikow.append((row[0][0] + " " + row[0][1], prob, face, row[0][2]))
                    textList.append(text)

                    macierz_wynikowx = list()
                    macierz_wynikowx.append(cv2.cvtColor(cv2.resize(face, (160, 160)), cv2.COLOR_BGR2RGB))
                    macierz_wynikowx.append(sorted_positions_and_probs)
                    macierz_wynikowx.append(lista_osob_pre)
                    macierz_wynikow_generalna.append(macierz_wynikowx)
            else:
                msg = QMessageBox.information(self, "Komunikat zwrotny", "No face detected in the photo.",
                                              QMessageBox.Yes)
                return
            macierz_wynikow2 = list()
            textList2 = list()
            macierz_wynikow_generalna2 = list()
            for i in range(len(macierz_wynikow)):
                if macierz_wynikow[i][1] >= wymagana_dokladnosc_klasyfikacji:
                    macierz_wynikow2.append(macierz_wynikow[i])
                    textList2.append(textList[i])
                    macierz_wynikow_generalna2.append(macierz_wynikow_generalna[i])
            macierz_wynikow_generalna = macierz_wynikow_generalna2
            macierz_wynikow = macierz_wynikow2

            if self.zwrotne_id_opcja_video == 2:
                if id_osoby_z_bazy != -1:
                    macierz_wynikow3 = list()
                    textList3 = list()
                    for i in range(len(macierz_wynikow)):
                        if int(id_osoby_z_bazy) == int(macierz_wynikow[i][3]):
                            macierz_wynikow3.append(macierz_wynikow[i])
                            textList3.append(textList2[i])
                    if (len(macierz_wynikow3) != 0):
                        self.DialogSearchPeoplesFromPhotoShowResults(macierz_wynikow, textList,
                                                                     macierz_wynikow_generalna)
                    else:
                        msg = QMessageBox.information(self, "Komunikat zwrotny",
                                                      "This person was not found in the movie.",
                                                      QMessageBox.Yes)
                else:
                    msg = QMessageBox.information(self, "Komunikat zwrotny", "Wrong ID.",
                                                  QMessageBox.Yes)
            elif self.zwrotne_id_opcja_video == 3:
                if len(macierz_wynikow) !=0:
                    self.DialogSearchPeoplesFromPhotoShowResults(macierz_wynikow, textList, macierz_wynikow_generalna)
                else:
                    msg = QMessageBox.information(self, "Komunikat zwrotny",
                                                  "No matches found.",
                                                  QMessageBox.Yes)

    def DialogVideoAnalysisFromFaceShowResults(self, macierz_wynikow):
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Database Management")
        dialog.setGeometry(400, 200, 160*5+200, 320+20)

        groupBox = QGroupBox("Database Management")
        gridLayout = QGridLayout()
        photos_amount = len(macierz_wynikow)
        tableWidget = QTableWidget()
        liczba_wierszy = int(photos_amount/5)
        if liczba_wierszy>0:
            liczba_kolumn=5
            liczba_wierszy+=1
        else:
            liczba_kolumn=photos_amount%5
            liczba_wierszy=1
        tableWidget.setRowCount(liczba_wierszy)
        tableWidget.setColumnCount(liczba_kolumn)
        tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        x,y = 0,0
        for i in range(photos_amount):
            item = CustomWidget2(str(macierz_wynikow[i][0])+"%", macierz_wynikow[i][1])
            tableWidget.setCellWidget(y, x, item)
            x += 1
            if x == 5:
                y += 1
                x = 0
        tableWidget.resizeColumnsToContents()
        tableWidget.resizeRowsToContents()
        gridLayout.addWidget(tableWidget, 0, 0)
        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)

        dialog.close
        dialog.exec_()


    def DialogCompareTwoGroupFaces(self):
        self.tablica_zdjec_os1 = list()
        self.tablica_zdjec_os2 = list()

        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Compare Two Faces")
        dialog.setGeometry(400, 200, 512, 300)

        groupBox = QGroupBox("Choose photos and start compare")
        gridLayout = QGridLayout()

        pole1 = QTextEdit("No photos selected.")
        pole1.setEnabled(False)
        pole1.setMinimumHeight(28)
        pole1.setMaximumHeight(28)

        pole2 = QTextEdit("No photos selected.")
        pole2.setEnabled(False)
        pole2.setMinimumHeight(28)
        pole2.setMaximumHeight(28)

        buttonChoosePhoto1 = QPushButton("Choose photo file face Nr.1", self)
        buttonChoosePhoto1.clicked.connect(lambda: self.choose_face_files_to_compare(1, pole1))
        gridLayout.addWidget(buttonChoosePhoto1, 0, 0)

        buttonChoosePhoto2 = QPushButton("Choose photo file face Nr.2", self)
        buttonChoosePhoto2.clicked.connect(lambda: self.choose_face_files_to_compare(2, pole2))
        gridLayout.addWidget(buttonChoosePhoto2, 0, 1)

        gridLayout.addWidget(pole1, 1, 0)
        gridLayout.addWidget(pole2, 1, 1)

        self.labelFace1 = QLabel("")
        self.labelFace1.setMinimumSize(256, 256)
        self.labelFace1.setMaximumSize(256, 256)
        self.labelFace1.setStyleSheet("QLabel{margin: 10px; border-radius: 25px; background: white; color: #4A0C46;}")
        gridLayout.addWidget(self.labelFace1, 2, 0)

        self.labelFace2 = QLabel("")
        self.labelFace2.setMinimumSize(256, 256)
        self.labelFace2.setMaximumSize(256, 256)
        self.labelFace2.setStyleSheet("QLabel{margin: 10px; border-radius: 25px; background: white; color: #4A0C46;}")
        gridLayout.addWidget(self.labelFace2, 2, 1)

        textResult = QLineEdit("")
        textResult.setEnabled(False)
        textResult.setPlaceholderText("Wyniki:")

        buttonStartCompare = QPushButton("Start comparing", self)
        buttonStartCompare.setMinimumHeight(28)
        buttonStartCompare.setMaximumHeight(28)
        buttonStartCompare.clicked.connect(lambda: self.DialogCompareTwoGroupsFacesShowResult(self.tablica_zdjec_os1, self.tablica_zdjec_os2))
        gridLayout.addWidget(buttonStartCompare, 3, 0)

        self.textPodobienstwo = QTextEdit("Similarity percentage: ")
        self.textPodobienstwo.setEnabled(False)
        self.textPodobienstwo.setMinimumHeight(28)
        self.textPodobienstwo.setMaximumHeight(28)
        gridLayout.addWidget(self.textPodobienstwo, 3, 1)

        groupBox.setLayout(gridLayout)

        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)

        dialog.exec()
        dialog.show()


    def DialogCompareTwoGroupsFacesShowResult(self, lista_zdjec_os_1, lista_zdjec_os_2):
        if len(lista_zdjec_os_1) < 1:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "The number of photos of the first person does not match.", QMessageBox.Yes)
            return
        elif len(lista_zdjec_os_2) < 1:
            msg = QMessageBox.information(self, "Komunikat zwrotny",
                                          "The number of photos of the second person does not match", QMessageBox.Yes)
            return
        import numpy as np
        wektory_osoby_nr_1 = list()
        wektory_osoby_nr_2 = list()
        for i in lista_zdjec_os_1:
                x = AIModule.get_embedding(np.asarray(i))
                wektory_osoby_nr_1.append(x)
        for i in lista_zdjec_os_2:
                x = AIModule.get_embedding(np.asarray(i))
                wektory_osoby_nr_2.append(x)
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Compare Two Faces")
        dialog.setGeometry(400, 200, 512, 300)

        groupBox = QGroupBox("Choose photos and start compare")
        gridLayout = QGridLayout()

        buttonAnaliza2D = QPushButton("Analiza 2D")
        buttonAnaliza3D = QPushButton("Analiza 3D")
        buttonHistogram = QPushButton("Histogram")
        textPrawdopodobienstwo = QTextEdit("Similarity percentage:")
        textPrawdopodobienstwo.setMinimumHeight(28)
        textPrawdopodobienstwo.setMaximumHeight(28)
        textPrawdopodobienstwo.setEnabled(False)

        gridLayout.addWidget(buttonAnaliza2D, 0, 0)
        gridLayout.addWidget(buttonAnaliza3D, 1, 0)
        gridLayout.addWidget(buttonHistogram, 2, 0)
        gridLayout.addWidget(textPrawdopodobienstwo, 3, 0)

        import comparison
        e = comparison.genHistDataForTwoGroups(wektory_osoby_nr_1, wektory_osoby_nr_2)
        from statistics import median
        from statistics import mean

        if len(e) == 0:
            self.textPodobienstwo.setText(
                "Similarity: " + str(AIModule.return_probability_from_distance(0)) + "%")
        else:
            self.textPodobienstwo.setText("Similarity: "+str(AIModule.return_probability_from_distance(median(e)))+"%")
        if (len(wektory_osoby_nr_1)+len(wektory_osoby_nr_2)) > 2:
            textPrawdopodobienstwo.setText(
                "Similarity: " + str(AIModule.return_probability_from_distance(median(e))) +"%")
            x, y, z = comparison.gen3DAnalysisForComparison(wektory_osoby_nr_1, wektory_osoby_nr_2)
            a, b, c, d = comparison.gen2DAnalysisForComparison(wektory_osoby_nr_1, wektory_osoby_nr_2)
            buttonAnaliza2D.clicked.connect(lambda: comparison.show2DAnalysisForComparison(a, b, c, d))
            buttonAnaliza3D.clicked.connect(lambda: comparison.show3DAnalysisForComparison(x, y, z))
            buttonHistogram.clicked.connect(lambda: comparison.drawHist(e))

            groupBox.setLayout(gridLayout)

            vbox = QVBoxLayout()
            vbox.addWidget(groupBox)
            dialog.setLayout(vbox)

            dialog.exec()
            dialog.show()


    def DialogCameraMainWindow(self):
        mpx = self
        #klasa MyQDialog zdefiniowana w celu obslugi zamykania okna
        class MyQDialog(QDialog):
            def closeEvent(self, event):
                if mpx.cam_name != "":
                    if mpx.cam_name !="":
                        cv2.destroyWindow(mpx.cam_name)
                        mpx.stan_kamery=False

        dialog = MyQDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Camera image processing")
        dialog.setGeometry(400, 200, 300, 300)

        groupBox = QGroupBox("Camera management")
        gridLayout = QGridLayout()

        box1 = QGroupBox("Select camera")
        hbox1 = QHBoxLayout()

        box1.setLayout(hbox1)
        gridLayout.addWidget(box1, 0,0,1,3)
        buttonPodglad = QPushButton("Image preview")
        buttonPodglad.clicked.connect(lambda: self.cam_preview(self.wybrana_kamerka))
        buttonZrzut = QPushButton("Screenshot")
        buttonZrzut.clicked.connect(self.cam_capture_image)
        buttonRozpoznawanie = QPushButton("Face recognition")
        buttonRozpoznawanie.clicked.connect(lambda: self.cam_recognition(self.wybrana_kamerka))
        buttonPodglad.setEnabled(False)
        buttonZrzut.setEnabled(False)
        buttonRozpoznawanie.setEnabled(False)

        liczba_wykrytych_kamer = countCams()
        self.wybrana_kamerka = -1
        self.cam_name=""
        self.stan_kamery=True
        for i in range(liczba_wykrytych_kamer):
            radiobutton = QRadioButton("Camera numer: " + str(i + 1))
            radiobutton.country = str(i)
            radiobutton.clicked.connect(lambda: self.radio_button_select_camera(buttonRozpoznawanie, buttonZrzut, buttonPodglad))
            hbox1.addWidget(radiobutton)

        gridLayout.addWidget(buttonPodglad, 1, 0)
        gridLayout.addWidget(buttonZrzut, 1, 1)
        gridLayout.addWidget(buttonRozpoznawanie, 1, 2)

        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)
        dialog.exec()


    def DialogAIModuleMenu(self):
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("AI Module options")
        dialog.setGeometry(400, 200, 300, 300)

        groupBox = QGroupBox("Embedding and classifier management")
        gridLayout = QGridLayout()

        buttonTrainFaceNetClassifierSVM = QPushButton("Generate facial embedding", self)
        buttonTrainFaceNetClassifierSVM.clicked.connect(AIModule.get_db_emb)
        gridLayout.addWidget(buttonTrainFaceNetClassifierSVM, 0, 0)

        buttonTrainVGGClassifierSVM = QPushButton("Train SVM classifier", self)
        buttonTrainVGGClassifierSVM.clicked.connect(AIModule.train_svm)
        gridLayout.addWidget(buttonTrainVGGClassifierSVM, 1, 0)

        import menagetimes as tzd
        etykieta_czas_generowania_wektorow = QLabel("Date of last generation face embedding:")
        czas_generowania_wektorow = QTextEdit(tzd.read_time_from_file('gen_time/vectors_time.txt'), self)
        czas_generowania_wektorow.setEnabled(False)
        etykieta_czas_trenowania_svm = QLabel("Date of last classifier training:")
        czas_trenowania_svm = QTextEdit(tzd.read_time_from_file('gen_time/svm_time.txt'), self)
        czas_trenowania_svm.setEnabled(False)
        gridLayout.addWidget(etykieta_czas_generowania_wektorow, 2, 0)
        gridLayout.addWidget(czas_generowania_wektorow, 3, 0)
        gridLayout.addWidget(etykieta_czas_trenowania_svm, 4 ,0)
        gridLayout.addWidget(czas_trenowania_svm, 5, 0)

        etykieta_postepu = QLabel("Process progress:")
        text_generowania_wektorow = QTextEdit("", self)
        text_generowania_wektorow.setEnabled(False)

        gridLayout.addWidget(etykieta_postepu, 6, 0)
        gridLayout.addWidget(text_generowania_wektorow, 7, 0)

        groupBox.setLayout(gridLayout)

        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)

        dialog.exec()
        dialog.show()


    def DialogAnalysisDatabase(self):
        liczba_kobiet = self.baza.get_amount_one_gender_people(0)
        liczba_mezczyzn = self.baza.get_amount_one_gender_people(1)
        liczba_bialych_osob_w_bazie = self.baza.get_amount_one_race_people(0)
        liczba_czarnych_osob_w_bazie = self.baza.get_amount_one_race_people(1)
        liczba_azjatow_w_bazie = self.baza.get_amount_one_race_people(2)
        dir = "./photos"
        lista_folderow = os.listdir(dir)
        liczba_zdjec_w_folderze=0
        lista_do_mediany = list()
        for i in range(len(lista_folderow)):
            path = dir + "/" + lista_folderow[i]
            liczba_zdjec_dla_osoby_pod_sciezka = len(next(os.walk(path))[2])
            lista_do_mediany.append(liczba_zdjec_dla_osoby_pod_sciezka)
            liczba_zdjec_w_folderze += liczba_zdjec_dla_osoby_pod_sciezka
        liczba_osob_w_bazie_wedlug_folderu_photos = len(lista_folderow)
        srednia_liczba_zdjec = round(liczba_zdjec_w_folderze/
                                     liczba_osob_w_bazie_wedlug_folderu_photos,2)
        from statistics import median
        mediana_liczby_zdjec = round(median(lista_do_mediany),2)
        najmniejsza_liczba_zdjec = min(lista_do_mediany)
        najwieksza_liczba_zdjec = max(lista_do_mediany)
        lista_do_mediany.sort()
        from numpy import percentile
        kwartyl_025 = round(percentile(lista_do_mediany,25),2)
        kwartyl_075 = round(percentile(lista_do_mediany, 75),2)

        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Analysis the database")
        dialog.setGeometry(50, 50, 1800, 900)

        groupBox = QGroupBox("Diagrams showing database distributions")
        gridLayout = QGridLayout()

        import stats
        canvas = stats.Canvas(self, width=6, height=4, title="Gender distribution")
        canvas2 = stats.Canvas(self, width=6, height=4, title="Race distribution")
        from numpy import array as NParray
        canvas.plot(NParray([liczba_mezczyzn, liczba_kobiet]), ["Men", "Women"])
        canvas2.plot(NParray([liczba_bialych_osob_w_bazie, liczba_czarnych_osob_w_bazie, liczba_azjatow_w_bazie]), lista_ras)
        gridLayout.addWidget(canvas, 0, 0)
        gridLayout.addWidget(canvas2, 0, 1)

        canvas3 = stats.Canvas3(self, width=12, height=4,
                                     title="Number of photos distribution",
                                     ylabel="Number of photos",
                                     xlabel="People in the database")
        canvas3.plot(tuple(lista_do_mediany),[])
        gridLayout.addWidget(canvas3, 1, 0, 1, 2)

        button1 = QPushButton("Embedding visualization module")
        button1.setMinimumHeight(90)
        button1.setStyleSheet("font-size: 18px;")
        button1.clicked.connect(self.DialogFaceEmbeddingVisualization)

        gridLayout.addWidget(button1, 2, 0)

        statystyki_text = QTextEdit("")
        statystyki_text.setFontPointSize(12)
        statystyki_text.setText("   The smallest number of photos: "+str(najmniejsza_liczba_zdjec)
                                    +"  The largest number of photos: "+str(najwieksza_liczba_zdjec)+"\n"
                                    +"   Average number of photos: "+str(srednia_liczba_zdjec)
                                    +"   Quartile 0.25: " + str(kwartyl_025)+"\n"
                                    +"   Median: "+ str(mediana_liczby_zdjec)
                                    +"                                   Quartile 0.75: "+ str(kwartyl_075) + "\n")
        statystyki_text.setEnabled(False)
        gridLayout.addWidget(statystyki_text, 2, 1, 3, 1)
        groupBox.setLayout(gridLayout)

        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)

        dialog.exec_()


    def DialogFaceEmbeddingVisualization(self):
        lista_osob = list()
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Embedding visualization module")
        dialog.setGeometry(400, 200, 300, 300)

        groupBox = QGroupBox("Embedding visualization ")
        gridLayout = QGridLayout()

        box1 = QGroupBox("Select an option for visualization")
        hbox1 = QHBoxLayout()

        qspinbox_id = QPushButton("Select person from DB")
        button_face = QPushButton("Choose photo file", self)

        label_data_generowania = QLabel("Date of last data generation:", self)
        text_data_generowania = QLineEdit("First choose a visualization method", self)
        text_data_generowania.setEnabled(False)

        self.aktualny_radio_button = -1
        self.aktualny_radio_button_osoby = 0

        radiobutton = QRadioButton("PCA 2D")
        radiobutton.country = "0"
        radiobutton.clicked.connect(lambda: self.radio_option_alg_select(text_data_generowania, textGenerowanie))
        hbox1.addWidget(radiobutton)

        radiobutton = QRadioButton("PCA 3D")
        radiobutton.clicked.connect(lambda: self.radio_option_alg_select(text_data_generowania, textGenerowanie))
        radiobutton.country = "1"
        hbox1.addWidget(radiobutton)

        radiobutton = QRadioButton("t-SNE 2D")
        radiobutton.clicked.connect(lambda: self.radio_option_alg_select(text_data_generowania, textGenerowanie))
        radiobutton.country = "2"
        hbox1.addWidget(radiobutton)

        radiobutton = QRadioButton("t-SNE 3D")
        radiobutton.clicked.connect(lambda: self.radio_option_alg_select(text_data_generowania, textGenerowanie))
        radiobutton.country = "3"
        hbox1.addWidget(radiobutton)

        radiobutton = QRadioButton("UMAP 2D")
        radiobutton.clicked.connect(lambda: self.radio_option_alg_select(text_data_generowania, textGenerowanie))
        radiobutton.country = "5"
        hbox1.addWidget(radiobutton)

        radiobutton = QRadioButton("UMAP 3D")
        radiobutton.clicked.connect(lambda: self.radio_option_alg_select(text_data_generowania, textGenerowanie))
        radiobutton.country = "6"
        hbox1.addWidget(radiobutton)

        radiobutton = QRadioButton("Histogram of Euclidean distances")
        radiobutton.clicked.connect(lambda: self.radio_option_alg_select(text_data_generowania, textGenerowanie))
        radiobutton.country = "4"
        hbox1.addWidget(radiobutton)

        box1.setLayout(hbox1)

        gridLayout.addWidget(box1, 0, 0, 1, 2)
        gridLayout.addWidget(label_data_generowania, 1, 0, 1, 1)
        text_data_generowania.setMinimumWidth(160)
        gridLayout.addWidget(text_data_generowania, 1, 1)

        etykiety_yes = QCheckBox("Enable labels for each embedding?", self)
        gridLayout.addWidget(etykiety_yes, 2, 0)

        buttonWyborOsoby = QPushButton("People selection", self)
        buttonWyborOsoby.setEnabled(False)


        etykieta_wyboru_osob = QLabel("All people selected", self)
        buttonWyborOsoby.clicked.connect(
            lambda: self.DialogDatabaseManagementForDbVizualization(self.baza.get_number_of_people_in_database(), etykieta_wyboru_osob, lista_osob))

        box2 = QGroupBox("Choose whose data you want to visualize")
        hbox2 = QHBoxLayout()

        radiobutton2 = QRadioButton("Everyone in the database")
        radiobutton2.country = "0"
        radiobutton2.setChecked(True)
        radiobutton2.clicked.connect(lambda: self.radio_option_people_select(buttonWyborOsoby, etykieta_wyboru_osob, lista_osob))
        hbox2.addWidget(radiobutton2)

        radiobutton2 = QRadioButton("Select people from the database")
        radiobutton2.clicked.connect(lambda: self.radio_option_people_select(buttonWyborOsoby, etykieta_wyboru_osob, lista_osob))
        radiobutton2.country = "1"
        hbox2.addWidget(radiobutton2)

        box2.setLayout(hbox2)
        gridLayout.addWidget(box2, 3, 0, 1, 2)
        gridLayout.addWidget(etykieta_wyboru_osob, 4, 0)
        gridLayout.addWidget(buttonWyborOsoby, 4, 1)

        buttonGenerowanie = QPushButton("Generate visualization data")
        buttonGenerowanie.clicked.connect(lambda: self.generate_embeddings_for_visualization(textGenerowanie, text_data_generowania))
        gridLayout.addWidget(buttonGenerowanie, 5, 0, 1, 2)

        textGenerowanie = QLineEdit("Generation progress:", self)
        textGenerowanie.setEnabled(False)
        gridLayout.addWidget(textGenerowanie, 6, 0, 1, 2)

        buttonZatwierdz = QPushButton("Visualize data")
        buttonZatwierdz.clicked.connect(lambda: self.DialogFaceEmbeddingVisualizationShowResult(etykiety_yes.isChecked(), lista_osob, text_data_generowania.text(), buttonWyborOsoby))
        gridLayout.addWidget(buttonZatwierdz, 7, 0, 1, 2)

        groupBox.setLayout(gridLayout)

        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)

        dialog.exec_()


    def DialogDatabaseManagementForDbVizualization(self, x, label_id, lista_osob):
        lista_osob.clear()
        label_id.setText("Number of people selected from the visualization database: " + str(len(lista_osob)))
        dialog = QDialog(self)
        dialog.setWindowIcon(QtGui.QIcon(self.iconName))
        dialog.setWindowTitle("Database Management")
        dialog.setGeometry(400, 200, 939, 340)

        groupBox = QGroupBox("Database Management")
        gridLayout = QGridLayout()

        tableWidget = QTableWidget()
        tableWidget.clear()
        tableWidget.setRowCount(0)
        self.do_testu=tableWidget
        tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        tableWidget.setRowCount(x)
        tableWidget.setColumnCount(8)
        tableWidget.setHorizontalHeaderLabels(["ID", "Firstname", "Lastname", "Gender", "DoB", "Nationality", "Rasy", "Number of photos"])
        liczba = self.baza.get_number_of_people_in_database()
        tab = self.baza.view_date_order_by_firstname_and_lastname()

        plec = ["Women","Men"]
        kraje = lista_panstw
        rasy = lista_ras

        for x in range(liczba):
            for y in [z for z in range(0,8) if z!=3 and z!=5 and z!=6]:
                item = QTableWidgetItem(str(tab[x][y]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                tableWidget.setItem(x, y, item)

            item = QTableWidgetItem(str( plec[int(tab[x][3])] ) )
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 3, item)

            item = QTableWidgetItem(str(kraje[int(tab[x][5])]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 5, item)

            item = QTableWidgetItem(str(rasy[int(tab[x][6])]))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            tableWidget.setItem(x, 6, item)

        tableWidget.resizeColumnsToContents()

        gridLayout.addWidget(tableWidget, 0, 0)

        groupBoxWew = QGroupBox("Face")
        gridLayoutWew = QGridLayout()

        etykieta_zdjecia = QLabel(self)
        etykieta_zdjecia.setMinimumSize(160,160)
        etykieta_zdjecia.setMaximumSize(160,160)
        gridLayoutWew.addWidget(etykieta_zdjecia, 0, 0)

        etykieta_zdjecia2 = QLabel(self)
        etykieta_zdjecia2.setMinimumSize(160, 160)
        etykieta_zdjecia2.setMaximumSize(160, 160)
        gridLayoutWew.addWidget(etykieta_zdjecia2, 0, 1)

        etykieta_zdjecia3 = QLabel(self)
        etykieta_zdjecia3.setMinimumSize(160, 160)
        etykieta_zdjecia3.setMaximumSize(160, 160)
        gridLayoutWew.addWidget(etykieta_zdjecia3, 1, 0)

        etykieta_zdjecia4 = QLabel(self)
        etykieta_zdjecia4.setMinimumSize(160, 160)
        etykieta_zdjecia4.setMaximumSize(160, 160)
        gridLayoutWew.addWidget(etykieta_zdjecia4, 1, 1)
        groupBoxWew.setLayout(gridLayoutWew)
        gridLayout.addWidget(groupBoxWew,0,1)

        groupBoxWewx = QGroupBox("")
        gridLayoutWewx = QGridLayout()
        self.zwrotne_id_do_wektorow = -1
        zatwierdz_zdjecie = QPushButton("Accept")
        zatwierdz_zdjecie.setMinimumHeight(20)
        zatwierdz_zdjecie.clicked.connect(lambda: self.DialogDatabaseManagementForDbVizualizationAccept(dialog, label_id, lista_osob))
        gridLayoutWewx.addWidget(zatwierdz_zdjecie)
        groupBoxWewx.setLayout(gridLayoutWewx)
        gridLayout.addWidget(groupBoxWewx, 1,0)

        groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(groupBox)
        dialog.setLayout(vbox)

        tableWidget.clicked.connect(lambda: self.db_management_for_visualization_cell_click(tableWidget, tableWidget.currentRow(),
                                                                  tableWidget.item(tableWidget.currentRow(),
                                                                                   0).text(), etykieta_zdjecia, etykieta_zdjecia2, etykieta_zdjecia3, etykieta_zdjecia4, lista_osob))
        dialog.exec_()


    def DialogDatabaseManagementForDbVizualizationAccept(self, dialog, label: QLabel, lista_osob: list):
        if self.zwrotne_id_do_wektorow != -1:
            dialog.accept()
            #label.setText("Wybrano "+str(len(lista_osob))+" osób.")
            label.setText("Liczba wybranych osób=" + str(len(lista_osob)))
            msg = QMessageBox.information(self, "Komunikat zwrotny", "The person from the base was correctly selected.", QMessageBox.Yes)
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "Select a person from the database or close the window.",
                                          QMessageBox.Yes)


    def DialogFaceEmbeddingVisualizationShowResult(self, etykiety, osoby: list, text, button):
        if text=="None":
            msg = QMessageBox.information(self, "Komunikat zwrotny", "First you need to generate data for the algorithm.", QMessageBox.Yes)
            return
        if button.isEnabled() == True:
            if len(osoby) == 0:
                msg = QMessageBox.information(self, "Komunikat zwrotny", "You need to select people from the base or change the option.", QMessageBox.Yes)
                return
        osoby.sort()
        algorytm = self.aktualny_radio_button
        if len(osoby) == 0 or self.aktualny_radio_button_osoby == 0:
            osoby = None
        if algorytm == 0:
            import visualizations2d
            dialog = visualizations2d.Window2D()
            dialog.draw_pca_2d(osoby,etykiety,None,None)
            dialog.exec_()
        elif algorytm == 1:
            import visualizations3d
            dialog = visualizations3d.Window3D()
            dialog.canvas2.canvas.draw_pca_3d(osoby,etykiety,None,None)
            dialog.exec_()
        elif algorytm == 2:
            import visualizations2d
            dialog = visualizations2d.Window2D()
            dialog.draw_tsne_2d(osoby,etykiety,None,None)
            dialog.exec_()
        elif algorytm == 3:
            import visualizations3d
            dialog = visualizations3d.Window3D()
            dialog.canvas2.canvas.draw_tsne_3d(osoby,etykiety)
            dialog.exec_()
        elif algorytm == 4:
            from comparison import processingDatabaseHistogramData
            x = processingDatabaseHistogramData(osoby)
            from comparison import drawHist
            if len(x) == 0:
                msg = QMessageBox.information(self, "Komunikat zwrotny", "Visualization of the histogram is possible only for one selected person or everyone in database.",
                                              QMessageBox.Yes)
                return
            drawHist(x)
        elif algorytm == 5:
            import visualizations2d
            dialog = visualizations2d.Window2D()
            dialog.draw_umap_2d(osoby,etykiety,None,None)
            dialog.exec_()
        elif algorytm == 6:
            import visualizations3d
            dialog = visualizations3d.Window3D()
            dialog.canvas2.canvas.draw_umap_3d(osoby,etykiety)
            dialog.exec_()
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "First select a method.", QMessageBox.Yes)
            return
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
    ################################################################################################################
    ################################################################################################################
    ################################################################################################################
    ################################################################################################################################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################


    def choose_video_file(self):
        self.testVideoPath.setText("")
        self.video_file_path=""
        fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\', "Video file (*.mp4)")
        if fname[0] != "":
            msg = QMessageBox.information(self, "Komunikat zwrotny", "The movie has been selected correctly.", QMessageBox.Yes)
            self.video_file_path=fname[0]
            self.testVideoPath.setText(fname[0])
        else:
            self.video_file_path=""
            self.testVideoPath.setText("")
            msg = QMessageBox.information(self, "Komunikat zwrotny", "You must select a movie.",
                                          QMessageBox.Yes)


    def choose_photo_to_add_new_person(self):
        self.AddPersonPhotoIsChoosen=False
        fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\', "Image files (*.jpg *.jpeg)")
        pixmap = QtGui.QPixmap("")
        self.label.setPixmap(QtGui.QPixmap(pixmap))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()
        if fname[0] != "":
            results = AIModule.extract_mtcnn_result_from_photo(fname[0])
            if len(results) > 1:
                msg = QMessageBox.information(self, "Komunikat zwrotny", "Too many faces have been detected.", QMessageBox.Yes)
                return
            elif len(results) == 0:
                msg = QMessageBox.information(self, "Komunikat zwrotny", "No face detected in the photo.", QMessageBox.Yes)
                return
            else:
                self.PhotoNr1 = AIModule.extract_face_file_to_save(fname[0], results)
                pixmap = QtGui.QPixmap.fromImage(ImageQt(self.PhotoNr1))
                #pixmap = pixmap.scaled(160,160,QtCore.Qt.KeepAspectRatio)
                pixmap = pixmap.scaled(160, 160, QtCore.Qt.IgnoreAspectRatio)
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setPixmap(QtGui.QPixmap(pixmap))
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.adjustSize()
                self.AddPersonPhotoIsChoosen = True
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "You must select a file.", QMessageBox.Yes)


    def choose_photo_to_find_on_video(self, label):
        self.testPhotoPath.setText("")
        fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\', "Image files (*.jpg *.jpeg)")
        if fname[0] != "":
            results = AIModule.extract_mtcnn_result_from_photo(fname[0])
            if len(results) != 1:
                msg = QMessageBox.information(self, "Komunikat zwrotny", "Invalid number of faces, equal to "+str(len(results))+".", QMessageBox.Yes)
                self.testPhotoPath.setText("")
                return
            else:
                self.testPhotoPath.setText(fname[0])
                self.PhotoNr2 = AIModule.extract_face_file_to_save(fname[0], results)
                pixmap = QtGui.QPixmap.fromImage(ImageQt(self.PhotoNr2))
                pixmap = pixmap.scaled(160,160,QtCore.Qt.KeepAspectRatio)
                label.setPixmap(QtGui.QPixmap(pixmap))
        else:
            self.testPhotoPath.setText("")
            msg = QMessageBox.information(self, "Komunikat zwrotny", "You must select a photo.", QMessageBox.Yes)


    def choose_face_photo_to_find(self):
        self.photo_imagePathSearch = ""
        fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\', "Image files (*.jpg *.jpeg)")
        imagePath = fname[0]
        self.photo_imagePathSearch=imagePath
        pixmap = QtGui.QPixmap(imagePath)
        pixmap = pixmap.scaled(640,480,QtCore.Qt.KeepAspectRatio)
        self.labelSearch.setPixmap(QtGui.QPixmap(pixmap))
        self.labelSearch.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSearch.adjustSize()


    def choose_person_face_files_to_add(self):
        fnames = QFileDialog.getOpenFileNames(self, 'Open file','c:\\', "Image files (*.jpg *.jpeg)")
        self.editAmountPhotos.setText("Selected "+str(len(fnames[0]))+ " photos.")
        self.photo_imagePath2 = fnames[0]

    def choose_face_files_to_compare(self, osoba, pole):
        if osoba==1:
            pixmap = QtGui.QPixmap("")
            self.labelFace1.setPixmap(QtGui.QPixmap(pixmap))
            self.labelFace1.setAlignment(QtCore.Qt.AlignCenter)
            self.labelFace1.adjustSize()
            self.tablica_zdjec_os1 = []
        else:
            pixmap = QtGui.QPixmap("")
            self.labelFace2.setPixmap(QtGui.QPixmap(pixmap))
            self.labelFace2.setAlignment(QtCore.Qt.AlignCenter)
            self.labelFace2.adjustSize()
            self.tablica_zdjec_os2 = []
        fnames = QFileDialog.getOpenFileNames(self, 'Open file', 'c:\\', "Image files (*.jpg *.jpeg)")
        if len(fnames[0]) == 0:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "You must select at least one photo.",
                                          QMessageBox.Yes)
            pole.setText("No photos selected.")
            return
        else:
            pole.setText("The selected number of photos is " + str(len(fnames[0])))
            twarze = list()
            for i in range(len(fnames[0])):
                results = AIModule.extract_mtcnn_result_from_photo(fnames[0][i])
                if len(results) == 1:
                    face = AIModule.extract_face_file_to_save(fnames[0][i], results)
                    twarze.append(face)
                else:
                    msg = QMessageBox.information(self, "Informacja o rezultacie",
                                                  "Na zdjęciu " + fnames[0][
                                                      i] + " wykryto nieprawidłową liczbę twarzy.",
                                                  QMessageBox.Yes)
                    pole.setText("No photos selected.")
                    return
            if osoba == 1:
                self.tablica_zdjec_os1 = twarze
                pixmap = QtGui.QPixmap.fromImage(ImageQt(twarze[0]))
                pixmap = pixmap.scaled(256, 256, QtCore.Qt.IgnoreAspectRatio)
                self.labelFace1.setAlignment(QtCore.Qt.AlignCenter)
                self.labelFace1.setPixmap(QtGui.QPixmap(pixmap))
                self.labelFace1.setAlignment(QtCore.Qt.AlignCenter)
                msg = QMessageBox.information(self, "Komunikat zwrotny",
                                              "The data was loaded correctly.",
                                              QMessageBox.Yes)
            elif osoba == 2:
                self.tablica_zdjec_os2 = twarze
                pixmap = QtGui.QPixmap.fromImage(ImageQt(twarze[0]))
                pixmap = pixmap.scaled(256, 256, QtCore.Qt.IgnoreAspectRatio)
                self.labelFace2.setAlignment(QtCore.Qt.AlignCenter)
                self.labelFace2.setPixmap(QtGui.QPixmap(pixmap))
                self.labelFace2.setAlignment(QtCore.Qt.AlignCenter)
                msg = QMessageBox.information(self, "Komunikat zwrotny",
                                              "The data was loaded correctly.",
                                              QMessageBox.Yes)
            else:
                msg = QMessageBox.information(self, "Komunikat zwrotny", "Unknown error file select to compare",
                                              QMessageBox.Yes)


    def btngenderstate(self,btn):
        if btn.text() == "Men":
            if btn.isChecked() == True:
                self.gender_result=1
            else:
                self.gender_result=0
        elif btn.text() == "Women":
            if btn.isChecked() == True:
                self.gender_result = 0
            else:
                self.gender_result = 1
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "Unknown error with gender radio button",
                                          QMessageBox.Yes)


    def db_management_cell_click(self,table,row, x):
        #table.selectRow(row)
        for i in range(table.columnCount()):
            table.item(row, i).setBackground(QtGui.QColor(57,255,20))
        self.currentRowTarget=x
        if self.poprzednie_zaznaczenie !=-1 and self.poprzednie_zaznaczenie != row:
            for i in range(table.columnCount()):
                if table.item(self.poprzednie_zaznaczenie, i) is not None:
                    table.item(self.poprzednie_zaznaczenie, i).setBackground(QtGui.QColor(255, 255, 255))
        self.poprzednie_zaznaczenie=row


    def db_management_for_video_cell_click(self,table,row, x, label1, label2, label3, label4):
        #table.selectRow(row)
        for i in range(table.columnCount()):
            table.item(row, i).setBackground(QtGui.QColor(57,255,20))
        self.currentRowTarget=x
        if self.poprzednie_zaznaczenie !=-1 and self.poprzednie_zaznaczenie != row:
            for i in range(table.columnCount()):
                if table.item(self.poprzednie_zaznaczenie, i) is not None:
                    table.item(self.poprzednie_zaznaczenie, i).setBackground(QtGui.QColor(255, 255, 255))
        self.poprzednie_zaznaczenie=row
        lista_zdjec=fsystem.return_list_files_for_person_id(x)
        path = './photos/'+str(x)+'/'
        lista_etykiet = [label1, label2, label3, label4]
        if len(lista_zdjec) < 4:
            for i in range(len(lista_zdjec)):
                pixmap = QPixmap(path + lista_zdjec[i])
                lista_etykiet[i].setPixmap(pixmap)
                #zdjecie = cv2.imread(path+lista_zdjec[i])
                #cv2.imshow(str(x)+' - '+str(i), zdjecie)
        else:
            for i in range(4):
                pixmap = QPixmap(path + lista_zdjec[i])
                lista_etykiet[i].setPixmap(pixmap)
                #zdjecie = cv2.imread(path+lista_zdjec[i])
                #cv2.imshow(str(x)+' - '+str(i), zdjecie)
        self.zwrotne_id = x


    def db_management_for_visualization_cell_click(self, table, row, x, label1, label2, label3, label4, lista1: list):
        if int(x) in lista1:
            lista1.remove(int(x))
            for i in range(table.columnCount()):
                if table.item(row, i) is not None:
                    table.item(row, i).setBackground(QtGui.QColor(255, 255, 255))
        else:
            lista1.append(int(x))
            for i in range(table.columnCount()):
                table.item(row, i).setBackground(QtGui.QColor(57,255,20))
        lista_zdjec = fsystem.return_list_files_for_person_id(x)
        path = './photos/' + str(x) + '/'
        lista_etykiet = [label1, label2, label3, label4]
        if len(lista_zdjec) < 4:
            for i in range(len(lista_zdjec)):
                pixmap = QPixmap(path + lista_zdjec[i])
                lista_etykiet[i].setPixmap(pixmap)
        else:
            for i in range(4):
                pixmap = QPixmap(path + lista_zdjec[i])
                lista_etykiet[i].setPixmap(pixmap)
        self.zwrotne_id_do_wektorow = x


    def radio_option_video_search(self, choose_image_photo, spin):
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.country == "0":
                choose_image_photo.setEnabled(True)
                spin.setEnabled(False)
                self.zwrotne_id_opcja_video = 0
            elif radioButton.country == "1":
                choose_image_photo.setEnabled(True)
                spin.setEnabled(False)
                self.zwrotne_id_opcja_video=1
            elif radioButton.country == "2":
                choose_image_photo.setEnabled(False)
                spin.setEnabled(True)
                self.zwrotne_id_opcja_video = 2
            elif radioButton.country == "3":
                choose_image_photo.setEnabled(False)
                spin.setEnabled(False)
                self.zwrotne_id_opcja_video = 3


    def radio_button_select_camera(self, buttonRozpoznawanie, buttonZrzut, buttonPodglad):
        radioButton = self.sender()
        buttonPodglad.setEnabled(True)
        buttonZrzut.setEnabled(True)
        buttonRozpoznawanie.setEnabled(True)
        self.wybrana_kamerka = int(radioButton.country)


    def cam_preview(self, cam_nr, mirror=True):
        if(self.cam_name != ""):
            cv2.destroyWindow(self.cam_name)
            self.cam.release()
        self.cam_name = 'Cam nr.' + str(cam_nr+1)+str(" ESC to close")
        self.cam = cv2.VideoCapture(cam_nr)
        while True:
            if self.stan_kamery == True:
                ret_val, img = self.cam.read()
                if mirror:
                    img = cv2.flip(img, 1)
                cv2.imshow('Cam nr.' + str(cam_nr+1)+str(" ESC to close"), img)
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
            else:
                break
        self.cam.release()
        self.cam_name=""
        cv2.destroyAllWindows()


    def cam_recognition(self, cam_nr, mirror=True):
        if (self.cam_name != ""):
            cv2.destroyWindow(self.cam_name)
            self.cam.release()
        self.cam_name = 'Cam nr.' + str(cam_nr+1)+str(" ESC to close")
        self.cam = cv2.VideoCapture(cam_nr)
        detector = AIModule.detector
        while (True):
            if self.stan_kamery == True:
                ret, frame = self.cam.read()
                results = detector.detect_faces(frame)
                if len(results) > 0:
                    for i in range(len(results)):
                        x = results[i]['box'][0]
                        y = results[i]['box'][1]
                        x2 = results[i]['box'][2] + x
                        y2 = results[i]['box'][3] + y
                        frame = cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 2)
                        a, b, c = AIModule.find_person_from_video(frame, results, (160, 160), i)
                        rows = self.baza.get_data_about_person(
                            int(AIModule.get_id_from_svm(a)))
                        text = ("ID=" + str(rows[0][2]) + " " + rows[0][0] + " " + rows[0][
                            1] + " - " + str(b) + " %\n")
                        yyy = y - 10 if y - 10 > 10 else y + 10
                        cv2.putText(frame, text, (x, yyy),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                cv2.imshow('Cam nr.' + str(cam_nr+1)+str(" ESC to close"), frame)
                if cv2.waitKey(1) == 27:
                    break
            else:
                break
        self.cam.release()
        self.cam_name = ""
        cv2.destroyAllWindows()


    def cam_capture_image(self):
        if self.cam_name == "":
            msg = QMessageBox.information(self, "Komunikat zwrotny", "You must first enable camera preview.",
                                          QMessageBox.Yes)
            return
        flag, frame = self.cam.read()
        path = r'./camera/photos'
        if flag is not None:
            if flag:
                from datetime import datetime
                now = str(datetime.now())
                now = now[:13]+"-"+now[14:16]+"-"+now[17:]
                name = str(now)+" Camera Nr-"+str(self.wybrana_kamerka)+".jpg"
                cv2.imwrite(os.path.join(path, name), frame)
                msg = QMessageBox.information(self, "Komunikat zwrotny", "Photo saved in "+os.path.join(path, name),
                                              QMessageBox.Yes)
            else:
                msg = QMessageBox.information(self, "Komunikat zwrotny", "Unknown error with camera",
                                              QMessageBox.Yes)
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "Unknown error with camera",
                                          QMessageBox.Yes)


    def add_found_photo(self, face, id_class, id_db):
        ilosc_w_bazie_przed = self.baza.get_photos_amount_for_person(id_db)
        tablica_nazw_zdjec = fsystem.return_list_files_for_person_id(id_db)
        aktualne_id_zdjecia = 1
        if len(tablica_nazw_zdjec) != 0:
            aktualne_id_zdjecia = (
                    int(sorted(fsystem.return_list_files_for_person_id(id_db), key=lambda x: int(x[:-4]))[-1][:-4]) + 1)
        import os
        path = r'./photos/'+str(id_db)
        name = str(aktualne_id_zdjecia)+".jpg"
        self.baza.update_photos_amount(id_db,ilosc_w_bazie_przed+1)
        cv2.imwrite(os.path.join(path, name), face)


    def generate_embeddings_for_visualization(self, etykieta, text_data_generowania):
        algorytm = self.aktualny_radio_button
        status = 0
        etykieta.setText("Generation progress: Started")
        def ustaw_date(nazwa_pliku):
            import menagetimes
            text_from_file = menagetimes.read_time_from_file("gen_time/" + nazwa_pliku)
            text_data_generowania.setText(text_from_file)
        if algorytm == 0:
            import visualizations2d
            visualizations2d.gen_pca_2d()
            import menagetimes
            menagetimes.save_time_tofile("pca2dtime.txt")
            ustaw_date("pca2dtime.txt")
        elif algorytm == 1:
            import visualizations3d
            visualizations3d.gen_pca_3d()
            import menagetimes
            menagetimes.save_time_tofile("pca3dtime.txt")
            ustaw_date("pca3dtime.txt")
        elif algorytm == 2:
            import visualizations2d
            visualizations2d.gen_tsne_2d()
            import menagetimes
            menagetimes.save_time_tofile("tsne2dtime.txt")
            ustaw_date("tsne2dtime.txt")
        elif algorytm == 3:
            import visualizations3d
            visualizations3d.gen_tsne_3d()
            import menagetimes
            menagetimes.save_time_tofile("tsne3dtime.txt")
            ustaw_date("tsne3dtime.txt")
        elif algorytm == 4:
            from comparison import genDatabaseHistogramData
            genDatabaseHistogramData()
            import menagetimes
            menagetimes.save_time_tofile("histogramtime.txt")
            ustaw_date("histogramtime.txt")
        elif algorytm == 5:
            import visualizations2d
            visualizations2d.gen_umap_2d()
            import menagetimes
            menagetimes.save_time_tofile("umap2dtime.txt")
            ustaw_date("umap2dtime.txt")
        elif algorytm == 6:
            import visualizations3d
            visualizations3d.gen_umap_3d()
            import menagetimes
            menagetimes.save_time_tofile("umap3dtime.txt")
            ustaw_date("umap3dtime.txt")
        else:
            msg = QMessageBox.information(self, "Komunikat zwrotny", "It is necessary to choose the visualization method.", QMessageBox.Yes)
            status = 1
            return
        if status == 0:
            etykieta.setText("Generation progress: Success")
        else:
            etykieta.setText("Generation progress: Error")


    def radio_option_people_select(self, button, text, lista_osob):
        lista_osob.clear()
        radioButton = self.sender()
        if radioButton.country == "0":
            button.setEnabled(False)
            text.setText("All people selected")
        elif radioButton.country == "1":
            text.setText("Number of people selected from the visualization database: 0")
            button.setEnabled(True)
        self.aktualny_radio_button_osoby = int(radioButton.country)

    def radio_option_alg_select(self, text, textGenerowania):
        textGenerowania.setText("Generation progress:")
        text2=text
        def ustaw_date(nazwa_pliku):
            import menagetimes
            text_from_file = menagetimes.read_time_from_file("gen_time/" + nazwa_pliku)
            text2.setText(text_from_file)

        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.country == "0":
                ustaw_date("pca2dtime.txt")
            elif radioButton.country == "1":
                ustaw_date("pca3dtime.txt")
            elif radioButton.country == "2":
                ustaw_date("tsne2dtime.txt")
            elif radioButton.country == "3":
                ustaw_date("tsne3dtime.txt")
            elif radioButton.country == "4":
                ustaw_date("histogramtime.txt")
            elif radioButton.country == "5":
                ustaw_date("umap2dtime.txt")
            elif radioButton.country == "6":
                ustaw_date("umap3dtime.txt")
        self.aktualny_radio_button=int(radioButton.country)


def get_QPixmap_from_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = QtGui.QImage(frame, frame.shape[1], frame.shape[0],
                   frame.strides[0], QtGui.QImage.Format_RGB888)
    return QtGui.QPixmap.fromImage(image)


def countCams():
    max_tested = 100
    for i in range(max_tested):
        temp_camera = cv2.VideoCapture(i)
        if temp_camera.isOpened():
            temp_camera.release()
            continue
        return i


class CustomWidget(QWidget):
    def __init__(self, text, img, parent=None):
        QWidget.__init__(self, parent)
        self._text = text
        self._img = img
        self.setLayout(QVBoxLayout())
        self.lbPixmap = QLabel(self)
        self.lbText = QLabel(self)
        self.layout().addWidget(self.lbPixmap)
        self.layout().addWidget(self.lbText)
        self.initUi()

    def initUi(self):
        self.lbPixmap.setPixmap(QPixmap(self._img).scaled(160,160))
        self.lbText.setText(self._text)


    #@pyqtProperty(str)
    def img(self):
        return self._img

    #@img.setter
    def total(self, value):
        if self._img == value:
            return
        self._img = value
        self.initUi()

    def get_text(self):
            return self._text


    #@pyqtProperty(str)
    def text(self):
        return self._text

    #@text.setter
    def text(self, value):
        if self._text == value:
            return
        self._text = value
        self.initUi()


class CustomWidget2(QWidget):
    def __init__(self, text, img, parent=None):
        QWidget.__init__(self, parent)

        self._text = text
        self._img = img

        self.setLayout(QVBoxLayout())
        self.lbPixmap = QLabel(self)
        self.lbText = QLabel(self)
        #self.lbText.setAlignment(Qt.AlignCenter)

        self.layout().addWidget(self.lbPixmap)
        self.layout().addWidget(self.lbText)

        self.initUi()

    def initUi(self):
        qim = ImageQt(Image.fromarray(self._img))
        self.lbPixmap.setPixmap(QtGui.QPixmap.fromImage(qim).scaled(160,160))

        #self.lbPixmap.setPixmap(QPixmap(self._img).scaled(160,160))
        self.lbText.setText(self._text)


    #@pyqtProperty(str)
    def img(self):
        return self._img

    #@img.setter
    def total(self, value):
        if self._img == value:
            return
        self._img = value
        self.initUi()

    def get_text(self):
            return self._text


    #@pyqtProperty(str)
    def text(self):
        return self._text

    #@text.setter
    def text(self, value):
        if self._text == value:
            return
        self._text = value
        self.initUi()


class TableWidget(QTableWidget):
    def __init__(self, photos_amount, id, parent=None):
        QTableWidget.__init__(self, parent)
        rows_amount = int(photos_amount/5)
        cols_amount = int(photos_amount%5)
        liczba_kolumn=0
        if photos_amount >= 5:
            liczba_kolumn=5
        else:
            liczba_kolumn=photos_amount
        if cols_amount != 0:
            rows_amount+=1

        self.setColumnCount(liczba_kolumn)
        self.setRowCount(rows_amount)

        nazwy_zdjec=sorted(fsystem.return_list_files_for_person_id(id), key=lambda x: int(x[:-4]))
        for i in range(rows_amount):
            for j in range(liczba_kolumn):
                if i*5+j == photos_amount:
                    break
                lb = CustomWidget("./photos/"+str(id)+"/"+nazwy_zdjec[(i*5+j)], "./photos/"+str(id)+"/"+nazwy_zdjec[(i*5+j)])
                self.setCellWidget(i, j, lb)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    #@pyqtSlot(int, int)
    def onCellClicked(self, row, column):
        w = self.cellWidget(row, column)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Window()
    sys.exit(app.exec())
