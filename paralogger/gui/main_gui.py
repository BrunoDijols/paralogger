# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'paraloger_GUI1.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1502, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 1261, 661))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_project_tree = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_project_tree.setObjectName("label_project_tree")
        self.verticalLayout.addWidget(self.label_project_tree)
        self.treeWidget = QtWidgets.QTreeWidget(self.horizontalLayoutWidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)
        self.label_object_details = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_object_details.setObjectName("label_object_details")
        self.verticalLayout.addWidget(self.label_object_details)
        self.tableView = QtWidgets.QTableView(self.horizontalLayoutWidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.label_info_bar = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_info_bar.setObjectName("label_info_bar")
        self.verticalLayout.addWidget(self.label_info_bar)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1502, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionimport = QtWidgets.QAction(MainWindow)
        self.actionimport.setObjectName("actionimport")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionimport)
        self.menuAbout.addAction(self.actionHelp)
        self.menuAbout.addAction(self.actionVersion)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_project_tree.setText(_translate("MainWindow", "Tree"))
        self.label_object_details.setText(_translate("MainWindow", "Details:"))
        self.label_info_bar.setText(_translate("MainWindow", "info bar"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuAbout.setTitle(_translate("MainWindow", "Abo&ut"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionimport.setText(_translate("MainWindow", "&import"))
        self.actionHelp.setText(_translate("MainWindow", "&Help"))
        self.actionVersion.setText(_translate("MainWindow", "&Version"))
        self.actionSave_as.setText(_translate("MainWindow", "&Save_as"))

