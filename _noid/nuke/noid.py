try:
    from PySide2 import QtGui as gui, QtWidgets as widgets
except ImportError:
    from PySide import QtGui as gui
    widgets= gui

import noid_database as ndb
import switchTask


g_switchTaskWnd= None


''' create windows
    ---------------------------------------------------------------------------------------------------------------------------- '''
def switchTaskWnd_show() :
    global g_switchTaskWnd

    if not g_switchTaskWnd :
        g_switchTaskWnd= switchTask._switchTaskWnd(gui.QApplication.activeWindow())

    g_switchTaskWnd.show()


''' create menu
    ---------------------------------------------------------------------------------------------------------------------------- '''


''' find user
    ---------------------------------------------------------------------------------------------------------------------------- '''
ndb.findUser()
