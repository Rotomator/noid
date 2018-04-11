import maya.cmds as cmds

import noid_database as ndb
import mayaUtils as mut


PUBLISHMODE_ALL= 0
PUBLISHMODE_ALLSETS= 1
PUBLISHMODE_SELECTEDSETS= 2


''' g_currentTask '''
''' ---------------------------------------------------------------------------------------------------------------------------- '''
g_currentTask= ndb.taskInfo()


def currentTask() :
    return g_currentTask


def currentTask_clear() :
    global g_currentTask
    g_currentTask.clear()


def currentTask_set(task) :
    global g_currentTask
    g_currentTask= task


def projectFolder(task) :
    #return "{}/{}/{}/maya".format(task.m_job.m_project.m_location, task.m_job.m_project.m_name, task.m_job.m_name)
    return "{}/{:08x}/{:08x}/maya".format(task.m_job.m_project.m_location, task.m_job.m_project.m_id, task.m_job.m_id)


def taskPath(task) :
    #return "{}/scenes/{}${}${:04d}.mb".format(projectFolder(task), ndb.taskTypeStr(task.m_type), task.m_name, task.m_v)
    return "{}/scenes/{:08x}/{:04d}.mb".format(projectFolder(task), task.m_id, task.m_v)


def publishPath(publish) :
    if publish.m_type == ndb.PUBLISHTYPE_MAYA : ext= "mb"
    elif publish.m_type == ndb.PUBLISHTYPE_ALEMBIC : ext= "abc"
    elif publish.m_type == ndb.PUBLISHTYPE_FBX : ext= "fbx"
    elif publish.m_type == ndb.PUBLISHTYPE_OBJ : ext= "obj"
    elif publish.m_type == ndb.PUBLISHTYPE_ARCHIVE : ext= "a"
    else : ext= "txt"
    #return "{}/scenes/pub/{}/{}#{:04d}.{}".format(projectFolder(publish.m_task), ndb.taskTypeStr(publish.m_task.m_type), publish.m_name, publish.m_v, ext)
    return "{}/scenes/pub/{:08x}/{:04d}.{}".format(projectFolder(publish.m_task), publish.m_id, publish.m_v, ext)


''' isPublishSet '''
''' ---------------------------------------------------------------------------------------------------------------------------- '''
def isPublishSet(setName) :
    if not cmds.objExists(setName) : return False
    if cmds.nodeType(setName) != "objectSet" : return False
    if not cmds.attributeQuery("active", node= setName, exists= True) : return False
    return True


''' createPublishSet '''
''' ---------------------------------------------------------------------------------------------------------------------------- '''
def createPublishSet(setName) :
    cmds.sets(name= setName)
    cmds.addAttr(setName, longName= "active", attributeType= "bool", defaultValue= 1)
    cmds.addAttr(setName, longName= "exportMaya", attributeType= "bool", defaultValue= 1)
    cmds.addAttr(setName, longName= "exportAlembic", attributeType= "bool", defaultValue= 0)
    cmds.addAttr(setName, longName= "exportFBX", attributeType= "bool", defaultValue= 0)
    cmds.addAttr(setName, longName= "exportOBJ", attributeType= "bool", defaultValue= 0)
    cmds.addAttr(setName, longName= "exportArchive", attributeType= "bool", defaultValue= 0)
    cmds.lockNode(setName, lock= True)


''' deletePublishSet '''
''' ---------------------------------------------------------------------------------------------------------------------------- '''
def deletePublishSet(setName) :
    if isPublishSet(setName) :
        cmds.lockNode(setName, lock= False)
        cmds.delete(setName)


''' listPublishSets '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def listPublishSets() :
    sets= cmds.ls(sets= True, exactType= "objectSet")

    publishSets= []
    for s in sets :
        if isPublishSet(s) : publishSets.append(s)

    #print(sets)
    #print(publishSets)

    return publishSets


''' listSelectedPublishSets '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def listSelectedPublishSets() :
    sets= cmds.ls(sets= True, exactType= "objectSet", selection= True)

    publishSets= []
    for s in sets :
        if isPublishSet(s) : publishSets.append(s)

    #print(sets)
    #print(publishSets)

    return publishSets


''' setCurrentTask '''
''' ---------------------------------------------------------------------------------------------------------------------------- '''
def setCurrentTask(projectId, taskId) :
    #if taskId == currentTask().m_id : return

    ''' scene changed : open confirm dialog '''
    if mut.isSceneChanged() :
        if not mut.confirmDialog('Warning: Scene Not Saved', 'Scene changes not saved, continue ?') :
            return

    lnk= ndb.link()
    task= ndb.taskInfo(projectId, taskId, lnk)
    if not task.m_id : return

    ''' create (or set) project '''
    mut.createProject(projectFolder(task))

    ''' task not started : update task & create new scene, else open scene '''
    if not task.m_state :
        task.m_state= ndb.TASKSTATE_STARTED
        task.m_v= 1

        mut.newScene()
        mut.saveScene(taskPath(task))

    else :
        mut.openScene(taskPath(task))

    ''' store task '''
    task.store(lnk)
    currentTask_set(task)


''' incrementCurrentTask '''
''' ---------------------------------------------------------------------------------------------------------------------------- '''
def incrementCurrentTask() :
    task= currentTask()
    if not task.m_id : return

    ''' update task '''
    task.m_state= max(currentTask().m_state, ndb.TASKSTATE_STARTED)
    task.m_v+= 1

    ''' save scene '''
    mut.saveScene(taskPath(task))

    ''' store task '''
    lnk= ndb.link()
    task.store(lnk)
    currentTask_set(task)


''' publishCurrentTask '''
''' ---------------------------------------------------------------------------------------------------------------------------- '''
def publishCurrentTask() :
    task= currentTask()
    if not task.m_id : return

    lnk= ndb.link()

    info= ndb.publishInfo()

    info.load(task.m_job.m_project.m_id, "", ndb.PUBLISHTYPE_MAYA, task.m_id, lnk)
    info.m_task.m_v= task.m_v
    info.m_v+= 1

    mut.exportMaya(publishPath(info), True)

    info.store(lnk)

    sets= listPublishSets()
    if len(sets) :
        for s in sets :
            if cmds.getAttr(s+'.active') :

                cmds.select(s)

                if cmds.getAttr(s+'.exportMaya') :
                    info.load(task.m_job.m_project.m_id, s, ndb.PUBLISHTYPE_MAYA, task.m_id, lnk)
                    info.m_task.m_v= task.m_v
                    info.m_v+= 1

                    mut.exportMaya(publishPath(info), False)

                    info.store(lnk)

                if cmds.getAttr(s+'.exportAlembic') :
                    info.load(task.m_job.m_project.m_id, s, ndb.PUBLISHTYPE_ALEMBIC, task.m_id, lnk)
                    info.m_task.m_v= task.m_v
                    info.m_v+= 1

                    mut.exportAlembic(publishPath(info), False)

                    info.store(lnk)

                if cmds.getAttr(s+'.exportFBX') :
                    info.load(task.m_job.m_project.m_id, s, ndb.PUBLISHTYPE_FBX, task.m_id, lnk)
                    info.m_task.m_v= task.m_v
                    info.m_v+= 1

                    mut.exportFBX(publishPath(info), False)

                    info.store(lnk)

                if cmds.getAttr(s+'.exportOBJ') :
                    info.load(task.m_job.m_project.m_id, s, ndb.PUBLISHTYPE_OBJ, task.m_id, lnk)
                    info.m_task.m_v= task.m_v
                    info.m_v+= 1

                    mut.exportOBJ(publishPath(info), False)

                    info.store(lnk)

                if cmds.getAttr(s+'.exportArchive') :
                    info.load(task.m_job.m_project.m_id, s, ndb.PUBLISHTYPE_ARCHIVE, task.m_id, lnk)
                    info.m_task.m_v= task.m_v
                    info.m_v+= 1

                    mut.exportArchive(publishPath(info), False)

                    info.store(lnk)

    ''' update & store task '''
    task.m_state= max(task.m_state, ndb.TASKSTATE_PUBLISHED)
    task.store(lnk)
    currentTask_set(task)


''' createPublishSetDlg '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def createPublishSetDlg() :
    if mut.promptDialog('Create Publish Sets', 'Set name :') :
        createPublishSet(cmds.promptDialog(query= True, text= True))


''' deleteSelectedPublishSetsDlg '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def deleteSelectedPublishSetsDlg() :
    if mut.confirmDialog('Delete Publish Sets', 'Delete selected publish sets ?') :
        sets= cmds.ls(sets= True, exactType= "objectSet", selection= True)
        for s in sets :
            deletePublishSet(s)
