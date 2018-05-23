import noid_database as ndb


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
    return "{}/{}/{}/maya".format(task.m_job.m_project.m_location, task.m_job.m_project.m_name, task.m_job.m_name)
    #return "{}/{:08x}/{:08x}/nuke".format(task.m_job.m_project.m_location, task.m_job.m_project.m_id, task.m_job.m_id)


def taskPath(task) :
    return "{}/scenes/{}${}${:04d}.mb".format(projectFolder(task), ndb.taskTypeStr(task.m_type), task.m_name, task.m_v)
    #return "{}/{:08x}/{:04d}.nk".format(projectFolder(task), task.m_id, task.m_v)
