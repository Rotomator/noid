# -*- coding: cp1252 -*-
######################################################################
#
# Royal Render Plugin script for Maya
# Author:  Royal Render, Holger Schoenberger, Binary Alchemy
# Last change: v 6.02.01
# Copyright (c) 2009-2010 Holger Schoenberger - Binary Alchemy
# rrInstall_Env: MAYA_PLUG_IN_PATH, Directory
#
######################################################################

import platform
import random
import os
import sys
import types
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import maya.mel
import maya.utils as mu
import copy



#Classes:
# rrDelightRenderPass
#    if 3delight is used for rendering, as 3delight has its own passes
# rrMayaLayer
#    get and hold all information about maya layer
# rrSceneInfo
#    basic information about the scene
# rrPlugin
#    the main class that is called. the funciton doIt is the main function executed
#
#
#

def rrWriteLog(msg):
        UIMode=True
        try:
            maya.mel.eval('global string $gMainWindow;')
            maya.mel.eval('setParent $gMainWindow;')
        except:
            UIMode=False
        if (UIMode):
            cmds.confirmDialog(message=msg, button=['Abort'])
        else:
            print (msg)

class rrDelightRenderPass:
    def __init__(self):
        self.name = ''
        self.camera =''
        self.seqStart = 1
        self.seqEnd = 100
        self.seqStep=1
        self.imageWidth=100
        self.imageHeight=100
        self.imageFileName=""
        self.imageFramePadding=1
        self.imageDir=""
        self.imageExtension=""
        self.imagePreNumberLetter=""
        self.ImageSingleOutputFile=False
        self.tmpId = 0
        self.channelFilenames = []
        self.channelExts = []
        self.requiredPlugins = "_3delight;"
        self.renderer = "_3delight"
        self.shortcodeAttrs = {'<ext>':self.getExtension,
                               '<scene>':self.getScene,
                               '<layer>':self.getLayer,
                               '<project>':self.getProject,
                               '<pass>':self.getPass,
                               '<camera>':self.getCamera,
                               '<output_variable>':self.getVariable
                               }

    def getProject(self):
        return cmds.workspace(q=True,fn=True)

    def getVariable(self):
        return cmds.getAttr(self.name+'.displayOutputVariables['+str(self.tmpId)+']')

    def getCamera(self):
        return self.camera

    def getPass(self):
        return self.name

    def getExtension(self):
        return cmds.getAttr(self.name+'.displayDrivers['+str(self.tmpId)+']')

    def getScene(self):
        return cmds.file(q=True,sn=True,shn=True).split('.')[0]

    def getLayer(self):
        current = cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True )
        if current == "defaultRenderLayer":
            return "masterLayer"
        return current

    def getPassSettings(self,dpass):
        self.name = dpass
        if not self.findConnections(self.camera, dpass+'.camera'):
            print ('No camera selected in Pass: '+dpass+'!')

        if cmds.getAttr(dpass+'.animation') == 0:
            print ('Animation checkbox is not on for pass: '+dpass+'!')

        #CONVERT TO INTS
        self.seqStart = int(cmds.getAttr(dpass+'.startFrame'))
        self.seqEnd = int(cmds.getAttr(dpass+'.endFrame'))
        self.seqStep = int(cmds.getAttr(dpass+'.increment'))

        res = cmds.getAttr(dpass+'.resolution')
        self.imageWidth = res[0][0]
        self.imageHeight = res[0][1]

        if not self.getRenderable(dpass):
            rrWriteLog('No Renderable Displays!')
            return False

#        get channels

        return True


    def findConnections(self,setting,plug):
        tmp = cmds.listConnections(plug,sh=True)
        if (tmp == None):
            return False
        if (len(tmp) == 0):
            return False
        setting = tmp[0]
        return True

    #EVAL SHORTCODES
    def evalShortcodes(self,path,variable):
        #replace short codes
        for k,v in self.shortcodeAttrs.iteritems():
            path = path.replace(k,v())

        #replace env vars
        for k,v in os.environ.iteritems():
            path = path.replace('${'+k+'}',v)

        path = path.replace("<aov>",variable)

        paths = os.path.split(path)
        self.imageDir = paths[0]
        if paths[1] == '':
            rrWriteLog('Needs Image Filename!')
            return False


        tokens = paths[1].split('.')
        tokens.append(paths[0])
        return tokens


    def getRenderable(self,dpass):
        #print("get renderable")
        ImageperiodInExt= cmds.getAttr('defaultRenderGlobals.periodInExt')
        max = cmds.getAttr(dpass+'.displayRenderables',s=True)
        primary = True
        for i in range(0,max):
            self.tmpId = i
            if cmds.getAttr(dpass+'.displayRenderables['+str(i)+']') == 1:
                path = cmds.getAttr(dpass+'.displayFilenames['+str(i)+']')
                variable = cmds.getAttr(dpass+'.displayOutputVariables['+str(i)+']')
                variable= variable.replace("color aov_","")
                tokens = self.evalShortcodes(path,variable)

                if primary:
                    self.imageExtension = '.'+tokens[-2]
                    self.imageFileName = tokens[0]
                    if ((self.imageFileName[len(self.imageFileName)-1]) == '#'):
                        self.imageFileName= self.imageFileName[:len(self.imageFileName)-1]
                    primary = False
                else:
                    channelFile=tokens[-1]+os.sep+tokens[0];
                    if ((channelFile[len(channelFile)-1]) == '#'):
                        channelFile= channelFile[:len(channelFile)-1]
                    self.channelFilenames.append(channelFile)
                    self.channelExts.append('.'+tokens[-2])

        if primary:
            return False

        return True


    def __str__(self):
        return ' '.join(['Image Dir',self.imageDir,'Image Extension',self.imageExtension,'Image File',self.imageFileName])




class rrMayaLayer:
    def __init__(self):
        self.name=""
        self.camera=""
        self.renderer=""
        self.requiredPlugins=""
        self.IsActive=False
        self.seqStart=1
        self.seqEnd=100
        self.seqStep=1
        self.seqFileOffset=0
        self.imageWidth=100
        self.imageHeight=100
        self.imageFileName=""
        self.imageFramePadding=1
        self.imageDir=""
        self.imageExtension=""
        self.imagePreNumberLetter=""
        self.ImageSingleOutputFile=False
        self.channelName=""
        self.maxChannels=0
        self.channelFileName=[]
        self.channelExtension=[]
        self.tempModifyExtension=False
        self.tempModifyByframe=1.0
        self.tempModifyStart=1
        self.tempImageFormat=1
        self.tempImfKeyPlugin=""
        self.tempImageExtension="unknown"
        self.tempImageFilePrefix="unknown"
        self.tempExtensionPadding=1
        self.tempVersionTag=""
        self.tempIsGI=False
        self.tempIsGI2=False
        self.tempGIFileName=""
        self.tempCamNames = []
        self.tempCamRenderable = []
        return


    def GetSceneFps(self):
        FpsName= cmds.currentUnit(query=True, time=True)
        if (FpsName=="game"):
            return 15.0
        elif (FpsName=="film"):
            return 24.0
        elif (FpsName=="pal"):
            return 25.0
        elif (FpsName=="ntsc"):
            return 30.0
        elif (FpsName=="show"):
            return 48.0
        elif (FpsName=="palf"):
            return 50.0
        elif (FpsName=="ntscf"):
            return 60.0
        elif (FpsName=="millisec"):
            return 1000.0
        elif (FpsName=="sec"):
            return 1.0
        elif (FpsName=="min"):
            return (1.0/60.0)
        elif (FpsName=="hour"):
            return (1.0/60.0/60.0)
        elif (FpsName=="2fps"):
            return 2.0
        elif (FpsName=="3fps"):
            return 3.0
        elif (FpsName=="4fps"):
            return 4.0
        elif (FpsName=="5fps"):
            return 5.0
        elif (FpsName=="6fps"):
            return 6.0
        elif (FpsName=="8fps"):
            return 8.0
        elif (FpsName=="10fps"):
            return 10.0
        elif (FpsName=="12fps"):
            return 12.0
        elif (FpsName=="16fps"):
            return 16.0
        elif (FpsName=="20fps"):
            return 20.0
        elif (FpsName=="40fps"):
            return 40.0
        elif (FpsName=="75fps"):
            return 75.0
        elif (FpsName=="80fps"):
            return 80.0
        elif (FpsName=="100fps"):
            return 100.0
        elif (FpsName=="120fps"):
            return 120.0
        elif (FpsName=="125fps"):
            return 125.0
        elif (FpsName=="150fps"):
            return 150.0
        elif (FpsName=="200fps"):
            return 200.0
        elif (FpsName=="240fps"):
            return 240.0
        elif (FpsName=="250fps"):
            return 250.0
        elif (FpsName=="300fps"):
            return 300.0
        elif (FpsName=="375fps"):
            return 375.0
        elif (FpsName=="400fps"):
            return 400.0
        elif (FpsName=="500fps"):
            return 500.0
        elif (FpsName=="600fps"):
            return 600.0
        elif (FpsName=="750fps"):
            return 750.0
        elif (FpsName=="1200fps"):
            return 1200.0
        elif (FpsName=="1500fps"):
            return 1500.0
        elif (FpsName=="2000fps"):
            return 2000.0
        elif (FpsName=="3000fps"):
            return 3000.0
        elif (FpsName=="6000fps"):
            return 6000.0
        else:
            return 25.0

    def CalcImageExtension(self):
        if (self.renderer=="renderMan"):
            rmanImages = maya.mel.eval('rman getPrefAsArray ImageFormatQuantizationTable;')
            for img in range(1, len(rmanImages)-1):
                if (rmanImages[img]==self.tempImfKeyPlugin):
                    self.tempImageExtension= rmanImages[img-1]
                    if (self.tempImageExtension.find("(")>=0):
                        self.tempImageExtension=self.tempImageExtension[self.tempImageExtension.find("(")+1:]
                        if (self.tempImageExtension.find(")")>=0):
                            self.tempImageExtension=self.tempImageExtension[:self.tempImageExtension.find("(")]
                            return
            self.tempImageExtension=".unknown"
            return

        #MRay, Maya Software, maxwell, arnold:
        if (self.tempImageFormat== 60):
            self.tempImageExtension="swf"
        elif (self.tempImageFormat== 61):
            self.tempImageExtension="ai"
        elif (self.tempImageFormat== 62):
            self.tempImageExtension="svg"
        elif (self.tempImageFormat== 63):
            self.tempImageExtension="swft"
        elif (self.tempImageFormat== 50):
            mayaimfPlugInExt = maya.mel.eval('$rrTempimfPlugInExt = $imfPlugInExt;')
            mayaimfPlugInKey = maya.mel.eval('$rrTempimfPlugInKey = $imfPlugInKey;')
            for i in range(0, len(mayaimfPlugInKey)):
                if (mayaimfPlugInKey[i]==self.tempImfKeyPlugin):
                    self.tempImageExtension=mayaimfPlugInKey[i]
        elif (self.tempImageFormat== 51):
            self.tempImageExtension=self.tempImfKeyPlugin
        else:
            try:
                mayaImgExt = maya.mel.eval('$rrTempimgExt = $imgExt;')
                if (len(mayaImgExt)==0):
                    maya.mel.eval('createImageFormats()')
                    mayaImgExt = maya.mel.eval('$rrTempimgExt2 = $imgExt;')
            except:
                maya.mel.eval('createImageFormats()')
                mayaImgExt = maya.mel.eval('$rrTempimgExt2 = $imgExt;')
            self.tempImageExtension = mayaImgExt[self.tempImageFormat]
        if (self.renderer=="mentalRay"):
            if (self.tempImageExtension=="sgi"):
                self.tempImageExtension="rgb"
            if (self.tempImageExtension=="tifu"):
                self.tempImageExtension="tif"
            if (self.tempImageExtension=="qntntsc"):
                self.tempImageExtension="yuv"
            if (self.tempImageExtension=="qntpal"):
                self.tempImageExtension="yuv"
        if (self.tempImageExtension=="jpeg"):
            self.tempImageExtension="jpg"
        if (self.renderer=="maxwell"):
            if (self.tempImageFormat== 31):
                self.tempImageExtension="exr"
            elif (self.tempImageFormat== 35):
                self.tempImageExtension="hdr"
            elif (self.tempImageFormat== 36):
                self.tempImageExtension="jp2"
        if (self.renderer=="arnold"):
            if (self.tempImageExtension=="jpg"):
                self.tempImageExtension="jpeg"
        if (self.renderer=="_3delight"):
            if (self.tempImageExtension=="tiff"):
                self.tempImageExtension="tif"


    # gather all information from a layer
    def getLayerSettings(self,Layer,DatabaseDir,SceneName,MayaVersion,isLayerRendering):
        #print ("rrSubmit - getLayerSettings '"+ Layer +"'")
        self.tempVersionTag = cmds.getAttr('defaultRenderGlobals.renderVersion')
        if ((self.tempVersionTag==None) or (len(self.tempVersionTag)==0)):
            self.tempVersionTag=""
        CurrentLayer=cmds.editRenderLayerGlobals( query=True, currentRenderLayer=True )
        LayerOverrides=cmds.listConnections( Layer+".adjustments", p=True, c=True)
        LayerOverridesMaster=cmds.listConnections( "defaultRenderLayer.adjustments", p=True, c=True)

        self.renderer= cmds.getAttr('defaultRenderGlobals.currentRenderer')
        if (CurrentLayer!=Layer):
            if ( (not (LayerOverridesMaster==None) ) and (len(LayerOverridesMaster)>1)):
                for o in range(0, len(LayerOverridesMaster) /2  ):
                    OWhat=LayerOverridesMaster[o*2+1]
                    LayerOverridesMaster[o*2]=LayerOverridesMaster[o*2].replace(".plug",".value")
                    OValue=cmds.getAttr(LayerOverridesMaster[o*2])
                    if (OWhat=="defaultRenderGlobals.currentRenderer"):
                        self.renderer= OValue
            if ( (not (LayerOverrides==None) ) and (len(LayerOverrides)>1)):
                for o in range(0, len(LayerOverrides) /2  ):
                    OWhat=LayerOverrides[o*2+1]
                    LayerOverrides[o*2]=LayerOverrides[o*2].replace(".plug",".value")
                    OValue=cmds.getAttr(LayerOverrides[o*2])
                    if (OWhat=="defaultRenderGlobals.currentRenderer"):
                        self.renderer= OValue
        if (self.renderer!="mayaSoftware"):
            self.requiredPlugins=self.renderer+";"

        cameraList=cmds.ls(ca=True)
        nbRenderableCams=0
        for cam in cameraList:
            self.tempCamNames.append(cam);
            if (cmds.getAttr(cam+'.renderable')):
                self.tempCamRenderable.append(True)
                nbRenderableCams=nbRenderableCams+1
            else:
                self.tempCamRenderable.append(False)


        #VRAY only:
        if (self.renderer=="vray"):
            vrayVersion=cmds.pluginInfo( 'vrayformaya', query=True, version=True )
            isVRay20=(vrayVersion.find("2.")==0)
            isVRay30=(vrayVersion.find("3.")==0)
            self.imageWidth= int(cmds.getAttr('vraySettings.width'))
            self.imageHeight= int(cmds.getAttr('vraySettings.height'))
            self.imageFramePadding=cmds.getAttr('vraySettings.fileNamePadding')
            self.imageFileName=cmds.getAttr('vraySettings.fileNamePrefix')
            self.imageExtension=cmds.getAttr('vraySettings.imageFormatStr')
            self.imagePreNumberLetter='.'
            self.camera=cmds.getAttr('vraySettings.batchCamera')
            isAnimation= cmds.getAttr('defaultRenderGlobals.animation')
            self.seqStart= int(cmds.getAttr('defaultRenderGlobals.startFrame'))
            self.seqEnd= int(cmds.getAttr('defaultRenderGlobals.endFrame'))
            self.seqStep= int(cmds.getAttr('defaultRenderGlobals.byFrameStep'))
            # print("start "+str(self.seqStart)+"\n")
            self.tempIsGI= cmds.getAttr('vraySettings.giOn')
            self.tempIsGI2= ( (cmds.getAttr('vraySettings.imap_mode')==6) or (cmds.getAttr('vraySettings.imap_mode')==1))
            self.tempGIFileName=cmds.getAttr('vraySettings.imap_autoSaveFile')

            self.ImageSingleOutputFile=False
            if (isAnimation!=1):
                self.ImageSingleOutputFile=True
                rrWriteLog("Still frames not allowed!\n Please use a sequence with one frame.\n Layer: "+Layer+"\n")
                return False
            if ((self.imageFileName==None) or (len(self.imageFileName)==0)):
                self.imageFileName=SceneName
                self.imageFileName=self.imageFileName.replace("\\","/")
                if (self.imageFileName.find("/")>=0):
                    splitted=self.imageFileName.split("/")
                    self.imageFileName=splitted[len(splitted)-1]
                if (self.imageFileName.find(".")>=0):
                    splitted=self.imageFileName.split(".")
                    self.imageFileName=""
                    for i in range(0, len(splitted)-2):
                        if (i>0):
                            self.imageFileName= self.imageFileName + "."
                        self.imageFileName= self.imageFileName + splitted[i]

            if (CurrentLayer!=Layer):
                if ( (not (LayerOverridesMaster==None) ) and (len(LayerOverridesMaster)>1)):
                    for o in range(0, len(LayerOverridesMaster) /2  ):
                        OWhat=LayerOverridesMaster[o*2+1]
                        LayerOverridesMaster[o*2]=LayerOverridesMaster[o*2].replace(".plug",".value")
                        OValue=cmds.getAttr(LayerOverridesMaster[o*2])

                        if (OWhat=="vraySettings.width"):
                            self.imageWidth= int(OValue)
                        elif (OWhat=="vraySettings.height"):
                            self.imageHeight= int(OValue)
                        elif (OWhat=="defaultRenderGlobals.startFrame"):
                            self.seqStart= int(OValue* self.GetSceneFps() +0.001 )
                        elif (OWhat=="defaultRenderGlobals.endFrame"):
                            self.seqEnd= int(OValue* self.GetSceneFps() +0.001 )
                        elif (OWhat=="defaultRenderGlobals.byFrameStep"):
                            self.seqStep= int(OValue* self.GetSceneFps() +0.001)
                        elif (OWhat=="vraySettings.fileNamePadding"):
                            self.imageFramePadding= int(OValue)
                        elif (OWhat=="vraySettings.fileNamePrefix"):
                            self.imageFileName=OValue
                        elif (OWhat=="vraySettings.imageFormatStr"):
                            self.imageExtension=OValue
                        elif (OWhat=="vraySettings.fileNameRenderElementSeparator"):
                            self.imagePreNumberLetter=OValue
                        elif (OWhat=="vraySettings.batchCamera"):
                            self.camera=OValue
                        elif (OWhat=="vraySettings.giOn"):
                            self.tempIsGI=OValue
                        elif (OWhat=="vraySettings.imap_mode"):
                            self.tempIsGI2=((int(OValue)==6) or (int(OValue)==1))
                        elif (OWhat=="vraySettings.imap_autoSaveFile"):
                            self.tempGIFileName=OValue
                if ( (not (LayerOverrides==None) ) and (len(LayerOverrides)>1)):
                    for o in range(0, len(LayerOverrides) /2  ):
                        OWhat=LayerOverrides[o*2+1]
                        LayerOverrides[o*2]=LayerOverrides[o*2].replace(".plug",".value")
                        OValue=cmds.getAttr(LayerOverrides[o*2])

                        if (OWhat=="vraySettings.width"):
                            self.imageWidth= int(OValue)
                        elif (OWhat=="vraySettings.height"):
                            self.imageHeight= int(OValue)
                        elif (OWhat=="defaultRenderGlobals.startFrame"):
                            self.seqStart= int(OValue* self.GetSceneFps() +0.001 )
                        elif (OWhat=="defaultRenderGlobals.endFrame"):
                            self.seqEnd= int(OValue* self.GetSceneFps() +0.001 )
                        elif (OWhat=="defaultRenderGlobals.byFrameStep"):
                            self.seqStep= int(OValue* self.GetSceneFps() +0.001)
                        elif (OWhat=="vraySettings.fileNamePadding"):
                            self.imageFramePadding= int(OValue)
                        elif (OWhat=="vraySettings.fileNamePrefix"):
                            self.imageFileName=OValue
                        elif (OWhat=="vraySettings.imageFormatStr"):
                            self.imageExtension=OValue
                        elif (OWhat=="vraySettings.fileNameRenderElementSeparator"):
                            self.imagePreNumberLetter=OValue
                        elif (OWhat=="vraySettings.batchCamera"):
                            self.camera=OValue
                        elif (OWhat=="vraySettings.giOn"):
                            self.tempIsGI=OValue
                        elif (OWhat=="vraySettings.imap_mode"):
                            self.tempIsGI2=((int(OValue)==6) or (int(OValue)==1))
                        elif (OWhat=="vraySettings.imap_autoSaveFile"):
                            self.tempGIFileName=OValue

            if ((self.imageExtension==None) or (len(self.imageExtension)==0)):
                self.imageExtension="png"
            self.imageExtension= "."+ self.imageExtension
            if ((self.imageExtension==".exr (multichannel)")):
                self.imageExtension=".exr"
                self.imagePreNumberLetter="."
            if ((self.imageExtension==".exr (deep)")):
                self.imageExtension=".exr"
            if ((self.camera==None) or (len(self.camera)==0)):
                self.camera=""
            if ((self.tempIsGI) and (self.tempIsGI2)):
                self.imageFileName=self.tempGIFileName
                self.imageExtension=""
                self.imagePreNumberLetter=""
                self.renderer="vray_prepass"
                if ((self.imageFileName==None) or (len(self.imageFileName)==0)):
                    rrWriteLog("No Vray Irradiancee Map File set.\n(Change mode to 'Animation(render)', set the filename, change mode back)\n Layer: "+Layer+"\n")
                    return False
                if (self.imageFileName.lower().find(".vrmap")>=0):
                    splitted=self.imageFileName.split(".vrmap")
                    self.imageFileName=splitted[0]
                    self.imageExtension=".vrmap"

            if (isVRay20) or (isVRay30) :
                print("vray 2.0 or 3.0")
                for c in range(0, len(self.tempCamRenderable)):
                    if (self.tempCamRenderable[c]):
                        transformNode = cmds.listRelatives(self.tempCamNames[c],parent=True)
                        transformNode=transformNode[0]
                        self.camera=transformNode


                if (nbRenderableCams>1):
                    for c in range(0, len(self.tempCamRenderable)):
                        if (self.tempCamRenderable[c]):
                            nbRenderableCams=nbRenderableCams+1
                            transformNode = cmds.listRelatives(self.tempCamNames[c],parent=True)
                            transformNode=transformNode[0]
                            if (self.camera!=transformNode):
                                self.channelFileName.append(self.imageFileName.replace('<Camera>',transformNode))
                                self.channelExtension.append(self.imageExtension)
                                self.maxChannels +=1
                    self.camera=self.camera + " MultiCam"


            self.imageFileName=self.imageFileName.replace("%/l","<Layer>/")
            self.imageFileName=self.imageFileName.replace("%l","<Layer>")
            self.imageFileName=self.imageFileName.replace("<RenderLayer>","<Layer>")
            self.imageFileName=self.imageFileName.replace("<RenderPass>","<Channel>")
            self.imageFileName=self.imageFileName.replace("%/c","<Camera>/")
            self.imageFileName=self.imageFileName.replace("%c","<Camera>")
            self.imageFileName=self.imageFileName.replace("%/s","<SceneFile>/")
            self.imageFileName=self.imageFileName.replace("%s","<SceneFile>")
            self.imageFileName=self.imageFileName.replace("<Scene>","<SceneFile>")
            self.imageFileName=self.imageFileName.replace("<Channel>","")
            self.imageFileName=self.imageFileName.replace("%e",self.tempImageExtension)
            self.imageFileName=self.imageFileName.replace("<Extension>",self.tempImageExtension)
            self.imageFileName=self.imageFileName.replace("<Version>",self.tempVersionTag)
            self.imageFileName=self.imageFileName.replace("%v",self.tempVersionTag)
            self.imageFileName=self.imageFileName.replace("%/v",self.tempVersionTag+"/")

            if (self.renderer=="vray_prepass"):
                self.imageFileName= self.imageFileName + self.imagePreNumberLetter
                self.ImageDir=""
            else:
                if (isLayerRendering and (self.imageFileName.lower().find("<layer>")<0)):
                    self.imageFileName="<Layer>/"+self.imageFileName
		#			edit by cgev  s'il y a deja camera dans le nom, on ne le prefixe pas
                if (nbRenderableCams>1 and (self.imageFileName.lower().find("<camera>")<0)):
                    self.imageFileName="<Camera>/"+self.imageFileName
                if (len(self.imageFileName)>1):
                    self.imageFileName=self.imageFileName.replace("\\","/")
                imageFileName_nopre=self.imageFileName
                imageDirName_nopre=self.imageFileName
                posDir=self.imageFileName.find("/");
                if (posDir>0):
                    imageFileName_nopre= os.path.basename(imageFileName_nopre)
                    imageDirName_nopre= os.path.dirname(imageDirName_nopre)+ "/"
                else:
                    imageDirName_nopre="";

                self.imageFileName= self.imageFileName + self.imagePreNumberLetter

                self.ImageDir= cmds.workspace(fre="images")
                isRelative=True
                if (len(self.imageFileName)>1):
                    self.imageFileName=self.imageFileName.replace("\\","/")
                    if ((self.imageFileName[0]=="/") or (self.imageFileName[1]==":")):
                        isRelative=False
                        self.ImageDir=""
                if (isRelative):
                    if (len(self.ImageDir)>1):
                        self.ImageDir=self.ImageDir.replace("\\","/")
                        if ((self.ImageDir[0]=="/") or (self.ImageDir[1]==":")):
                            isRelative=False
                if (isRelative):
                    self.ImageDir=DatabaseDir+self.ImageDir
                    self.ImageDir+="/"
                vrayElemSeperateFolders= cmds.getAttr('vraySettings.relements_separateFolders')
                vrayElemSep= cmds.getAttr('vraySettings.fileNameRenderElementSeparator')
                vrayElements= maya.mel.eval('$rrTempExisting = vrayRenderElementsExisting();')
                for elem in vrayElements:
                    if (cmds.getAttr(elem+'.enabled')):
                        suffix=elem
                        suffix=suffix.replace(" ","")
                        suffix=suffix.replace("_","")
                        suffix=suffix.replace("-","")
                        suffix= suffix[:1].lower() + suffix[1:]
                        attribs=cmds.listAttr( elem, ud=True, a=False, s=False )
                        for attr in attribs:
                            if (attr.find("_name_")>0):
                                suffix=cmds.getAttr(elem+"." + attr)
                        if (vrayElemSeperateFolders):
                            self.channelFileName.append(imageDirName_nopre+suffix+"/"+imageFileName_nopre+vrayElemSep+suffix+self.imagePreNumberLetter)
                        else:
                            self.channelFileName.append(imageDirName_nopre+imageFileName_nopre+vrayElemSep+suffix+self.imagePreNumberLetter)
                        self.channelExtension.append(self.imageExtension)
                        self.maxChannels +=1

            if ((self.camera.find(":")>0) and (self.imageFileName.lower().find("<camera>")<0)):
                self.camera=""

            return True
            #"VRay Only" return


        #MentalRay, Maya software, hardware renderer, Renderman, Arnold, _3delight:
        attrNameImfkey="defaultRenderGlobals.imfPluginKey"
        if (self.renderer=="renderMan"):
            attrNameImfkey="rmanFinalOutputGlobals0.rman__riopt__Display_type"
        self.imageWidth= int(cmds.getAttr('defaultResolution.width'))
        self.imageHeight= int(cmds.getAttr('defaultResolution.height'))
        self.seqStart= int(cmds.getAttr('defaultRenderGlobals.startFrame'))
        self.seqEnd= int(cmds.getAttr('defaultRenderGlobals.endFrame'))
        self.seqStep= int(cmds.getAttr('defaultRenderGlobals.byFrameStep'))
        self.tempModifyExtension=(cmds.getAttr('defaultRenderGlobals.modifyExtension')==True)
        self.tempModifyStart=int(cmds.getAttr('defaultRenderGlobals.startExtension'))
        self.tempModifyByframe=cmds.getAttr('defaultRenderGlobals.byExtension')
        self.tempImageFormat=int(cmds.getAttr('defaultRenderGlobals.imageFormat'))
        self.tempImfKeyPlugin=cmds.getAttr(attrNameImfkey)
        self.tempImageFilePrefix=cmds.getAttr('defaultRenderGlobals.imageFilePrefix')
        self.tempExtensionPadding=cmds.getAttr('defaultRenderGlobals.extensionPadding')
        isAnimation= cmds.getAttr('defaultRenderGlobals.animation')
        if (isAnimation!=1):
            self.ImageSingleOutputFile=True
            rrWriteLog("Still frames not allowed!\n Please use a sequence with one frame.\n Layer: "+Layer+"\n");
            return False

        self.ImageSingleOutputFile=False
        if (CurrentLayer!=Layer):
            if ( (not (LayerOverridesMaster==None) ) and (len(LayerOverridesMaster)>1)):
                for o in range(0, len(LayerOverridesMaster) /2  ):
                    OWhat=LayerOverridesMaster[o*2+1]
                    LayerOverridesMaster[o*2]=LayerOverridesMaster[o*2].replace(".plug",".value")
                    OValue=cmds.getAttr(LayerOverridesMaster[o*2])

                    for c in range(0, len(self.tempCamNames)):
                        if (self.tempCamNames[c]+'.renderable'== OWhat):
                            if (OValue):
                                self.tempCamRenderable[c]=True
                            else:
                                self.tempCamRenderable[c]=False
                    if (OWhat=="defaultResolution.width"):
                        self.imageWidth= int(OValue)
                    elif (OWhat=="defaultResolution.height"):
                        self.imageHeight= int(OValue)
                    elif (OWhat=="defaultRenderGlobals.startFrame"):
                        self.seqStart= int(OValue* self.GetSceneFps() +0.001 )
                    elif (OWhat=="defaultRenderGlobals.endFrame"):
                        self.seqEnd= int(OValue* self.GetSceneFps() +0.001 )
                    elif (OWhat=="defaultRenderGlobals.byFrameStep"):
                        self.seqStep= int(OValue* self.GetSceneFps() +0.001)
                    elif (OWhat=="defaultRenderGlobals.modifyExtension"):
                        self.tempModifyExtension=(OValue==True)
                    elif (OWhat=="defaultRenderGlobals.startExtension"):
                        self.tempModifyStart=int(OValue)
                    elif (OWhat=="defaultRenderGlobals.byExtension"):
                        self.tempModifyByframe=OValue
                    elif (OWhat=="defaultRenderGlobals.imageFormat"):
                        self.tempImageFormat=int(OValue)
                    elif (OWhat==attrNameImfkey):
                        self.tempImfKeyPlugin=OValue
                    elif (OWhat=="defaultRenderGlobals.imageFilePrefix"):
                        self.tempImageFilePrefix=OValue
                    elif (OWhat=="defaultRenderGlobals.extensionPadding"):
                        self.tempExtensionPadding=OValue
            if ( (not (LayerOverrides==None) ) and (len(LayerOverrides)>1)):
                for o in range(0, len(LayerOverrides) /2  ):
                    OWhat=LayerOverrides[o*2+1]
                    LayerOverrides[o*2]=LayerOverrides[o*2].replace(".plug",".value")
                    OValue=cmds.getAttr(LayerOverrides[o*2])

                    for c in range(0, len(self.tempCamNames)):
                        if (self.tempCamNames[c]+'.renderable'== OWhat):
                            if (OValue):
                                self.tempCamRenderable[c]=True
                            else:
                                self.tempCamRenderable[c]=False
                    if (OWhat=="defaultResolution.width"):
                        self.imageWidth= int(OValue)
                    elif (OWhat=="defaultResolution.height"):
                        self.imageHeight= int(OValue)
                    elif (OWhat=="defaultRenderGlobals.startFrame"):
                        self.seqStart= int(OValue* self.GetSceneFps() +0.001)
                    elif (OWhat=="defaultRenderGlobals.endFrame"):
                        self.seqEnd= int(OValue* self.GetSceneFps() +0.001)
                    elif (OWhat=="defaultRenderGlobals.byFrameStep"):
                        self.seqStep= int(OValue* self.GetSceneFps() +0.001)
                    elif (OWhat=="defaultRenderGlobals.modifyExtension"):
                        self.tempModifyExtension=(OValue==True)
                    elif (OWhat=="defaultRenderGlobals.startExtension"):
                        self.tempModifyStart=int(OValue)
                    elif (OWhat=="defaultRenderGlobals.byExtension"):
                        self.tempModifyByframe=OValue
                    elif (OWhat=="defaultRenderGlobals.imageFormat"):
                        self.tempImageFormat=int(OValue)
                    elif (OWhat==attrNameImfkey):
                        self.tempImfKeyPlugin=OValue
                    elif (OWhat=="defaultRenderGlobals.imageFilePrefix"):
                        self.tempImageFilePrefix=OValue
                    elif (OWhat=="defaultRenderGlobals.extensionPadding"):
                        self.tempExtensionPadding=OValue

        for c in range(0, len(self.tempCamRenderable)):
            if (self.tempCamRenderable[c]):
                transformNode = cmds.listRelatives(self.tempCamNames[c],parent=True)
                transformNode=transformNode[0]
                if (self.renderer=="_3delight"):
                    self.camera=self.tempCamNames[c]
                else:
                    self.camera=transformNode


        self.CalcImageExtension()

        if ( self.tempModifyExtension):
            self.seqFileOffset=self.tempModifyStart-1
            if (self.tempModifyByframe!=1.0):
                rrWriteLog("No 'By Frame' renumbering allowed!\n Value: "+str(self.tempModifyByframe)+"  Layer: "+Layer+"\n")
                return False
        if (not self.getImageOut(DatabaseDir,MayaVersion,SceneName)):
            print ("rrSubmit - getLayerSettings '"+ Layer +"' getImageOut failed")
            return False

        if (nbRenderableCams>1):
            for c in range(0, len(self.tempCamRenderable)):
                if (self.tempCamRenderable[c]):
                    nbRenderableCams=nbRenderableCams+1
                    transformNode = cmds.listRelatives(self.tempCamNames[c],parent=True)
                    transformNode=transformNode[0]
                    if (self.camera!=transformNode):
                        self.channelFileName.append(self.imageFileName.replace('<Camera>',transformNode))
                        self.channelExtension.append(self.imageExtension)
                        self.maxChannels +=1
            self.camera=self.camera + " MultiCam"

        if (self.renderer == 'mentalRay') and (MayaVersion>=2009.0):
            self.addChannelsToLayer()
        if (self.renderer == 'arnold') and (MayaVersion>=2009.0):
            self.addAOVToLayer()
        if ((self.camera.find(":")>0) and (self.imageFileName.lower().find("<camera>")<0)):
            self.camera=""

        return True


    #add Arnold AOV to layer
    def addAOVToLayer(self):
        name = self.name
        if self.name == 'masterLayer':
            name = 'defaultRenderLayer'
        passes = cmds.ls(type='aiAOV')
        if passes == None or len(passes) == 0:
            return
        for p in passes:
            if((cmds.nodeType(p)=='aiAOV') and (cmds.getAttr(p+'.enabled') == 1)):
                self.channelFileName.append(self.imageFileName.replace('<Channel>', cmds.getAttr(p+'.name')))
                self.channelExtension.append(self.imageExtension)
                self.maxChannels +=1


    #add MRay Render Passes to layer
    def addChannelsToLayer(self):
        name = self.name
        if self.name == 'masterLayer':
            name = 'defaultRenderLayer'
        passes = cmds.listConnections(name+'.renderPass')
        if passes == None or len(passes) == 0:
            return
        for p in passes:
            if ((cmds.nodeType(p)=="renderPass") and (cmds.getAttr(p+'.renderable') == 1)):
                self.channelFileName.append(self.imageFileName.replace('<Channel>',p))
                self.channelExtension.append(self.imageExtension)
                self.maxChannels +=1



    #calculate image name from layer/render settings for Maya 2009+:
    def getImageOut2009(self):
        maya.mel.eval('renderSettings -fin -lyr "'+self.name+'";') # workaround for batch mode to load command
        RenderOut=cmds.renderSettings(ign=True,lyr=self.name)
        RenderOut=RenderOut[0]
        RenderOut=RenderOut.replace("\\","/")
        FNsplitter=""
        if (RenderOut.find("%0n")>=0):
            FNsplitter="%0n"
            self.imageFramePadding=1
        if (RenderOut.find("%1n")>=0):
            FNsplitter="%1n"
            self.imageFramePadding=1
        if (RenderOut.find("%2n")>=0):
            FNsplitter="%2n"
            self.imageFramePadding=2
        if (RenderOut.find("%3n")>=0):
            FNsplitter="%3n"
            self.imageFramePadding=3
        if (RenderOut.find("%4n")>=0):
            FNsplitter="%4n"
            self.imageFramePadding=4
        if (RenderOut.find("%5n")>=0):
            FNsplitter="%5n"
            self.imageFramePadding=5
        if (RenderOut.find("%6n")>=0):
            FNsplitter="%6n"
            self.imageFramePadding=6
        if (RenderOut.find("%7n")>=0):
            FNsplitter="%7n"
            self.imageFramePadding=7
        if (RenderOut.find("%8n")>=0):
            FNsplitter="%8n"
            self.imageFramePadding=8
        if (RenderOut.find("%9n")>=0):
            FNsplitter="%9n"
            self.imageFramePadding=9
        if (len(FNsplitter)>0):
            Splitted=RenderOut.split(FNsplitter,1)
            self.imageFileName=Splitted[0]
            self.imageExtension=Splitted[1]
            if ((self.renderer=="renderMan") and (self.imagePreNumberLetter=="_")):
                if (self.name=="masterLayer"):
                    self.imageFileName+="__"
                else:
                    self.imageFileName+="_"
        else:
            self.imageFileName=RenderOut
            self.imageExtension=""

        self.imageFileName=self.imageFileName.replace("%/l","<Layer>/")
        self.imageFileName=self.imageFileName.replace("%l","<Layer>")
        self.imageFileName=self.imageFileName.replace("<RenderLayer>","<Layer>")
        self.imageFileName=self.imageFileName.replace("%/c","<Camera>/")
        self.imageFileName=self.imageFileName.replace("%c","<Camera>")
        self.imageFileName=self.imageFileName.replace("%/s","<SceneFile>/")
        self.imageFileName=self.imageFileName.replace("%s","<SceneFile>")
        self.imageFileName=self.imageFileName.replace("<Scene>","<SceneFile>")
        self.imageFileName=self.imageFileName.replace("<RenderPass>","<Channel>")
        self.imageFileName=self.imageFileName.replace("<Version>",self.tempVersionTag)
        self.imageFileName=self.imageFileName.replace("%v",self.tempVersionTag)
        self.imageFileName=self.imageFileName.replace("%/v",self.tempVersionTag+"/")
        self.imageFileName=self.imageFileName.replace("<RenderPass>","<Channel>")
        self.imageFileName=self.imageFileName.replace("<Scene>","<SceneFile>")
        self.imageFileName=self.imageFileName.replace("%e",self.tempImageExtension)
        self.imageFileName=self.imageFileName.replace("<Extension>",self.tempImageExtension)

        if ((self.name=="masterLayer") and (self.renderer=="renderMan")):
            self.imageFileName=self.imageFileName.replace("<Layer>","")
        self.imageFileName=self.imageFileName.replace("//","/")


        if (self.imageFileName.find("<Channel>")>=0):
            if (self.renderer=="mentalRay") :
                self.channelName="MasterBeauty"
            elif (self.renderer=="arnold") :
                self.channelName="beauty"
            else:
                self.imageFileName=self.imageFileName.replace("<Channel>","")
        self.imageFileName=self.imageFileName.replace("%e",self.tempImageExtension)
        self.imageExtension=self.imageExtension.replace("%e",self.tempImageExtension)
        self.imageFileName=self.imageFileName.replace("<Extension>",self.tempImageExtension)
        self.imageExtension=self.imageExtension.replace("<Extension>",self.tempImageExtension)


    #calculate image name from layer/render settings for Maya 8.5:
    def getImageOut85(self,SceneName):
        ImageNoExtension= cmds.getAttr('defaultRenderGlobals.outFormatControl')
        ImageperiodInExt= cmds.getAttr('defaultRenderGlobals.periodInExt')
        ImageputFrameBeforeExt= cmds.getAttr('defaultRenderGlobals.putFrameBeforeExt')
        self.imageFramePadding=self.tempExtensionPadding
        self.imageExtension=""
        if ((self.tempImageFilePrefix==None) or (len(self.tempImageFilePrefix)==0)):
            self.tempImageFilePrefix=SceneName
            self.tempImageFilePrefix=self.tempImageFilePrefix.replace("\\","/")
            if (self.tempImageFilePrefix.find("/")>=0):
                splitted=self.tempImageFilePrefix.split("/")
                self.tempImageFilePrefix=splitted[len(splitted)-1]
            if (self.tempImageFilePrefix.find(".")>=0):
                splitted= self.tempImageFilePrefix.split(".")
                self.tempImageFilePrefix=""
                for i in range(0, len(splitted)-2):
                    if (i>0):
                        self.tempImageFilePrefix= self.tempImageFilePrefix + "."
                    self.tempImageFilePrefix= self.tempImageFilePrefix + splitted[i]
        if (ImageperiodInExt==0):
            self.imagePreNumberLetter=""
        elif (ImageperiodInExt==1):
            self.imagePreNumberLetter="."
        elif (ImageperiodInExt==2):
            self.imagePreNumberLetter="_"

        if (not self.ImageSingleOutputFile):
            if (ImageNoExtension):
                self.imageFileName=self.tempImageFilePrefix
            else:
                self.imageFileName=self.tempImageFilePrefix+"."+self.tempImageExtension
        elif (ImageNoExtension):
            self.imageFileName=self.tempImageFilePrefix+"."
        elif (ImageperiodInExt==0):
            self.imageFileName=self.tempImageFilePrefix
            self.imageExtension="."+self.tempImageExtension
        elif (ImageperiodInExt==2):
            self.imageFileName=self.tempImageFilePrefix+"_"
            self.imageExtension="."+self.tempImageExtension
        elif (ImageputFrameBeforeExt):
            self.imageFileName=self.tempImageFilePrefix+"."
            self.imageExtension="."+self.tempImageExtension
        else:
            self.imageFileName=self.tempImageFilePrefix+"."
            self.imageExtension="."+self.tempImageExtension
            rrWriteLog("'name.ext.#' not supported!\n Layer: "+Layer+"\n")
            return False

        self.imageFileName=self.imageFileName.replace("<Version>",self.tempVersionTag)
        RenderLayer=cmds.listConnections( "renderLayerManager", t="renderLayer")

        return True


    #prepare image name from layer/render settings:
    def getImageOut(self,DatabaseDir,MayaVersion,SceneName):
        #print ("rrSubmit - getImageOut")
        ImageperiodInExt= cmds.getAttr('defaultRenderGlobals.periodInExt')
        if (ImageperiodInExt==0):
            self.imagePreNumberLetter=""
        elif (ImageperiodInExt==1):
            self.imagePreNumberLetter="."
        elif (ImageperiodInExt==2):
            self.imagePreNumberLetter="_"

        if (self.renderer=="renderMan"):
            self.ImageDir=""
            self.imageFileName = maya.mel.eval('rman workspace GetDir rfmImages;')
            return True
        else:
            self.ImageDir= cmds.workspace(fre="images")
            isRelative=True
            self.imageFramePadding=0
            if (MayaVersion>=2009.0):
                self.getImageOut2009()
            else:
                self.getImageOut85(SceneName)
            if (len(self.imageFileName)>1):
                self.imageFileName=self.imageFileName.replace("\\","/")
                if ((self.imageFileName[0]=="/") or (self.imageFileName[1]==":")):
                    isRelative=False
                    self.ImageDir=""
            if (isRelative):
                if (len(self.ImageDir)>1):
                    self.ImageDir=self.ImageDir.replace("\\","/")
                    if ((self.ImageDir[0]=="/") or (self.ImageDir[1]==":")):
                        isRelative=False
            if (isRelative):
                self.ImageDir=DatabaseDir+self.ImageDir
                self.ImageDir+="/"
            if (cmds.objExists ( "mentalcoreGlobals" ) and (int(cmds.getAttr ('mentalcoreGlobals.enable'))==1 )):
                outMode = int(cmds.getAttr ('mentalcoreGlobals.file_mode'))
                if (outMode!=2):
                    ImageperiodInExt= cmds.getAttr('defaultRenderGlobals.periodInExt')
                    if (ImageperiodInExt!=1):
                        rrWriteLog('You have to use name.#.ext for MentalCore!')
                        return False
                    filepath=""
                    filename=""
                    (filepath, filename)=os.path.split(self.imageFileName)
                    self.channelName="beauty"
                    filepath=filepath+"/<Channel-removeVar>/"
                    if (filename[len(filename)-1]=="."):
                        filename=filename[:len(filename)-1]
                        filename=filename+"_<Channel-removeVar>."
                    else:
                        filename=filename+"_<Channel-removeVar>"
                    self.imageFileName=filepath+filename
            return True





class rrSceneInfo:
    def __init__(self):
        self.MayaVersion=""
        self.SceneName=""
        self.DatabaseDir=""

    def getSceneInfo(self):
        self.DatabaseDir=cmds.workspace( q=True, rd=True )
        self.SceneName=cmds.file( q=True, location=True )
        self.MayaVersion=maya.mel.eval('getApplicationVersionAsFloat')




def rrGetRR_Root():
        if os.environ.has_key('RR_ROOT'):
            return os.environ['RR_ROOT']
        HCPath="%"
        if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
            HCPath="%RRLocationWin%"
        elif (sys.platform.lower() == "darwin"):
            HCPath="%RRLocationMac%"
        else:
            HCPath="%RRLocationLx%"
        if HCPath[0]!="%":
            return HCPath
        rrWriteLog("No RR_ROOT environment variable set!\n Please execute rrWorkstationInstaller and restart the machine.")
        return"";


def rrSetNewTempFileName(UIMode):
        random.seed()
        if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
            if os.environ.has_key('TEMP'):
                nam=os.environ['TEMP']
            else:
                nam=os.environ['TMP']
            nam+="\\"
        else:
            nam="/tmp/"
        nam+="rrSubmitMaya_"
        if (UIMode):
            nam+=str(random.randrange(1000,10000,1))
        nam+=".xml"
        return nam


def rrWriteNodeStr(fileID,name,text):
        #print ("    <"+name+">  "+text+"   </"+name+">")
        text=text.replace("&","&amp;")
        text=text.replace("<","&lt;")
        text=text.replace(">","&gt;")
        text=text.replace("\"","&quot;")
        text=text.replace("'","&apos;")
        text=text.replace(unichr(228),"&#228;")
        text=text.replace(unichr(246),"&#246;")
        text=text.replace(unichr(252),"&#252;")
        text=text.replace(unichr(223),"&#223;")
        try:
            fileID.write("    <"+name+">  "+text+"   </"+name+">\n")
        except:
            rrWriteLog("Unable to write attribute '"+name+"' = '"+text+"'")

def rrWriteNodeInt(fileID,name,number):
        #print ("    <"+name+">  "+str(number)+"   </"+name+">")
        fileID.write("    <"+name+">  "+str(number)+"   </"+name+">\n")

def rrWriteNodeBool(fileID,name,value):
        if value:
            #print ("    <"+name+">   1   </"+name+">")
            fileID.write("    <"+name+">   1   </"+name+">\n")
        else:
            #print ("    <"+name+">   0   </"+name+">")
            fileID.write("    <"+name+">   0   </"+name+">\n")


def rrWritePassToFile(fileID, Layer, DPass, sceneInfo,camera,LocalTextureFile):
        fileID.write("<Job>\n")
        if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
            rrWriteNodeStr(fileID,"SceneOS", "win")
        elif (sys.platform.lower() == "darwin"):
            rrWriteNodeStr(fileID,"SceneOS", "mac")
        else:
            rrWriteNodeStr(fileID,"SceneOS", "lx")
        rrWriteNodeStr(fileID,"Software", "Maya")
        rrWriteNodeInt(fileID,"Version", sceneInfo.MayaVersion)
        rrWriteNodeStr(fileID,"SceneName", sceneInfo.SceneName)
        rrWriteNodeStr(fileID,"SceneDatabaseDir", sceneInfo.DatabaseDir)
        if DPass.renderer != 'vray':
            rrWriteNodeStr(fileID,"Renderer", DPass.renderer)
        else:
            rrWriteNodeStr(fileID,"Renderer", DPass.renderer+'NOID')
        rrWriteNodeStr(fileID,"RequiredPlugins", DPass.requiredPlugins)
        rrWriteNodeStr(fileID,"Camera",camera)
        rrWriteNodeStr(fileID,"Layer", Layer)
        rrWriteNodeStr(fileID,"Channel", DPass.name)
        rrWriteNodeBool(fileID,"IsActive",True)
        rrWriteNodeInt(fileID,"SeqStart",DPass.seqStart)
        rrWriteNodeInt(fileID,"SeqEnd",DPass.seqEnd)
        rrWriteNodeInt(fileID,"SeqStep",DPass.seqStep)
        rrWriteNodeInt(fileID,"SeqFileOffset",0)
        rrWriteNodeInt(fileID,"ImageWidth",DPass.imageWidth)
        rrWriteNodeInt(fileID,"ImageHeight",DPass.imageHeight)
        rrWriteNodeStr(fileID,"ImageDir",DPass.imageDir)
        rrWriteNodeStr(fileID,"ImageFilename",DPass.imageFileName)
        rrWriteNodeStr(fileID,"ImageExtension",DPass.imageExtension)
    #        rrWriteNodeStr(fileID,"ImagePreNumberLetter",Layer.imagePreNumberLetter)
        rrWriteNodeInt(fileID,"ImageFramePadding",4)
    #        rrWriteNodeBool(fileID,"ImageSingleOutputFile",Layer.ImageSingleOutputFile)
        for c in range(0,len(DPass.channelFilenames)):
           rrWriteNodeStr(fileID,"ChannelFilename",DPass.channelFilenames[c])
           rrWriteNodeStr(fileID,"ChannelExtension",DPass.channelExts[c])
        rrWriteNodeStr(fileID,"LocalTexturesFile",LocalTextureFile)
        if os.environ.get('VRAY_VERSION'):
            rrWriteNodeStr(fileID,"CustomA",os.environ.get('VRAY_VERSION'))
        if os.environ.get('ARCHIVE_VERSION'):
            rrWriteNodeStr(fileID,"CustomB",os.environ.get('ARCHIVE_VERSION'))
        fileID.write("</Job>\n")


def rrWriteLayerToFile(fileID,Layer, channel,sceneInfo,camera,LocalTextureFile):
        #print("\n\n")
        #print LayerID
        fileID.write("<Job>\n")
        if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
            rrWriteNodeStr(fileID,"SceneOS", "win")
        elif (sys.platform.lower() == "darwin"):
            rrWriteNodeStr(fileID,"SceneOS", "mac")
        else:
            rrWriteNodeStr(fileID,"SceneOS", "lx")
        rrWriteNodeStr(fileID,"Software", "Maya")
        rrWriteNodeInt(fileID,"Version", sceneInfo.MayaVersion)
        rrWriteNodeStr(fileID,"SceneName", sceneInfo.SceneName)
        rrWriteNodeStr(fileID,"SceneDatabaseDir", sceneInfo.DatabaseDir)
        if Layer.renderer != 'vray':
            rrWriteNodeStr(fileID,"Renderer", Layer.renderer)
        else:
            rrWriteNodeStr(fileID,"Renderer", Layer.renderer+'NOID')
        rrWriteNodeStr(fileID,"RequiredPlugins", Layer.requiredPlugins)
        rrWriteNodeStr(fileID,"Camera",camera)
        rrWriteNodeStr(fileID,"Layer", Layer.name)
        rrWriteNodeStr(fileID,"Channel", channel)
        rrWriteNodeBool(fileID,"IsActive",Layer.IsActive)
        rrWriteNodeInt(fileID,"SeqStart",Layer.seqStart)
        rrWriteNodeInt(fileID,"SeqEnd",Layer.seqEnd)
        rrWriteNodeInt(fileID,"SeqStep",Layer.seqStep)
        rrWriteNodeInt(fileID,"SeqFileOffset",Layer.seqFileOffset)
        rrWriteNodeInt(fileID,"ImageWidth",Layer.imageWidth)
        rrWriteNodeInt(fileID,"ImageHeight",Layer.imageHeight)
        rrWriteNodeStr(fileID,"ImageDir",Layer.ImageDir)
        rrWriteNodeStr(fileID,"ImageFilename",Layer.imageFileName)
        rrWriteNodeStr(fileID,"ImageExtension",Layer.imageExtension)
        rrWriteNodeStr(fileID,"ImagePreNumberLetter",Layer.imagePreNumberLetter)
        rrWriteNodeInt(fileID,"ImageFramePadding",Layer.imageFramePadding)
        rrWriteNodeBool(fileID,"ImageSingleOutputFile",Layer.ImageSingleOutputFile)
        for c in range(0,Layer.maxChannels):
           rrWriteNodeStr(fileID,"ChannelFilename",Layer.channelFileName[c])
           rrWriteNodeStr(fileID,"ChannelExtension",Layer.channelExtension[c])
        rrWriteNodeStr(fileID,"LocalTexturesFile",LocalTextureFile)
        if os.environ.get('VRAY_VERSION'):
            rrWriteNodeStr(fileID,"CustomA",os.environ.get('VRAY_VERSION'))
        if os.environ.get('ARCHIVE_VERSION'):
            rrWriteNodeStr(fileID,"CustomB",os.environ.get('ARCHIVE_VERSION'))
        fileID.write("</Job>\n")





class rrPlugin(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.RR_ROOT=""
        self.RR_ROOT=rrGetRR_Root()
        self.TempFileName=""
        self.MayaVersion="0.0"
        self.DatabaseDir=""
        self.maxLayer=0
        self.layer=[]
        self.cameras=[]
        self.passes = []
        self.SceneInfo = rrSceneInfo()
        self.multiCameraMode= False
        self.locTexFile=""
        return

    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr( rrPlugin() )


    #get list of all cameras in scene
    def getAllCameras(self):
        cameraList=cmds.ls(ca=True)
        for cam in cameraList:
            transformNode = cmds.listRelatives(cam,parent=True)
            transformNode=transformNode[0]
            if ((transformNode!="front") and (transformNode!="top") and (transformNode!="side")):
                if (self.layer[0].renderer=="_3delight"):
                    self.cameras.append(cam)
                else:
                    self.cameras.append(transformNode)


    #write list of all textures used into localtex file
    def writeTextureList(self):
        self.locTexFile=self.SceneInfo.SceneName
        if (self.locTexFile.find(".ma")>=0):
            self.locTexFile= self.locTexFile.replace(".ma",".localtex")
        elif (self.locTexFile.find(".mb")>=0):
            self.locTexFile= self.locTexFile.replace(".mb",".localtex")
        else:
            self.locTexFile=self.locTexFile+".localtex"
        fileID=0
        fileID = file(self.locTexFile, "w")
        fileID.write("<RR_LocalTextures syntax_version=\"6.0\">\n")
        if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
            rrWriteNodeStr(fileID,"SceneOS", "win")
        elif (sys.platform.lower() == "darwin"):
            rrWriteNodeStr(fileID,"SceneOS", "mac")
        else:
            rrWriteNodeStr(fileID,"SceneOS", "lx")
        rrWriteNodeStr(fileID,"Software", "Maya")
        rrWriteNodeStr(fileID,"DatabaseDir", self.SceneInfo.DatabaseDir)
        texList=cmds.ls(type='file')
        for tex in texList:
            fileID.write("<File>\n")
            texFileName=str(cmds.getAttr(tex+'.fileTextureName'))
            if (texFileName.startswith(self.SceneInfo.DatabaseDir)):
                texFileName=texFileName.replace(self.SceneInfo.DatabaseDir,self.SceneInfo.DatabaseDir+"/")
            rrWriteNodeStr(fileID,"Orginal", texFileName )
            fileID.write("</File>\n")
        fileID.write("</RR_LocalTextures>\n")
        fileID.close()
        if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
            os.system("\""+self.RR_ROOT+"\\bin\\win\\rrSubmitterconsole.exe\"  "+self.locTexFile)
        elif (sys.platform.lower() == "darwin"):
            os.system("\""+self.RR_ROOT+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter\"  "+self.locTexFile)
        else:
            os.system("\""+self.RR_ROOT+"/bin/mac/rrSubmitterconsole\"  "+self.locTexFile)


    #get all 3delight passes
    def getAllPasses(self):
        self.passes= []
        passes = cmds.ls(type='delightRenderPass')
        if passes == None or len(passes) == 0:
            print ('No passes found!')
            return False

        for p in passes:
            #print ("Parsing pass"+p)
            hpass = rrDelightRenderPass()
            if not hpass.getPassSettings(p):
                return False

            self.passes.append(hpass)
            #print (str(hpass))

        return True



    #get all render layers
    def getAllLayers(self):
        RenderLayer=cmds.listConnections( "renderLayerManager", t="renderLayer")
        isLayerRendering= (len(RenderLayer)>1)
        #Get MasterLayer Info
        self.maxLayer=1
        self.layer.append(rrMayaLayer())
        self.layer[0].name="masterLayer"
        self.layer[0].IsActive= (cmds.getAttr('defaultRenderLayer.renderable')==True)

        if (not (self.layer[0].getLayerSettings("defaultRenderLayer",self.SceneInfo.DatabaseDir,self.SceneInfo.SceneName,self.SceneInfo.MayaVersion,isLayerRendering))):
            print ("rrSubmit - unable to get settings from layer 'defaultRenderLayer'")
            return False

        #now get all layer:
        if (len(RenderLayer)>1):
            for Layer in RenderLayer:
                if (Layer=="defaultRenderLayer"):
                    continue

                self.maxLayer+=1
                self.layer.append(rrMayaLayer())

                self.layer[self.maxLayer-1].name=Layer
                self.layer[self.maxLayer-1].IsActive= (cmds.getAttr(Layer+'.renderable')==True)

                if (not (self.layer[self.maxLayer-1].getLayerSettings(Layer,self.SceneInfo.DatabaseDir,self.SceneInfo.SceneName,self.SceneInfo.MayaVersion,isLayerRendering))):
                    print ("rrSubmit - unable to get settings from layer "+ Layer)
                    return False
        if (self.maxLayer==1) and (self.layer[0].imageFileName.lower().find("<layer>")<0):
            self.layer[0].name="";
        return True


    #write all information (layer/passes) into RR job file
    def writeAllLayers(self,UIMode):
        self.TempFileName=rrSetNewTempFileName(UIMode)
        fileID=0
        fileID = file(self.TempFileName, "w")
        fileID.write("<RR_Job_File syntax_version=\"6.0\">\n")
        fileID.write("<DeleteXML>1</DeleteXML>\n")
        if (self.multiCameraMode):
            self.getAllCameras()
            for cam in self.cameras:
                for L in range(0, self.maxLayer):
                    if (self.layer[L].renderer=="_3delight"):
                        if not self.getAllPasses():
                            return False
                        for p in self.passes:
                            rrWritePassToFile(fileID,self.layer[L].name, p, self.SceneInfo,cam,self.locTexFile)
                    else:
                        rrWriteLayerToFile(fileID,self.layer[L],self.layer[L].channelName,self.SceneInfo,cam,self.locTexFile)
        else:
            for L in range(0, self.maxLayer):
                if (self.layer[L].renderer=="_3delight"):
                    if not self.getAllPasses():
                        return False
                    for p in self.passes:
                        rrWritePassToFile(fileID,self.layer[L].name, p, self.SceneInfo,p.camera ,self.locTexFile)
                else:
                    rrWriteLayerToFile(fileID,self.layer[L],self.layer[L].channelName,self.SceneInfo,self.layer[L].camera,self.locTexFile)
        fileID.write("</RR_Job_File>\n")
        fileID.close()


    #call the submitter
    def submitLayers(self):
        if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
            #print ("Executing: \""+self.RR_ROOT+"\\win__rrSubmitter.bat\"  "+self.TempFileName)
            os.system("\""+self.RR_ROOT+"\\win__rrSubmitter.bat\"  "+self.TempFileName)
        elif (sys.platform.lower() == "darwin"):
            #print ("Executing: \""+self.RR_ROOT+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter\"  "+self.TempFileName)
            os.system("\""+self.RR_ROOT+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter\"  "+self.TempFileName)
        else:
            #print ("Executing: \""+self.RR_ROOT+"/lx__rrSubmitter.sh\"  "+self.TempFileName)
            os.system("\""+self.RR_ROOT+"/lx__rrSubmitter.sh\"  "+self.TempFileName)



    #Main function called by menu execution:
    def doIt(self, arglist):
        print ("rrSubmit v 6.02.01")

        #check if we are in console batch mode
        UIMode=True
        try:
            maya.mel.eval('global string $gMainWindow;')
            maya.mel.eval('setParent $gMainWindow;')
        except:
            UIMode=False
            print ("We are running in batch mode")

        # Ask for scene save:
        if (UIMode and (cmds.file(q=True, mf=True))):  # //Ignore ifcheck
            ConfirmResult=(cmds.confirmDialog(message="Scene should be saved before network rendering.\n Save scene?", button=['Yes','No','Cancel'], defaultButton='Yes', cancelButton='Cancel', dismissString='Cancel'))
            if (ConfirmResult=="Cancel"):
                return True
            elif (ConfirmResult=="Yes"):
                cmds.file(s=True)

        #get information about the scene:
        self.SceneInfo.getSceneInfo()
        if (self.SceneInfo.SceneName=="unknown"):
            if (UIMode):
                cmds.confirmDialog(message="Scene was never saved!\n", button=['Abort'])
            return True

        #check if this function was called with parameters:
        self.multiCameraMode= False
        if ((arglist.length()>0) and arglist.asBool(0)):
            self.multiCameraMode= True
        if ((arglist.length()>1) and arglist.asBool(1)):
            self.writeTextureList()

        #get all layers:
        #print ("rrSubmit - get all layers")
        if (not self.getAllLayers()):
            #print ("rrSubmit - unable to get render/layer information")
            return False

        #write layers into file:
        #print ("rrSubmit - write layers into file")
        self.writeAllLayers(UIMode)

        #call submitter
        #print ("rrSubmit - call submitter")
        if UIMode:
            self.submitLayers()





# Initialize the script plug-in
def initializePlugin(mobject):
    '''
    try:
        maya.mel.eval('global string $RRMenuCtrl;')
        maya.mel.eval('if (`menu -exists $RRMenuCtrl `) deleteUI $RRMenuCtrl;')
        maya.mel.eval('global string $gMainWindow;')
        maya.mel.eval('setParent $gMainWindow;')
        maya.mel.eval('$RRMenuCtrl = `menu -p $gMainWindow -to true -l "RRender"`;')
        maya.mel.eval('menuItem -p $RRMenuCtrl -l "Submit scene..." -c "rrSubmit";')
        maya.mel.eval('menuItem -p $RRMenuCtrl -l "Submit scene - Select camera..." -c "rrSubmit true";')
        maya.mel.eval('menuItem -p $RRMenuCtrl -l "Submit scene - Local Textures" -c "rrSubmit false true";')
    except:
        print ("We are running in batch mode")
    '''

    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( "rrSubmit", rrPlugin.creator )
    except:
        sys.stderr.write( "Failed to register RR commands\n" )
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    maya.mel.eval('global string $RRMenuCtrl;')
    maya.mel.eval('if (`menu -exists $RRMenuCtrl `) deleteUI $RRMenuCtrl;')
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( "rrSubmit" )
    except:
        sys.stderr.write( "Failed to unregister RR commands\n" )
        raise







