# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\CGEV_DEV\cgevPipeline\maya\modules\archiveManager\scripts\ARCHIVE_MANAGER_UI.ui'
#
# Created: Tue May 02 13:30:55 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

#from PySide import QtCore, QtGui
try:
    from PySide2 import QtCore as core, QtGui as gui, QtWidgets as widgets
except ImportError:
    from PySide import QtCore as core, QtGui as gui
    widgets= gui
    core.QItemSelectionModel= gui.QItemSelectionModel
    widgets.QHeaderView.setSectionResizeMode= widgets.QHeaderView.setResizeMode


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(470, 245)
        sizePolicy = widgets.QSizePolicy(widgets.QSizePolicy.Fixed, widgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(core.QSize(470, 245))
        MainWindow.setMaximumSize(core.QSize(470, 245))
        MainWindow.setLayoutDirection(core.Qt.LeftToRight)
        self.centralwidget = widgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = widgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(core.QRect(20, 10, 431, 171))
        sizePolicy = widgets.QSizePolicy(widgets.QSizePolicy.Expanding, widgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = widgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget_2 = widgets.QWidget(self.tab)
        self.verticalLayoutWidget_2.setGeometry(core.QRect(5, 10, 411, 126))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = widgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = widgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(widgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_import = widgets.QVBoxLayout()
        self.verticalLayout_import.setObjectName("verticalLayout_import")
        self.pushButton_import = widgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_import.setObjectName("pushButton_import")
        self.verticalLayout_import.addWidget(self.pushButton_import)
        self.horizontalLayout_3 = widgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setSizeConstraint(widgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_imp_arc = widgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_imp_arc.setChecked(True)
        self.checkBox_imp_arc.setObjectName("checkBox_imp_arc")
        self.horizontalLayout_3.addWidget(self.checkBox_imp_arc)
        self.checkBox_imp_shd = widgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_imp_shd.setChecked(True)
        self.checkBox_imp_shd.setObjectName("checkBox_imp_shd")
        self.horizontalLayout_3.addWidget(self.checkBox_imp_shd)
        self.verticalLayout_import.addLayout(self.horizontalLayout_3)
        spacerItem = widgets.QSpacerItem(20, 20, widgets.QSizePolicy.Minimum, widgets.QSizePolicy.Expanding)
        self.verticalLayout_import.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_import)
        self.verticalLayout_export = widgets.QVBoxLayout()
        self.verticalLayout_export.setSizeConstraint(widgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_export.setObjectName("verticalLayout_export")
        self.pushButton_export = widgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_export.setObjectName("pushButton_export")
        self.verticalLayout_export.addWidget(self.pushButton_export)
        self.horizontalLayout_2 = widgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setSizeConstraint(widgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_exp_arc = widgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_exp_arc.setChecked(True)
        self.checkBox_exp_arc.setObjectName("checkBox_exp_arc")
        self.horizontalLayout_2.addWidget(self.checkBox_exp_arc)
        self.checkBox_exp_shd = widgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_exp_shd.setChecked(True)
        self.checkBox_exp_shd.setObjectName("checkBox_exp_shd")
        self.horizontalLayout_2.addWidget(self.checkBox_exp_shd)
        self.checkBox_exp_vc = widgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_exp_vc.setChecked(True)
        self.checkBox_exp_vc.setObjectName("checkBox_exp_vc")
        self.horizontalLayout_2.addWidget(self.checkBox_exp_vc)
        self.verticalLayout_export.addLayout(self.horizontalLayout_2)
        self.checkBox_exp_ani = widgets.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_exp_ani.setObjectName("checkBox_exp_ani")
        self.verticalLayout_export.addWidget(self.checkBox_exp_ani)
        self.horizontalLayout_4 = widgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_frame = widgets.QLabel(self.verticalLayoutWidget_2)
        self.label_frame.setEnabled(True)
        self.label_frame.setObjectName("label_frame")
        self.horizontalLayout_4.addWidget(self.label_frame)
        self.lineEdit_start = widgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_start.setObjectName("lineEdit_start")
        self.horizontalLayout_4.addWidget(self.lineEdit_start)
        self.lineEdit_end = widgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_end.setObjectName("lineEdit_end")
        self.horizontalLayout_4.addWidget(self.lineEdit_end)
        self.verticalLayout_export.addLayout(self.horizontalLayout_4)
        spacerItem1 = widgets.QSpacerItem(20, 20, widgets.QSizePolicy.Minimum, widgets.QSizePolicy.Expanding)
        self.verticalLayout_export.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_export)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = widgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget = widgets.QWidget(self.tab_2)
        self.verticalLayoutWidget.setGeometry(core.QRect(50, 35, 321, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = widgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_mayaR = widgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_mayaR.setLayoutDirection(core.Qt.LeftToRight)
        self.pushButton_mayaR.setObjectName("pushButton_mayaR")
        self.verticalLayout_3.addWidget(self.pushButton_mayaR)
        self.pushButton_clean = widgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_clean.setObjectName("pushButton_clean")
        self.verticalLayout_3.addWidget(self.pushButton_clean)
        self.tabWidget.addTab(self.tab_2, "")
        self.progressBar = widgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(core.QRect(20, 195, 409, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = widgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        core.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("ARCHIVE MANAGER")
        self.pushButton_import.setText("IMPORT")
        self.checkBox_imp_arc.setText("ARCHIVE")
        self.checkBox_imp_shd.setText("SHADER")
        self.pushButton_export.setText("EXPORT")
        self.checkBox_exp_arc.setText("ARCHIVE")
        self.checkBox_exp_shd.setText("SHADER")
        self.checkBox_exp_vc.setText("VERTEX COLOR")
        self.checkBox_exp_ani.setText("ANIMATION")
        self.label_frame.setText("start/end")
        self.lineEdit_start.setText("1")
        self.lineEdit_end.setText("24")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "ARCHIVE I/O")
        self.pushButton_mayaR.setText("REPLACE NODES")
        self.pushButton_clean.setText("CLEAN ARCHIVE NAME")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "ARCHIVE REPLACEMENT")

