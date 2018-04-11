from PySide import QtCore, QtGui

import noid_utils as nut
import noid_database as ndb
import mayaUtils as mut
import mayaSession
import listTable


''' publishListView '''
''' ============================================================================================================================ '''
class publishListView(listTable._listTable) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, parent= None) :
        self.m_rows= []

        listTable._listTable.__init__(self, ["Name", "Type", "Time"], parent)
        self.setWidth(1, 80)
        self.setWidth(2, 120)

    ''' rowCount '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def rowCount(self) : return len(self.m_rows)

    ''' data '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def data(self, columnIdx, rowIdx) :
        if columnIdx == 0: return self.m_rows[rowIdx][0]
        elif columnIdx == 1: return ndb.publishTypeStr(self.m_rows[rowIdx][1])
        #elif columnIdx == 2: return self.m_rows[rowIdx][2].strftime("%Y-%m-%d %H:%M:%S")
        elif columnIdx == 2: return nut.elapsedTimeStr(self.m_rows[rowIdx][2])
        return None

    ''' loadRows '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def loadRows(self, project_id, task_id= 0) :
        if not project_id :
            self.clearRows()
            return

        lnk= ndb.link()

        ''' 0: name, 1: type, 2: create time '''
        query= "\
        SELECT pbl.m_name, pbl.m_type, pbl.m_create_time\
        FROM tbl_publish{} pbl\
            INNER JOIN tbl_task{} tsk ON tsk.m_id= pbl.m_task_id".format(project_id, project_id)

        if task_id : query+= " WHERE tsk.m_id= {}".format(task_id)

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


''' _publishWnd '''
''' ============================================================================================================================ '''
class _publishWnd(QtGui.QDialog) :
    ''' __init__ '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def __init__(self, parent= mut.mainWindow()) :
        super(_publishWnd, self).__init__(parent)

        ''' title & size'''
        self.setWindowTitle("Publish")
        self.resize(600, 600)

        ''' restore geometry '''
        self.settings= QtCore.QSettings('noid', 'publishWnd_maya')
        geometry= self.settings.value('geometry', '')
        self.restoreGeometry(geometry)

        ''' setup UI '''
        self.setup_UI()


    ''' setup_UI '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def setup_UI(self) :
        ''' make a vertical box layout and set it's parent to the central widget '''
        self.mainLayout= QtGui.QVBoxLayout()
        self.hl1= QtGui.QHBoxLayout()
        self.vl1= QtGui.QVBoxLayout()
        self.vl1.setAlignment(QtCore.Qt.AlignTop)
        self.vl2= QtGui.QVBoxLayout()
        self.vl2.setAlignment(QtCore.Qt.AlignTop)

        #self.r0= QtGui.QRadioButton("All")
        #self.r0.setChecked(True)
        self.r0= QtGui.QRadioButton("All sets")
        self.r0.setChecked(True)
        self.r1= QtGui.QRadioButton("Selected sets")

        self.c0= QtGui.QCheckBox("Maya Scene")
        self.c0.setChecked(True)
        self.c1= QtGui.QCheckBox("Alembic")
        self.c2= QtGui.QCheckBox("FBX")
        self.c3= QtGui.QCheckBox("OBJ")
        self.c4= QtGui.QCheckBox("Archive")

        ''' table '''
        self.table= publishListView()


        ''' ok button '''
        self.okButton= QtGui.QPushButton("OK")
        self.okButton.clicked.connect(self.ok_onClick)

        ''' add widgets to the main layout '''
        self.mainLayout.addLayout(self.hl1)
        self.mainLayout.addSpacing(8)
        self.hl1.addLayout(self.vl1)
        self.vl1.addWidget(self.r0)
        self.vl1.addWidget(self.r1)
        #self.vl1.addWidget(self.r2)
        self.hl1.addLayout(self.vl2)
        self.vl2.addWidget(self.c0)
        self.vl2.addWidget(self.c1)
        self.vl2.addWidget(self.c2)
        self.vl2.addWidget(self.c3)
        self.vl2.addWidget(self.c4)
        self.mainLayout.addSpacing(8)
        self.mainLayout.addWidget(self.table)
        self.mainLayout.addSpacing(8)
        self.mainLayout.addWidget(self.okButton)

        ''' bind this layout to QMainWindow '''
        self.setLayout(self.mainLayout)


    ''' showEvent '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def showEvent(self, event):
        self.table.loadRows(mayaSession.currentTask().m_job.m_project.m_id, mayaSession.currentTask().m_id)

        #lst= ndb.publishList(task_id= mayaSession.currentTask().m_id)
        #self.table.setList(lst)


    ''' closeEvent '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def closeEvent(self, event) :
        ''' store geometry '''
        geometry= self.saveGeometry()
        self.settings.setValue('geometry', geometry)

        super(_publishWnd, self).closeEvent(event)


    ''' ok_onClick '''
    ''' ------------------------------------------------------------------------------------------------------------------------ '''
    def ok_onClick(self) :
        ''' close window '''
        self.close()

        mayaSession.publishCurrentTask()


