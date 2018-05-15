# v150629 1057
# 3DE4.script.hide: true
import os
import string
import re

import tde4


# RESOLTION CLASS
class Resolution(object):
    def __init__(self, width, height):

        self.width = width
        self.height = height

    def __str__(self):
        strRep = 'width : {width}, height :{height}'
        strRep = strRep.format(width=str(self.width),
                               height=str(self.height))
        return strRep

    def __repr__(self,):
        return self.__str__()


# General Outils
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def validName(name):
    name = name.replace("-", "_")
    name = name.replace(" ", "_")
    name = name.replace("\n", "")
    name = name.replace("\r", "")
    return name


def nukify_name(s):
    if s == "":
        return "_"
    if s[0] in "0123456789":
        t = "_"
    else:
        t = ""
    t += string.join(re.sub("[+,:; _-]+", "_", s.strip()).split())
    return t


# 3DE Specific OUTILS
class DistorsionParameters(object):
    def __init__(self,):
        self.Filter = None
        self.tde4_focal_length_cm = None
        self.tde4_filmback_width_cm = None
        self.tde4_filmback_height_cm = None
        self.tde4_pixel_aspect = None
        self.Distortion = None
        self.Anamorphic_Squeeze = None
        self.Curvature_X = None
        self.Curvature_Y = None
        self.Quartic_Distortion = None
        self.name = None


writeFilePathBase = "//{lan}/{disk}/{projectName}/{shot}/images/undisto/"
writeFilePathBase += "{date}_{camShortName}/{imagesName}-undisto{padding}.jpg"


class TDECamInfo(object):

    def __init__(self, cam, index):
        self.cam = cam
        self.index = index

        self.getInfoCam()
        self.getInfoCamPath()

    def getInfoCam(self):
        cam = self.cam
        index = self.index
        self.offset = tde4.getCameraFrameOffset(cam)
        self.cameraPath = tde4.getCameraPath(cam).replace('\\',
                                                          '/')
        self.camType = tde4.getCameraType(cam)
        self.noframes = tde4.getCameraNoFrames(cam)
        self.lens = tde4.getCameraLens(cam)
        self.rez_x = tde4.getCameraImageWidth(cam)
        self.rez_y = tde4.getCameraImageHeight(cam)
        self.model = tde4.getLensLDModel(self.lens)
        self.firstFrame = tde4.getCameraSequenceAttr(cam)[0]
        self.name = "%s_%s_1" % (validName(tde4.getCameraName(cam)),
                                 index)
        self.lastFrame = '%d' % (self.firstFrame+self.noframes-1)
        self.firstFrame = '%d' % self.firstFrame
        self.focal_cm = tde4.getCameraFocalLength(cam, 1)

    def getShortName(self):
        return validName('camera_%s' % self.name)

    def isSeq(self):
        return (self.lastFrame != self.firstFrame)

    def getInfoCamPath(self):
        pathSplited = self.cameraPath.replace('//', '').split('/')

        self.lan = pathSplited[0]
        self.disk = pathSplited[1]
        self.projectName = pathSplited[2]

        self.shot = pathSplited[3]

        self.shotName = pathSplited[-1]
        self.shotDir = pathSplited[4]

        shotNameSplited = self.shotName.split(".")
        if len(shotNameSplited) == 3:
            self.imagesName = shotNameSplited[0]
            self.imagesPad = shotNameSplited[1]
            self.imagesExtension = shotNameSplited[2]
        else:
            self.imagesPad = shotNameSplited[0].split('_')[-1]
            self.imagesName = shotNameSplited[0].split(self.imagesPad)[0]
            self.imagesExtension = shotNameSplited[1]

        self.pad = str(len(self.imagesPad))

        self.imageNameLong = self.shotName[:-4]

        projectPatbBase = "//{lan}/{disk}/{projectName}/"
        self.projectPath = projectPatbBase.format(lan=self.lan,
                                                  disk=self.disk,
                                                  projectName=self.projectName)

    def getPaddingFormat(self, usePercent=True):
        if not self.isSeq():
            return ''
        elif usePercent:
            return (".%0" + self.pad + "d")
        else:
            return '#'*int(self.pad)

    def getImagesNameFormat(self):
        return self.imagesName if self.isSeq() else self.imageNameLong

    def getUndistoImagePath(self, app, date):
        paddingFormat = self.getPaddingFormat(usePercent=True)
        imagesNameFormat = self.getImagesNameFormat()

        filePath = writeFilePathBase.format(lan=self.lan,
                                            disk=self.disk,
                                            projectName=self.projectName,
                                            shot=self.shot,
                                            date=date,
                                            camShortName=self.getShortName(),
                                            imagesName=imagesNameFormat,
                                            padding=paddingFormat)
        if app == 'maya' and self.isSeq():
            filePath = filePath % int(self.firstFrame)

        return filePath

    def getWriteNodeName(self):
        if self.isSeq():
            writeNodeName = 'WRT_UND_'
        else:
            writeNodeName = 'WRT_UND_REF'

        writeNodeName += self.getShortName()

        return writeNodeName


class TDELensInfo(object):

    def __init__(self, lens):
        self.lens = lens
        self.getInfoLens()

    def getInfoLens(self):
        lens = self.lens
        self.fback_w_cm = tde4.getLensFBackWidth(lens)
        self.fback_h_cm = tde4.getLensFBackHeight(lens)
        self.p_aspect = tde4.getLensPixelAspect(lens)
        self.lco_x = tde4.getLensLensCenterX(lens)
        self.lco_y = tde4.getLensLensCenterY(lens)


def correctCameraPath(cameraTmp):
    if tde4.getCameraType(cameraTmp) == 'REF_FRAME':
        return True

    cameraPath = tde4.getCameraPath(cameraTmp).replace('\\', '/')
    shotNameSplited = cameraPath.replace('//', '').split('/')[-1].split(".")

    if len(shotNameSplited) == 3:
        return True
    else:
        shotNameSplited = shotNameSplited[0].split('_')
    return (len(shotNameSplited) >= 2)


def getDistorsionParametersFromLenClassic(lens, camShortName, focal_cm):
    lensInfo = TDELensInfo(lens)

    # get the focalLenght
    fotalLenght = tde4.getLensFocalLength(lens)
    # get the focusDistance
    focus = tde4.getLensFocus(lens)

    distorsionParameters = DistorsionParameters()
    distorsionParameters.Filter = 'Simon'
    distorsionParameters.tde4_focal_length_cm = repr(focal_cm)
    distorsionParameters.tde4_filmback_width_cm = repr(lensInfo.fback_w_cm)
    distorsionParameters.tde4_filmback_height_cm = repr(lensInfo.fback_h_cm)
    distorsionParameters.tde4_pixel_aspect = repr(lensInfo.p_aspect)
    paramDistortion = tde4.getLensLDAdjustableParameter(lens,
                                                        'Distortion',
                                                        fotalLenght,
                                                        focus)
    distorsionParameters.Distortion = repr(paramDistortion)
    paramASqueeze = tde4.getLensLDAdjustableParameter(lens,
                                                      'Anamorphic Squeeze',
                                                      fotalLenght,
                                                      focus)
    distorsionParameters.Anamorphic_Squeeze = repr(paramASqueeze)
    paramCurvatureX = tde4.getLensLDAdjustableParameter(lens,
                                                        'Curvature X',
                                                        fotalLenght,
                                                        focus)
    distorsionParameters.Curvature_X = repr(paramCurvatureX)
    paramCurvatureY = tde4.getLensLDAdjustableParameter(lens,
                                                        'Curvature Y',
                                                        fotalLenght,
                                                        focus)
    distorsionParameters.Curvature_Y = repr(paramCurvatureY)
    paramQuarticDist = tde4.getLensLDAdjustableParameter(lens,
                                                         'Quartic Distortion',
                                                         fotalLenght,
                                                         focus)
    distorsionParameters.Quartic_Distortion = repr(paramQuarticDist)
    distorsionParameters.name = 'LD_3DE_Classic_LD_Model1_' + camShortName

    distorsionParameters.tde4_lens_center_offset_x_cm = '0'  # TODO
    distorsionParameters.tde4_lens_center_offset_y_cm = '0'  # TODO

    return distorsionParameters


def getLDmodelParameterList(model):
    l = []
    for p in range(tde4.getLDModelNoParameters(model)):
        l.append(tde4.getLDModelParameterName(model, p))
    return l


def getLDmodelMayaParameterName(para):
    p = para.replace(' ', '_')
    p = p.replace('-', '_')
    return p


def getLDmodelNukeNodeName(model):
    if model == '3DE Classic LD Model':
        n = 'tde4_ldp_classic_3de_mixed'
    if model == '3DE4 Radial - Standard, Degree 4':
        n = 'tde4_ldp_radial_decentered_deg_4_cylindric'
    if model == '3DE4 Radial - Fisheye, Degree 8':
        n = 'tde4_ldp_radial_deg_8'
    if model == '3DE4 Anamorphic, Degree 6':
        n = 'tde4_ldp_anamorphic_deg_6'
    if model == '3DE4 Anamorphic - Standard, Degree 4':
        n = 'tde4_ldp_anamorphic_deg_4_rotate_squeeze_xy'
    return n


def getCameraModel(camera):
    lens = tde4.getCameraLens(camera)
    model = tde4.getLensLDModel(lens)
    return model


def isClassicModel(camera):
    return (getCameraModel(camera) == '3DE Classic LD Model')


def isRadialFishEye(camera):
    return (getCameraModel(camera) == '3DE4 Radial - Fisheye, Degree 8')


def isRadialStandar(camera):
    return (getCameraModel(camera) == '3DE4 Radial - Standard, Degree 4')


def isAnamorphicStandar(camera):
    return (getCameraModel(camera) == '3DE4 Anamorphic - Standard, Degree 4')


def isAnamorphic(camera):
    return (getCameraModel(camera) == '3DE4 Anamorphic, Degree 6')


def cameraHasDistortionClassic(camera):
    cameraLens = tde4.getCameraLens(camera)
    dpClassic = getDistorsionParametersFromLenClassic(cameraLens, '', 1)
    if float(dpClassic.Distortion) == 0 and\
       float(dpClassic.Anamorphic_Squeeze) == 1 and\
       float(dpClassic.Curvature_X) == 0 and\
       float(dpClassic.Curvature_Y) == 0 and\
       float(dpClassic.Quartic_Distortion) == 0:
        return False
    else:
        return True


def cameraHasDistortion(camera):
    if isClassicModel(camera):
        return cameraHasDistortionClassic(camera)
    else:
        lens = tde4.getCameraLens(camera)
        model = getCameraModel(camera)
        for parameterName in getLDmodelParameterList(model):
            defaultValue = tde4.getLDModelParameterDefault(model,
                                                           parameterName)
            # distorsionMode
            dyndistmode = tde4.getLensDynamicDistortionMode(lens)
            if dyndistmode == "DISTORTION_STATIC":
                actualValue = tde4.getLensLDAdjustableParameter(lens,
                                                                parameterName,
                                                                1,
                                                                1)
                if defaultValue != actualValue:
                    return True
            else:
                num_frames = tde4.getCameraNoFrames(camera)
                for frame in range(1, num_frames + 1):
                    focal = tde4.getCameraFocalLength(camera, frame)
                    focus = tde4.getCameraFocus(camera, frame)
                    actualValue = tde4.getLensLDAdjustableParameter(
                                                                lens,
                                                                parameterName,
                                                                focal,
                                                                focus
                                                                    )
                    if defaultValue != actualValue:
                        return True
        return False


def supportedCameraMode(camera):
    lens = tde4.getCameraLens(camera)
    model = tde4.getLensLDModel(lens)
    return model in [
                        '3DE Classic LD Model',
                        '3DE4 Radial - Fisheye, Degree 8',
                        '3DE4 Radial - Standard, Degree 4',
                        '3DE4 Anamorphic - Standard, Degree 4',
                        '3DE4 Anamorphic, Degree 6',
                    ]


def validCamera(camera):
    return correctCameraPath(camera) and supportedCameraMode(camera)
