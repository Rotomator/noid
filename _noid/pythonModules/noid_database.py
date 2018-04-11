import os
import getpass
import datetime
import mysql.connector


''' constants
    ---------------------------------------------------------------------------------------------------------------------------- '''
JOBTYPESTR= ["None", "Shot", "2D Asset", "3D Asset"]
JOBTYPE_SHOT= 0
JOBTYPE_ASSET2D= 1
JOBTYPE_ASSET3D= 2

TASKTYPESTR= ["LAYOUT", "MODEL", "RIG", "CFX", "ANIM", "SURFACE", "LIGHT", "FX", "RENDER", "COMP"]
TASKTYPE_LAYOUT= 0
TASKTYPE_MODEL= 1
TASKTYPE_RIG= 2
TASKTYPE_CFX= 3
TASKTYPE_ANIM= 4
TASKTYPE_SURFACE= 5
TASKTYPE_LIGHT= 6
TASKTYPE_FX= 7
TASKTYPE_RENDER= 8
TASKTYPE_COMP= 9
TASKTYPE_MIN= TASKTYPE_LAYOUT
TASKTYPE_MAX= TASKTYPE_COMP

TASKSTATESTR= ["ASSIGNED", "STARTED", "PUBLISHED", "APPROVED"]
TASKSTATE_ASSIGNED= 0
TASKSTATE_STARTED= 1
TASKSTATE_PUBLISHED= 2
TASKSTATE_APPROVED= 3
TASKSTATE_MIN= TASKSTATE_ASSIGNED
TASKSTATE_MAX= TASKSTATE_APPROVED

PUBLISHTYPESTR= ["Image", "Alembic", "FBX", "OBJ", "Archive", "Maya", "Nuke", "Houdini", "3DE", "ZBrush", "Mudbox"]
PUBLISHTYPE_IMAGE= 0
PUBLISHTYPE_ALEMBIC= 1
PUBLISHTYPE_FBX= 2
PUBLISHTYPE_OBJ= 3
PUBLISHTYPE_ARCHIVE= 4
PUBLISHTYPE_MAYA= 5
PUBLISHTYPE_NUKE= 6
PUBLISHTYPE_HOUDINI= 7
PUBLISHTYPE_3DE= 8
PUBLISHTYPE_ZBRUSH= 9
PUBLISHTYPE_MUDBOX= 10
PUBLISHTYPE_MIN= PUBLISHTYPE_IMAGE
PUBLISHTYPE_MAX= PUBLISHTYPE_MUDBOX


''' host
    ---------------------------------------------------------------------------------------------------------------------------- '''
#_HOST= "172.16.2.37"
#_HOST= "localhost"
_HOST= os.getenv("NOID_HOST")
_DATABASE= "test"
_USER= "root"
_PASSWORD= "rootpass"


''' user
    ---------------------------------------------------------------------------------------------------------------------------- '''
_g_user_id= 0
_g_user_login= ""
_g_user_name= ""


def jobTypeStr(jobType) :
    return JOBTYPESTR[taskType]

def taskTypeStr(taskType) :
    return TASKTYPESTR[taskType]

def taskStateStr(taskState) :
    return TASKSTATESTR[taskState]

def publishTypeStr(publishType) :
    return PUBLISHTYPESTR[publishType]


''' link
    ============================================================================================================================ '''
class link :
    def __init__(self) :
        ''' connect '''
        self.m_cnx= mysql.connector.connect(user= _USER, password= _PASSWORD, host= _HOST, database= _DATABASE)
        self.m_cursor= self.m_cnx.cursor()

    def __del__(self) :
        ''' commit & disconnect '''
        self.m_cursor.close()
        self.m_cnx.commit()
        self.m_cnx.close()

    def execute(self, query) :
        self.m_cursor.execute(query)
        return self.m_cursor


''' findUser
    ---------------------------------------------------------------------------------------------------------------------------- '''
def findUser() :
    global _g_user_id
    global _g_user_login
    global _g_user_name

    lnk= link()

    result= lnk.execute("SELECT m_id, m_login, m_name FROM tbl_user WHERE m_login= '{}'".format(getpass.getuser()))
    rows= result.fetchall()
    if len(rows) == 1 :
        _g_user_id= rows[0][0]
        _g_user_login= rows[0][1]
        _g_user_name= rows[0][2]
        print("{} {} {}".format(_g_user_id, _g_user_login, _g_user_name))

    return _g_user_id > 0


''' user_id, user_login, user_name
    ---------------------------------------------------------------------------------------------------------------------------- '''
def user_id() : return _g_user_id
def user_login() : return _g_user_name
def user_name() : return _g_user_name


''' projectCount
    ---------------------------------------------------------------------------------------------------------------------------- '''
def projectCount(lnk) :
    result= lnk.execute("SELECT COUNT(*) FROM tbl_project")

    count= 0
    rows= result.fetchall()
    if len(rows) == 1 : count= rows[0][0]

    return count


''' jobCount
    ---------------------------------------------------------------------------------------------------------------------------- '''
def jobCount(lnk, project_id) :
    lnk.execute("SELECT COUNT(*) FROM tbl_job{}".format(project_id))

    count= 0
    rows= result.fetchall()
    if len(rows) == 1 : count= rows[0][0]

    return count


''' userList
    ---------------------------------------------------------------------------------------------------------------------------- '''
def userList(lnk) :
    ''' 0: id, 1: name '''
    result= lnk.execute("\
        SELECT m_id, m_name\
        FROM tbl_user\
        ORDER BY m_name\
    ")

    return result.fetchall()


''' projectList
    ---------------------------------------------------------------------------------------------------------------------------- '''
def projectList(lnk) :
    ''' 0: id, 1: name '''
    result= lnk.execute("\
        SELECT m_id, m_name\
        FROM tbl_project\
        ORDER BY m_name\
    ")

    return result.fetchall()


''' jobList
    ---------------------------------------------------------------------------------------------------------------------------- '''
def jobList(lnk, project_id) :
    ''' 0: id, 1: name '''
    result= lnk.execute("\
        SELECT m_id, m_name\
        FROM tbl_job{}\
        ORDER BY m_name\
    ".format(project_id))

    return result.fetchall()


''' taskTypeList
    ---------------------------------------------------------------------------------------------------------------------------- '''
def taskTypeList(lnk, project_id, job_id= 0) :
    ''' 0: id, 1: name '''
    if job_id :
        query= "\
            SELECT DISTINCT m_type\
            FROM tbl_task{}\
            WHERE m_job_id= {}\
            ORDER BY m_type".format(project_id, job_id)
    else :
        query= "\
            SELECT DISTINCT tsk.m_type\
            FROM tbl_task{} tsk\
            ORDER BY tsk.m_type".format(project_id)

    result= lnk.execute(query)

    return result.fetchall()


''' rows_valueIndex
    ---------------------------------------------------------------------------------------------------------------------------- '''
def rows_valueIndex(rows, columnIdx, value) :
    idx= -1
    for i in range(0, len(rows)):
        if rows[i][columnIdx] == value :
            idx= i
            break
    return idx


''' projectInfo
    ============================================================================================================================ '''
class projectInfo :
    def __init__(self, project_id= 0, lnk= 0) :
        self.clear()
        self.load(project_id, lnk)

    def clear(self) :
        self.m_id= 0
        self.m_name= ""
        self.m_location= ""
        self.m_desc= ""
        self.m_image= ""
        self.m_create_user_id= 0
        self.m_create_time= datetime.datetime.now()

    def load(self, project_id, lnk) :
        if project_id == self.m_id : return True
        self.clear()

        if project_id and lnk :
            result= lnk.execute("\
                SELECT m_name, m_location, m_desc, m_image, m_create_user_id, m_create_time\
                FROM tbl_project\
                WHERE m_id= '{}'\
            ".format(project_id))

            ''' get row '''
            rows= result.fetchall()
            if len(rows) == 1 :
                self.m_id= project_id
                self.m_name= rows[0][0]
                self.m_location= rows[0][1]
                self.m_desc= rows[0][2]
                self.m_image= rows[0][3]
                self.m_create_user_id= rows[0][4]
                self.m_create_time= rows[0][5]
                #print("projectInfo loaded!")
                return True

        return False


''' jobInfo
    ============================================================================================================================ '''
class jobInfo :
    def __init__(self, project_id= 0, job_id= 0, lnk= 0) :
        self.clear()
        self.load(project_id, job_id, lnk)

    def clear(self) :
        self.m_project= projectInfo()
        self.m_id= 0
        self.m_type= 0
        self.m_name= ""
        self.m_create_user_id= 0
        self.m_create_time= datetime.datetime.now()

    def load(self, project_id, job_id, lnk) :
        if ( project_id == self.m_project.m_id ) and ( job_id == self.m_id ) : return True
        self.clear()

        if job_id and lnk :
            result= lnk.execute("\
                SELECT m_type, m_name, m_create_user_id, m_create_time\
                FROM tbl_job{}\
                WHERE m_id= '{}'\
            ".format(project_id, job_id))

            ''' get row '''
            rows= result.fetchall()
            if len(rows) == 1 :
                if self.m_project.load(project_id, lnk) :
                    self.m_id= job_id
                    self.m_type= rows[0][0]
                    self.m_name= rows[0][1]
                    self.m_create_user_id= rows[0][2]
                    self.m_create_time= rows[0][3]
                    #print("jobInfo loaded!")
                    return True

        return False


''' taskInfo
    ============================================================================================================================ '''
class taskInfo :
    def __init__(self, project_id= 0, task_id= 0, lnk= 0) :
        self.clear()
        self.load(project_id, task_id, lnk)

    def clear(self) :
        self.m_job= jobInfo()
        self.m_id= 0
        self.m_type= 0
        self.m_user_id= 0
        self.m_start= datetime.date.today()
        self.m_end= datetime.date.today()
        self.m_desc= ""
        self.m_create_user_id= 0
        self.m_create_time= datetime.datetime.now()
        self.m_state= 0
        self.m_v= 0

    def load(self, project_id, task_id, lnk) :
        if ( project_id == self.m_job.m_project.m_id ) and ( task_id == self.m_id ) : return True
        self.clear()

        if task_id and lnk :
            result= lnk.execute("\
                SELECT m_job_id, m_type, m_user_id, m_start, m_end, m_desc, m_create_user_id, m_create_time, m_state, m_v\
                FROM tbl_task{}\
                WHERE m_id= '{}'\
            ".format(project_id, task_id))

            ''' get row '''
            rows= result.fetchall()
            if len(rows) == 1 :
                if self.m_job.load(project_id, rows[0][0], lnk) :
                    self.m_id= task_id
                    self.m_type= rows[0][1]
                    self.m_user_id= rows[0][2]
                    self.m_start= rows[0][3]
                    self.m_end= rows[0][4]
                    self.m_desc= rows[0][5]
                    self.m_create_user_id= rows[0][6]
                    self.m_create_time= rows[0][7]
                    self.m_state= rows[0][8]
                    self.m_v= rows[0][9]
                    #print("taskInfo loaded!")
                    return True

        return False

    def store(self, lnk) :
        if not ( self.m_id and lnk ) : return False

        ''' store m_state & m_v '''
        lnk.execute("UPDATE tbl_task{} SET m_state= {}, m_v= {} WHERE m_id= {}".format(self.m_job.m_project.m_id, self.m_state, self.m_v, self.m_id))

        return True


''' publishInfo
    ============================================================================================================================ '''
class publishInfo :
    def __init__(self, project_id= 0, name= "", type= 0, task_id= 0, lnk= 0) :
        self.clear()
        self.load(project_id, name, type, task_id, lnk)

    def clear(self) :
        self.m_task= taskInfo()
        self.m_id= 0
        self.m_name= ""
        self.m_type= 0
        self.m_v= 0

    def load(self, project_id, name, type, task_id, lnk) :
        self.m_task.load(project_id, task_id, lnk)
        self.m_id= 0
        self.m_name= name
        self.m_type= type
        self.m_v= 0

        if not ( self.m_task.m_id and lnk ) : return False

        result= lnk.execute("\
            SELECT m_id, m_v\
            FROM tbl_publish{}\
            WHERE m_name= '{}' AND m_type= {} AND m_task_id= {}\
        ".format(project_id, self.m_name, self.m_type, task_id))

        rows= result.fetchall()

        if len(rows) == 1 :
            self.m_id= rows[0][0]
            self.m_v= rows[0][1]

        else :
            result= lnk.execute("\
                INSERT INTO tbl_publish{} (m_name, m_type, m_task_id, m_task_v, m_create_user_id, m_create_time, m_v)\
                VALUES ('{}', {}, {}, {}, {}, NOW(), {})\
            ".format(self.m_task.m_job.m_project.m_id, self.m_name, self.m_type, self.m_task.m_id, self.m_task.m_v, user_id(), self.m_v))

            self.m_id= result.lastrowid

        return True

    def store(self, lnk) :
        if not ( self.m_id and lnk ) : return False

        lnk.execute("UPDATE tbl_publish{} SET m_task_v= {}, m_create_user_id= {}, m_create_time= NOW(), m_v= {} WHERE m_id= {}".format(self.m_task.m_job.m_project.m_id, self.m_task.m_v, user_id(), self.m_v, self.m_id))

        return True
