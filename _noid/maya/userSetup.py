#print('noid_maya initializing...')


import os
import sys
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om


''' noid_path
    ---------------------------------------------------------------------------------------------------------------------------- '''
def noid_path(path) :
    return os.path.expandvars(path).replace('\\', '/')


''' noid_setEnv
    ---------------------------------------------------------------------------------------------------------------------------- '''
def noid_setEnv(key, value) :
    if key[0] == '+' :
        key= key[1:]
        if os.getenv(key) : os.environ[key]+= ";"+noid_path(value)
        else : os.environ[key]= noid_path(value)
    else :
        os.environ[key]= noid_path(value)
    #print(key+" :\n"+os.environ[key])


''' noid_setEnvs
    ---------------------------------------------------------------------------------------------------------------------------- '''
def noid_setEnvs(envs) :
    for i in range(0, len(envs), 2):
        noid_setEnv(envs[i], envs[i+1])


''' envs
    ---------------------------------------------------------------------------------------------------------------------------- '''
MAYA_VERSION= os.getenv("MAYA_VERSION")
VRAY_VERSION= os.getenv("VRAY_VERSION")
ARCHIVE_VERSION= os.getenv("ARCHIVE_VERSION")

noid_setEnvs([
    'NOID_HOST'                                     , 'localhost',

	'ARCHIVE_PATH'					                , '%NOID_PATH%/archive/'+ARCHIVE_VERSION,

	'+VRAY_FOR_MAYA'+MAYA_VERSION+'_MAIN_x64'	    , '%NOID_BIN_PATH%/vray/'+VRAY_VERSION+'/maya'+MAYA_VERSION+'/maya_vray',
	'+VRAY_FOR_MAYA'+MAYA_VERSION+'_PLUGINS_x64'    , '%VRAY_FOR_MAYA'+MAYA_VERSION+'_MAIN_x64%/vrayplugins',
	'+VRAY_OSL_PATH_MAYA'+MAYA_VERSION+'_x64'	    , '%VRAY_FOR_MAYA'+MAYA_VERSION+'_PLUGINS_x64%',
	'+VRAY_AUTH_CLIENT_FILE_PATH'	                , '%NOID_BIN_PATH%/vray',
    '+PATH'                                         , '%NOID_BIN_PATH%/vray/'+VRAY_VERSION+'/maya'+MAYA_VERSION+'/maya_root/bin',
	'+MAYA_PLUG_IN_PATH'			                , '%VRAY_FOR_MAYA'+MAYA_VERSION+'_MAIN_x64%/plug-ins',
	'+MAYA_SCRIPT_PATH'				                , '%VRAY_FOR_MAYA'+MAYA_VERSION+'_MAIN_x64%/scripts',
	'+XBMLANGPATH'					                , '%VRAY_FOR_MAYA'+MAYA_VERSION+'_MAIN_x64%/icons',

	'+VRAY_FOR_MAYA'+MAYA_VERSION+'_PLUGINS_x64'	, '%ARCHIVE_PATH%/vray/'+VRAY_VERSION,
	'+MAYA_PLUG_IN_PATH'			                , '%ARCHIVE_PATH%/maya/plug-ins/'+MAYA_VERSION,
	'+MAYA_SCRIPT_PATH'				                , '%ARCHIVE_PATH%/maya/scripts',
	'+XBMLANGPATH'				                    , '%ARCHIVE_PATH%/maya/icons/',

    'RR_ROOT'                                       , '//storb/diskb/RoyalRender',
	'+MAYA_PLUG_IN_PATH'			                , '%NOID_PATH%/maya/royalrender',

    '+MAYA_SCRIPT_PATH'                             , '%NOID_PATH%/maya/tools',
    '+MAYA_SCRIPT_PATH'                             , '%NOID_PATH%/maya/tools/cometScripts',
    'MAYA_ENABLE_LEGACY_VIEWPORT'                   , '1',
    '+MAYA_PLUG_IN_PATH'                            , '%NOID_BIN_PATH%/maya/plugins/smoothSkinClusterWeight',
    '+MAYA_PLUG_IN_PATH'                            , '%NOID_BIN_PATH%/maya/plugins/iDeform',
    '+MAYA_PLUG_IN_PATH'                            , '%NOID_BIN_PATH%/maya/plugins/ZivaVFX-Maya-1_2/plug-ins'


])


''' python modules path
    ---------------------------------------------------------------------------------------------------------------------------- '''
sys.path.append(noid_path('%NOID_PATH%/pythonModules'))
sys.path.append(noid_path('%NOID_BIN_PATH%/vray/'+VRAY_VERSION+'/maya'+MAYA_VERSION+'/maya_vray/scripts'))
sys.path.append(noid_path('%NOID_PATH%/maya/tools'))


''' royalRender
    ---------------------------------------------------------------------------------------------------------------------------- '''
mel.eval('source "'+noid_path('%NOID_PATH%/maya/royalrender/noid_rrSubmit.mel')+'"')


''' isBatchMode '''
''' -----------------------------------------------------------------------------------------------------------------------------'''
def isBatchMode() :
    return om.MGlobal.mayaState() == om.MGlobal.kBatch


''' import noid module (deferred)
    ---------------------------------------------------------------------------------------------------------------------------- '''
if not isBatchMode() :
    cmds.evalDeferred('import noid')
