# v150622 1515
# 3DE4.script.hide: true
# from vl_sdv import *
import vl_sdv

import tde4

import tools


# global variables
yup = 1


def convertToAngles(r3d):
    rot = vl_sdv.rot3d(vl_sdv.mat3d(r3d)).angles(vl_sdv.VL_APPLY_ZXY)
    rx = (rot[0]*180.0)/3.141592654
    ry = (rot[1]*180.0)/3.141592654
    rz = (rot[2]*180.0)/3.141592654
    return(rx, ry, rz)


def convertZup(p3d, yup):
    if yup == 1:
        return(p3d)
    else:
        return([p3d[0], -p3d[2], p3d[1]])


def angleMod360(d0, d):
    dd = d-d0
    if dd > 180.0:
        d = angleMod360(d0, d-360.0)
    else:
        if dd < -180.0:
            d = angleMod360(d0, d+360.0)
    return d


def prepareImagePath(path, startframe):
    path = path.replace("\\", "/")

    pathPadding = path.split('.')[-2]

    if '#' in pathPadding:
        lenpad = len(pathPadding)
        pathTmp = path.replace(pathPadding, '%0'+str(lenpad)+'d')
    else:
        pathTmp = path
    pathPrepared = pathTmp % startframe

    return pathPrepared


def touchParam(f, paramName, insertKey=True, lock=True):
    if insertKey:
        f.write('setAttr -e-keyable true (' + paramName + ') ;  \n')
        f.write('setKeyframe             (' + paramName + ') ;  \n')
    if lock:
        f.write('setAttr -lock true      (' + paramName + ') ;  \n')


# export Functions
def exportCameras(f, cameras, camFrameStart, exportPath, campg, outSize, date):

    for cameraIndex, cam in enumerate(cameras):

        frameStart = int(camFrameStart[cameraIndex])
        frame0 = frameStart - 1

        camInfo = tools.TDECamInfo(cam, cameraIndex)
        cameraName = camInfo.name
        cameraPath = camInfo.cameraPath
        projectName = camInfo.projectName
        projectPath = camInfo.projectPath

        rez_x = camInfo.rez_x
        rez_y = camInfo.rez_y

        firstFrame = camInfo.firstFrame
        lastFrame = camInfo.lastFrame
        offset = camInfo.offset

        noframes = camInfo.noframes

        offset = int(firstFrame)-int(frameStart)

        model = camInfo.model

        camType = camInfo.camType

        model_maya = tools.getLDmodelNukeNodeName(model)

        lens = camInfo.lens

        if lens is not None:
            fback_w = tde4.getLensFBackWidth(lens)
            fback_h = tde4.getLensFBackHeight(lens)
            p_aspect = tde4.getLensPixelAspect(lens)
            focal = tde4.getCameraFocalLength(cam, 1)
            lco_x = tde4.getLensLensCenterX(lens)
            lco_y = tde4.getLensLensCenterY(lens)

            # convert filmback to inch...
            fback_w = fback_w/2.54
            fback_h = fback_h/2.54
            lco_x_in = -lco_x/2.54
            lco_y_in = -lco_y/2.54

            # convert focal length to mm...
            focal = focal*10.0

            # get the focalLenght
            # fotalLenght = tde4.getLensFocalLength(lens) # UNUSED

            # get the focusDistance
            # focus = tde4.getLensFocus(lens) # UNUSED

            # create camera
            f.write("\n")
            f.write("// create camera %s...\n" % cameraName)
            f.write("string $cameraNodes[] = `camera -name \"camera_%s\" -hfa %.15f  -vfa %.15f -fl %.15f -ncp 0.01 -fcp 10000 -shutterAngle 180 -ff \"overscan\"`;\n" % (cameraName, fback_w, fback_h, focal))
            f.write("string $cameraTransform = $cameraNodes[0];\n")
            f.write("string $cameraShape = $cameraNodes[1];\n")
            f.write("xform -zeroTransformPivots -rotateOrder zxy $cameraTransform;\n")
            f.write("setAttr ($cameraShape+\".horizontalFilmOffset\") %.15f;\n" % lco_x_in);
            f.write("setAttr ($cameraShape+\".verticalFilmOffset\") %.15f;\n" % lco_y_in);
            f.write('addAttr -ln "distortion_model" -dt "string" $cameraShape;\n');
            f.write('setAttr -type "string" ($cameraShape + ".distortion_model") %s;\n' % model_maya)
            '''
            for para in (tools.getLDmodelParameterList(model)):
                f.write('addAttr -ln %s -dt "string" $cameraShape;\n'%tools.getLDmodelMayaParameterName(para));
                f.write('setAttr -type "string" ($cameraShape + ".%s") %s;\n'%(tools.getLDmodelMayaParameterName(para),tde4.getLensLDAdjustableParameter(lens, para, fotalLenght, focus)))
            '''
            f.write('addAttr -ln "pixel_aspect_ratio" -at "float" $cameraShape;\n');
            f.write('setAttr ($cameraShape + ".pixel_aspect_ratio") %s;\n'%p_aspect)
            '''
            'f.write('addAttr -ln "plate_resolution_x" -at "long" $cameraShape;\n');
            f.write('setAttr ($cameraShape + ".plate_resolution_x") %s;\n'%rez_x)
            f.write('addAttr -ln "plate_resolution_y" -at "long" $cameraShape;\n');
            f.write('setAttr ($cameraShape + ".plate_resolution_y") %s;\n'%rez_y)
            '''
            f.write('addAttr -ln "frameOffset" -at "long" $cameraShape;\n');
            f.write("setAttr ($cameraShape + \".frameOffset\") %s;\n" % offset)
            f.write('addAttr -ln "lcoX" -at "double" $cameraShape;\n');
            f.write("setAttr ($cameraShape + \".lcoX\") %s;\n" % lco_x)
            f.write('addAttr -ln "lcoY" -at "double" $cameraShape;\n');
            f.write("setAttr ($cameraShape + \".lcoY\") %s;\n" % lco_y)
            f.write('addAttr -ln "lcoXin" -at "double" $cameraShape;\n');
            f.write("setAttr ($cameraShape + \".lcoXin\") %s;\n" % lco_x_in)
            f.write('addAttr -ln "lcoYin" -at "double" $cameraShape;\n');
            f.write("setAttr ($cameraShape + \".lcoYin\") %s;\n" % lco_y_in)
            p3d = tde4.getPGroupPosition3D(campg, cam,1)
            p3d = convertZup(p3d, yup)
            f.write("xform -translation %.15f %.15f %.15f $cameraTransform;\n" % (p3d[0], p3d[1], p3d[2]))
            r3d = tde4.getPGroupRotation3D(campg, cam,1)
            rot = convertToAngles(r3d)
            f.write("xform -rotation %.15f %.15f %.15f $cameraTransform;\n" % rot)
            f.write("xform -scale 1 1 1 $cameraTransform;\n")

            # image plane...
            f.write("\n")
            f.write("// create image plane...\n")
            f.write("string $imagePlanes[] = `imagePlane`;\n")
            f.write("string $imagePlane = $imagePlanes[1];\n")
            f.write("select $imagePlane;\n")
            f.write("string $imagePlaneTransfo[] = `pickWalk -d up`;\n")
            f.write("select -cl;\n")
            f.write("cameraImagePlaneUpdate ($cameraShape, $imagePlane);\n")
            f.write("setAttr ($imagePlane + \".frameOffset\") %s;\n" % offset)
            f.write("setAttr ($imagePlane + \".offsetX\") %.15f;\n" % lco_x)
            f.write("setAttr ($imagePlane + \".offsetY\") %.15f;\n" % lco_y)
            f.write("setAttr ($imagePlane + \".type\") 1;\n")
            f.write("parent $imagePlaneTransfo[0] $cameraTransform;\n")

            path = tde4.getCameraPath(cam)
            sattr = tde4.getCameraSequenceAttr(cam)
            if camType == "SEQUENCE":
                f.write("setAttr ($imagePlane+\".useFrameExtension\") 1;\n")
                f.write("expression -n \"frame_ext_expression\" -s($imagePlane+\".frameExtension=frame\");\n")
                pathPrepared = prepareImagePath(path, sattr[0])
            else:
                f.write("setAttr ($imagePlane+\".useFrameExtension\") 0;\n")
                pathPrepared = path.replace("\\", "/")

            f.write("setAttr ($imagePlane + \".imageName\") -type \"string\" \"%s\";\n" % (pathPrepared))

            f.write("setAttr ($imagePlane + \".fit\") 4;\n")
            f.write("setAttr ($imagePlane + \".displayOnlyIfCurrent\") 1;\n")
            f.write("setAttr ($imagePlane  + \".depth\") (9000/2);\n")

            # parent camera to scene group...
            f.write("\n")
            f.write("// parent camera to scene group...\n")
            f.write("parent $cameraTransform $sceneGroupName;\n")

            if camType == "REF_FRAME":  # and hide_ref:
                f.write("setAttr ($cameraTransform +\".visibility\") 0;\n")

            # animate camera...
            if camType != "REF_FRAME":
                f.write("\n")
                f.write("// animating camera %s...\n" % cameraName)
                f.write("playbackOptions -min %d -max %d;\n" % (
                                                            1+frame0,
                                                            noframes+frame0)
                        )
                f.write("\n")

            frame = 1
            rot0 = None

            while frame <= noframes:
                # rot/pos...
                p3d = tde4.getPGroupPosition3D(campg, cam, frame)
                p3d = convertZup(p3d, yup)
                r3d = tde4.getPGroupRotation3D(campg, cam, frame)
                rot = convertToAngles(r3d)

                if frame > 1:
                    rot = [angleMod360(rot0[0], rot[0]),
                           angleMod360(rot0[1], rot[1]),
                           angleMod360(rot0[2], rot[2])]
                rot0 = rot

                f.write("setKeyframe -at translateX -t %d -v %.15f $cameraTransform; " % (frame+frame0, p3d[0]))
                f.write("setKeyframe -at translateY -t %d -v %.15f $cameraTransform; " % (frame+frame0, p3d[1]))
                f.write("setKeyframe -at translateZ -t %d -v %.15f $cameraTransform; " % (frame+frame0, p3d[2]))
                f.write("setKeyframe -at rotateX -t %d -v %.15f $cameraTransform;    " % (frame+frame0, rot[0]))
                f.write("setKeyframe -at rotateY -t %d -v %.15f $cameraTransform;    " % (frame+frame0, rot[1]))
                f.write("setKeyframe -at rotateZ -t %d -v %.15f $cameraTransform;    " % (frame+frame0, rot[2]))

                # focal length...
                focal = tde4.getCameraFocalLength(cam, frame)
                focal = focal*10.0
                f.write("setKeyframe -at focalLength -t %d -v %.15f $cameraShape;\n" % (frame+frame0, focal))

                frame += 1

            # set Distortion
            f.write('addAttr -ln "distortion" -at "bool" $cameraShape;\n')

            if tools.cameraHasDistortion(cam):
                f.write('setAttr ($cameraShape + ".distortion") 1;\n')
            else:
                f.write('setAttr ($cameraShape + ".distortion") 0;\n')

        # change params as in old export to nuke

        # create new ones
        f.write('addAttr -ln "first_tracked_frame" -at long -dv 0 $cameraShape;\n')
        f.write('addAttr -ln "last_tracked_frame" -at long -dv 0 $cameraShape;\n')
        f.write('addAttr -ln "colorspace"  -dt "string" $cameraShape;\n')
        f.write('addAttr -ln "RenderRez_X" -at long -dv 0 $cameraShape;\n')
        f.write('addAttr -ln "RenderRez_Y" -at long -dv 0 $cameraShape;\n')
        f.write('addAttr -ln "disto_comp" -dt "string" $cameraShape;\n')

        # set values
        minFrame = firstFrame
        f.write('int $minFrame = '+str(minFrame)+';  \n')
        f.write('setAttr ($cameraShape + ".first_tracked_frame") $minFrame;\n')
        maxFrame = lastFrame
        f.write('int $maxFrame = '+str(maxFrame)+'; \n')
        f.write('setAttr ($cameraShape + ".last_tracked_frame") $maxFrame;\n')

        # if firstFrame == lastFrame:
        if 'labo/log' in cameraPath:
            colorspace = getdata.getRootColorSpace(projectName)
        else:
            colorspace = 'sRGB'

        f.write('string $colorspace = "'+colorspace+'"; \n')
        f.write('setAttr -type "string" ($cameraShape + ".colorspace") $colorspace;\n')

        renderOutX = str(max(int(rez_x), int(outSize[cameraIndex].width)))
        renderOutY = str(max(int(rez_y), int(outSize[cameraIndex].height)))

        f.write('int $renderOutX = '+str(renderOutX)+'; \n')

        # TODO if positive disto is other value
        f.write('setAttr ($cameraShape + ".RenderRez_X") $renderOutX; \n')

        # TODO if positive disto is other value
        f.write('int $renderOutY = '+str(renderOutY)+'; \n')
        f.write('setAttr ($cameraShape + ".RenderRez_Y") $renderOutY; \n')

        f.write('string $exportFileName = "' + exportPath.replace("\\", "/") + '_undisto/' + cameraName + '_undisto.nk";\n')
        f.write('setAttr -type "string"($cameraShape + ".disto_comp") $exportFileName; \n')

        # other values

        coefX = 1.0*int(renderOutX) / rez_x
        coefY = 1.0*int(renderOutY) / rez_y

        oldhfa = fback_w
        oldvfa = fback_h

        newHfa = str(coefX * oldhfa)
        newVfa = str(coefY * oldvfa)

        f.write('setAttr ($cameraShape + ".hfa") '+newHfa+'; \n')
        f.write('setAttr ($cameraShape + ".vfa") '+newVfa+'; \n')

        f.write('string $initIplane[] = `listConnections -type "imagePlane" $cameraShape`; \n')
        f.write('string $camIplaneShape = $initIplane[0]; \n')
        f.write('setAttr ($camIplaneShape + ".sizeX") '+newHfa+'; \n')
        f.write('setAttr ($camIplaneShape + ".sizeY") '+newVfa+'; \n')

        undistoFilePath = camInfo.getUndistoImagePath(app='maya', date=date)

        f.write('setAttr -type "string" ($camIplaneShape + ".imageName") "'+undistoFilePath+'";  \n')

        f.write('setAttr ($camIplaneShape + ".type") 0;  \n')

        # camera rendeable
        f.write('setAttr ($cameraShape + ".renderable") 1;  \n')

        # keys in some params
        touchParam(f, '$cameraShape + ".hfa"', insertKey=True, lock=False)
        touchParam(f, '$cameraShape + ".vfa"', insertKey=True, lock=False)
        pixelAspectRatioParamName = '$cameraShape + ".pixel_aspect_ratio"'
        touchParam(f, pixelAspectRatioParamName, insertKey=True, lock=True)
        renderRezXparamName = '$cameraShape + ".RenderRez_X"'
        touchParam(f, renderRezXparamName, insertKey=True, lock=True)
        renderRezTparamName = '$cameraShape + ".RenderRez_Y"'
        touchParam(f, renderRezTparamName, insertKey=True, lock=True)
        touchParam(f, '$cameraShape + ".distortion"')

        touchParam(f, '$cameraShape + ".first_tracked_frame"', insertKey=False)
        touchParam(f, '$cameraShape + ".last_tracked_frame"', insertKey=False)
        touchParam(f, '$cameraShape + ".colorspace"', insertKey=False)
        touchParam(f, '$cameraShape + ".frameOffset"', insertKey=False)

        # set render globals
        f.write('setAttr "defaultResolution.width"  ' + renderOutX + '; \n')
        f.write('setAttr "defaultResolution.height" ' + renderOutY + '; \n')

        # delete old params
        f.write('deleteAttr ($cameraShape + ".distortion_model");     \n')
        f.write('deleteAttr ($cameraShape + ".lcoX");                 \n')
        f.write('deleteAttr ($cameraShape + ".lcoY");                 \n')
        f.write('deleteAttr ($cameraShape + ".lcoXin");               \n')
        f.write('deleteAttr ($cameraShape + ".lcoYin");               \n')


def exportCameraPoints(f, campg):
    #
    # write camera point group...
    f.write("\n")
    f.write("// create camera point group...\n")
    name = "cameraPGroup_%s_1" % tools.validName(tde4.getPGroupName(campg))
    f.write("string $pointGroupName = `group -em -name  \"%s\" -parent $sceneGroupName`;\n" % name)
    f.write("$pointGroupName = ($sceneGroupName + \"|\" + $pointGroupName);\n")
    f.write("\n")

    # write points...
    l = tde4.getPointList(campg)
    particleExists = 0
    f.write("\nparticle;")
    for p in l:
        if tde4.isPointCalculated3D(campg, p):
            name = tde4.getPointName(campg, p)
            name = "p%s" % tools.validName(name)
            p3d = tde4.getPointCalcPosition3D(campg, p)
            p3d = convertZup(p3d, yup)
            f.write("\n")
            if 'agisoft_' in name:
                particleStr = "emit -object particle1 -pos %.15f %.15f %.15f ;"
                f.write(particleStr % (p3d[0], p3d[1], p3d[2]))
                particleExists = 1
            else:
                f.write("// create point %s...\n" % name)
                f.write("string $locator = stringArrayToString(`spaceLocator -name %s`, \"\");\n" % name)
                f.write("$locator = (\"|\" + $locator);\n")
                f.write("xform -t %.15f %.15f %.15f $locator;\n" % (p3d[0],
                                                                    p3d[1],
                                                                    p3d[2]))
                f.write("parent $locator $pointGroupName;\n")

    f.write("\n")
    f.write("xform -zeroTransformPivots -rotateOrder zxy -scale 1.000000 1.000000 1.000000 $pointGroupName;\n")
    f.write("\n")
    if particleExists == 1:
        f.write("particle -q -ct particle1;")
        f.write('disconnectAttr time1.outTime particleShape1.currentTime;\n')
        f.write('saveInitialState -atr "pos" particle1;\n')
        f.write('parent "particle1" $sceneGroupName;\n')
        f.write('rename "Scene|particle1" "agisoft_points";\n')
    else:
        f.write('delete "particle1";')


def exportMocaObjects(f, frameStart):
    #
    # write object/mocap point groups...
    frameStart = int(frameStart)
    frame0 = frameStart - 1

    camera = tde4.getCurrentCamera()
    noframes = tde4.getCameraNoFrames(camera)
    pgl = tde4.getPGroupList()
    index = 1
    for pg in pgl:
        if tde4.getPGroupType(pg) == "OBJECT" and camera is not None:
            f.write("\n")
            f.write("// create object point group...\n")
            groupValidName = tools.validName(tde4.getPGroupName(pg))
            pgname = "objectPGroup_%s_%d_1" % (groupValidName, index)
            index += 1
            f.write("string $pointGroupName = `group -em -name  \"%s\" -parent $sceneGroupName`;\n" % pgname)
            f.write("$pointGroupName = ($sceneGroupName + \"|\" + $pointGroupName);\n")

            # write points...
            l = tde4.getPointList(pg)
            for p in l:
                if tde4.isPointCalculated3D(pg, p):
                    name = tde4.getPointName(pg, p)
                    name = "p%s" % tools.validName(name)
                    p3d = tde4.getPointCalcPosition3D(pg, p)
                    p3d = convertZup(p3d, yup)
                    if 'agisoft' not in name:
                        f.write("\n")
                        f.write("// create point %s...\n" % name)
                        f.write("string $locator = stringArrayToString(`spaceLocator -name %s`, \"\");\n" % name)
                        f.write("$locator = (\"|\" + $locator);\n")
                        f.write("xform -t %.15f %.15f %.15f $locator;\n" % (p3d[0],
                                                                            p3d[1],
                                                                            p3d[2])
                               )
                        f.write("parent $locator $pointGroupName;\n")

            f.write("\n")
            scale = tde4.getPGroupScale3D(pg)
            f.write("xform -zeroTransformPivots -rotateOrder zxy -scale %.15f %.15f %.15f $pointGroupName;\n" % (scale, scale, scale))

            # animate object point group...
            f.write("\n")
            f.write("// animating point group %s...\n" % pgname)
            frame = 1
            rot0 = None

            while frame <= noframes:
                # rot/pos...
                p3d = tde4.getPGroupPosition3D(pg, camera, frame)
                p3d = convertZup(p3d, yup)
                r3d = tde4.getPGroupRotation3D(pg, camera, frame)
                rot = convertToAngles(r3d)
                if frame > 1:
                    rot = [angleMod360(rot0[0], rot[0]),
                           angleMod360(rot0[1], rot[1]),
                           angleMod360(rot0[2], rot[2])]
                rot0 = rot
                f.write("setKeyframe -at translateX -t %d -v %.15f $pointGroupName; " % (frame+frame0, p3d[0]))
                f.write("setKeyframe -at translateY -t %d -v %.15f $pointGroupName; " % (frame+frame0, p3d[1]))
                f.write("setKeyframe -at translateZ -t %d -v %.15f $pointGroupName; " % (frame+frame0, p3d[2]))
                f.write("setKeyframe -at rotateX -t %d -v %.15f $pointGroupName; " % (frame+frame0, rot[0]))
                f.write("setKeyframe -at rotateY -t %d -v %.15f $pointGroupName; " % (frame+frame0, rot[1]))
                f.write("setKeyframe -at rotateZ -t %d -v %.15f $pointGroupName;\n" % (frame+frame0, rot[2]))

                frame += 1

        # mocap point groups...
        if tde4.getPGroupType(pg) == "MOCAP" and camera is not None:
            f.write("\n")
            f.write("// create mocap point group...\n")
            groupValidName = tools.validName(tde4.getPGroupName(pg))
            pgname = "objectPGroup_%s_%d_1" % (groupValidName, index)
            index += 1
            f.write("string $pointGroupName = `group -em -name  \"%s\" -parent $sceneGroupName`;\n" % pgname)
            f.write("$pointGroupName = ($sceneGroupName + \"|\" + $pointGroupName);\n")

            # write points...
            l = tde4.getPointList(pg)
            for p in l:
                if tde4.isPointCalculated3D(pg, p):
                    name = tde4.getPointName(pg, p)
                    name = "p%s" % tools.validName(name)
                    p3d = tde4.getPointMoCapCalcPosition3D(pg, p, camera, 1)
                    p3d = convertZup(p3d, yup)
                    f.write("\n")
                    f.write("// create point %s...\n" % name)
                    f.write("string $locator = stringArrayToString(`spaceLocator -name %s`, \"\");\n" % name)
                    f.write("$locator = (\"|\" + $locator);\n")
                    f.write("xform -t %.15f %.15f %.15f $locator;\n" % (p3d[0],
                                                                        p3d[1],
                                                                        p3d[2])
                            )
                    for frame in range(1, noframes+1):
                        p3d = tde4.getPointMoCapCalcPosition3D(pg, p, camera,
                                                               frame)
                        p3d = convertZup(p3d, yup)
                        f.write("setKeyframe -at translateX -t %d -v %.15f $locator; " % (frame+frame0, p3d[0]))
                        f.write("setKeyframe -at translateY -t %d -v %.15f $locator; " % (frame+frame0, p3d[1]))
                        f.write("setKeyframe -at translateZ -t %d -v %.15f $locator; " % (frame+frame0, p3d[2]))
                    f.write("parent $locator $pointGroupName;\n")

            f.write("\n")
            scale = tde4.getPGroupScale3D(pg)
            f.write("xform -zeroTransformPivots -rotateOrder zxy -scale %.15f %.15f %.15f $pointGroupName;\n" % (scale, scale, scale))

            # animate mocap point group...
            f.write("\n")
            f.write("// animating point group %s...\n" % pgname)
            frame = 1
            while frame <= noframes:
                # rot/pos...
                p3d = tde4.getPGroupPosition3D(pg, camera, frame)
                p3d = convertZup(p3d, yup)
                r3d = tde4.getPGroupRotation3D(pg, camera, frame)
                rot = convertToAngles(r3d)
                if frame > 1:
                    rot = [angleMod360(rot0[0], rot[0]),
                           angleMod360(rot0[1], rot[1]),
                           angleMod360(rot0[2], rot[2])]
                rot0 = rot
                f.write("setKeyframe -at translateX -t %d -v %.15f $pointGroupName; " % (frame+frame0, p3d[0]))
                f.write("setKeyframe -at translateY -t %d -v %.15f $pointGroupName; " % (frame+frame0, p3d[1]))
                f.write("setKeyframe -at translateZ -t %d -v %.15f $pointGroupName; " % (frame+frame0, p3d[2]))
                f.write("setKeyframe -at rotateX -t %d -v %.15f $pointGroupName; " % (frame+frame0, rot[0]))
                f.write("setKeyframe -at rotateY -t %d -v %.15f $pointGroupName; " % (frame+frame0, rot[1]))
                f.write("setKeyframe -at rotateZ -t %d -v %.15f $pointGroupName;\n" % (frame+frame0, rot[2]))

                frame += 1


def checkCameraGroups():
    campg = None
    pgl = tde4.getPGroupList()
    for pg in pgl:
        if tde4.getPGroupType(pg) == "CAMERA":
            campg = pg
    return campg


# Main script
def toMaya(params):
    # print "To Maya - Start"

    # search for camera point group...
    campg = checkCameraGroups()
    if campg is None:
        tde4.postQuestionRequester("Export Maya...",
                                   "Error, there is no camera point group.",
                                   "Ok")
        return

    # getParams
    filepath = params['file_browser'] + '.mel'

    cameras = params['cameras']
    camerasOutSize = params['camerasOutSize']
    camerasFrameStart = params['camerasFirstFrame']

    # openFile
    tools.ensure_dir(filepath)
    f = open(filepath, 'w')

    # write header
    f.write("//\n")
    f.write("// Maya/MEL export data written by %s\n" % tde4.get3DEVersion())
    f.write("//\n")
    f.write("// All lengths are in centimeter, all angles are in degree.\n")
    f.write("//\n\n")

    # write scene group...
    f.write("// create scene group...\n")
    f.write("string $sceneGroupName = `group -em -name \"Scene\"`;\n")

    # wrtie cameras
    exportCameras(f, cameras, camerasFrameStart, params['file_browser'],
                  campg, camerasOutSize, params['date'])

    # write camera points : campg

    exportCameraPoints(f, campg)

    # write moca / Objects
    exportMocaObjects(f, camerasFrameStart[0])

    # write global (scene node) transformation...
    p3d = tde4.getScenePosition3D()
    p3d = convertZup(p3d, yup)
    r3d = tde4.getSceneRotation3D()
    rot = convertToAngles(r3d)
    s = tde4.getSceneScale3D()
    f.write("xform -zeroTransformPivots -rotateOrder zxy -translation %.15f %.15f %.15f -scale %.15f %.15f %.15f -rotation %.15f %.15f %.15f $sceneGroupName;\n\n" % (p3d[0], p3d[1], p3d[2], s, s, s, rot[0], rot[1], rot[2]))

    f.write("\n")

    # close file
    f.close()
    # print "To Maya - End"
