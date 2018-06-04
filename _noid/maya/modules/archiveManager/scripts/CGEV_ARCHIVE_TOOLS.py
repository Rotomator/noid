import pymel.core as pm
import maya.OpenMaya as om
import maya.mel as mel
import os
import random
import time
import re
import string
import operator
import math
import os.path


from functools import wraps


import CGEV_genLib as gl
reload(gl)

# load archive plugin

if not pm.pluginInfo("maya_archive",q=True,l=True):
	pm.loadPlugin( "maya_archive" )

if not pm.pluginInfo("vrayformaya",q=True,l=True):
	pm.loadPlugin( "vrayformaya" )


@gl.viewportOff
def archiveDesc(sel,archive_dirPath=list()):

    dict_obj={};sg_node=list();shaderPath=list();fileTextExt = '.adesc'
    pm.select(cl=True)

    if  archive_dirPath is not None:

        i=0

        for item in sel:


            if ":" in item :
                dirname=item.replace(":","_")
            else :
                dirname=item.nodeName()


            if os.path.exists(archive_dirPath+'/'+dirname)==False:
                archiveSubDir=os.mkdir(archive_dirPath+'/'+dirname)
                archiveSubDir=archive_dirPath+'/'+dirname

            else:
                archiveSubDir=archive_dirPath+'/'+dirname

            root_node= item

            shape_nodeList=gl.getNodes(item,'Mesh',1)


            shape_node=[shape for shape in shape_nodeList]

            #change str(shape) to shape !

            shadingEngine_node=[pm.PyNode(item).outputs(type='shadingEngine') for item in shape_node]

            sg_node=list(set([item[0] for item in shadingEngine_node if item ]))

            shader_node=[pm.listConnections(item+'.surfaceShader') for item in sg_node]


            # flatten list
            shader_node=[shaderB for shaderA in shader_node for shaderB in shaderA]

            shader_list=[str(shader.name().split(':')[-1]) for shader in shader_node]

            vrayUserAttr=[pm.PyNode(item).getAttr('vrayUserAttributes') for item in shape_node if pm.attributeQuery('vrayUserAttributes',n=item,exists=True)]
            vrayUserAttr=list(set(vrayUserAttr))

            rtPivot=pm.PyNode(root_node).getRotatePivot('world')

            dict_obj['ARCHIVE_'+str(i)]={'shapes':shape_node,'root':root_node ,'shader':shader_node,'shadingG':sg_node,'shaderName': shader_list,'vray_UserAttr':vrayUserAttr,'rtPivot':rtPivot,'archiveSubdir':archiveSubDir}

            i+=1

    return  dict_obj

def choosePoolDirectory():

    archive_dirPath=pm.fileDialog2(cap="IMPORT ARCHIVE POOL",fm=1,ds=1,ff='*.apool')

    if archive_dirPath==None:
        pm.warning('select pool file !')
    else:
        if '\\' in archive_dirPath[0]:
            archive_dirPath=archive_dirPath[0].replace('\\','/')
        else:
            archive_dirPath=archive_dirPath[0]

        return archive_dirPath

def readArchiveDescritpion(path=''):

    archive_dirPath=path
    allDir=[item for item in os.listdir(path) if os.path.isdir(path+'/'+item)]
    importLine=list()
    for elem in allDir:
        archiveDir=archive_dirPath+'/'+elem
        listFiles = os.listdir(archiveDir)

        for fileName in listFiles :
            tmpList=list()
            if fileName.endswith('.adesc') :
                file = open(archiveDir+os.sep+fileName, 'r')
                tmpList.append([line.split('=')  for line in file.read().splitlines()])
                importLine.append(tmpList)
                file.close()
    return importLine

def readArchivePool(path=''):

    archivePool_dirPath=path
    existingPoolFile=[item for item in os.listdir(path) if item.endswith('.apool')]
    importLine=list()
    archive_nodes=list()
    shader_nodes=list()

    if len(existingPoolFile)!=0:
        tmpList=list()
        poolFile=path+os.sep+existingPoolFile[0];
        file = open(poolFile, 'r')
        tmpList.append([line.split('=')  for line in file.read().splitlines()])
        importLine.append(tmpList)
        archive_nodes=importLine[0][0][0][1]
        shader_nodes=importLine[0][0][1][1]
        file.close()
        return archive_nodes,shader_nodes

def poolArchive(description=list()):

    node_value=description

    shader_list=list()

    proxyNodesList=list()
    shaderDict=dict()

    exportedShaders=list()

    archive_path=list()
    shader_path=list()

    for index,item in enumerate (node_value):

        archive_path.append(item[0][2][1])
        shader_path=[elem for elem in item[0][3][1].split(',')]

        for shader in shader_path:
            shader_list.append(shader)

    for shader in shader_list:

        name=os.path.splitext(os.path.basename(shader))[0]


        if name not in shaderDict:
            shaderDict[name] = list()
            shaderDict[name].append(shader)

    for name, shds in shaderDict.iteritems():

        shaderDict[name].sort()
        exportedShaders.append(shaderDict[name][0])

    return archive_path,exportedShaders



def export_arc(sel,archiveDict,mainWindow,bakeVC,anim,sf,ef):



    mainWindow.setupProgressBar(len(archiveDict.values()),'EXPORT ARCHIVE')

    ''' RENAME SHADER WITH ARC_ BEFORE ARCHIVE EXPORT'''

    shdName=rename_arc_shd(sel,archiveDict)

    for item in archiveDict.values():


        subdirName=item['archiveSubdir']+'/'
        pm.showHidden(item['root'])

        ''' BAKE COLOR VERTEX'''

        if bakeVC==1:
            objList=item['shapes']
            bakeVertexColor(objList)

        ''' EXPORT ARCHIVE '''
        archiveName= item['root'].nodeName().replace(':','_')+'_base'


        pm.select(item['root'])

        if anim==1:

            export_archive=r'arc_export("%s%s",0,"N, ST, Cd",1,%s,%s,1,1,1,0)'%(subdirName,archiveName,sf,ef)

        else:
            export_archive=r'arc_export("%s%s",0,"N, ST, Cd",0,%s,%s,1,1,1,0)'%(subdirName,archiveName,sf,ef)
# ne pas exporter le proxy a cette etape
        run_export=mel.eval(export_archive)

        pm.hide(item['root'])
        pm.select(cl=True)

        mainWindow.growBar()


    ''' RENAME SHADER BACK TO ORIGINAL NAME'''

    for shd in set (list(shdName) ):

        if "ARC_" in str(shd):
            pm.rename(shd,shd.replace("ARC_",""))

    pm.showHidden(sel)




def rename_arc_shd(sel,archiveDict):

    arc_shadingList=list()

    for item in archiveDict.values():

        for node in item['shadingG']:

            ''' EXCEPTION FOR REFERENCE with : '''
            if ":" not in node.name():

                if node!="initialShadingGroup":


                    shadingGroupName=str(node)

                    shader=pm.listConnections(shadingGroupName+'.surfaceShader')

                    shaderName=shader[0].name()

                    ''' RENAME SHADER WITH PREFIX ARC_'''


                    sg_ArcName="ARC_"+shadingGroupName
                    shader_ArcName="ARC_"+shaderName


                    if "ARC_" not in str(node):

                        renamed_sg=pm.rename(shadingGroupName,sg_ArcName)
                        renamed_shader=pm.rename(shaderName,shader_ArcName)

                        arc_shadingList.append(renamed_sg)
                        arc_shadingList.append(renamed_shader)
                        node= renamed_sg


                pm.select(node,ne=True)

    return  arc_shadingList




def export_shd(sel,archiveDict,mainWindow):

    ''' EXPORT SHADERS '''

    mainWindow.setupProgressBar(len(archiveDict.values()),'EXPORT SHADER')

    shdName=rename_arc_shd(sel,archiveDict)

    for item in archiveDict.values():

        i=0

        subdirName=item['archiveSubdir']+'/'

        for node in item['shadingG']:

            if node!="initialShadingGroup":

                shadingGroupName=str(node)

                shader=pm.listConnections(shadingGroupName+'.surfaceShader')

                shaderName=shader[0].name()

                pm.select(node,ne=True)

                pm.exportSelected(subdirName+item['shaderName'][i]+'.mb',f=True,constructionHistory=False,type='mayaBinary')

                i+=1

                pm.select(cl=True)

                mainWindow.growBar()

    for shd in set (list(shdName) ):

        if "ARC_" in str(shd):
            pm.rename(shd,shd.replace("ARC_",""))



def export_arc_override(sel,archiveDict):

    arcName=list()
    for item in archiveDict.values():

        subdirName=item['archiveSubdir']+'/'
        archiveName= item['root'].nodeName().replace(':','_')
        fileTextNameExporting = ('%s%s' % (subdirName,archiveName) ) + '.a'

        arc_override_file=open(fileTextNameExporting,'w+',0)

        arc_override_file.write ('import("' + ('%s%s' % (subdirName,archiveName) )+'_base.a");' )
        arc_override_file.write (u"\r\n")
        arc_override_file.write (u"\r\n")

        ''' CREATE MASK CONTEXT'''

        arc_override_file.write ('context("mask");')
        arc_override_file.write (u"\r\n")
        arc_override_file.write ('node("instance","*");')
        arc_override_file.write (u"\r\n")
        arc_override_file.write ('\tattribute("sShader");')
        arc_override_file.write (u"\r\n")
        arc_override_file.write ('\tset("ARC_SHD_MASK");')
        arc_override_file.write (u"\r\n")
        arc_override_file.write (u"\r\n")

        ''' CREATE CUSTOM SHADER CONTEXT'''

        arc_override_file.write ('context("customShader");')
        arc_override_file.write (u"\r\n")
        arc_override_file.write ('node("instance","*");')
        arc_override_file.write (u"\r\n")
        arc_override_file.write ('\tattribute("sShader");')
        arc_override_file.write (u"\r\n")
        arc_override_file.write ('\tset("ARC_SHD_CUSTOM");')


        arc_override_file.close()
        arcName.append(fileTextNameExporting)

    return  arcName




def export_adesc(sel,archiveDict,mainWindow):

    ''' EXPORT ARCHIVE DESCRIPTION FILE '''
    mainWindow.setupProgressBar(len(archiveDict.values()),'EXPORT ADESC')
    for item in archiveDict.values():

        subdirName=item['archiveSubdir']+'/'
        archiveName= item['root'].nodeName().replace(':','_')

        fileTextNameExporting = ('%s%s' % (subdirName,archiveName) ) + '.adesc'

        desc_file=open(fileTextNameExporting,'w+',0)

        desc_file.write("root_node="+archiveName)
        desc_file.write (u"\r\n")
        desc_file.write("shape_nodes="+str(item['shapes']))
        desc_file.write (u"\r\n")
        desc_file.write("archive_path="+subdirName+archiveName+'.a')
        desc_file.write (u"\r\n")

        i=0
        shaderPath=list()
        for shader in item['shader']:
            shaderPath.append(str(subdirName+item['shaderName'][i]+'.mb'))

            i+=1

        desc_file.write("shader_path="+','.join(shaderPath))
        desc_file.write (u"\r\n")
        desc_file.write("shader_node="+str(str(item['shaderName'])))
        desc_file.write (u"\r\n")
        desc_file.write("'vray_UserAttr'="+str(item['vray_UserAttr']))
        desc_file.write (u"\r\n")
        desc_file.write("rtPivot="+str(item['rtPivot']))

        desc_file.close()
        mainWindow.growBar()



def export_apool(archive_dirPath,mainWindow):

    all_desc=readArchiveDescritpion(archive_dirPath)

    archive_datas=poolArchive(all_desc)
    poolFileName = ('%s/%s' % (archive_dirPath,archive_dirPath.split('/')[-1]) ) + '.apool'

    pool_file=open( poolFileName,'w+',0)

    pool_file.write("archive_nodes="+str(archive_datas[0]))
    pool_file.write (u"\r\n")
    pool_file.write("shader_nodes="+str(archive_datas[1]))

    pool_file.close()

@gl.viewportOff
def archiveExport(mode,bakeVC,sf,ef,mainWindow):

    if not mode:
        pm.warning('Choose at least one option !')

    else:

        sel=[ obj for obj in pm.ls (sl=1)]
        selShader=list()



        if len(sel)==0:
            pm.warning( 'Noting selected !')

        else:
            archive_dirPath=pm.fileDialog2(cap="EXPORT ARCHIVE DIRECTORY",fm=2,ds=1,okc=' OK !')

            if  archive_dirPath is None:
                pm.warning( 'No folder selected !')

            else:


                if '\\' in archive_dirPath[0]:
                    archive_dirPath=archive_dirPath[0].replace('\\','/')
                else:
                    archive_dirPath=archive_dirPath[0]

                archiveDict=archiveDesc(sel,archive_dirPath)

            if mode&(1<<0):



                if mode&(1<<2):

                    export_arc(sel,archiveDict,mainWindow,bakeVC,1,sf,ef)

                    print 'export anim'

                else:

                    export_arc(sel,archiveDict,mainWindow,bakeVC,0,sf,ef)
                    print 'export static'

                ''' EXPORT OVERRIDE AND PROXY'''
                arc_o=export_arc_override(sel,archiveDict)
                arcToPrxCmd=os.environ["ARCHIVE_PATH"].replace('\\','/')+"/bin/archive2prx.exe"

                for arc in arc_o:

                    os.system(str(arcToPrxCmd) +" "+ str (arc))



            if mode&(1<<1):

                ''' EXCEPTION FOR REFERENCE with : '''

                for item in sel:
                    if ":" in item:
                        sel.remove(item)


                if len(sel)!=0:
                    export_shd(sel,archiveDict,mainWindow)
                    print 'export shader'


            export_adesc(sel,archiveDict,mainWindow)
            export_apool(archive_dirPath,mainWindow)


def import_arc(dir,mainWindow):

    importLine=list()
    file =open(dir, 'r')
    importLine=[line.split('=')  for line in file.read().splitlines()]
    file.close()

    archive_path=eval(importLine[0][1])
    shader_path=eval(importLine[1][1])

    mainWindow.setupProgressBar(len(archive_path),'IMPORT ARCHIVES')

    for archive in archive_path:



        if os.path.isfile(archive):

            adesc=archive.replace('.a','.adesc')
            adescFile=open(adesc,'r')
            shaderLine=[line.split('=')  for line in adescFile.read().splitlines()][3][1]
            adescFile.close()

            shaderLine=shaderLine.split(',')

            archiveName=os.path.splitext(os.path.basename(archive))[0]

            archiveNode_tmp=mel.eval('arc_createArchiveNode')
            print archiveNode_tmp

            #CONFIGURE ARCHIVE PARAMETERS

            archiveNode=pm.rename(pm.PyNode(archiveNode_tmp).getParent(), archiveName)
            pm.PyNode(archiveNode).setAttr('filePrefix',archive)
            pm.PyNode(archiveNode).setAttr('animationMode',1)
            pm.PyNode(archiveNode).setAttr('viewType',1)
            pm.PyNode(archiveNode).setAttr('pointSize',3)
            pm.PyNode(archiveNode).setAttr('viewBBox',0)

            # ADD SHADER PATH ATTRIBUTE

            i=0
            for item in shaderLine:
                shaderAttr='shader_'+str(i)
                if pm.attributeQuery(shaderAttr,n=archiveNode,exists=True)==False:
                    pm.PyNode(archiveNode).addAttr(shaderAttr,dt='string')

                getattr(pm.PyNode(archiveNode),shaderAttr).set(item)

                i+=1

            #SCENE HIERARCHY
            #fix : deselect before parenting
            pm.select(cl=True)

            groupArchive=pm.group(n=archiveName+'_ARCHIVE_GRP',w=True)


            pm.parent(archiveNode,groupArchive)

            mainWindow.growBar()

def import_shd(dir,mainWindow):

    importLine=list()
    file =open(dir, 'r')
    importLine=[line.split('=')  for line in file.read().splitlines()]
    file.close()
    archive_path=eval(importLine[0][1])
    shader_path=eval(importLine[1][1])

    mainWindow.setupProgressBar(len(archive_path),'IMPORT SHADER')

    for shader in shader_path:

        if os.path.isfile(shader):

#        '''IMPORT SHADERS'''

            allSG=pm.ls(type='shadingEngine')

            allShader=[pm.listConnections(node+'.surfaceShader')[0].name() for node in allSG]

            shdName="ARC_"+shader.split('.')[0].split('/')[-1]

            importShader=r'pm.importFile("%s")' % (shader)

            if shdName not in allShader:

                eval(importShader)

            else:
                print shdName+' already in scene'
                sgName=pm.listConnections(shdName+'.outColor')
                shaderGraph=[shd for shd in pm.listHistory(sgName) if pm.nodeType(shd)!='mesh']
                pm.delete(shaderGraph)
                eval(importShader)
                mainWindow.growBar()

@gl.viewportOff
def archiveImport(mode,mainWindow):


    ' PRE/POST RENDER MEL FOR SHADER ASIGNEMENT'''

    pm.setAttr('defaultRenderGlobals.preMel', "attachFakeVRayShaders;", type='string')
    pm.setAttr('defaultRenderGlobals.postMel', "detachFakeVRayShaders;", type='string')

    if not mode:
        pm.warning('Choose at least one option !')
    else:
        poolPath=choosePoolDirectory()

        if poolPath!=None:

            if mode&(1<<0):
                import_arc(poolPath,mainWindow)

            if mode&(1<<1):
                import_shd(poolPath,mainWindow)


#@gl.viewportOff
def bakeVertexColor(objList=list()):

    if pm.objExists("vraySettings")==False:
        pm.shadingNode("VRaySettingsNode", asUtility=True, name = "vraySettings")

    defLightSet=pm.PyNode("defaultLightSet")

    allLights=[ node for node in defLightSet.members() if node.name()!="a_bakeVC" ]

    if len(defLightSet)!=0:
        defLightSet.removeMembers(allLights)


    bakeLight=pm.ambientLight(ambientShade=0,n='a_bakeVC')
    bakeLight=bakeLight.getParent()


    pm.PyNode("vraySettings").setAttr("baking_engine",4)
    pm.PyNode("vraySettings").setAttr("bakeAlpha",0)
    pm.PyNode("vraySettings").setAttr("colorSetName",'archive_vertexColor')

    pm.select(cl=True)

    pm.select(objList)
    mel.eval('vrend')
    pm.select(cl=True)

    pm.PyNode("vraySettings").setAttr("baking_engine",1)
    defLightSet.addMembers(allLights)
    pm.delete(bakeLight)


def cleanArchiveName(mainWindow):

    sel=gl.getNodes(None,'Transform',0)
    archiveNodes=pm.ls(type='archiveNode')

    i=0
    mainWindow.setupProgressBar(len(archiveNodes),'RENAME ARCHIVE')
    for node in archiveNodes:

        shortName=node.filePrefix.get().split('.')[0].split('/')[-1]
        shortName=node.name(long=None)
        #regular expression
        idName=re.match(r'.*_id.*',shortName,re.M|re.I)
        if idName:
            id=idName.group().split('_')[-1]
            shortName=shortName.replace('_'+id,'')
        newName=shortName+'_id'+str(i)
        node.getParent().rename(newName)
        i+=1
        mainWindow.growBar()


