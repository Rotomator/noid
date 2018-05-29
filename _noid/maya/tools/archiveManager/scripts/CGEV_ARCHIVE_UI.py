from PySide import QtCore, QtGui
import pymel.core as pm
import ARCHIVE_MANAGER_UI as cui
reload(cui)
from shiboken import wrapInstance
import maya.OpenMayaUI as omui

import CGEV_ARCHIVE_TOOLS as art
reload(art)

import CGEV_ARCHIVE_REPLACEMENT as arr
reload(arr)

import CGEV_genLib as gl
reload(gl)

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)

class ControlMainWindow (QtGui.QMainWindow):

    def __init__(self, parent=None):

        super(ControlMainWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui =cui.Ui_MainWindow()
        self.ui.setupUi(self)

#        vpGrp=gl.getSetMembers('VRAY_PROXY_SET')
#
#        if vpGrp:
#            self.ui.comboBox_vpGrp.addItems(vpGrp)
#
#        ptcSet=gl.getSetMembers('PTC_SCATTER_SET')
#        if ptcSet:
#            self.ui.comboBox_ptcNode.addItems(ptcSet)


        self.ui.pushButton_import.clicked.connect(self.importArchive)
        self.ui.pushButton_export.clicked.connect(self.exportArchive)
        self.ui.pushButton_clean.clicked.connect(self.cleanArchiveName)
        self.ui.pushButton_mayaR.clicked.connect(self.replaceNodeByArchive)

        self.ui.progressBar.setVisible(False)

    def importArchive(self):

        check=QtCore.Qt.CheckState.Checked
        uncheck=QtCore.Qt.CheckState.Unchecked

        mode=0
        if self.ui.checkBox_imp_arc.checkState()==check:
            mode|=(1<<0)

        if self.ui.checkBox_imp_shd.checkState()==check:
            mode|=(1<<1)


        self.ui.progressBar.setVisible(True)
        art.archiveImport(mode,self)
        self.ui.progressBar.setVisible(False)

    def exportArchive(self):

        check=QtCore.Qt.CheckState.Checked
        uncheck=QtCore.Qt.CheckState.Unchecked
        bakeVC=0
        if self.ui.checkBox_exp_vc.checkState()==check:
            bakeVC=1


        mode=0
        if self.ui.checkBox_exp_arc.checkState()==check:
            mode|=(1<<0)

        if self.ui.checkBox_exp_shd.checkState()==check:
            mode|=(1<<1)

        if self.ui.checkBox_exp_ani.checkState()==check:
            mode|=(1<<2)


        sf=self.ui.lineEdit_start.text()
        ef=self.ui.lineEdit_end.text()

        self.ui.progressBar.setVisible(True)
        art.archiveExport(mode,bakeVC,sf,ef,self)
        self.ui.progressBar.setVisible(False)

    def cleanArchiveName(self):

        self.ui.progressBar.setVisible(True)
        doClean=art.cleanArchiveName(self)
        self.ui.progressBar.setVisible(False)

    def replaceNodeByArchive(self):
        self.ui.progressBar.setVisible(True)
        doReplace=arr.mayaNodes_replaceByArchive(self)
        self.ui.progressBar.setVisible(False)


    def setupProgressBar(self,max, text=''):
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(max)
        if max<=100:
            self.elemDiv=1
        else:
            self.elemDiv=max/100.0

        self.ui.progressBar.setFormat(text+" %p%")

    def growBar(self):
        value=self.ui.progressBar.value()
        self.ui.progressBar.setValue(value+1)
        inc=1
        if inc>=(value/self.elemDiv):
            self.refresh()
            inc+=1

    def refresh(self):
        QtGui.QApplication.instance().processEvents()



def vptUI():

    windowName='ARCHIVE TOOLS'

    if pm.window('ARCHIVE TOOLS',exists=True):
        pm.deleteUI('ARCHIVE TOOLS',wnd=True)

    myWin=ControlMainWindow(parent=maya_main_window())
    myWin.setObjectName(windowName)
    myWin.show()
