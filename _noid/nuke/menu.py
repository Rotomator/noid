print "NOID pipeline initializing..."


try:
    from PySide2 import QtGui as gui
except ImportError:
    from PySide import QtGui as gui

import nuke

import noid
import nukeSession


''' currentTask_clear '''
''' ---------------------------------------------------------------------------------------------------------------------------- '''
def currentTask_clear(*args, **kwargs) :
    print "currentTask_clear\n"
    nukeSession.currentTask_clear()


nuke.callbacks.addOnScriptClose(currentTask_clear)
nuke.callbacks.addOnScriptLoad(currentTask_clear)


''' create menu
    ---------------------------------------------------------------------------------------------------------------------------- '''
nukeMenu= nuke.menu("Nuke")
noidMenu= nukeMenu.addMenu("NOID")
noidMenu.addCommand("Set Current Task", "noid.switchTaskWnd_show()")
noidMenu.addSeparator()
noidMenu.addCommand("Increment", "")


''' write_addKnobs
    ---------------------------------------------------------------------------------------------------------------------------- '''
def write_addKnobs():
    node= nuke.thisNode()

    # tab
    batch= nuke.Tab_Knob("noid", "NOID")
    node.addKnob(batch)

    # auto
    lock= nuke.Boolean_Knob("lock", "Lock Filename")
    lock.setFlag(nuke.STARTLINE)
    node.addKnob(lock)

    # suffix
    suffix= nuke.String_Knob("suffix", "Suffix")
    suffix.setFlag(nuke.STARTLINE)
    node.addKnob(suffix)

    node.addKnob(nuke.Text_Knob("",""))

    # batch
    batch= nuke.PyScript_Knob("batch", "Batch", "")
    batch.setFlag(nuke.STARTLINE)
    node.addKnob(batch)

    node['file'].setEnabled(False)
    node['lock'].setValue(1)


# add callback to execute this every time a Write node is created
nuke.addOnUserCreate(write_addKnobs, nodeClass= "Write")
