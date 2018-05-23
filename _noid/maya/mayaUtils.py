try:
    from PySide2 import QtCore as core, QtGui as gui, QtWidgets as widgets
except ImportError:
    from PySide import QtCore as core, QtGui as gui
    widgets= gui
    core.QItemSelectionModel= gui.QItemSelectionModel
    widgets.QHeaderView.setSectionResizeMode= widgets.QHeaderView.setResizeMode

try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance

import os
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import maya.mel as mel

import noid_utils as nut


''' mainWindow '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def mainWindow() :
    ptr= omui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), widgets.QWidget)


''' isBatchMode '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def isBatchMode() :
    return om.MGlobal.mayaState() == om.MGlobal.kBatch


''' createProject '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def createProject(folder) :
    nut.createFolder(folder)

    mel.eval('setProject \"'+folder+'\"')

    for file_rule in cmds.workspace(query= True, fileRuleList= True):
        file_rule_dir= cmds.workspace(fileRuleEntry= file_rule)
        maya_file_rule_dir= os.path.join(folder, file_rule_dir)
        nut.createFolder(maya_file_rule_dir)


''' setProject '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def setProject(folder):
    if nut.folderExists(folder) :
        print("Setting project to {}".format(folder))
        mel.eval('setProject \"'+folder+'\"')


''' isSceneChanged '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def isSceneChanged() :
    return cmds.file(q= True, mf= True)


''' newScene '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def newScene() :
    cmds.file(new= True, force= True)


''' openScene '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def openScene(name) :
    print("Opening {}".format(name))
    cmds.file(name, open= True, type='mayaBinary', de= True, force= True)


''' saveScene '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def saveScene(name) :
    print("Saving {}".format(name))
    nut.createFolder(os.path.dirname(name))
    cmds.file(rename= name)
    cmds.file(save= True, type='mayaBinary', de= True, force= True)


''' exportMaya '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def exportMaya(name, exportAll) :
    print("Exporting {}".format(name))
    nut.createFolder(os.path.dirname(name))
    if exportAll : cmds.file(name, ea= True, type='mayaBinary', de= True, force= True)
    else : cmds.file(name, es= True, type='mayaBinary', de= True, force= True)


''' exportAlembic '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def exportAlembic(name, exportAll) :
    print("Exporting {}".format(name))
    return


''' exportFBX '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def exportFBX(name, exportAll) :
    print("Exporting {}".format(name))
    return


''' exportOBJ '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def exportOBJ(name, exportAll) :
    print("Exporting {}".format(name))
    return


''' exportArchive '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def exportArchive(name, exportAll) :
    print("Exporting {}".format(name))
    return


''' confirmDialog '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def confirmDialog(i_title, i_message) :
    confirm= cmds.confirmDialog(title= i_title, message= i_message, button= ['Yes', 'No'], defaultButton= 'No', cancelButton= 'No', dismissString= 'No')
    if confirm == 'Yes' :
        return True
    return False


''' promptDialog '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def promptDialog(i_title, i_message) :
    confirm= cmds.promptDialog(title= i_title, message= i_message, button= ['Ok', 'Cancel'], defaultButton= 'Ok', cancelButton= 'Cancel', dismissString= 'Cancel')
    if confirm == 'Ok' :
        return True
    return False
