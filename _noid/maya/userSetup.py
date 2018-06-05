#print('noid_maya initializing...')


import os
import sys
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om


# noid_path
# ----------------------------------------------------------------------------------------------------------------------------
def noid_path(path) :
    return os.path.expandvars(path).replace('\\', '/')


# noid_setEnv
# ----------------------------------------------------------------------------------------------------------------------------
def noid_setEnv(key, value) :
    if key[0] == '+' :
        key= key[1:]
        if os.getenv(key) : os.environ[key]+= ";"+noid_path(value)
        else : os.environ[key]= noid_path(value)
    else :
        os.environ[key]= noid_path(value)
    #print(key+" :\n"+os.environ[key])


# noid_setEnvs
# ----------------------------------------------------------------------------------------------------------------------------
def noid_setEnvs(envs) :
    for i in range(0, len(envs), 2):
        noid_setEnv(envs[i], envs[i+1])


''' royalRender
    ---------------------------------------------------------------------------------------------------------------------------- '''
mel.eval('source "'+noid_path('%NOID_PATH%/maya/royalrender/noid_rrSubmit.mel')+'"')


''' attachFakeVRayShaders, detachFakeVRayShaders
    ---------------------------------------------------------------------------------------------------------------------------- '''
mel.eval('source "'+noid_path('%NOID_PATH%/maya/tools/attachFakeVRayShaders.mel')+'"')
mel.eval('source "'+noid_path('%NOID_PATH%/maya/tools/detachFakeVRayShaders.mel')+'"')


# isBatchMode '''
# ----------------------------------------------------------------------------------------------------------------------------
def isBatchMode() :
    return om.MGlobal.mayaState() == om.MGlobal.kBatch


# import noid module (deferred)
# ----------------------------------------------------------------------------------------------------------------------------
if not isBatchMode() :
    cmds.evalDeferred('import noid')

