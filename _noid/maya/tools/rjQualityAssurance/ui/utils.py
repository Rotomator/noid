import os
from maya import OpenMaya, OpenMayaUI, cmds

# import pyside, do qt version check for maya 2017 >
qtVersion = cmds.about(qtVersion=True)
if qtVersion.startswith("4") or type(qtVersion) not in [str, unicode]:
    from PySide.QtGui import *
    from PySide.QtCore import *
    import shiboken
else:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import shiboken2 as shiboken

# ----------------------------------------------------------------------------

FONT = QFont()
FONT.setFamily("Consolas")

BOLT_FONT = QFont()
BOLT_FONT.setFamily("Consolas")
BOLT_FONT.setWeight(100)

# ----------------------------------------------------------------------------

ALIGN_LEFT_STYLESHEET = "QPushButton{text-align: left}"
URGENCY_STYLESHEET = {
    0: "QPushButton{ background-color: green;}",
    1: "QPushButton{ background-color: orange;}",
    2: "QPushButton{ background-color: red;}",
}

CHECK_ICON = ":/checkboxOff.png"
SELECT_ICON = ":/redSelect.png"
FIX_ICON = ":/interactivePlayback.png"

COLLAPSE_ICONS = {
    True: ":/arrowDown.png",
    False: ":/arrowRight.png"
}

# ----------------------------------------------------------------------------

def mayaWindow():
    """
    Get Maya's main window.
    
    :rtype: QMainWindow
    """
    window = OpenMayaUI.MQtUtil.mainWindow()
    window = shiboken.wrapInstance(long(window), QMainWindow)
    
    return window  

# ----------------------------------------------------------------------------
    
def findIcon(icon):
    """
    Loop over all icon paths registered in the XBMLANGPATH environment 
    variable ( appending the tools icon path to that list ). If the 
    icon exist a full path will be returned.

    :param str icon: icon name including extention
    :return: icon path
    :rtype: str or None
    """
    paths = []

    # get maya icon paths
    if os.environ.get("XBMLANGPATH"):     
        paths = os.environ.get("XBMLANGPATH").split(os.pathsep)                                 

    # append tool icon path
    paths.insert(
        0,
        os.path.join(
            os.path.split(__file__)[0], 
            "icons" 
        ) 
    )

    # loop all potential paths
    for path in paths:
        filepath = os.path.join(path, icon)
        if os.path.exists(filepath):
            return filepath