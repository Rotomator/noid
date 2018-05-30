# Royal Render Plugin script for Fusion 5+
# Author: Royal Render, Holger Schoenberger, Binary Alchemy
# Last change: v 6.01.70
# Copyright (c) 2009-2012 Holger Schoenberger - Binary Alchemy
# rrInstall_Copy: \plugins\
# rrInstall_Change_File: \plugins\menu.py, before "# Help menu", "m =  menubar.addMenu(\"RRender\");\nm.addCommand(\"Submit Comp\", \"nuke.load('rrSubmit_Nuke_5'), rrSubmit_Nuke_5()\")\n\n"

import nuke
import os
import sys
import platform
import random
import string
import time


from xml.etree.ElementTree import ElementTree, Element, SubElement

#from cgev.pipeline.data import getdata
#from cgev.pipeline.data import session

writeDisabled = list()


###############################################################################
# This function has to be changed if an app should show info                  #
# and error dialog box                                                        #
###############################################################################

def writeInfo(msg):
    print(msg)
#    nuke.message(msg)


def writeError(msg):
    # print(msg)
    nuke.message(msg)


##############################################
# JOB CLASS                                  #
##############################################


class rrJob(object):
    """Stores scene information """
    version = ""
    software = ""
    renderer = ""
    requiredPlugins = ""
    sceneName = ""
    sceneDatabaseDir = ""
    seqStart = 0
    seqEnd = 100
    seqStep = 1
    seqFileOffset = 0
    seqFrameSet = ""
    imageWidth = 99
    imageHeight = 99
    imageDir = ""
    imageFileName = ""
    imageFramePadding = 4
    imageExtension = ""
    imagePreNumberLetter = ""
    imageSingleOutput = False
    sceneOS = ""
    camera = ""
    layer = ""
    channel = ""
    maxChannels = 0
    channelFileName = []
    channelExtension = []
    isActive = False
    sendAppBit = ""
    preID = ""
    waitForPreID = ""
    CustomA = ""
    CustomB = ""
    CustomC = ""
    LocalTexturesFile = ""

    def __init__(self):
        pass

    # from infix.se (Filip Solomonsson)
    def indent(self, elem, level=0):
        i = "\n" + level * ' '
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + " "
            for e in elem:
                self.indent(e, level + 1)
                if not e.tail or not e.tail.strip():
                    e.tail = i + " "
            if not e.tail or not e.tail.strip():
                e.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
        return True

    def subE(self, r, e, t):
        sub = SubElement(r, e)
        sub.text = str(t)
        return sub

    def writeToXMLstart(self, submitOptions):
        rootElement = Element("RR_Job_File")
        rootElement.attrib["syntax_version"] = "6.0"
        self.subE(rootElement, "DeleteXML", "1")
        self.subE(rootElement, "SubmitterParameter", submitOptions)
        # YOU CAN ADD OTHER NOT SCENE-INFORMATION PARAMETERS USING THIS FORMAT:
        # self.subE(jobElement,"SubmitterParameter","PARAMETERNAME=" +
        #         PARAMETERVALUE_AS_STRING)
        return rootElement

    def writeToXMLJob(self, rootElement):

        jobElement = self.subE(rootElement, "Job", "")
        self.subE(jobElement, "Software", self.software)
        self.subE(jobElement, "Renderer", self.renderer)
        self.subE(jobElement, "RequiredPlugins", self.requiredPlugins)
        self.subE(jobElement, "Version", self.version)
        self.subE(jobElement, "SceneName", self.sceneName)
        self.subE(jobElement, "SceneDatabaseDir", self.sceneDatabaseDir)
        self.subE(jobElement, "IsActive", self.isActive)
        self.subE(jobElement, "SeqStart", self.seqStart)
        self.subE(jobElement, "SeqEnd", self.seqEnd)
        self.subE(jobElement, "SeqStep", self.seqStep)
        self.subE(jobElement, "SeqFileOffset", self.seqFileOffset)
        self.subE(jobElement, "SeqFrameSet", self.seqFrameSet)
        self.subE(jobElement, "ImageWidth", int(self.imageWidth))
        self.subE(jobElement, "ImageHeight", int(self.imageHeight))
        self.subE(jobElement, "ImageDir", self.imageDir)
        self.subE(jobElement, "ImageFilename", self.imageFileName)
        self.subE(jobElement, "ImageFramePadding", self.imageFramePadding)
        self.subE(jobElement, "ImageExtension", self.imageExtension)
        self.subE(jobElement, "ImageSingleOutput", self.imageSingleOutput)
        self.subE(jobElement, "ImagePreNumberLetter",
                  self.imagePreNumberLetter)
        self.subE(jobElement, "SceneOS", self.sceneOS)
        self.subE(jobElement, "Camera", self.camera)
        self.subE(jobElement, "Layer", self.layer)
        self.subE(jobElement, "Channel", self.channel)
        self.subE(jobElement, "SendAppBit", self.sendAppBit)
        self.subE(jobElement, "PreID", self.preID)
        self.subE(jobElement, "WaitForPreID", self.waitForPreID)
        self.subE(jobElement, "CustomA", self.CustomA)
        self.subE(jobElement, "CustomB", self.CustomB)
        self.subE(jobElement, "CustomC", self.CustomC)
        self.subE(jobElement, "LocalTexturesFile", self.LocalTexturesFile)
        for c in range(0, self.maxChannels):
            self.subE(jobElement, "ChannelFilename", self.channelFileName[c])
            self.subE(jobElement, "ChannelExtension", self.channelExtension[c])
        return True

    def writeToXMLEnd(self, f, rootElement):
        xml = ElementTree(rootElement)
        self.indent(xml.getroot())
        if f is not None:
            xml.write(f)
            f.close()
        else:
            print("No valid file has been passed to the function")
            try:
                f.close()
            except:
                pass
            return False
        return True

##############################################
# Global Functions                           #
##############################################


def getRR_Root():
    if 'RR_ROOT' in os.environ:
        return os.environ['RR_ROOT']
    HCPath = "%"
    if ((sys.platform.lower() == "win32") or
            (sys.platform.lower() == "win64")):
        HCPath = "\\\\storb\\diskb\\RoyalRender"
    elif (sys.platform.lower() == "darwin"):
        HCPath = "%RRLocationMac%"
    else:
        HCPath = "%RRLocationLx%"
    if HCPath[0] != "%":
        return HCPath
    writeError("This plugin was not installed via rrWorkstationInstaller!")


def getNewTempFileName():
    random.seed()
    if ((sys.platform.lower() == "win32") or
            (sys.platform.lower() == "win64")):
        if 'TEMP' in os.environ:
            name = os.environ['TEMP']
        else:
            name = os.environ['TMP']
        name += "\\"
    else:
        name = "/tmp/"
    name += "rrSubmitNuke_"
    name += str(random.randrange(1000, 10000, 1))
    name += ".xml"
    return name


def getRRSubmitterPath(commandLine=False):
    ''' returns the rrSubmitter filename '''
    rrRoot = getRR_Root()
    if commandLine is True:
        rrSubmitter = rrRoot+"\\bin\\win\\rrSubmitterconsole.exe"
    elif ((sys.platform.lower() == "win32") or
            (sys.platform.lower() == "win64")):
        rrSubmitter = rrRoot+"\\win__rrSubmitter.bat"
    elif (sys.platform.lower() == "darwin"):
        rrSubmitter = rrRoot+"/bin/mac/rrSubmitter.app/Contents/"
        rrSubmitter += "MacOS/rrSubmitter"
    else:
        rrSubmitter = rrRoot+"/lx__rrSubmitter.sh"
    return rrSubmitter


def getOSString():
    if ((sys.platform.lower() == "win32") or
            (sys.platform.lower() == "win64")):
        return "win"
    elif (sys.platform.lower() == "darwin"):
        return "osx"
    else:
        return "lx"


def submitJobsToRR(jobList, submitOptions, commandLine=False):
    tmpFileName = getNewTempFileName()
    tmpFile = open(tmpFileName, "w")
    xmlObj = jobList[0].writeToXMLstart(submitOptions)
    for submitjob in jobList:
        submitjob.writeToXMLJob(xmlObj)
    ret = jobList[0].writeToXMLEnd(tmpFile, xmlObj)
    if ret:
        writeInfo("Job written to " + tmpFile.name)
    else:
        writeError("Error - There was a problem writing the job file to " +
                   tmpFile.name)
    os.system(getRRSubmitterPath(commandLine)+"  \""+tmpFileName+"\"")


###########################################
# Read Nuke file                          #
###########################################

def disableWrite(node):
    """Desactive les node write autre que celui qui est selectionne"""

    writes = list()
    # creer une list des write customs
    for write in nuke.allNodes('Write'):
        for knob in write.knobs():
            if knob == 'order':
                writes.append(write)
                break
        else:
            if not write['disable'].value():
                write['disable'].setValue(1)
                writeDisabled.append(write)

    for write in nuke.allNodes('DeepWrite'):
        for knob in write.knobs():
            if knob == 'order':
                writes.append(write)
                break
        else:
            if not write['disable'].value():
                write['disable'].setValue(1)
                writeDisabled.append(write)

    for listWrite in writes:
        if listWrite != node and not listWrite['order'].value():
            if listWrite['disable'].setValue(1):
                writeDisabled.append(listWrite)
            listWrite['disable'].setValue(1)
        else:
            listOrder = listWrite['render_order'].value()
            nodeOrder = node['render_order'].value()
            if listOrder and listOrder > nodeOrder:
                if listWrite['disable'].setValue(1):
                    writeDisabled.append(listWrite)
                listWrite['disable'].setValue(1)
            else:
                if not listWrite['disable'].value():
                    listWrite['disable'].setValue(0)


def rrSubmit_fillGlobalSceneInfo(newJob):
    newJob.version = nuke.NUKE_VERSION_STRING
    newJob.software = "Nuke"
    newJob.sceneOS = getOSString()
    newJob.sceneName = nuke.root().name()
    newJob.seqStart = nuke.root().firstFrame()
    newJob.seqEnd = nuke.root().lastFrame()
    newJob.imageFileName = ""


def rrSubmit_CreateAllJob(jobList, noLocalSceneCopy, readList):
    newJob = rrJob()
    rrSubmit_fillGlobalSceneInfo(newJob)
    n = nuke.allNodes('Write')
    mainNode = True
    for writeNode in n:
        if (writeNode['disable'].value()):
            continue
        pathScripted = writeNode['file'].value()
        if ((pathScripted.lower().find("root.name") >= 0) or
                (pathScripted.lower().find("root().name") >= 0)):
            noLocalSceneCopy[0] = True
        if (mainNode):
            if (writeNode['use_limit'].value()):
                newJob.seqStart = writeNode['first'].value()
                newJob.seqEnd = writeNode['last'].value()
            newJob.imageFileName = nuke.filename(writeNode)
            mainNode = False
        else:
            newJob.maxChannels = newJob.maxChannels + 1
            newJob.channelFileName.append(string.replace(string.replace(nuke.filename(writeNode),"%v","l"),"%V","left"))
            newJob.channelExtension.append("")
    if ((newJob.imageFileName.find("%V") >= 0) or
            (newJob.imageFileName.find("%v") >= 0)):
        newJob.maxChannels = newJob.maxChannels + 1
        newJob.channelFileName.append(string.replace(string.replace(newJob.imageFileName,"%v","l"),"%V","left"))
        newJob.channelExtension.append("")
        newJob.imageFileName = string.replace(string.replace(newJob.imageFileName,"%v","r"),"%V","right")
    newJob.layer = str()
    for n in readList:
        newJob.layer = newJob.layer+' '+n.name()
    newJob.isActive = True
    jobList.append(newJob)


def rrSubmit_CreateSingleJobs(jobList):
    n = nuke.allNodes('Write')
    for i in n:
        if (i['disable'].value()):
            continue
        newJob = rrJob()
        rrSubmit_fillGlobalSceneInfo(newJob)
        if (i['use_limit'].value()):
            newJob.seqStart = i['first'].value()
            newJob.seqEnd = i['last'].value()
        newJob.imageFileName = nuke.filename(i)
        if ((newJob.imageFileName.find("%V") >= 0) or
                (newJob.imageFileName.find("%v") >= 0)):
            newJob.maxChannels = newJob.maxChannels + 1
            newJob.channelFileName.append(string.replace(string.replace(newJob.imageFileName,"%v","l"),"%V","left"))
            newJob.channelExtension.append("")
            newJob.imageFileName = string.replace(string.replace(newJob.imageFileName,"%v","r"),"%V","right")
        newJob.layer = i['name'].value()
        newJob.isActive = False
        jobList.append(newJob)


def rrSubmit_CreateSelectedJobs(node, jobList):
    if node['disable'].value():
        writeError("please enable the Write node")
        return

    newJob = rrJob()
    rrSubmit_fillGlobalSceneInfo(newJob)

    #if node.knob('renderUseful').value():
    #    newJob.sceneName = newJob.sceneName.replace('.nk', '_lite.nk')

    if (node['use_limit'].value()):
        newJob.seqStart = node['first'].value()
        newJob.seqEnd = node['last'].value()
    newJob.imageFileName = nuke.filename(node)
    if ((newJob.imageFileName.find("%V") >= 0) or
            (newJob.imageFileName.find("%v") >= 0)):
        newJob.maxChannels = newJob.maxChannels + 1
        newJob.channelFileName = list()
        newJob.channelFileName.append(string.replace(string.replace(newJob.imageFileName,"%v","l"),"%V","left"))

        newJob.channelExtension.append("")
        newJob.imageFileName = string.replace(string.replace(newJob.imageFileName,
                                                             "%v", "r"),
                                              "%V", "right")
        # newJob.imageDir=os.path.dirname(newJob.imageFileName)
    newJob.layer = node['name'].value()
    newJob.isActive = False
    jobList.append(newJob)


# to launch from button rrSubmit_Nuke_5(nuke.thisNode())
def rrSubmit_Nuke_5(node=None, order=False, metadata=dict(), commandLine=False,
                    submitterParameterOptions={}):
    writeInfo("rrSubmit v 6.01.70")

    for nodeToDeslect in nuke.allNodes():
        nodeToDeslect.setSelected(False)
#   nuke.scriptSave()
    compName = os.path.basename(nuke.root().name())
    dirName = os.path.dirname(nuke.root().name())
#    if ((CompName==None) or (len(CompName)==0)):  modified to fit my needs
    if ((compName == 'Root') or (len(compName) == 0)):
        writeError("please save comp first")
        return
    try:
        # create a render name with added _rr and the date
        # so it's unique and different from the current working comp
        if node:
            name = os.path.basename(node['file'].value())
            name = name.replace('%v', '').replace('%V', '').split('.')[0]

            RenderName = os.path.dirname(nuke.filename(node)) + "/rr/" + name +"_rr"+time.strftime('%y%m%d-%H%M%S',time.localtime())+".nk"
        else:
            RenderName = os.path.join(os.path.join(dirName, "rr"),
                                      (compName.split(".nk")[0])+"_rr"+time.strftime('%y%m%d-%H%M%S',time.localtime())+".nk")

        if not os.path.exists(os.path.dirname(RenderName)):
            os.mkdir(os.path.dirname(RenderName))

        #if node.knob('renderUseful').value():
        #    saveNode = node.name()
            # Save temporarily before adding nodes
            # to recover this version at the end
        #    nuke.scriptSaveAs(RenderName.replace('.', '_temp.'))

        # ajoute le script en metadata
        '''
        node.input(0).setSelected(True)
        metaKeys = list()
        if node.knob('file').value().endswith('.exr'):
            meta = nuke.createNode("ModifyMetaData",
                                   "metadata {{set exr/nuke/input/project %s}}" % (RenderName))
            # ajoute les metadata de project
            metaKeys.append('{set exr/nuke/input/project "%s"}' % (RenderName))
        else:
            meta = nuke.createNode("ModifyMetaData",
                                   "metadata {{set input/project %s}}" % (RenderName))
            # ajoute les metadata de project
            metaKeys.append('{set input/project "%s"}' % (RenderName))

        for m in metadata.keys():
            metaKeys.append('{set %s "%s"}' % (m, metadata[m]))
        meta['metadata'].fromScript("\n".join(metaKeys))

        # ajoute le script en metadata
        node.input(0).setSelected(True)
        timecode = nuke.createNode('AddTimeCode')
        timecode['metafps'].setValue(False)
        timecode['useFrame'].setValue(False)
        '''

        '''
        #projectName = session.getContext().getProjectName()

        #projectFps = getdata_.getProjectFps(projectName)  # TODO use filePath
        #if projectFps is not None:
        #    timecode['fps'].setValue(projectFps)
        #else:
        timecode['fps'].setValue(24)

        #projectStartCode = getdata_.getProjectStartCode(projectName)  # TODO use filePath
        #timecode['startcode'].setValue(projectStartCode)

        #startFrame = getdata_.getStartFrame(projectName, node['file'].value())
        #if startFrame is not None:
        #    timecode['frame'].setValue(startFrame)
        #    timecode['useFrame'].setValue(True)
        #else:
        timecode['frame'].setValue(int(nuke.root()['first_frame'].value()))
        '''

        # disable la lut
        viewerProcessDict = dict()
        for viewerNode in nuke.allNodes('Viewer'):
            colorspace = viewerNode['viewerProcess'].value()
            viewerProcessDict[viewerNode] = colorspace
            viewerNode['viewerProcess'].setValue(0)

        # desactive les writes dispensables
        rrSubmit_Nuke_5.writeDisabled = list()
        disableWrite(node)
        node['disable'].setValue(0)

        # desactive les reading de write
        listRead = list()
        reading = list()

        if order:
            for n in nuke.allNodes("Write"):
                if not n['disable'].value():
                    listRead.append(n)
                    if n['reading'].value():
                        n['reading'].setValue(0)
                        reading.append(n)

        # add ouput node
        '''
        outputNode = nuke.nodes.Output()
        outputNode.setInput(0, node)
        outputNode.setXYpos(node.xpos(), node.ypos()+150)
        '''

        # save and submit with the render name
        if not os.path.exists(os.path.dirname(RenderName)):
            os.makedirs(os.path.dirname(RenderName))
        nuke.scriptSaveAs(RenderName)

        jobList = []
        noLocalSceneCopy = [False]
        if order:
            rrSubmit_CreateAllJob(jobList, noLocalSceneCopy, listRead)
            # rrSubmit_CreateSingleJobs(jobList)
        else:
            rrSubmit_CreateSelectedJobs(node, jobList)

        submitOptions = ""
        if (noLocalSceneCopy[0]):
            submitOptions = "AllowLocalSceneCopy=0~0"
        #if node['presets'].value() == 'colormatch':
        #    submitOptions += ' PPcolormatchMakeQT24=1~1'
        #    submitOptions += ' PPcopyQTtodeliveryfol=1~1'
        #    submitOptions += ' PPCopyftrackQTtodeliv=1~1 '

        for key in submitterParameterOptions.keys():
            submitOptions += ' ' + key + '='
            submitOptions += submitterParameterOptions[key] + ' '

        print "submitOptions : ", submitOptions

        if jobList != []:
            submitJobsToRR(jobList, submitOptions, commandLine)

        # generate the "lite" file
        for noToDisable in nuke.allNodes():
            noToDisable.setSelected(False)

        #from cgev.nuke.tools.nodes import operations

        #operations.selectDependencies(outputNode)
        #operations.selectRelatedBackdrops(nuke.selectedNodes())

        '''
        if node.knob('renderUseful').value():
            # New script to save lite comp
            nuke.invertSelection()
            for node in nuke.selectedNodes():
                nuke.delete(node)

            nuke.scriptSaveAs(RenderName.replace('.', '_lite.'))

            for node in nuke.allNodes():
                nuke.delete(node)

            nuke.nodePaste(RenderName.replace('.', '_temp.'))
            os.remove(RenderName.replace('.', '_temp.'))
            nuke.invertSelection()
            nuke.toNode(saveNode).setSelected(True)
            nuke.zoomToFitSelected()
            nuke.selectedNode().setSelected(False)
        else:
            # Here is a way to save root node in the comp so that there is
            # No problem when trying to batch lite comp
            nuke.nodeCopy(RenderName.replace('.', '_lite.'))
            r = nuke.Root()
            rootLines = []
            fileLines = []
            path = RenderName.replace('.', '_lite.')
            wantedKnobs = ('inputs', 'name', 'first_frame', 'last_frame',
                           'format', 'proxy_type', 'proxy_format')

            rootLines.append('Root {\n')
            for k, v in r.knobs().iteritems():
                if k in wantedKnobs:
                    if k in ['format', 'proxy_format']:
                        rootLines.append(k + ' "' + r[k].toScript() + '"\n')
                    else:
                        rootLines.append(k + ' ' + r[k].toScript() + '\n')
            rootLines.append('}\n')

            with open(path) as f:
                fileLines = f.readlines()

            with open(path, 'w') as f:
                for line in rootLines:
                    f.write(line)

                for line in fileLines:
                    f.write(line)

            # supprime le node de metadata et le output
            nuke.delete(meta)
            nuke.delete(timecode)
            nuke.delete(outputNode)

            # retabli la lut
            for viewer in viewerProcessDict:
                viewer['viewerProcess'].setValue(viewerProcessDict[viewer])

            # reactive les reading
            if order:
                for n in reading:
                    n['reading'].setValue(1)

            # reactive les write
            for n in writeDisabled:
                n['disable'].setValue(0)

            # deselect Nodes
            for noToDisable in nuke.allNodes():
                noToDisable.setSelected(False)
        '''
    except:
        nuke.scriptSaveAs(filename=os.path.join(dirName, compName),
                          overwrite=1)
        raise
    # save back with original name so the artist can continue on working
    # with previous name with no risk
    nuke.scriptSaveAs(filename=os.path.join(dirName, compName), overwrite=1)
