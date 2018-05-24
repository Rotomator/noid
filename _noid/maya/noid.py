import noid_database as ndb
import mayaUtils as mut
import mayaSession
import switchTask
import importAsset
import publish

import maya.cmds as cmds


if not mut.isBatchMode() :
    print "Creating windows and menus..."

    ''' create windows
        ---------------------------------------------------------------------------------------------------------------------------- '''
    switchTaskWnd= switchTask._switchTaskWnd()
    importWnd= importAsset._importWnd()
    publishWnd= publish._publishWnd()


    ''' create menu
        ---------------------------------------------------------------------------------------------------------------------------- '''
    cmds.menu(label= 'NOID', parent='MayaWindow')
    cmds.menuItem(label= 'Set Current Task', command= 'noid.switchTaskWnd.show()')
    cmds.menuItem(divider= True)
    cmds.menuItem(label= 'Increment', command= 'noid.mayaSession.incrementCurrentTask()')
    cmds.menuItem(divider= True)
    cmds.menuItem(label= 'Create Publish Set', command= 'noid.mayaSession.createPublishSetDlg()')
    cmds.menuItem(label= 'Delete Selected Publish Sets', command= 'noid.mayaSession.deleteSelectedPublishSetsDlg()')
    cmds.menuItem(label= 'Publish', command= 'noid.mayaSession.publishCurrentTask()')
    cmds.menuItem(divider= True)
    cmds.menuItem(label= 'Import', command= 'noid.importWnd.show()')
    cmds.menuItem(divider= True)
    cmds.menuItem(label= 'Submit To RoyalRender', command= 'mel.eval("noid_rrSubmit(1);")')


    ''' find user
        ---------------------------------------------------------------------------------------------------------------------------- '''
    ndb.findUser()
