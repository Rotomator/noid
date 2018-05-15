# 3DE4.script.name:      Export -  Maya & Nuke
# 3DE4.script.version:   v1.0.2
# 3DE4.script.gui:       Main Window::NOID
# 3DE4.script.comment:   Creates a Nuke script file for the undistor / distor
# v150622 1515

import os
import re
import subprocess
from time import gmtime, strftime

import tde4

# import NOID Tools

import tools
import get_bounding_box

# import NOID exporters
import mayaExporter
import nukeExporter

# cgev common import
import noid_log

# nukeVersions = ['Nuke 8', 'Nuke 7']

camResWidgetText = "Width, Height, first Frame"
camWidgetFormat = '{imageWidth}{sep}{imageHeight}{sep}{firstFrame}'
camWidgetPrefix = 'iwhO'
resSpliter = ';'


def listNukeVersions():
    apps = dict()
    base = 'C:/Program Files'

    for app in os.listdir(base):
        path = os.path.join(base, app)

        if not os.path.isdir(path):
            continue
        if not re.match('Nuke[0-9]\.[0-9]v[0-9]', app):
            continue

        label = 'Nuke %s' % app.split('Nuke')[1]
        exe = '%s.exe' % app.split('v')[0]
        exe = os.path.join(path, exe)

        if os.path.exists(exe):
            apps[label] = exe

    return apps

nukeVersions = listNukeVersions()


def findNukeExe(index):
    apps = nukeVersions.keys()
    apps.sort()
    apps.reverse()

    if index < 1 or index > len(apps):
        return nukeVersions[apps[0]]

    return nukeVersions[apps[index - 1]]


def callBackExportAll(req, widgetName, widgetStatus):
    for cameraIndex in range(tde4.getNoCameras()):
        try:
            # cameraTmp = tde4.getIndexCamera(cameraIndex)
            nametmp = "exportCamera"+str(cameraIndex)
            tde4.setWidgetValue(req,
                                nametmp,
                                str(tde4.getWidgetValue(req, widgetName)))
        except:
            pass


def callBackExportCamera(req, widgetName, widgetStatus):
    exportAll = True
    for cameraIndex in range(tde4.getNoCameras()):
        # cameraTmp = tde4.getIndexCamera(cameraIndex)
        nametmp = "exportCamera"+str(cameraIndex)
        try:
            if not tde4.getWidgetValue(req, nametmp):
                exportAll = False
                break
        except:
            pass
    tde4.setWidgetValue(req, "exportAllCameras", str(exportAll))


def buildUICamera(req, cameraIndex, cameraTmp):
    imageHeightOuttmp, imageWidthOuttmp = getOutSize(req,
                                                     cameraIndex,
                                                     cameraTmp)

    nametmp = "exportCamera"+str(cameraIndex)
    texttmp = "Export Camera " + str(tde4.getCameraName(cameraTmp))
    tde4.addToggleWidget(req, nametmp, texttmp, 1)
    tde4.setWidgetCallbackFunction(req, nametmp, "callBackExportCamera")

    firstFrame = tde4.getCameraSequenceAttr(cameraTmp)[0]

    strRes = camWidgetFormat.format(imageWidth=str(imageWidthOuttmp),
                                    sep=resSpliter,
                                    imageHeight=str(imageHeightOuttmp),
                                    firstFrame=firstFrame)

    camResWidgetName = camWidgetPrefix + str(cameraIndex)
    log.debug('camResWidgetName (creation): '+camResWidgetName)

    tde4.addTextFieldWidget(req,
                            camResWidgetName,
                            camResWidgetText,
                            strRes)

    tde4.addSeparatorWidget(req, "sep"+str(cameraIndex))


def getFocalParameters(lensTmp):
    # get the captor size
    fbxTmp = tde4.getLensFBackWidth(lensTmp)
    fbyTmp = tde4.getLensFBackHeight(lensTmp)

    # get lensTmp Parameters
    folcalParameter = dict()
    folcalParameter["filmW"] = fbxTmp
    folcalParameter["filmH"] = fbyTmp
    folcalParameter["focalLength"] = tde4.getLensFocalLength(lensTmp)
    folcalParameter["pixelAspect"] = tde4.getLensPixelAspect(lensTmp)#TODO

    log.debug(folcalParameter)

    return folcalParameter


def getLDmodelParameterList(model):
    l = []
    for p in range(tde4.getLDModelNoParameters(model)):
        l.append(tde4.getLDModelParameterName(model, p))
    # print model,l
    return l


def getLensModelParameter(camera=None, lens=None, frame=None):
    lensModelParameter = dict()
    if frame is None and camera is None:
        # get the focusDistance
        focus = tde4.getLensFocus(lens)
        # get the focalLenght
        fotalLenght = tde4.getLensFocalLength(lens)

    else:
        # get the focusDistance
        focus = tde4.getCameraFocus(camera, frame)
        # get the focalLenght
        fotalLenght = tde4.getCameraFocalLength(camera, frame)

    model = tde4.getLensLDModel(lens)

    for parameterName in (getLDmodelParameterList(model)):
        varTemp = tde4.getLensLDAdjustableParameter(lens,
                                                    parameterName,
                                                    fotalLenght,
                                                    focus)
        lensModelParameter[parameterName] = varTemp

    lensModelParameter['model'] = model
    return lensModelParameter


def getOutSize(req, cameraIndex, cameraTmp):
    # get the actual image size from cameraTmp
    imageHeightInTmp = tde4.getCameraImageHeight(cameraTmp)
    imageWidthInTmp = tde4.getCameraImageWidth(cameraTmp)

    lensTmp = tde4.getCameraLens(cameraTmp)

    folcalParameter = getFocalParameters(lensTmp)

    # distorsionMode
    dyndistmode = tde4.getLensDynamicDistortionMode(lensTmp)

    log.debug('dyndistmode : ' + str(dyndistmode))

    if dyndistmode == "DISTORTION_STATIC":
        lensModelParameter = getLensModelParameter(camera=None,
                                                   lens=lensTmp,
                                                   frame=None)
        resOutTmp = get_bounding_box.calculateBoundigBox(imageWidthInTmp,
                                                         imageHeightInTmp,
                                                         "undistort",
                                                         folcalParameter,
                                                         lensModelParameter)
        imageWidthOuttmp = resOutTmp.width
        imageHeightOuttmp = resOutTmp.height
    else:
        imageHeightOuttmp = imageHeightInTmp
        imageWidthOuttmp = imageWidthInTmp
        for frame in range(1, tde4.getCameraNoFrames(cameraTmp) + 1):
            lensModelParameter = getLensModelParameter(camera=cameraTmp,
                                                       lens=lensTmp,
                                                       frame=frame)
            resOuttmp = get_bounding_box.calculateBoundigBox(imageWidthInTmp,
                                                             imageHeightInTmp,
                                                             "undistort",
                                                             folcalParameter,
                                                             lensModelParameter
                                                             )
            if imageHeightOuttmp < resOuttmp.height:
                imageHeightOuttmp = resOuttmp.height
            if imageWidthOuttmp < resOuttmp.width:
                imageWidthOuttmp = resOuttmp.width

    if imageHeightInTmp > imageHeightOuttmp:
        imageHeightOuttmp = imageHeightInTmp
    if imageWidthInTmp > imageWidthOuttmp:
        imageWidthOuttmp = imageWidthInTmp

    log.debug('****************** lensModelParameter ********************')
    for key in lensModelParameter.keys():
        log.debug(key + ' : ' + str(lensModelParameter.get(key)))

    return imageHeightOuttmp, imageWidthOuttmp


def buildUINotSupported(req, cameraIndex, cameraTmp):
    message = ''
    '''
    if not tools.isClassicModel(cameraTmp):
        message += "Model not suported"
    '''
    if not tools.correctCameraPath(cameraTmp):
        message += "Worng format padding, it should be imageName.padding.ext"

    tde4.addTextFieldWidget(req,
                            "noExport"+str(cameraIndex),
                            "Camera " + str(tde4.getCameraName(cameraTmp)),
                            message)


def buildUI():

    # calculate Output file
    # we will get the path of the first camera - changed
    # to path to file .3DE wo extension
    '''
    firstCam = tde4.getIndexCamera(0)
    firstCamPath = tde4.getCameraPath(firstCam).replace('\\', '/')
    '''
    if tde4.getProjectPath() == None:
        print "Can't get the Project Path"
        outputFile = "Can't get the Project Path"
    else:
        # the same as the file 3DE wo the extension (asume in the 4 last chars)
        outputFile = tde4.getProjectPath().replace('/', '\\')[:-4]

    # open requester...
    req = tde4.createCustomRequester()
    tde4.addFileWidget(req, "file_browser", "Browse...", "*", outputFile)
    # tde4.addTextFieldWidget(req, "filePath", "Optuput file", outputFile)
    labels = nukeVersions.keys()
    labels.sort()
    labels.reverse()

    tde4.addOptionMenuWidget(req, "nukeVersion", "Nuke Version", *labels)

    tde4.addToggleWidget(req, "openNuke", "Open nuke after Export", 0)

    # To Export
    tde4.addSeparatorWidget(req, "sep2")

    # export all cameras
    tde4.addToggleWidget(req, "exportAllCameras", "Export all Cameras", 1)
    tde4.setWidgetCallbackFunction(req,
                                   "exportAllCameras",
                                   "callBackExportAll")

    tde4.addSeparatorWidget(req, "sepAllCameras")
    # cameras to select
    for cameraIndex in range(tde4.getNoCameras()):
        cameraTmp = tde4.getIndexCamera(cameraIndex)
        if not tools.validCamera(cameraTmp):
            buildUINotSupported(req, cameraIndex, cameraTmp)
        else:
            buildUICamera(req, cameraIndex, cameraTmp)
    return req


def exportCGEV():
    # print 'Start exportCGEV'
    req = buildUI()
    ret = tde4.postCustomRequester(req,
                                   "Export CGEV - (Maya & Nuke)",
                                   0,
                                   0,
                                   "Export",
                                   "Cancel")

    if ret == 1:  # Canceled by the user
        # get the parameters selecteds
        params = {}
        params['file_browser'] = tde4.getWidgetValue(req, "file_browser")
        params['nukeVersion'] = tde4.getWidgetValue(req, "nukeVersion")
        params['openNuke'] = tde4.getWidgetValue(req, "openNuke")

        params['cameras'] = []
        params['camerasOutSize'] = []
        params['camerasFirstFrame'] = list()

        date = strftime("%y%m%d%H%M%S", gmtime())  # YYMMDDhhmmss
        params['date'] = date

        for cameraIndex in range(tde4.getNoCameras()):
            cameraObj = tde4.getIndexCamera(cameraIndex)
            # cameraName = str(tde4.getCameraName(cameraObj)) # NO USED
            exprtCamWidgetName = "exportCamera"+str(cameraIndex)

            exprtCamWidgetExists = tde4.widgetExists(req, exprtCamWidgetName)
            exprtCamWidgetValue = tde4.getWidgetValue(req, exprtCamWidgetName)

            if exprtCamWidgetExists and exprtCamWidgetValue:

                camResWidgetName = camWidgetPrefix + str(cameraIndex)
                log.debug('camResWidgetName : '+str(camResWidgetName))
                camResWidgetValue = tde4.getWidgetValue(req, camResWidgetName)

                log.debug('camResWidgetValue: '+str(camResWidgetValue))

                imageWidth, imageHeight, firstFrame = camResWidgetValue.split(resSpliter)

                imageResolution = tools.Resolution(width=imageWidth,
                                                   height=imageHeight)

                params['cameras'].append(cameraObj)
                params['camerasOutSize'].append(imageResolution)
                params['camerasFirstFrame'].append(firstFrame)

                log.debug('imageResolution : '+str(imageResolution))

        if params['cameras'] == []:
            message = 'Aborting, Nothing selected to Export'
            log.debug(message)
            return

        # debug params
        for paramName in params:
            paramValue = params[paramName]
            log.debug('param : '+str(paramName))
            log.debug('value : '+str(paramValue))

        # Export to Maya
        mayaExporter.toMaya(params)

        # Export to Nuke
        nukeFilesPath = nukeExporter.toNuke(params)


        # open Nuke or not
        if params['openNuke']:
            for nukeFilePath in nukeFilesPath:
                nukeExePath = findNukeExe(int(params['nukeVersion']))
                toExecute = [nukeExePath, '-q', nukeFilePath]

                log.debug(toExecute)

                useSubProcess = True
                if useSubProcess:
                    subprocess.Popen(toExecute, executable=nukeExePath)
                else:
                    os.system(toExecute)

        tde4.postQuestionRequester('Export finished',
                                   'All the cameras selected were exported',
                                   'OK')
    else:
        message = 'Canceled by user'
        log.debug(message)

    message = 'End exportCGEV'
    log.debug(message)
