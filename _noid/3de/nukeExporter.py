# v151208 1234
# 3DE4.script.hide: true
import os

import tde4

# functions
import scramble

from cgev.tde import tools
from cgev.pipeline.data import getdata

from cgev.common import newconfig
from cgev.common import log

scramble


def getLDNodeName(cam, direction, offset=0, index=0):
    nameNode = 'LD_3DE4_%s_%s_1'
    nameNode = nameNode % (tools.validName(tde4.getCameraName(cam)), index)
    return nameNode


def generateNukeNode(cam, direction, offset=0, index=0):
    lens = tde4.getCameraLens(cam)
    model = tde4.getLensLDModel(lens)
    num_frames = tde4.getCameraNoFrames(cam)
    w_fb_cm = tde4.getLensFBackWidth(lens)
    h_fb_cm = tde4.getLensFBackHeight(lens)
    lco_x_cm = tde4.getLensLensCenterX(lens)
    lco_y_cm = tde4.getLensLensCenterY(lens)
    pxa = tde4.getLensPixelAspect(lens)
# xa,xb,ya,yb in unit coordinates, in this order.
    fov = tde4.getCameraFOV(cam)

    print 'camera: ', tde4.getCameraName(cam)
    print 'offset:', offset
    print 'lens:', tde4.getLensName(lens)
    print 'model: ', model

    nukeNode = []

    nukeNode.append('# Created by 3DEqualizer4 ')
    nukeNode.append('# using Export Nuke Distortion Nodes export script')
    nukeNode.append("LD" + tools.nukify_name(model) + ' {')
    nukeNode.append(' direction '+direction)

# write focal length curve if dynamic
    if tde4.getCameraZoomingFlag(cam):
        print 'dynamic focal length'
        dynFocalLength = []

        for frame in range(1, num_frames + 1):
            dynFocalLength.append('x%i' % (frame+offset))
            dynFocalLength.append(' %.7f ' % tde4.getCameraFocalLength(cam,
                                                                       frame))
        focalLenghtStr = "".join(dynFocalLength)
        nukeNode.append(' tde4_focal_length_cm {{curve '+focalLenghtStr+' }}')

# write static focal length else
    else:
        print 'static focal length'
        focalLenghtStr = ' tde4_focal_length_cm %.7f '
        focalLenghtStr = focalLenghtStr % tde4.getCameraFocalLength(cam, 1)
        nukeNode.append(focalLenghtStr)

# write focus distance curve if dynamic
    try:
        if tde4.getCameraFocusMode(cam) == "FOCUS_DYNAMIC":
            print 'dynamic focus distance'
            dynFocusDistance = []
            for frame in range(1, num_frames + 1):
                dynFocusDistance.append('x%i' % (frame+offset))
                dynFocusDistance.append(' %.7f ' % tde4.getCameraFocus(cam,
                                                                       frame))
            focusDStr = "".join(dynFocusDistance)
            toWrite = ' tde4_custom_focus_distance_cm {{curve '+focusDStr+'}}'
            nukeNode.append(toWrite)
    except:
        # For 3DE4 Release 1:
        pass
# write static focus distance else
    else:
        print 'static focus distance'
        try:
            cameraFocus = ' tde4_custom_focus_distance_cm %.7f '
            cameraFocus = cameraFocus % tde4.getCameraFocus(cam, 1)
            nukeNode.append(cameraFocus)
        except:
            # For 3DE4 Release 1:
            nukeNode.append(' tde4_custom_focus_distance_cm 100.0 ')
# write camera
    nukeNode.append(' tde4_filmback_width_cm %.7f ' % w_fb_cm)
    nukeNode.append(' tde4_filmback_height_cm %.7f ' % h_fb_cm)
    nukeNode.append(' tde4_lens_center_offset_x_cm %.7f ' % lco_x_cm)
    nukeNode.append(' tde4_lens_center_offset_y_cm %.7f ' % lco_y_cm)
    nukeNode.append(' tde4_pixel_aspect %.7f ' % pxa)
    nukeNode.append(' field_of_view_xa_unit %.7f ' % fov[0])
    nukeNode.append(' field_of_view_ya_unit %.7f ' % fov[2])
    nukeNode.append(' field_of_view_xb_unit %.7f ' % fov[1])
    nukeNode.append(' field_of_view_yb_unit %.7f ' % fov[3])
    nukeNode.append(' filter Simon')

# dynamic distortion
    try:
        dyndistmode = tde4.getLensDynamicDistortionMode(lens)
    except:
        # For 3DE4 Release 1:
        if tde4.getLensDynamicDistortionFlag(lens) == 1:
            dyndistmode = "DISTORTION_DYNAMIC_FOCAL_LENGTH"
        else:
            dyndistmode = "DISTORTION_STATIC"

    if dyndistmode == "DISTORTION_STATIC":
        print 'static lens distortion'
        for para in (tools.getLDmodelParameterList(model)):
            distStr = ' %.7f ' % tde4.getLensLDAdjustableParameter(lens,
                                                                   para,
                                                                   1, 1)
            nukeNode.append(' ' + tools.nukify_name(para) + distStr)
    else:
        print 'dynamic lens distortion,'
        # dynamic
        for para in (tools.getLDmodelParameterList(model)):

            lensCurve = []
            for frame in range(1, num_frames + 1):
                focal = tde4.getCameraFocalLength(cam, frame)
                focus = tde4.getCameraFocus(cam, frame)
                lensCurve.append('x%i' % (frame+offset))
                frameParam = tde4.getLensLDAdjustableParameter(lens,
                                                               para,
                                                               focal,
                                                               focus)
                lensCurve.append(' %.7f ' % frameParam)
            lensCurveStr = ' {{curve ' + "".join(lensCurve) + ' }}'
            nukeNode.append(' ' + tools.nukify_name(para) + lensCurveStr)

    nameNode = 'name '+getLDNodeName(cam, direction, offset, index)
    nukeNode.append(nameNode)
    nukeNode.append('}')

    return nukeNode


def writeLines(fileObj, lines):
    for line in lines:
        fileObj.write(line + '\n')


formatTemplate = '"{rX} {rY} 0 0 {rX} {rY} {pAspect} {projName}'
fmatNameBase = formatTemplate+'_Base"'
fundNameBase = formatTemplate+'_Undisto_{imagesName}"'


def exportNuke(cam, index, size, filepath, date, frameStart):
    # print 'Nuke ',nukeVersion,' version'
    offsetXNodes = str(index*400)

    camInfo = tools.TDECamInfo(cam, index)
    camShortName = camInfo.getShortName()
    readFilePath = camInfo.cameraPath
    projectName = camInfo.projectName
    projectPath = camInfo.projectPath
    imagesName = camInfo.imagesName
    shot = camInfo.shot

    rez_x = camInfo.rez_x  # width
    rez_y = camInfo.rez_y  # height

    firstFrame = camInfo.firstFrame
    lastFrame = camInfo.lastFrame
    offset = int(frameStart) - 1

    if camInfo.lens is None:
        return -1

    lensInfo = tools.TDELensInfo(camInfo.lens)
    p_aspect = lensInfo.p_aspect

    readFormat = fmatNameBase.format(rX=str(rez_x),
                                     rY=str(rez_y),
                                     pAspect=str(p_aspect),
                                     projName=str(projectName))

    undistoGroupName = 'UNDISTO'

    if camInfo.isSeq():
        undistoGroupLabel = '"' + projectName + '\\n' + imagesName + '"'
    else:
        undistoGroupLabel = '"Reference frame\\n' + camShortName + '"'

    projectConfig = newconfig.ProjectCFile(projectName,
                                           projectPath,
                                           checkConfigured=False)

    # Working on OCIO prod
    if projectConfig.isOCIO():
        cspaceInName = 'Workingspace_to_LogC'
        cspaceOutName = 'LogC_to_Workingspace'
        OCIOConfig = projectConfig.getOCIOConfig()

        if readFilePath.endswith('.exr'):
            readColorSpace = OCIOConfig['floatLut']
        elif readFilePath.endswith('.dpx'):
            readColorSpace = OCIOConfig['logLut']
        else:
            readColorSpace = OCIOConfig['int8Lut']

        readColorSpace = OCIOConfig['floatLut']
        colorspaceInLine = 'in_colorspace ' + OCIOConfig['workingSpaceLut']
        colorspaceInLine += '\n  out_colorspace ' + OCIOConfig['logLut']

    # Working on normal prod
    else:
        cspaceInName = 'Lin_to_Log'
        cspaceOutName = 'Log_to_Lin'

        if readFilePath.endswith('.exr'):
            readColorSpace = 'linear'
        elif readFilePath.endswith('.dpx'):
            readColorSpace = getdata.getRootColorSpace(projectName)
        else:
            readColorSpace = 'sRGB'

        colorspaceInLine = 'out_colorspace ' + readColorSpace

    log.debug("rez_x : " + str(rez_x))
    log.debug("rez_y : " + str(rez_y))
    log.debug("size width : " + str(size.width))
    log.debug("size height : " + str(size.height))

    undistoW = str(max(int(rez_x), int(size.width)))
    undistoH = str(max(int(rez_y), int(size.height)))

    Reformat_REZ_UNDISTO_Format = fundNameBase.format(rX=str(undistoW),
                                                      rY=str(undistoH),
                                                      pAspect=str(p_aspect),
                                                      projName=projectName,
                                                      imagesName=imagesName)

    writeNodeFile = camInfo.getUndistoImagePath(app='nuke', date=date)
    writeNodeName = camInfo.getWriteNodeName()

    Reformat_BASE_REZ_Format = readFormat
    Reformat_BASE_BOX_Format = readFormat

    redistoGroupName = 'REDISTO'
    redistoGroupLabel = undistoGroupLabel

    # check if there is or not disto
    # distortion = tools.cameraHasDistortion(cam)

    # Compose File Lines
    # Root
    rootString = ['Root { ',
                  ' inputs 0',
                  ' frame '+firstFrame,
                  ' first_frame '+firstFrame,
                  ' last_frame '+lastFrame,
                  ' lock_range true',
                  '}',
                  ]
    # Read
    readString = ['Read {',
                  ' inputs 0',
                  ' file '+readFilePath,
                  ' format '+readFormat,
                  ' first '+firstFrame,
                  ' last '+lastFrame,
                  ' colorspace '+readColorSpace,
                  ' name Master',
                  ' xpos '+offsetXNodes,
                  ' ypos 0',
                  '}',
                  ]
    # Group UNDISTO
    LDNodeName = getLDNodeName(cam, "undistort", offset, index=0)
    undistroGroupString = ['Group {',
                           ' name '+undistoGroupName,
                           ' label '+undistoGroupLabel,
                           ' xpos '+offsetXNodes,
                           ' ypos 150',
                           ' knobChanged "\nif nuke.thisKnob().name().endswith(\'_solo\') and nuke.thisKnob().value() is True:\n    for knob in \[knob for knob in nuke.thisNode().knobs().values() if knob != nuke.thisKnob() and knob.name().endswith(\'_solo\')]:\n        knob.setValue(False)\n"',
                           ' addUserKnob {20 User l UNDISTO}',
                           ' addUserKnob {41 out_colorspace l "@b; ColorSpace" T '+cspaceInName+'.out_colorspace}',
                           ' addUserKnob {26 S01 l " "}',
                           ' addUserKnob {41 filter_LD l "@b; Filter" T '+LDNodeName+'.filter}',
                           ' addUserKnob {26 S02 l " "}',
                           ' addUserKnob {26 Clamp l "@b; Clamp" T " "}',
                           ' addUserKnob {41 minimum l min T Clamp2.minimum}',
                           ' addUserKnob {41 minimum_enable l enable -STARTLINE T Clamp2.minimum_enable}',
                           ' addUserKnob {41 maximum l max T Clamp2.maximum}',
                           ' addUserKnob {41 maximum_enable l enable -STARTLINE T Clamp2.maximum_enable}',
                           ' addUserKnob {26 S03 l " "}',
                           ' addUserKnob {26 bbox l "@b; Bounding Box" T " "}',
                           ' addUserKnob {6 bbox_input_solo l "Preserve Input" +STARTLINE}',
                           ' bbox_input_solo true',
                           ' addUserKnob {6 bbox_crop_solo l "Crop to Format" +STARTLINE}',
                           ' addUserKnob {6 bbox_addpixel_solo l "Add Pixels              " +STARTLINE}',
                           ' addUserKnob {41 numpixels l "" -STARTLINE T AdjBBox1.numpixels}',
                           ' addUserKnob {26 by1 l " " T " "}',
                           ' addUserKnob {26 by2 l " " T "                                                                                               "}',
                           ' addUserKnob {26 CGEV l " " t "\nEn cas de probleme, contacter Gaetan Baldy sur le chat\n" -STARTLINE T "<font color=\\"#1C1C1C\\"> v02 - CGEV - 2016"}',
                           '}',
                           ' Input {',
                           '  inputs 0',
                           '  name Input1',
                           '  xpos '+offsetXNodes,
                           '  ypos 0',
                           ' }',
                           ' Clamp {',
                           '  maximum 10',
                           '  name Clamp2',
                           '  xpos '+offsetXNodes,
                           '  ypos 40',
                           ' }',
                           ' Clamp {',
                           '  channels alpha',
                           '  name Clamp1',
                           '  xpos '+offsetXNodes,
                           '  ypos 80',
                           ' }',
                           ' OCIOColorSpace {',
                           '  ' + colorspaceInLine,
                           '  name ' + cspaceInName,
                           '  xpos '+offsetXNodes,
                           '  ypos 120',
                           ' }',
                           ]

    undistroGroupString.extend(generateNukeNode(cam,
                                                "undistort",
                                                offset,
                                                index=0))

    undistroGroupString.extend([
                        ' Reformat {',
                        '  format '+Reformat_REZ_UNDISTO_Format,
                        '  resize none',
                        '  filter {{input0.filter}}',
                        '  clamp false',
                        '  pbb {{parent.bbox_input_solo}}',
                        '  name Reformat_REZ_UNDISTO',
                        '  xpos '+offsetXNodes,
                        '  ypos 160',
                        ' }',
                        ' AdjBBox {',
                        '  numpixels {100 100}',
                        '  name AdjBBox1',
                        '    label ADD_PIXELS',
                        '  xpos '+offsetXNodes,
                        '  ypos 200',
                        '  disable {{!parent.bbox_addpixel_solo}}',
                        ' }',
                        ' OCIOColorSpace {',
                        '  in_colorspace {{'+cspaceInName+'.out_colorspace}}',
                        '  out_colorspace {{'+cspaceInName+'.in_colorspace}}',
                        '  name ' + cspaceOutName,
                        '  xpos '+offsetXNodes,
                        '  ypos 240',
                        ' }',
                        ' Clamp {',
                        '  minimum {{parent.Clamp2.minimum}}',
                        '  minimum_enable {{parent.Clamp2.minimum_enable}}',
                        '  maximum {{parent.Clamp2.maximum}}',
                        '  maximum_enable {{parent.Clamp2.maximum_enable}}',
                        '  name Clamp3',
                        '  xpos '+offsetXNodes,
                        '  ypos 280',
                        ' }',
                        ' Clamp {',
                        '  channels alpha',
                        '  minimum {{parent.Clamp1.minimum}}',
                        '  maximum {{parent.Clamp1.maximum}}',
                        '  name Clamp4',
                        '  xpos '+offsetXNodes,
                        '  ypos 320',
                        ' }',
                        ' Output {',
                        '  name Output1',
                        '  xpos '+offsetXNodes,
                        '  ypos 360',
                        ' }',
                        'end_group',
                        ])
    # node Write
    writeNodeString = ['Write {',
                       ' inputs 1',
                       ' file '+writeNodeFile,
                       ' file_type jpeg',
                       ' checkHashOnRead false',
                       ' name '+writeNodeName,
                       ' xpos '+str(200+400*index),
                       ' ypos 156',
                       '}',
                       ]
    # Group REDISTO
    LDNodeName = getLDNodeName(cam, "distort", offset, index)
    redistroGroupString = ['Group {',
                           ' inputs 0',
                           ' name '+redistoGroupName,
                           ' label '+redistoGroupLabel,
                           ' xpos '+offsetXNodes,
                           ' ypos 250',
                           ' knobChanged "\nif nuke.thisKnob().name().endswith(\'_solo\') and nuke.thisKnob().value()  == True:\n    for knob in \[knob for knob in nuke.thisNode().knobs().values() if knob != nuke.thisKnob() and knob.name().endswith(\'_solo\')]:\n        knob.setValue(False)\n"',
                           ' addUserKnob {20 User l REDISTO}',
                           ' addUserKnob {41 out_colorspace l "@b; ColorSpace" T '+cspaceInName+'.out_colorspace}',
                           ' addUserKnob {26 S01 l " "}',
                           ' addUserKnob {41 filter_LD l "@b; Filter" T '+LDNodeName+'.filter}',
                           ' addUserKnob {26 S02 l " "}',
                           ' addUserKnob {26 Clamp l "@b; Clamp" T " "}',
                           ' addUserKnob {41 minimum l min T Clamp2.minimum}',
                           ' addUserKnob {41 minimum_enable l enable -STARTLINE T Clamp2.minimum_enable}',
                           ' addUserKnob {41 maximum l max T Clamp2.maximum}',
                           ' addUserKnob {41 maximum_enable l enable -STARTLINE T Clamp2.maximum_enable}',
                           ' addUserKnob {26 S03 l " "}',
                           ' addUserKnob {26 bbox l "@b; Bounding Box" T " "}',
                           ' addUserKnob {6 bbox_input_solo l "Preserve Input" +STARTLINE}',
                           ' bbox_input_solo true',
                           ' addUserKnob {6 bbox_crop_solo l "Crop to Format" +STARTLINE}',
                           ' addUserKnob {26 by2 l " " T "                                                                                               "}',
                           ' addUserKnob {26 CGEV l " " t "\nEn cas de probleme, contacter Gaetan Baldy sur le chat\n" -STARTLINE T "<font color=\\"#1C1C1C\\"> v02 - CGEV - 2016"}',

                           '}',
                           ' Input {',
                           '  inputs 0',
                           '  name Input1',
                           '  xpos '+offsetXNodes,
                           '  ypos 0',
                           ' }',
                           ' Clamp {',
                           '  maximum 10',
                           '  name Clamp2',
                           '  xpos '+offsetXNodes,
                           '  ypos 40',
                           ' }',
                           ' Clamp {',
                           '  channels alpha',
                           '  name Clamp1',
                           '  xpos '+offsetXNodes,
                           '  ypos 80',
                           ' }',
                           ' OCIOColorSpace {',
                           '  ' + colorspaceInLine,
                           '  name ' + cspaceInName,
                           '  xpos '+offsetXNodes,
                           '  ypos 120',
                           ' }',
                           ' Reformat {',
                           '  format '+Reformat_BASE_REZ_Format,
                           '  resize none',
                           '  filter {{'+LDNodeName+'.filter}}',
                           '  clamp false',
                           '  pbb true',
                           '  name Reformat_BASE_REZ',
                           '  xpos '+offsetXNodes,
                           '  ypos 160',
                           ' }',
                           ]

    redistroGroupString.extend(generateNukeNode(cam, "distort", offset, index))

    redistroGroupString.extend([
                        ' Reformat {',
                        '  format '+Reformat_BASE_BOX_Format,
                        '  resize none',
                        '  filter {{'+LDNodeName+'.filter}}',
                        '  pbb {{!parent.bbox_crop_solo}}',
                        '  name Reformat_BASE_BOX',
                        '  xpos '+offsetXNodes,
                        '  ypos 200',
                        '  clamp {{Reformat_BASE_REZ.clamp}}'
                        ' }',
                        ' OCIOColorSpace {',
                        '  in_colorspace {{'+cspaceInName+'.out_colorspace}}',
                        '  out_colorspace {{'+cspaceInName+'.in_colorspace}}',
                        '  name ' + cspaceOutName,
                        '  xpos '+offsetXNodes,
                        '  ypos 240',
                        ' }',
                        ' Clamp {',
                        '  minimum {{parent.Clamp2.minimum}}',
                        '  minimum_enable {{parent.Clamp2.minimum_enable}}',
                        '  maximum {{parent.Clamp2.maximum}}',
                        '  maximum_enable {{parent.Clamp2.maximum_enable}}',
                        '  name Clamp3',
                        '  xpos '+offsetXNodes,
                        '  ypos 280',
                        ' }',
                        ' Clamp {',
                        '  channels alpha',
                        '  minimum {{parent.Clamp1.minimum}}',
                        '  maximum {{parent.Clamp1.maximum}}',
                        '  name Clamp4',
                        '  xpos '+offsetXNodes,
                        '  ypos 320',
                        ' }',
                        ' Output {',
                        '  name Output1',
                        '  xpos '+offsetXNodes,
                        '  ypos 360',
                        ' }',
                        'end_group',
                                ])

    allstring = rootString + readString + undistroGroupString +\
        writeNodeString + redistroGroupString

    argsToBatch = [filepath, writeNodeFile,
                   firstFrame, lastFrame,
                   writeNodeName, 1]

    return allstring, argsToBatch


def toNuke(params, oneFile=False):
    log.debug('To Nuke - Start')

    cameras = params['cameras']
    camerasOutSize = params['camerasOutSize']
    camerasFrameStart = params['camerasFirstFrame']

    filesGenerated = []
    argsToBatchs = []

    if oneFile:
        filepath = params['file_browser'] + '_undisto.nk'
        tools.ensure_dir(filepath)
        fileObj = open(filepath, 'w')
        for index, cam in enumerate(cameras):
            fileLines = []
            argsExportNuke = [cam,
                              index,
                              camerasOutSize[index],
                              filepath,
                              params['date'],
                              camerasFrameStart[index]]

            fileLines, argsToBatch = exportNuke(*argsExportNuke)

            if fileLines == -1:
                # print ("Problem with camera "+ str(cam) )
                continue

            writeLines(fileObj, fileLines)
            argsToBatchs.append(argsToBatch)
        filesGenerated.append(filepath)

    else:
        # create Directory
        folderCameras = params['file_browser'] + '_undisto/'
        try:
            os.makedirs(folderCameras)
        except:
            pass  # Todo check if is only that the folder exists

        for index, cam in enumerate(cameras):
            cameraName = "%s_%s_1" % (tools.validName(tde4.getCameraName(cam)),
                                      index)
            filepath = folderCameras + cameraName + '_undisto.nk'
            tools.ensure_dir(filepath)
            fileObj = open(filepath, 'w')
            fileLines = []
            argsExportNuke = [cam,
                              index,
                              camerasOutSize[index],
                              filepath,
                              params['date'],
                              camerasFrameStart[index]]

            fileLines, argsToBatch = exportNuke(*argsExportNuke)

            if fileLines == -1:
                # print ("Problem with camera "+ str(cam) )
                continue

            writeLines(fileObj, fileLines)
            argsToBatchs.append(argsToBatch)
            filesGenerated.append(filepath)

    # Launch batch Render
    log.debug('Launching batch Render')

    from cgev.common import toBatch
    for argsToBatch in argsToBatchs:
        if params['nukeVersion'] == 2:  # 'Nuke 7':
            argsToBatch.append('7.0')
        elif params['nukeVersion'] == 1:  # 'Nuke 8':
            argsToBatch.append('8.0')

        toBatch.batch3DE(*(argsToBatch))
    return filesGenerated

    log.debug('To Nuke - End')
