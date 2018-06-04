try:
    from PySide2 import QtCore as core, QtGui as gui, QtWidgets as widgets
except ImportError:
    from PySide import QtCore as core, QtGui as gui
    widgets= gui
    core.QItemSelectionModel= gui.QItemSelectionModel
    widgets.QHeaderView.setSectionResizeMode= widgets.QHeaderView.setResizeMode

import noid_database as ndb
import listTable
import infoTable

<<<<<<< HEAD
import maya.OpenMaya as om
import mayaUtils as mut
import mayaSession
=======
#import maya.OpenMaya as om
#import mayaUtils as mut
#import mayaSession
>>>>>>> c19bfa8b2e3b225b306790e2ed7f77464ba1d0e0



''' currentTask_clear '''
''' ---------------------------------------------------------------------------------------------------------------------------- '''
def currentTask_clear(*args, **kwargs) :
<<<<<<< HEAD
    mayaSession.currentTask_clear()

om.MSceneMessage.addCallback(om.MSceneMessage.kAfterNew, currentTask_clear)
om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, currentTask_clear)
=======
    return
    #mayaSession.currentTask_clear()

#om.MSceneMessage.addCallback(om.MSceneMessage.kAfterNew, currentTask_clear)
#om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, currentTask_clear)
>>>>>>> c19bfa8b2e3b225b306790e2ed7f77464ba1d0e0


''' projectListView '''
''' ============================================================================================================================ '''
class projectListView(listTable._listTable) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, parent= None) :
        self.m_rows= []

        listTable._listTable.__init__(self, ["Project"], parent)
        self.setFixedWidth(120)

    ''' columnCount, rowCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def rowCount(self) : return len(self.m_rows)

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, columnIdx, rowIdx) :
        if columnIdx == 0 : return self.m_rows[rowIdx][1]
        return None

    ''' loadRows '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def loadRows(self, lnk) :
        result= lnk.execute("\
            SELECT m_id, m_name\
            FROM tbl_project\
            ORDER BY m_name")

        self.m_rows= result.fetchall()

        self.update()

    ''' clearRows '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def clearRows(self) :
        del self.m_rows [:]
        self.update()

    ''' row '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def row(self, idx) : return self.m_rows[idx]


''' jobListView '''
''' ============================================================================================================================ '''
class jobListView(listTable._listTable) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, parent= None) :
        self.m_rows= []

        listTable._listTable.__init__(self, ["Job"], parent)
        self.setFixedWidth(120)

    ''' columnCount, rowCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def rowCount(self) : return len(self.m_rows)+1

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, columnIdx, rowIdx) :
        if not rowIdx : return "All"
        elif columnIdx == 0 : return self.m_rows[rowIdx-1][1]
        return None

    ''' loadRows '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def loadRows(self, lnk, project_id, user_id) :
        if not project_id :
            self.clearRows()
            return

        query= "\
            SELECT job.m_id, CONCAT(REPEAT('   ', job.m_depth), job.m_name)\
            FROM tbl_task{} tsk\
                INNER JOIN tbl_job{} job ON job.m_id= tsk.m_job_id\
            WHERE tsk.m_type <= {}".format(project_id, project_id, ndb.TASKTYPE_RENDER)

        if user_id : query+= " AND tsk.m_user_id= {}".format(user_id)
        query+= " GROUP BY job.m_id ORDER BY job.m_left"

        result= lnk.execute(query)
        self.m_rows= result.fetchall()

        self.update()

    ''' clearRows '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def clearRows(self) :
        del self.m_rows [:]
        self.update()

    ''' row '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def row(self, idx) : return self.m_rows[idx-1]


''' taskListView '''
''' ============================================================================================================================ '''
class taskListView(listTable._listTable) :
    m_stateColors= [gui.QColor(232, 17, 35), gui.QColor(255, 140, 0), gui.QColor(0, 140, 251), gui.QColor(29, 221, 29)]

    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, parent= None) :
        self.m_rows= []

        listTable._listTable.__init__(self, ["Job", "Task type", "State", "Version", "Desc"], parent)
        self.setWidth(1, 80)
        self.setWidth(2, 80)
        self.setWidth(3, 80)

    ''' columnCount, rowCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def rowCount(self) : return len(self.m_rows)

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, columnIdx, rowIdx) :
        if columnIdx == 0 : return self.m_rows[rowIdx][6]
        elif columnIdx == 1 :
            str= ndb.taskTypeStr(self.m_rows[rowIdx][1])
            if self.m_rows[rowIdx][2] != ndb.user_id() : str+= " (!)"
            return str
        elif columnIdx == 2 : return ndb.taskStateStr(self.m_rows[rowIdx][4])
        elif columnIdx == 3 : return self.m_rows[rowIdx][5]
        elif columnIdx == 4 : return self.m_rows[rowIdx][3]
        return None

    ''' fgColor '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def fgColor(self, columnIdx, rowIdx) :
        if columnIdx == 2 : return taskListView.m_stateColors[self.m_rows[rowIdx][4]]
        return None

    ''' loadRows '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def loadRows(self, lnk, project_id, job_id= 0, user_id= 0) :
        if not project_id :
            self.clearRows()
            return

        query= "\
            SELECT t.m_id, t.m_type, t.m_user_id, t.m_desc, t.m_state, t.m_v, j.m_name\
            FROM tbl_task{} t\
                INNER JOIN tbl_job{} j ON j.m_id= t.m_job_id\
            WHERE t.m_type <= {}".format(project_id, project_id, ndb.TASKTYPE_RENDER)

        if job_id : query+= " AND j.m_id= {}".format(job_id)
        if user_id : query+= " AND t.m_user_id= {}".format(user_id)

        query+= " ORDER BY j.m_left"

        result= lnk.execute(query)
        self.m_rows= result.fetchall()

        self.update()

    ''' clearRows '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def clearRows(self) :
        del self.m_rows [:]
        self.update()

    ''' row '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def row(self, idx) : return self.m_rows[idx]


''' _switchTaskWnd '''
''' ============================================================================================================================ '''
class _switchTaskWnd(widgets.QDialog) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
<<<<<<< HEAD
    def __init__(self, parent= mut.mainWindow()) :
=======
    def __init__(self, parent) :
>>>>>>> c19bfa8b2e3b225b306790e2ed7f77464ba1d0e0
        super(_switchTaskWnd, self).__init__(parent)

        self.m_showMyTasks= True
        self.m_showMyTasks_valid= False
        self.m_projectId= 0
        self.m_projectList_valid= False
        self.m_jobId= 0
        self.m_jobList_valid= False
        self.m_taskList_valid= False

        ''' title & size '''
        self.setWindowTitle("Switch Task")
        self.resize(600, 600)

        ''' restore geometry '''
<<<<<<< HEAD
        self.settings= core.QSettings('noid', 'switchTaskWnd_maya')
=======
        self.settings= core.QSettings('noid', 'switchTaskWnd_nuke')
>>>>>>> c19bfa8b2e3b225b306790e2ed7f77464ba1d0e0
        geometry= self.settings.value('geometry', '')
        self.restoreGeometry(geometry)

        ''' setup UI '''
        self.setup_UI()

    ''' setup_UI '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setup_UI(self) :
        self.mainLayout= widgets.QVBoxLayout()

        ''' options '''
        self.m_showMyTasksCB= widgets.QCheckBox("Show my tasks only")
        self.m_showMyTasksCB.stateChanged.connect(self.showEveryTasksCB_onClick)

        ''' task table '''
        self.hLayout= widgets.QHBoxLayout()
        self.m_projectList= projectListView()
        selection= self.m_projectList.selectionModel()
        selection.selectionChanged.connect(self.projectList_selectionChanged)
        self.m_jobList= jobListView()
        selection= self.m_jobList.selectionModel()
        selection.selectionChanged.connect(self.jobList_selectionChanged)
        self.m_taskList= taskListView()
        #selection= self.m_taskList.selectionModel()
        #selection.selectionChanged.connect(self.table_onSelect)

        ''' ok button '''
        self.okButton= widgets.QPushButton("OK")
        self.okButton.clicked.connect(self.ok_onClick)

        ''' add the widgets to the main layout '''
        self.hLayout.addWidget(self.m_projectList)
        self.hLayout.addWidget(self.m_jobList)
        self.hLayout.addSpacing(8)
        self.hLayout.addWidget(self.m_taskList)
        self.mainLayout.addWidget(self.m_showMyTasksCB)
        self.mainLayout.addSpacing(8)
        self.mainLayout.addLayout(self.hLayout)
        self.mainLayout.addSpacing(8)
        self.mainLayout.addWidget(self.okButton)

        ''' bind this layout to QMainWindow '''
        self.setLayout(self.mainLayout)

    ''' showEvent '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def showEvent(self, event) :
        super(_switchTaskWnd, self).showEvent(event)

        if not event.spontaneous() :
            self.setShowEveryTasks(True)
            self.m_projectList_valid= False
            self.m_jobList_valid= False
            self.m_taskList_valid= False
            self.validate()

    ''' closeEvent '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def closeEvent(self, event) :
        ''' store geometry '''
        geometry= self.saveGeometry()
        self.settings.setValue('geometry', geometry)

        super(_switchTaskWnd, self).closeEvent(event)

    ''' showEveryTasksCB_onClick '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def showEveryTasksCB_onClick(self, state) :
        self.setShowEveryTasks(state>0)
        self.validate()

    ''' projectList_selectionChanged '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def projectList_selectionChanged(self, selected, deselected) :
        indexes= self.m_projectList.selectionModel().selectedRows()
        if len(indexes) :
            index= indexes[0].row()
            projectId= self.m_projectList.row(index)[0]

            self.setCurrentProject(projectId)
            self.validate()

    ''' jobList_selectionChanged '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def jobList_selectionChanged(self, selected, deselected) :
        indexes= self.m_jobList.selectionModel().selectedRows()
        if len(indexes) :
            index= indexes[0].row()
            if index : jobId= self.m_jobList.row(index)[0]
            else : jobId= 0

            self.setCurrentJob(jobId)
            self.validate()

    ''' ok_onClick '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def ok_onClick(self) :
        ''' get selected task '''
        projectIdxs= self.m_projectList.selectionModel().selectedRows()
        if not len(projectIdxs) : return

        taskIdxs= self.m_taskList.selectionModel().selectedRows()
        if not len(taskIdxs) : return

        ''' taskId '''
        projectId= self.m_projectList.row(projectIdxs[0].row())[0]
        taskId= self.m_taskList.row(taskIdxs[0].row())[0]

        ''' close window '''
        self.close()

<<<<<<< HEAD
        mayaSession.setCurrentTask(projectId, taskId)
=======
        #print "ok"
        #mayaSession.setCurrentTask(projectId, taskId)
>>>>>>> c19bfa8b2e3b225b306790e2ed7f77464ba1d0e0

    ''' setShowEveryTasks '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setShowEveryTasks(self, state) :
        if self.m_showMyTasks != state :
            self.m_showMyTasks= state
            self.m_showMyTasks_valid= False
            self.m_jobList_valid= False
            self.m_taskList_valid= False

    ''' setCurrentProject '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setCurrentProject(self, projectId) :
        if self.m_projectId != projectId :
            self.m_projectId= projectId
            self.m_jobList_valid= False
            self.m_taskList_valid= False

    ''' setCurrentJob '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setCurrentJob(self, jobId) :
        if self.m_jobId != jobId :
            self.m_jobId= jobId
            self.m_taskList_valid= False

    ''' validate '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def validate(self) :
        if not self.isVisible() : return

        self.m_showMyTasksCB.blockSignals(True)
        self.m_projectList.selectionModel().blockSignals(True)
        self.m_jobList.selectionModel().blockSignals(True)
        self.m_taskList.selectionModel().blockSignals(True)

        lnk= ndb.link()

        if self.m_showMyTasks : userId= ndb.user_id()
        else : userId= 0

        ''' validate m_setShowEveryTasksCB '''
        if not self.m_showMyTasks_valid :
            print("validating m_showMyTasks")
            self.m_showMyTasks_valid= True
            self.m_showMyTasksCB.setChecked(self.m_showMyTasks)

        ''' validate m_projectList '''
        if not self.m_projectList_valid :
            print("validating m_projectList")
            self.m_projectList_valid= True
            self.m_projectList.loadRows(lnk)

            idx= ndb.rows_valueIndex(self.m_projectList.m_rows, 0, self.m_projectId)    # compute m_projectId index in m_projectList
            if idx < 0 :                                                                # if index < 0 : m_projectId= 1st project id (or 0 if no preoject)
                idx= 0
                if len(self.m_projectList.m_rows) : self.m_projectId= self.m_projectList.m_rows[0][0]
                else : self.m_projectId= 0

            if self.m_projectId :
                self.m_projectList.selectionModel().select(self.m_projectList.model().index(idx, 0), core.QItemSelectionModel.Select);

        ''' validate m_jobList '''
        if not self.m_jobList_valid :
            print("validating m_jobList")
            self.m_jobList_valid= True
            self.m_jobList.loadRows(lnk, self.m_projectId, userId)

            idx= ndb.rows_valueIndex(self.m_jobList.m_rows, 0, self.m_jobId)    # compute m_jobId index in m_jobList
            if idx < 0 : self.m_jobId= 0                                        # if index < 0 : m_jobId= 0

            self.m_jobList.selectionModel().select(self.m_jobList.model().index(idx+1, 0), core.QItemSelectionModel.Select);

        ''' validate m_taskList '''
        if not self.m_taskList_valid :
            print("validating m_taskList")
            self.m_taskList_valid= True
            self.m_taskList.loadRows(lnk, self.m_projectId, self.m_jobId, userId)

        self.m_showMyTasksCB.blockSignals(False)
        self.m_projectList.selectionModel().blockSignals(False)
        self.m_jobList.selectionModel().blockSignals(False)
        self.m_taskList.selectionModel().blockSignals(False)


    ''' refresh_onClick '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def refresh_onClick(self) :
        return
