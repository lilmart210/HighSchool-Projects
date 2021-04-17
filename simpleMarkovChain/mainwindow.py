# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(330, 10, 181, 61))
        self.label_4.setWordWrap(True)
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 0, 312, 501))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_2)

        self.StartNumberEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.StartNumberEdit.setObjectName(u"StartNumberEdit")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.StartNumberEdit)

        self.EndNumberEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.EndNumberEdit.setObjectName(u"EndNumberEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.EndNumberEdit)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_5 = QLabel(self.verticalLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_5)

        self.WordCountEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.WordCountEdit.setObjectName(u"WordCountEdit")

        self.verticalLayout_3.addWidget(self.WordCountEdit)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.ChosenWordEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.ChosenWordEdit.setObjectName(u"ChosenWordEdit")

        self.verticalLayout.addWidget(self.ChosenWordEdit)

        self.pushButton = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(320, 80, 391, 381))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Note: Goes from 1 to 1000. Go above this and I can't gaurantee this won't crash", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Start Page", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"End Page", None))
        self.StartNumberEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter Number", None))
        self.EndNumberEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter Number", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Word Count", None))
        self.WordCountEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"100(clear for default)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Want to pick a word? Type a word and to see if it will work", None))
        self.ChosenWordEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter Word(Clear to use random)", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Go", None))
    # retranslateUi

