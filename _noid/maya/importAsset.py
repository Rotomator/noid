from PySide import QtCore, QtGui

import noid_database as ndb
import mayaUtils as mut
import mayaSession
import listTable
import infoTable


''' importListView '''
''' ============================================================================================================================ '''
''' 0: id, 1: name, 2: type, 3: taskType, 4: jobName, 5: projectName'''
class importListView(listTable._listTable) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, parent= None) :
        self.m_rows= []

        listTable._listTable.__init__(self, ["Job", "Task", "Name", "Type"], parent)
        self.setWidth(1, 80)
        self.setWidth(3, 80)

    ''' rowCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def rowCount(self) : return len(self.m_rows)

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, columnIdx, rowIdx) :
        if columnIdx == 0: return self.m_rows[rowIdx][4]
        elif columnIdx == 1: return ndb.taskTypeStr(self.m_rows[rowIdx][3])
        elif columnIdx == 2: return self.m_rows[rowIdx][1]
        elif columnIdx == 3: return ndb.publishTypeStr(self.m_rows[rowIdx][2])
        return None

    ''' loadRows '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def loadRows(self, project_id, job_id= 0, task_type= -1) :
        if not project_id :
            self.clearRows()
            return

        lnk= ndb.link()

        query= "\
        SELECT pbl.m_id, pbl.m_name, pbl.m_type, tsk.m_type, job.m_name\
        FROM tbl_publish{} pbl\
            INNER JOIN tbl_task{} tsk ON tsk.m_id= pbl.m_task_id\
            INNER JOIN tbl_job{} job ON job.m_id= tsk.m_job_id".format(project_id, project_id, project_id)

        if job_id : query+= " WHERE job.m_id= {}".format(job_id)
        if task_type >= 0 : query+= " AND tsk.m_type= {}".format(task_type)

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
    def row(self, idx) : return self.m_rows[index]


''' _importWnd '''
''' ============================================================================================================================ '''
class _importWnd(QtGui.QDialog) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, parent= mut.mainWindow()) :
        ''' runs __init__ in QMainWindow first, then overrides with _importWnd '''
        super(_importWnd, self).__init__(parent)

        self.m_projects_valid= False
        self.m_projects= 0
        self.m_projectId= 0

        self.m_jobs_valid= False
        self.m_jobs= 0
        self.m_jobId= 0

        self.m_taskTypes_valid= False
        self.m_taskTypes= 0
        self.m_taskType= -1

        self.m_table_valid= False

        ''' set the window title & size '''
        self.setWindowTitle("Import")
        self.resize(600, 600)

        ''' restore geometry '''
        self.settings= QtCore.QSettings('noid', 'importWnd_maya')
        geometry= self.settings.value('geometry', '')
        self.restoreGeometry(geometry)

        ''' setup UI '''
        self.setup_UI()


    ''' setup_UI '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setup_UI(self) :
        self.m_mainL= QtGui.QVBoxLayout()

        ''' top menus '''
        self.m_topL= QtGui.QHBoxLayout()
        self.m_projectsM= QtGui.QComboBox()
        self.m_projectsM.currentIndexChanged.connect(self.projectsM_onChange)
        self.m_jobsM= QtGui.QComboBox()
        self.m_jobsM.currentIndexChanged.connect(self.jobsM_onChange)
        self.m_taskTypesM= QtGui.QComboBox()
        self.m_taskTypesM.currentIndexChanged.connect(self.taskTypesM_onChange)

        ''' m_table '''
        self.m_table= importListView()

        ''' infos '''
        self.m_infoTable= infoTable._infoTable(["Project", "Job", "Task", "Task Version", "Type", "Version", "Date"])

        ''' ok button '''
        self.m_okB= QtGui.QPushButton("OK")
        self.m_okB.clicked.connect(self.ok_onClick)

        ''' add the widgets to the main layout '''
        self.m_topL.addWidget(self.m_projectsM)
        self.m_topL.addWidget(self.m_jobsM)
        self.m_topL.addWidget(self.m_taskTypesM)
        self.m_mainL.addLayout(self.m_topL)
        self.m_mainL.addSpacing(8)
        self.m_mainL.addWidget(self.m_table)
        self.m_mainL.addSpacing(8)
        self.m_mainL.addWidget(self.m_infoTable)
        self.m_mainL.addSpacing(8)
        self.m_mainL.addWidget(self.m_okB)

        ''' bind this layout to QMainWindow '''
        self.setLayout(self.m_mainL)


    ''' setFilters '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setFilters(self, projectId= -1, jobId= -1, taskType= -2) :
        if projectId == -1 : projectId= self.m_projectId
        elif self.m_projectId != projectId :
            self.m_projectId= projectId
            self.m_jobs_valid= False
            self.m_taskTypes_valid= False
            self.m_table_valid= False

        if jobId == -1 : jobId= self.m_jobId
        elif self.m_jobId != jobId :
            self.m_jobId= jobId
            self.m_taskTypes_valid= False
            self.m_table_valid= False

        if taskType == -2 : taskType= self.m_taskType
        elif self.m_taskType != taskType :
            self.m_taskType= taskType
            self.m_table_valid= False

        self.validate()


    ''' validate '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def validate(self) :
        if not self.isVisible() : return

        lnk= ndb.link()

        ''' projects '''
        if not self.m_projects_valid :
            self.m_projects_valid= True

            ''' project rows '''
            self.m_projects= ndb.projectList(lnk)
            idx= ndb.rows_valueIndex(self.m_projects, 0, self.m_projectId)          # compute m_jobId index in m_jobs
            if idx < 0 :                                                            # if idx < 0 : m_projectId= 1st project id (or 0 if no preoject)
                if len(self.m_projects) : self.m_projectId= self.m_projects[0][0]
                else : self.m_projectId= 0

            ''' build menu '''
            self.m_projectsM.blockSignals(True)
            self.m_projectsM.clear()
            for i in range(0, len(self.m_projects)) : self.m_projectsM.addItem(self.m_projects[i][1]) # add item to menu
            if idx > 0 : self.m_projectsM.setCurrentIndex(idx)
            self.m_projectsM.blockSignals(False)

        ''' jobs '''
        if not self.m_jobs_valid :
            self.m_jobs_valid= True

            ''' job rows '''
            self.m_jobs= ndb.jobList(lnk, self.m_projectId)
            idx= ndb.rows_valueIndex(self.m_jobs, 0, self.m_jobId)  # compute m_jobId index in m_jobs
            if idx < 0 : self.m_jobId= 0                            # if index < 0 : m_jobId= 0

            ''' build menu '''
            self.m_jobsM.blockSignals(True)
            self.m_jobsM.clear()
            self.m_jobsM.addItem("Any")
            for i in range(0, len(self.m_jobs)) : self.m_jobsM.addItem(self.m_jobs[i][1]) # add item to menu
            if idx >= 0 : self.m_jobsM.setCurrentIndex(idx+1)
            self.m_jobsM.blockSignals(False)

        ''' taskTypes '''
        if not self.m_taskTypes_valid :
            self.m_taskTypes_valid= True

            ''' taskType rows '''
            self.m_taskTypes= ndb.taskTypeList(lnk, self.m_projectId, self.m_jobId)
            idx= ndb.rows_valueIndex(self.m_taskTypes, 0, self.m_taskType)  # compute m_taskType index in m_jobs
            if idx < 0 : self.m_taskType= -1                                # if idx < 0 : m_taskType= -1

            ''' build menu '''
            self.m_taskTypesM.blockSignals(True)
            self.m_taskTypesM.clear()
            self.m_taskTypesM.addItem("Any")
            for i in range(0, len(self.m_taskTypes)) : self.m_taskTypesM.addItem(ndb.taskTypeStr(self.m_taskTypes[i][0]))  # add item to menu
            if idx >= 0 : self.m_taskTypesM.setCurrentIndex(idx+1)
            self.m_taskTypesM.blockSignals(False)

        ''' table '''
        if not self.m_table_valid :
            self.m_table_valid= True

            self.m_table.loadRows(self.m_projectId, self.m_jobId, self.m_taskType)


    ''' showEvent '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def showEvent(self, event) :
        super(_importWnd, self).showEvent(event)

        if not event.spontaneous() :
            self.m_projects_valid= False
            self.m_jobs_valid= False
            self.m_taskTypes_valid= False
            self.m_table_valid= False
            self.validate()


    ''' closeEvent '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def closeEvent(self, event) :
        ''' store geometry '''
        geometry= self.saveGeometry()
        self.settings.setValue('geometry', geometry)

        super(_importWnd, self).closeEvent(event)


    ''' projectsM_onChange '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def projectsM_onChange(self, idx) :
        self.setFilters(projectId= self.m_projects[idx][0])


    ''' jobsM_onChange '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def jobsM_onChange(self, idx) :
        if idx : i= self.m_jobs[idx-1][0]
        else : i= 0
        self.setFilters(jobId= i)


    ''' taskTypesM_onChange '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def taskTypesM_onChange(self, idx) :
        if idx : i= self.m_taskTypes[idx-1][0]
        else : i= -1
        self.setFilters(taskType= i)


    ''' ok_onClick '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def ok_onClick(self) :
        return
