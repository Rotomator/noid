'''
#
# Here are defined the tools to comunicate with the dispacher Royal Render (RR)
#
#
'''
#from cgev.pipeline.appconnector import connectortools

import xml.etree.ElementTree as xml
import os

from subprocess import Popen

#from time import strftime
#from time import gmtime

#from cgev.common import environment
#from cgev.common import envvars
#from cgev.common import files
#from cgev.common import newconfig
#from cgev.common import helpers
#from cgev.common import log
#from cgev.common import texts
#from cgev.common import decoder
#from cgev.common import sealer
#from cgev.common import resourceslocation

import noid_utils as nut

#if connectortools.appIsNuke():
#    import nuke

rrRoot = os.getenv("RR_ROOT").replace('\\', '/')

submitter = rrRoot + "/bin/win/rrSubmitterconsole.exe"
submitterUI = rrRoot + "/bin/win/rrSubmitter.exe"
ffmpeg = rrRoot + '/render_apps/scripts/ffmpeg/bin/ffmpeg.exe'
ffmpegLast = rrRoot + '/render_apps/scripts/ffmpegLast/bin/ffmpeg.exe'
font = rrRoot + '/render_apps/scripts/ffmpeg/bin/Arial.ttf'

# POUR LES EXEMPLES DE COMMANDS ELLE SONT ICI:
# \\STORB\diskb\RoyalRender\sub\cfg_global\submitter_first.txt

# Job Colors
BatchColor_Nuke = '4'  # Yellow
BatchColor_3DE = '2'  # Green
BatchColor_ToQt = '1'  # Red
BatchColor_RealFlow = '3'  # Blue
BatchColor_BatchTask = '7'  # Gray
BatchColor_Mp4 = BatchColor_BatchTask
BatchColor_Seal = BatchColor_BatchTask
BatchColor_Maya = '5'


class Pulls(object):
    '''
    class to define the available pools
    '''
    all = 'ALL'
    ram64 = '64go'
    realflow = 'Realflow'
    batchTasks = 'batch_tasks'
    egg = 'egg'
    mayaNight = 'mayanight'
    render3D = 'render3D'
    renderFarm = 'renderfarm'
    toQt = 'toQT'
    workstations = 'workstations'

# Default Pulls
pullNk = Pulls.renderFarm
pullNkEgg = Pulls.egg
pull3DE = Pulls.renderFarm
pullToQt = Pulls.toQt
pullToMp4 = Pulls.batchTasks
pullToSeal = Pulls.batchTasks
pullToVrayProxy = Pulls.renderFarm


class Batch(object):
    '''
    original class created by Christian
    creates an xml then submit it
    @var _self._defautltAttrib: is the list of valid attributes that can be passed to the xml, others are ignored
    '''

    def __init__(self, parameters={}):
        '''
        constructor
        @param parameters: dict of parameters to pass name, value
        '''

        self._root = xml.Element('RR_Job_File')
        self._root.set('syntax_version', '6.0')

        for elem in parameters.keys():
            params = xml.Element(elem)
            params.text = parameters[elem]
            self._root.append(params)

        self._defautltAttrib = [
                                'SceneName',
                                'Layer',
                                'Software',
                                'Version',
                                'Tiled',
                                'JobBit',
                                'SendAppBit',
                                'SeqStart',
                                'SeqEnd',
                                'SeqStep',
                                'ImageFilename',
                                'ImageFileNameVariables',
                                'ImageDir',
                                'ImageFramePadding',
                                'ImageSingleOutputFile',
                                'ImageExtension',
                                'CustomA',
                                'CustomB',
                                'CustomC',
                                'SeqDivMin',
                                'SeqDivMax',
                                'SeqDivideEnabled',
                                'MaxClientsAtATime',
                                'disabled',
                                'verboseLevel',
                                'renderQuality',
                                'Priority',
                                'NotifyFinishParam',
                                'NotifyFinishWhen',
                                'RRO_DoNotCheckForFrames',
                                'RRO_LittleJob',
                                'PrePostCommand',
                                'Clients',
                                'SceneOS',
                                'AutoDeleteEnabled',
                                'SubmitterParameter',
                                'Renderer',
                                'PreID',
                                'RequiredPlugins',
                                'RequiredLicenses',
                                'UserName'
                         ]

    def addJob(self):
        '''
        adds a job to the existing submission
        '''
        job = xml.Element('Job')
        self._root.append(job)
        return job

    def setAttrib(self, job, attrib, value):
        '''
        sets for the job the attribute with its value
        @param job: sub xml entry that contains one job
        @param attrib: name of the attribute to set
        @param value: value of the attribute to set
        '''

        if (attrib in self._defautltAttrib and
                attrib not in self.getAttribs(job)):
            if attrib in self.getAttribs(job):
                att = job.find(attrib)
            else:
                att = xml.Element(attrib)
            att.text = value
            job.append(att)
            return att
        else:
            print attrib + " bad attribute"
            return None

    def getAttribs(self, job):
        '''
        returns all the attributes of a job
        @param job: job to query
        '''
        result = list()
        for child in job:
            result.append(child.tag)
        return result

    def setAttribs(self, job, attribs):
        '''sets multiple attributes to a job
        @param job: sub xml entry that contains one job
        @param attribs:  dict of attrib, value
        '''
        for attrib, value in attribs.items():
            self.setAttrib(job, attrib, value)

    def batch(self, path, UI=False, delete=False):
        '''
        generates the xml and submits the job(s) to RR
        @param path: where to store the xml
        @param UI: bool to see if we use ui submitter or console
        @param delete: enable to force auto delete of the images in commandline version, in UI the question will popup if necessary
        @return: exit  code of RR
        '''

        root = open(path, 'w')
        xml.ElementTree(self._root).write(root)
        root.close()

        # os.system('%s %s' % (submitter,path))
        if UI:
            submit = submitterUI
        else:
            submit = submitter
        command = submit+' '+path
        if not UI and delete:
            command += " -ADE"
        # print command
        p = Popen(command, shell=True)
        # ,stdout=PIPE, stderr=PIPE, stdin=PIPE)
        return p.communicate()


def batchNk(scene, path, first=1, last=1, write='Write1', clients=1,
<<<<<<< HEAD
            nukeVersion='6.0', defaultClientGroup=pullNk,
=======
            nukeVersion='8.0', defaultClientGroup=pullNk,
>>>>>>> c19bfa8b2e3b225b306790e2ed7f77464ba1d0e0
            singleOutPut=False, checkForFrames=True,
            colorId=BatchColor_Nuke, postjobList=list(),
            requiredlicense='', user=''):
    '''
    function to batch nuke files using xml, not used for nuke itself which
    uses standard rrsubmitter/parser

    @see: rrSubmit_Nuke_5.py
    @see: Batch
    @param scene: path of the scene to render
    @param path: path of the output files that RR will seek
    @param first: first frame to render   (int)
    @param last: last frame to render   (int)
    @param write: name of nuke write node to be rendered
    @param clients: number of simult clients
    @param nukeVersion: nuke version to use
    @param defaultClientGroup: name of pool to use
    @param singleOutPut: true to inform rr of a rendering of a single file like mov
    @param checkForFrames: if rr will seek output frames to monitor the render
    @param colorId: color that the job will have in RR
    @todo: needs checks
    @param postjobList:list of post jobs to enable in RR
    @param requiredlicense: name of license that need to be counted for this job
    '''

    submitterParameters = [
                           '"DefaultClientGroup=1~'+defaultClientGroup+'"',
                           '"Color_ID=1~{colorId}"'.format(colorId=colorId),
                           '"PPDeleteJob=1~1"'
                           ]
    if user != '':
        submitterParameters.append('"UserName=0~{0}"'.format(user))

    for postJobName in postjobList:
        submitterParameters.append('"{0}=1~1"'.format(postJobName))

    submitterParameter = ' '.join(submitterParameters)

    thisBatch = Batch(parameters={'SubmitterParameter': submitterParameter})

    job = thisBatch.addJob()

    att = {
            'SceneName': scene,
            'Layer': write,
            'ImageFilename': path,
            'SeqStart': str(first),
            'SeqEnd': str(last),
            'SeqStep': '1',
            'MaxClientsAtATime': str(clients),
            'RRO_DoNotCheckForFrames': 'False',
            'Software': 'Nuke',
            'RequiredLicenses': requiredlicense,
            'Version': nukeVersion,
            'AutoDeleteEnabled': 'True',
            'ImageSingleOutputFile': str(singleOutPut),
            'RRO_DoNotCheckForFrames': str(not checkForFrames),
        }

    thisBatch.setAttribs(job, att)
<<<<<<< HEAD
    path = ("%s\\submitFiles\\nk_%s.xml") % (environment.getCGEVBasePath(),
                                             helpers.dateTime())
=======
    path = ("%s\\submitFiles\\nk_%s.xml") % (os.getenv("NOID_PATH"),nut.dateTimeStr())
>>>>>>> c19bfa8b2e3b225b306790e2ed7f77464ba1d0e0
    return thisBatch.batch(path)


def batch3DE(scene, path, first=1, last=1, write='Write1', clients=1,
             nukeVersion='8.0', defaultClientGroup=pull3DE):
    '''
    same as batchNk but for 3DE-generated nuke files
    additionnal test on write name   WRT_UND_REF  means single output
    file is mandatory. Jobs are auto approved
    @todo: try to integrate in batchNK
    @param scene: path of the scene to render
    @param path: path of the output files that RR will seek
    @param first: first frame to render   (int)
    @param last: last frame to render   (int)
    @param write: name of nuke write node to be rendered
    @param clients: number of simult clients
    @param nukeVersion: nuke version to use
    @param defaultClientGroup: name of pool to use
    '''

    submitterParameters = [
                           '"AutoApproveJob=1~1"',
                           '"DefaultClientGroup=1~'+defaultClientGroup+'"'
                           ]

    submitterParameter = ' '.join(submitterParameters)

    thisBatch = Batch(parameters={'SubmitterParameter': submitterParameter})
    job = thisBatch.addJob()

    att = {
         'SceneName': scene,
         'Layer': write,
         'ImageFilename': path,
         'SeqStart': str(first),
         'SeqEnd': str(last),
         'SeqStep': '1',
         'MaxClientsAtATime': str(clients),
         'RRO_DoNotCheckForFrames': 'False',
         'Software': 'Nuke',
         'Version': nukeVersion,
         'AutoDeleteEnabled': 'True',
         'ImageSingleOutputFile': 'False',
          }

    if "WRT_UND_REF" in write:
        att['ImageSingleOutputFile'] = 'True'

    thisBatch.setAttribs(job, att)
    path = ("%s\\submitFiles\\nk_%s.xml") % (os.getenv("NOID_PATH"),nut.dateTimeStr())
    return thisBatch.batch(path)


#NOT USED ANYMORE
def batchToQtDNX(sequence, first=int(), last=int(), lut='noLut',
                 colorspace='Cineon', dnx=None, infoOnTop="stamp1",
                 defaultClientGroup=pullNk, slateFrame='sf0',
                 cropValues='x0 y0 r1 t1', dateSlate='00/00/0000',
                 artistNameSlate='name', disableGama='True',
                 nameSufix=''
                 ):
    '''
    not used anymore
    was used to batch a .nk that contains external args that are passed as custom parameters directly to RR
    they are parameters of the nuke render within RR job, and they are evaluated at render time
    '''
    if dnx is None:
        print "no dnx description found"
        return -1

    submitterParameters = [
                           '"AutoApproveJob=1~1"',
                           '"PPCopyftrackQTtodeliv=1~1"',
                           '"DefaultClientGroup=1~'+defaultClientGroup+'"',
                           ]

    submitterParameter = ' '.join(submitterParameters)
    thisBatch = Batch(parameters={'SubmitterParameter': submitterParameter})
    job = thisBatch.addJob()

    if not first:
        first = sequence.getFirstFrame()
    if not last:
        last = sequence.getLastFrame()

    customA = '%s' % (sequence.getFilename())
    customB = 'i%d o%d %s %s %s %s %s %s %s %s' % (
                                                   first,
                                                   last,
                                                   lut,
                                                   colorspace,
                                                   infoOnTop,
                                                   slateFrame,
                                                   cropValues,
                                                   dateSlate,
                                                   artistNameSlate,
                                                   disableGama
                                                   )

    if len(customA) > 250:
        print "Can't submit the job, the paths are too long"
        return False

    pathNukeToQT = '/render_apps/pyLink/toQt_base_testCrop.nk'

    att = {
         'SceneName': os.environ[envvars.RR_ROOT] + pathNukeToQT,
         'Layer': dnx,
         'SeqStart': str(first),
         'SeqEnd': str(last),
         'SeqStep': '1',
         'ImageFilename': sequence.getFilename(short=True)+nameSufix,
         'ImageDir': sequence.getDirname(),
         'ImageSingleOutputFile': 'True',
         'ImageExtension': texts.qtFileExt,
         'CustomA': customA,
         'CustomB': customB,
         'MaxClientsAtATime': '1',
         'RRO_DoNotCheckForFrames': 'True',
         'Software': 'Nuke',
         'Version': '9.0',
         'AutoDeleteEnabled': 'True',
         'Renderer': 'toQtDNX',
          }

    thisBatch.setAttribs(job, att)
    path = ("%s\\submitFiles\\toQt_%s.xml") % (environment.getCGEVBasePath(),
                                               helpers.dateTime())

    # Create place holder
    seq = sequence.getFilename(short=True) + texts.qtPlaceHoldExt
    qtPlaceHoldPath = os.path.join(sequence.getDirname(), seq)
    files.touch(qtPlaceHoldPath)

    return thisBatch.batch(path, UI=False, delete=True)


def batchExrToMp4(sequence, projectConfig, defaultClientGroup=pullToMp4):
    sequenceFilePath = sequence.getFileName()
    sequenceFolderPath = os.path.dirname(sequenceFilePath)
    sequenceFileName = sequence.getFileName(short=True)
    mp4FilePath = sequenceFolderPath + '/' + sequenceFileName + '.mp4'
    currentDate = helpers.dateTime()

    nukeFileName = '_'.join(['toMp4',
                             sequenceFileName,
                             currentDate]) + '.nk'

    nukeFilePath = os.path.join(sequenceFolderPath,
                                'rr',
                                nukeFileName)

    first = sequence.getFirstFrame()
    last = sequence.getLastFrame()

    toQtInfo = dict()

    try:
        version = nuke.NUKE_VERSION_STRING
    except:
        version = '10.5v5'

    OCIOConfig = projectConfig.getOCIOConfig()
    toQtInfo['readcolorspace'] = OCIOConfig['floatLut']
    toQtInfo['framerate'] = projectConfig.getFrameRate()
    toQtInfo['first'] = str(first)
    toQtInfo['last'] = str(last)
    toQtInfo['shotname'] = sequenceFileName
    toQtInfo['inputFilePath'] = sequenceFilePath
    toQtInfo['outFilePath'] = mp4FilePath

    templatePath = resourceslocation.toACESMp4TemplatePath
    toQtTemplateContent = files.fillTemplate(templatePath, toQtInfo)

    nukeFileFolderPath = os.path.dirname(nukeFilePath)
    if not os.path.exists(nukeFileFolderPath):
        os.makedirs(nukeFileFolderPath)

    with open(nukeFilePath, 'w') as toMp4Compo:
        toMp4Compo.write(toQtTemplateContent)

    if os.path.exists(mp4FilePath):
        try:
            os.remove(mp4FilePath)
        except:
            log.error("Can't remove .mp4 file : " + mp4FilePath)

    toBatchResult = batchNk(scene=nukeFilePath,
                            path=mp4FilePath,
                            first=first,
                            last=last,
                            clients=1,
                            nukeVersion=version,
                            singleOutPut=True,
                            checkForFrames=False,
                            colorId=BatchColor_BatchTask,
                            defaultClientGroup=defaultClientGroup,
                            user='batchtask')

    if not toBatchResult:
        log.error('can not submit file')


def batchToMp4(sequence, first=int(), last=int(), lut=str(), waitForPreID=None,
               defaultClientGroup=pullToMp4):
    '''
    function to batch mp4 renderig jobs using xml files it creates a bat,
    and submit it as an rr exe type job, the bat calls ffmpeg with args
    @todo remove the template from the .bat file
    @requires: images must not be .exr files and must be a sequence
    @param sequence: files.ImgFile object
    @param first: first frame to render   (int)
    @param last: last frame to render   (int)
    @param lut: path to the lut (implemented but not used,
           it doesnt work well in ffmpeg)
    @param waitForPreID: ID of job to wait before doing mp4
           (for cascading stuff, not used)
    @param defaultClientGroup: name of pool to use
    '''

    # FIX FOR EXR TO DELETE
    if 'exr' == sequence.getExtension().lower():
        projectTmp = sequence.getPath()

        # To be abble to create the projectConfig
        if '//storf/diskf/moreOf_cadeauDuCiel' in projectTmp:
            projectTmp = projectTmp.replace('storf/diskf/moreOf_cadeauDuCiel',
                                            'store/diske/cadeauDuCiel')
        projectTmp = projectTmp.split('/')
        projectName = projectTmp[4]
        projectPath = '/'.join(projectTmp[0:5])
        projectConfig = newconfig.ProjectCFile(projectName,
                                               projectPath,
                                               checkConfigured=False)
        # Here, test if on OCIO project and if yes, batch a .nk to generate mp4
        # Since ffmpeg is unable to batch mp4 from .exr
        if projectConfig.isOCIO():
            batchExrToMp4(sequence, projectConfig)
        return

    elif sequence.soloFile():
        return

    submitterParameters = [
                           '"AutoApproveJob=1~1"',
                           '"UserName=0~batchtask"',
                           '"DefaultClientGroup=1~'+defaultClientGroup+'"',
                           '"DoNotCheckForFrames=0~1"',
                           ]
    submitterParameter = ' '.join(submitterParameters)
    thisBatch = Batch(parameters={'SubmitterParameter': submitterParameter})
    job = thisBatch.addJob()

    batFileName = sequence.getFilename(short=True)+'_mp4.bat'
    batPath = os.path.join(sequence.getDirname(),
                           'rr',
                           batFileName)

    files.createDirs(batPath)

    if not first:
        first = sequence.getFirstFrame()
    if not last:
        last = sequence.getLastFrame()

    att = {
         'SceneName': batPath,
         'SeqStart': '1',
         'SeqEnd': '1',
         'ImageFilename': sequence.getFilename(short=True),
         'ImageDir': sequence.getDirname(),
         'ImageSingleOutputFile': 'True',
         'ImageExtension': '.mp4',
         'MaxClientsAtATime': '1',
         'Clients': defaultClientGroup,  # TODO setup in config exterior
         'Software': 'Execute',
         'AutoDeleteEnabled': 'True',
         'SceneOS': 'win',
         'Renderer': 'Once',
         'Version': '1',
         'PreID': '12'
          }

    if waitForPreID is not None:
        att['WaitForPreID'] = waitForPreID

    lutfile = str()
    if lut:
        lutfile = ',lut3d=file="' + lut + '":interp=trilinear'

    # creation du bat
    bat = open(batPath, "w")

    if sequence.getExtension() not in ['exr', ]:
        ffmpegToUse = ffmpeg
    else:
        ffmpegToUse = ffmpegLast

    try:
        seqDirName = sequence.getDirname().replace('\\', '/')
        seqDirNameSplited = seqDirName.split('/')
        projectName = seqDirNameSplited[4]
        projectPath = '/'.join(seqDirNameSplited[0:5])
        seq = sequence.getSequence()
        shot = sequence.getShot()
        configProd = newconfig.ProjectCFile(projectName, projectPath)
        if seq and shot:
            configProd.loadOverload(seq, shot)
        if "maquette" in sequence.getDirname():
            aspectRatio = '1'
        else:
            configAspectRatio = configProd.get("project_project", "format")
            aspectRatio = str(newconfig.evaluate(configAspectRatio)['ratio'])
        fps = float(configProd.get("project_project", "fps"))
    except Exception:
        aspectRatio = '1'
        fps = 24

    cmd = '{ffmpegToUse} -y -start_number {first} -r {fps} -i "{sequence}"'
    cmd += ' -c:v libx264 -pix_fmt yuv420p -g 30 -vf setsar={aspectRatio}'
    cmd += ',scale="trunc((a*oh)/2)*2:720"{lutFile}'
    cmd += ',drawtext=text="{text}":x=0:y=0:fontfile={font}:fontcolor=white'
    cmd += ' -vprofile high -bf 0 -strict experimental -r {fps} -f mp4 '
    cmd += '"{seqDirName}/{mp4fileName}.mp4"'

    sequenceName = sequence.getFilename(replacePadding=True).replace('%',
                                                                     '%%')
    mp4FileName = sequence.getFilename(short=True)
    textToDraw = sequence.getFilename(short=True)
    cmd = cmd.format(
                     ffmpegToUse=ffmpegToUse,
                     first=str(first),
                     sequence=sequenceName,
                     aspectRatio=aspectRatio,
                     lutFile=lutfile,
                     text=textToDraw,
                     font=font,
                     seqDirName=sequence.getDirname(),
                     mp4fileName=mp4FileName,
                     fps=fps,
                     )

    bat.write(cmd)
    bat.close()

    thisBatch.setAttribs(job, att)
    xmlFileName = sequence.getFilename(short=True) + '_mp4.xml'
    xmlFilePath = os.path.join(sequence.getDirname(),
                               'rr',
                               xmlFileName)

    return thisBatch.batch(xmlFilePath)


def batchToProxy(sequence, defaultClientGroup=Pulls.batchTasks):
    '''
    not used at the moment
    to render a sequence of proxy from a sequence, using ffmpeg
    '''

    submitterParameters = [
                           '"AutoApproveJob=1~1"',
                           '"UserName=0~batchtask"',
                           '"DefaultClientGroup=1~'+defaultClientGroup+'"',
                           '"DoNotCheckForFrames=0~1"',
                           ]
    submitterParameter = ' '.join(submitterParameters)
    thisBatch = Batch(parameters={'SubmitterParameter': submitterParameter})
    job = thisBatch.addJob()

    log.debug(sequence.getDirname())

    batFilename = sequence.getFilename(short=True)+'_proxy.bat'
    batBasePath = sequence.getDirname() + '/rr'
    batPath = batBasePath + '/' + batFilename

    files.createDirs(batPath)

    # Create Proxy folder
    proxyFolder = sequence.getDirname() + '/' + "proxy" + '/'

    log.debug("proxyFolder : {0}", proxyFolder)

    files.createDirs(proxyFolder)

    first = sequence.getFirstFrame()

    att = {
           'SceneName': batPath,
           'SeqStart': '1',
           'SeqEnd': '1',
           'ImageFilename': sequence.getFilename(short=True),
           'ImageDir': sequence.getDirname(),
           'ImageSingleOutputFile': 'True',
           'ImageExtension': '.executeOnce',
           'MaxClientsAtATime': '1',
           'Software': 'Execute',
           'AutoDeleteEnabled': 'True',
           'SceneOS': 'win',
           'Renderer': 'Once',
           'Version': '1',
           'PreID': '13'
           }

    if sequence.getExtension() not in ['exr', ]:
        ffmpegToUse = ffmpeg
    else:
        ffmpegToUse = ffmpegLast
    '''
    try:
        if "maquette" in sequence.getDirname():
            aspectRatio = '1'
        else:
            projectName = sequence.getDirname().replace('\\', '/').split('/')[4]
            projectPath = '/'.join(sequence.getDirname().replace('\\', '/').split('/')[0:5])
            configProd = newconfig.ProjectCFile(projectName, projectPath)
            aspectRatio = str(newconfig.evaluate(configProd.get("project_project", "format"))['ratio'])
    except Exception as ex:
        print ex
        aspectRatio = '1'
    '''

    # Creation du bat
    batFile = open(batPath, "w")

    sequencePadding = sequence.getFilename(replacePadding=True).replace('%',
                                                                        '%%')
    sequenceProxyPadding = files.getProxyPath(sequencePadding)
    # textToDraw = os.path.basename(sequence.getFilename(short=True))

    cmd = '{ffmpegToUse} -y -start_number {first}  -i "{sequencePadding"'
    cmd += ' -qscale 1 '
    cmd += ' "{sequenceProxyPadding}"'

    # cmd += ' -vf setsar=' + aspectRatio
    # cmd += ',drawtext=text="' + textToDraw + '":x=0:y=0:fontfile=' + font
    # cmd += ':fontcolor=white -qscale 1 '

    cmd = cmd.format(ffmpegToUse=ffmpegToUse,
                     first=str(first),
                     sequencePadding=sequencePadding,
                     sequenceProxyPadding=sequenceProxyPadding
                     )

    batFile.write(cmd)
    batFile.close()

    thisBatch.setAttribs(job, att)
    xmlFileName = sequence.getFilename(short=True) + '_proxy.xml'
    xmlFilePath = os.path.join(sequence.getDirname(),
                               'rr',
                               xmlFileName)
    return thisBatch.batch(xmlFilePath)


def batchToSeal(sequence, option, seq_type, defaultClientGroup=pullToSeal):
    '''
    same as toMp4 but to seal images
    @param sequence: files.ImgFile object
    @param option:   seal/unseal choice
    @param seq_type: REMOVE ME !!
    @param defaultClientGroup: name of pool to use
    '''
    log.debug3('------------------------ BATCH TO SEAL ----------------------')
    submitterParameters = [
                           '"AutoApproveJob=1~1"',
                           '"UserName=0~batchtask"',
                           '"DefaultClientGroup=1~'+defaultClientGroup+'"',
                           '"LittleJob=0~1"',
                           '"DoNotCheckForFrames=0~1"',
                           ]
    submitterParameter = ' '.join(submitterParameters)

    thisBatch = Batch(parameters={'SubmitterParameter': submitterParameter})
    job = thisBatch.addJob()

    batFileName = sequence.getFilename(short=True) + '_seal.bat'
    batPath = os.path.join(sequence.getDirname(),
                           'rr',
                           batFileName)

    files.createDirs(batPath)

    att = {
         'SceneName': batPath,
         'SeqStart': '1',
         'SeqEnd': '1',
         'CustomA': '%s %s %s' % (sequence.getDirname(), option, seq_type),
         'ImageFilename': sequence.getFilename(short=True),
         'ImageDir': sequence.getDirname(),
         'ImageSingleOutputFile': 'True',
         'ImageExtension': '.seal',
         'MaxClientsAtATime': '1',
         'Clients': defaultClientGroup,  # TODO setup in config exterior
         'RRO_DoNotCheckForFrames': 'True',
         'Software': 'Execute',
         'AutoDeleteEnabled': 'True',
         'SceneOS': 'win',
         'Renderer': 'Once',
         'Version': '1',
         'PreID': '17'
          }

    # creation du bat
    bat = open(batPath, "w")
    filepath = '{0}/{1}*{2}'.format(
                        sequence.getDirname(),
                        sequence.getFilename(replaceSlashes=True, short=True),
                        sequence.getExtension())

    bat.write("{0} {1} {2}".format(
                sealer.sealerExePath,
                filepath.replace("/", "\\"),
                option)
              )

    bat.close()

    thisBatch.setAttribs(job, att)

    xmlFileName = sequence.getFilename(short=True) + '_seal.xml'
    xmlFilePath = os.path.join(sequence.getDirname(),
                               'rr',
                               xmlFileName)

    return thisBatch.batch(xmlFilePath)


def batchVrayProxy(sequence, outFile, bat, first, last, dirPath, preview):
    '''
    Batch export Vray Proxies based on  existing "setExportVrayProxy" in maya scenes
    it calls a bat that calls maya with python command and arguments
    resume: rr->bat->maya->pythonInMaya->vrayProxy ...simple ?
    @param sequence: files.ImgFile object
    @param outFile: path of preview images
    @param bat: name of the bat that will call maya
    @param first: first item to proxify in scene
    @param last: last item to proxify in scene
    @param dirPath:path of ouptut proxy files
    @param preview: maximal faces in the proxy
    '''
    thisBatch = Batch()
    job = thisBatch.addJob()

    files.createDirs(outFile)

    att = {
            'SceneName': bat,
            'CustomA': sequence,
            'CustomB': dirPath,
            'CustomC': str(preview),
            'SeqStart': str(first),
            'SeqEnd': str(last),
            'ImageFilename': os.path.basename(outFile),
            'ImageDir': os.path.dirname(outFile),
            'ImageSingleOutputFile': 'False',
            'ImageExtension': '.jpg',  # TOREVIEW change .done by .jpeg
            'Clients': 'render3D',
            'Software': 'Maya',
            'SceneOS': 'win',
            'Renderer': 'ProxyExport',
            'Version': '1',
         }

    thisBatch.setAttribs(job, att)

    xmlFileName = os.path.basename(sequence) + '.xml'
    xmlFilepath = os.path.join(os.path.dirname(sequence),
                               'rr',
                               xmlFileName)
    files.createDirs(xmlFilepath)

    return thisBatch.batch(xmlFilepath, UI=True)


def generateCommand(listOfStrings):
    '''
    makes a string from a list of strings
    @param listOfStrings: list of strings
    '''
    command = ''

    for element in listOfStrings:
        command += element

    return command


def batchRealFlow(scriptFile, outFile, firstFrame, lastFrame, sceneType, preID,
                  renderer='Batcher', defaultClientGroup='RealFlow'):
    '''
    batch a realflow job using new method ie call submitter with everything as parameters, nor more xml
    @param scriptFile: realflow scene
    @param outFile: where is the ouptut file for rr to monitor
    @param firstFrame: first frame to render
    @param lastFrame: last frame to render
    @param sceneType: depending of the job type, render is differently configured (not used anymore)
    @param preID: ID used for grouping jobs and run them in cascade
    @param renderer: is the RR job config to use
    @param defaultClientGroup: default pool to use
    @TODO: use a pull class for defaultClientGroup
    '''

    imageDir = scriptFile.replace(scriptFile.split('/')[-1], '')
    outFile = outFile.replace(imageDir, '')

    commandLines = [submitter,
                    ' ' + scriptFile,
                    " -Software RealFlow",
                    " -Renderer " + renderer,
                    " -SeqStart " + str(firstFrame),
                    " -SeqEnd " + str(lastFrame),
                    " -ImageFileName " + str(outFile),
                    " -ImageDir " + str(imageDir),
                    " -AutoDeleteEnabled ",
                    " -PreID " + str(preID),
                    " DefaultClientGroup=1~"+defaultClientGroup,
                    " Color_ID=1~"+BatchColor_RealFlow,
                    # + " UserName=0~batchtask"
                    ]

    commandLinesPlus = []

    '''
    if sceneType in ['CORE','SECOND','GENERIC_MONO']:
        commandLinesPlus = [" SequenceDivide= 1~0 ",
                            #" #SeqDivMIN= 0~0 ",
                            #" #SeqDivMAX= 1~25",
                            " MaxClientsAtATime=1~1",
                           ]

    elif sceneType in ['GENERIC_MULTI'] :
        commandLinesPlus = [
                        #" SequenceDivide= 1~1 ",
                        #" SeqDivMIN= 1~"+str(int((lastFrame-firstFrame)/4)),
                        #" SeqDivMAX= 1~"+str(int(lastFrame-firstFrame)),
                        #" SeqDivMIN= 1~20 ",
                        #" SeqDivMAX= 1~50 ",
                        " MaxClientsAtATime=1~4",
                        #" -SeqDivMin 10",
                        #" -SeqDivMin 50",
                        #" -SeqDivideEnabled true ",
                        ]
    '''

    commandLines += commandLinesPlus

    '''
    if int(firstFrame) > 0:
         commandLines +=[ " DoNotCheckForFrames=1~1 "] #NO work,activate seqdiv
    '''

    command = generateCommand(commandLines)
    p = Popen(command, shell=True)  # ,stdout=PIPE, stderr=PIPE, stdin=PIPE)
    return command, p.communicate()


def batchRealFlowPreview(sceneFile, pythonPath, outFile, firstFrame, lastFrame,
                         preID=None, waitForPreID=False, sendMailMp4=False):
    '''
    to batch a preview of a simu in a machine with GPU
    @param sceneFile: realflow scene
    @param pythonPath: path to pyhton code to execute inside realflow
    @param outFile: where is the ouptut file for rr to monitor
    @param firstFrame: first frame to render
    @param lastFrame: last frame to render
    @param preID: ID used for grouping jobs and run them in cascade
    @param waitForPreID: to wait for the inital job to finish before rendering preview
    @param sendMailMp4: default pool to use
    @TODO: add a parameter defaultClientGroup and use a pull with it
    @TODO put a machine in Realflow_preview
    '''

    commandLines = [submitter,
                    ' ' + sceneFile,
                    " -Software Realflow_gui",
                    " -Renderer Preview",
                    " -SeqStart " + str(firstFrame),
                    " -SeqEnd " + str(lastFrame),
                    " -ImageFileName " + str(outFile),
                    " -AutoDeleteEnabled",
                    " -CustomA "+pythonPath,
                    " -PreID " + str(preID),
                    " SequenceDivide= 1~0",
                    " DefaultClientGroup=1~Realflow_preview",
                    " MaxClientsAtATime=1~1",
                    " PPSendMailMp4=1~"+str(int(sendMailMp4)),
                    ]

    if waitForPreID is True:
        commandLines += [" -WaitForPreID "+str(preID)]

    command = generateCommand(commandLines)
    p = Popen(command, shell=True)
    return command, p.communicate()


def batchRealFlowFromScript(scriptFile, outFile, firstFrame, lastFrame):
    '''
    to batch a reaflow scence that will laod and execute some script passed to it
    @param scriptFile: script that will be execute by Rf
    @param outFile: expected out files of images
    @param firstFrame: first frame to render
    @param lastFrame: last frame to render
    '''
    # addtionalCommandLine = '' if idoc is None else ' -idoc '+ idoc

    commandLines = [submitter,
                    ' ' + scriptFile,
                    " -Software RealFlow",
                    " -Renderer Script",
                    " -SeqStart " + str(firstFrame),
                    " -SeqEnd " + str(lastFrame),
                    " -ImageFileName " + str(outFile),
                    " -AutoDeleteEnabled",
                    " DefaultClientGroup=1~RealFlow",
                    " MaxClientsAtATime=1~1",
                    " AdditionalCommandlineParam=1~1~-script "+scriptFile,
                    " SequenceDivide= 1~0",
                    #  " -AdditionalCommandlineParam " + addtionalCommandLine,
                    #  + " UserName=0~batchtask"
                    ]
    command = generateCommand(commandLines)
    p = Popen(command, shell=True)  # ,stdout=PIPE, stderr=PIPE, stdin=PIPE)
    return command, p.communicate()


# NOT USED

def batchBat(batFile, outFile, firstFrame, lastFrame, clientGroup="renderfarm",
             maxClients=1, seqDivide=0):
    '''
    batches a bat file
    @param batFile: path of bat file to execute
    @param outFile: output file for rr to  monitor
    @param firstFrame: first frame to render
    @param lastFrame: last frame to rende
    @param clientGroup: pull to use
    @param maxClients: max number of clients
    @param seqDivide: RR paramater (see RR)
    @todo: clientgroup should use pull class (pool class)
    '''

    commandLines = [submitter,
                    ' ' + batFile,
                    " -Software Execute",
                    " -Renderer Once",
                    " -SeqStart " + str(firstFrame),
                    " -SeqEnd " + str(lastFrame),
                    " DefaultClientGroup=1~"+clientGroup,
                    " MaxClientsAtATime=1~"+str(maxClients),
                    " SequenceDivide= 1~"+str(seqDivide),
                    " Color_ID=1~1",
                    ]
    command = generateCommand(commandLines)
    p = Popen(command, shell=True)
    return command, p.communicate()


def batchBatFluid(preID, batFile, outFile, firstFrame, lastFrame,
                  clientGroup="render3D", maxClients=1, seqDivide=0,
                  layer=None, deleteOld=False, singleOutput=False):
    '''
    to batch fluids from maya
    @param preID: ID used for grouping jobs and run them in cascade
    @param batFile: path of bat file to execute
    @param outFile: output file for rr to  monitor
    @param firstFrame: first frame to render
    @param lastFrame: last frame to rende
    @param clientGroup: pull to use
    @param maxClients: max number of clients
    @param seqDivide: RR paramater (see RR)
    @param layer: name of the layer in maya that we render
    @param deleteOld: to delete existing files before render
    @param singleOutput: rr parameter to infor to monitor for a single file only
    '''

    commandLines = [submitter,
                    ' ' + batFile,
                    " -Software Maya",
                    " -Renderer Sfluids",
                    " -SeqStart " + str(firstFrame),
                    " -SeqEnd " + str(lastFrame),
                    " DefaultClientGroup=1~"+clientGroup,
                    " MaxClientsAtATime=1~"+str(maxClients),
                    " SequenceDivide= 1~"+str(seqDivide),
                    " Color_ID=1~1",
                    " -PreID " + str(preID),
                    #  ' -CustomrrEnvFile  "//storb/diskb/RoyalRender/render_apps/_setenv/win/maya.bat"',
                    ]
    if layer is not None:
        commandLines += [" -Layer " + layer, ]

    imageSplit = outFile.replace(':', '_').replace('\\', '/').split('/')

    imageDir = "//"+os.path.join(*(imageSplit[:-1])).replace('\\', '/')

    imageFileName, imageExtension = imageSplit[-1].split('.')

    if '.' not in imageExtension:
        imageExtension = '.' + imageExtension

    commandLines += [
                     " -ImageFileName "+imageFileName,
                     " -imageDir "+imageDir,
                     " -ImageExtension " + imageExtension,
                     ]

    if deleteOld:
        commandLines += [" -AutoDeleteEnabled True"]

    if singleOutput:
        commandLines += [" -ImageSingleOutputFile True"]

    command = generateCommand(commandLines)
    p = Popen(command, shell=True)
    return command, p.communicate()


def batchMayaMRAO(preID, sceneFile, outFile, firstFrame, lastFrame,
                  clientGroup="render3D", maxClients=1, seqDivide=0,
                  ImageFramePadding=4, waitForPreID=False, layer='masterLayer',
                  camera=None, deleteOld=False):
    '''
    to batch a maya file and render ambiant occlusion in Mentalray
    opens maya, alters stuffs and render
    @param preID: ID used for grouping jobs and run them in cascade
    @param sceneFile: path of scene file to render
    @param outFile: output file for rr to  monitor
    @param firstFrame: first frame to render
    @param lastFrame: last frame to rende
    @param clientGroup: pull to use
    @param maxClients: max number of clients
    @param seqDivide: RR paramater (see RR)
    @param ImageFramePadding: padding of output files
    @param waitForPreID: to enable waiting for preID job(s)
    @param layer: name of the layer in maya that we render
    @param camera: name of the camera to render
    @param deleteOld: to delete existing files before render
    '''

    imageSplit = outFile.replace('\\', '/').split('/')

    path3LastImageSplit = os.path.join(*(imageSplit[-3:])).replace('\\', '/')
    path1LastImageSplit = os.path.join(*(imageSplit[:-1])).replace('\\', '/')

    imageFileName = path3LastImageSplit.split('.')[0]
    imageFileNameOnly = imageSplit[-1].split('.')[0]
    imageDir = "//"+path3LastImageSplit  # outFile.replace(imageFileName,'')
    imageDirComplete = "//"+path1LastImageSplit  # outFile.replace(imageFileName,'')

    imageExtension = '.'+imageSplit[-1].split('.')[-1]

    # channelFilename = path3LastImageSplit.replace(':', '_').split('.')[0]

    print "imageFileName", imageFileName
    print "imageDir", imageDir

    print "imageFileNameOnly", imageFileNameOnly
    print "imageDirComplete", imageDirComplete

    print "imageExtension", imageExtension

    commandLines = [submitter,
                    ' ' + sceneFile,
                    " -Software Maya",
                    " -Renderer mentalRayAO",
                    " -Layer " + layer,
                    " -ImageFileName "+imageFileName,
                    " -ImageDir "+imageDir,
                    " -ImageFileNameOnly "+imageFileName,
                    " -ImageDirComplete "+imageDirComplete,
                    " -ImageExtension " + imageExtension,
                    #  " -ChannelFilename " + channelFilename,
                    #  " -ChannelExtension " + imageExtension,
                    " -SeqStart " + str(firstFrame),
                    " -SeqEnd " + str(lastFrame),
                    " -SeqStep " + str(1),
                    #  " -ImageFramePadding " + str(ImageFramePadding),
                    " DefaultClientGroup=1~" + clientGroup,
                    #  " MaxClientsAtATime=1~"+str(maxClients),
                    #  " SequenceDivide= 1~"+str(seqDivide),
                    " SeqDivMin=1~10",
                    " SeqDivMax=1~60",
                    " Color_ID=1~1",
                    " -PreID " + str(preID),
                    " -rrSequencecheck False",
                    " PPSequenceCheck= 1~0",
                    #  ' -CustomrrEnvFile  "//storb/diskb/RoyalRender/render_apps/_setenv/win/maya.bat"',
                    ]

    if waitForPreID is True:
        commandLines += [" -WaitForPreID "+str(preID)]

    if camera is not True:
        commandLines += [" -camera "+str(camera)]

    if deleteOld:
        commandLines += [" AutoDeleteEnabled=1~1",
                         " RRO_Overwriteexistingfiles=1~1"
                         ]

    command = generateCommand(commandLines)
    p = Popen(command, shell=True)
    return command, p.communicate()


def batchHoudiniSim(sceneFile, outFile, firstFrame, lastFrame, layer, hip,
                    preID=None, waitForPreID=False, sendMailMp4=False,
                    renderer="default", ui=False,
                    singleOutPut=False):
    '''
    to batch houdini sims
    @param sceneFile: path of scene file to render
    @param outFile: output file for rr to  monitor
    @param firstFrame: first frame to render
    @param lastFrame: last frame to rende
    @param layer: name of the node to render
    @param hip: hip variable that needs to be set in houdini to match users hip setting
    @param preID: ID used for grouping jobs and run them in cascade
    @param waitForPreID: to enable waiting for preID job(s)
    @param sendMailMp4: not implemented
    @param renderer: type of renderer config to use
    @param ui: to display the rr submitter ui
    @param singleOutPut: rr parameter....
    '''

    if ui:
        subbmiterToUse = submitterUI
    else:
        subbmiterToUse = submitter

    if not singleOutPut:
        imageExtension = outFile.split('#')[-1]
        ImageFileNameOnly = os.path.basename(outFile).split('#')[0]
        imageFileName = os.path.basename(outFile)
    else:
        imageExtension = '.'+outFile.split('.')[-1]
        ImageFileNameOnly = os.path.basename(outFile).split(imageExtension)[0]
        imageFileName = ImageFileNameOnly

    imageDirComplete = os.path.dirname(outFile)

    print "imageDirComplete", imageDirComplete
    print "imageFileName", imageFileName
    print "ImageFileNameOnly", ImageFileNameOnly
    print "imageExtension", imageExtension

    '''
    outFileSplited = outFile.replace('\\', '/').split('/')
    imageExtension = outFile.split('#')[-1]
    imageFileName = outFileSplited[-1].split('#')[0]
    imageDirComplete = outFile.replace('\\', '/').replace(outFileSplited[-1],'')
    '''

    print "singleOutPut", singleOutPut

    print "layer", layer
    print "HIP", hip

    commandLines = [subbmiterToUse,
                    ' ' + sceneFile,
                    " -Software Houdini",
                    " -Renderer "+renderer,
                    " -SeqStart " + str(firstFrame),
                    " -SeqEnd " + str(lastFrame),
                    # " -ImageFileName " + str(outFile),
                    # " -ImageFileNameOnly "+ImageFileNameOnly,
                    #" -ImageDirComplete "+imageDirComplete,
                    " -ImageDir "+imageDirComplete,
                    " -ImageFilename "+imageFileName,
                    " -ImageExtension " + imageExtension,
                    " -AutoDeleteEnabled",
                    " -ImageSingleOutputFile " + str(singleOutPut),
                    " -PreID " + str(preID),
                    " -Layer " + layer,
                    " -CustomA " + layer,
                    " -CustomB " + hip,
                    " SequenceDivide= 0~0",
                    " DefaultClientGroup=1~64Go",
                    " MaxClientsAtATime=1~1",
                    " CropEXR= 0~0",
                    " PPEXRCropchannels = 0~0",

                    #" PPSendMailMp4=1~"+str(int(sendMailMp4)),
                    ]

    if waitForPreID is True:
        commandLines += [" -WaitForPreID "+str(preID)]

    command = generateCommand(commandLines)
    log.debug(command)

    p = Popen(command, shell=True)
    return command, p.communicate()

'''
class Batcher(object):
    def __init__(self, createCopy=True, useUi=False, appConnector):
        self.createCopy = True
        self.useUi = useUi
        self.appConnector = appConnector

    def batch(self):
        if self.createCopy:
            self.createCopyScene()

        # batch It
        self.parseScene()

        self.submitBatch()

        if self.createCopy:
            self.restoreOriginalScene()

    def createCopyScene(self):
        self.originalSceneName = self.getSceneName()

    def restoreOriginalScene(self):
        self.appConnector.restoreScene(self.originalSceneName)

    def getSceneName(self):
        return self.appConnector.getSceneName()

    def parseScene(self):
        pass

    def submitBatch(self):
        if self.useUi:
            self.submitBatchUi()
        else:
            self.submitBatchCommandLine()

    def submitBatchUi(self):
        pass

    def submitBatchCommandLine(self):
        pass


class RRSubmiter(Batcher):
    def __init__(self, createCopy=True, useUi=False, appConnector):
        super(RRSubmiter, self).__init__()

    def submitBatchUi(self):
        pass

    def submitBatchCommandLine(self):
        pass
'''


def batchMayaPy(pythonFilePath, options=dict(), clientGroup="render3D",
                mayaVersion='2016'):
    '''
    executes mayapy with a python to execute ( as parameter)
    @param pythonFilePath: path to python file to execute in maya
    @param options: dict of rr options ( evolution !)
    @param clientGroup:pull to use
    @param mayaVersion:version of maya to use
    '''

    if options.get('ui'):
        subbmiterToUse = submitterUI
    else:
        subbmiterToUse = submitter

    customA = ''
    customB = ''

    if 'CustomA' in options:
        customA = " -CustomA " + options.get('CustomA')

    if 'CustomB' in options:
        customB = " -CustomB " + options.get('CustomB')

    layer = options.get('layer')
    imageFileName = options.get('imageFileName')
    imageDir = options.get('imageDir')
    imageExtension = options.get('imageExtension')
    singleOutPut = options.get('singleOutPut')

    firstFrame = options.get('firstFrame')
    lastFrame = options.get('lastFrame')

    commandLines = [subbmiterToUse,
                    ' ' + pythonFilePath,
                    " -Software Maya",
                    " -Renderer MayaPy",
                    " -version " + mayaVersion,
                    " -Layer " + layer,
                    " -ImageFileName "+imageFileName,
                    customA,
                    customB,
                    " -imageDir "+imageDir,
                    " -ImageExtension " + imageExtension,
                    " -AutoDeleteEnabled",
                    " -ImageSingleOutputFile " + str(singleOutPut),
                    " -SeqStart " + str(firstFrame),
                    " -SeqEnd " + str(lastFrame),
                    " -SeqStep " + str(1),
                    " DefaultClientGroup=1~" + clientGroup,
                    " Color_ID=1~1",
                    " -rrSequencecheck False",
                    " PPSequenceCheck= 1~0",
                    " SequenceDivide= 0~0",
                    " MaxClientsAtATime=1~1",
                    ]

    for paramName, paramValue in options.items():
        if 'PP' in paramName:
            commandLines.append(" {0}={1}".format(paramName, paramValue))

    command = generateCommand(commandLines)
    p = Popen(command, shell=True)
    return command, p.communicate()


def batchMayaExport(scenePath, options, ExporterClassName, exportPath):
    '''
    to generate a python and pass it to batchMayaExport()
    used to prepare a python that will do actions on a maya scene
    @param scenePath: path of maya scene to process
    @param options: export options as a dict
    @param ExporterClassName:name of export to use (ex alembic)
    @param exportPath: path were objects will be generated
    '''
    optionsCopy = options.copy()
    optionsCopy.pop('decodeInfo')

    pythonFile = 'import sys\n'
    pythonFile += 'import maya.standalone\nmaya.standalone.initialize()\n'
    pythonFile += 'import scramble\n'

    pythonFile += 'from cgev.common import decoder\n'
    pythonFile += 'from cgev.maya.tools import exporter\n'
    pythonFile += 'from maya import cmds\n'

    pythonFile += 'cmds.file("{scenePath}", open=True)\n'.format(scenePath=scenePath)

    pythonFile += 'exportOptions = '+str(optionsCopy)+'\n'

    optionLine = 'exportOptions["decodeInfo"] = decoder.DecodeInfo()\n'
    optionLine += 'exportOptions["decodeInfo"].__dict__ = ' + str(options.get('decodeInfo').__dict__) + '\n'

    pythonFile += optionLine

    optionLine = 'exportOptions["useRenderFarm"] = False\n'
    optionLine += 'exportOptions["usingRenderFarm"] = True\n'

    pythonFile += optionLine

    pythonFile += 'ae = exporter.{ExporterClassName}(exportOptions)\n'.format(ExporterClassName=ExporterClassName)
    pythonFile += 'ae.export()\n'
    pythonFile += 'cmds.quit(force=True, exitCode=0)\n'

    layer = '_'.join([
                      options.get('assetName'),
                      options.get('assetType'),
                      options.get('assetVersion'),
                      ExporterClassName,
                    ])

    sceneFileName = '.'.join(os.path.basename(scenePath).split('.')[:-1])
    sceneFileDir = os.path.dirname(scenePath)
    pythonFileName = sceneFileName + '_' + layer + '.py'
    pythonFileDir = os.path.join(sceneFileDir, 'RR')

    if not os.path.exists(pythonFileDir):
        os.makedirs(pythonFileDir)

    pythonFilePath = os.path.join(pythonFileDir,
                                  pythonFileName)

    with open(pythonFilePath, 'w') as fileObj:
        fileObj.write(pythonFile)

    optionsRR = dict()

    optionsRR['layer'] = layer

    optionsRR['imageFileName'] = '.'.join(os.path.basename(exportPath).split('.')[:-1])+'.'
    optionsRR['imageDir'] = os.path.dirname(exportPath)
    optionsRR['imageExtension'] = os.path.basename(exportPath).split('.')[-1]

    if options.get('exportAnimation'):
        if ExporterClassName == 'AlembicExporter':
            optionsRR['singleOutPut'] = not options.get('alembicOneFilePerFrame')
        elif ExporterClassName == 'VRSceneExporter':
            optionsRR['singleOutPut'] = not options.get('vrSceneOneFilePerFrame')
        elif ExporterClassName == 'ShaderExporter':
            optionsRR['singleOutPut'] = True
        else:
            if ExporterClassName == 'ArchiveExporter':
                optionsRR['imageFileName'] = '.'.join(os.path.basename(exportPath).split('.')[:-2])+'.'
                optionsRR['imageExtension'] = '.' + optionsRR['imageExtension']
            optionsRR['singleOutPut'] = False
    else:
        optionsRR['singleOutPut'] = True

    optionsRR['firstFrame'] = int(float(options.get('frameStart')))
    optionsRR['lastFrame'] = int(float(options.get('frameEnd')))

    optionsRR['PPPublishJob'] = "1~1"

    if 'ARCHIVE_VERSION' in os.environ:
        optionsRR['CustomA'] = os.environ.get('VRAY_VERSION')
        optionsRR['CustomB'] = os.environ.get('ARCHIVE_VERSION')

    return batchMayaPy(pythonFilePath, optionsRR)


def rrScenePathGenerator(originalScenePath):
    '''
    return a path where to store the scene copied only for rr rendering (dated)
    @param originalScenePath: original scene path
    '''
    currentDate = strftime("%y%m%d%H%M%S", gmtime())  # YYMMDDhhmmss
    originalScenePathReplaced = originalScenePath.replace('\\', '/')
    toBeReplaced = originalScenePathReplaced.split('/')[-1]
    toReplace = 'rr_'+currentDate + '/' + toBeReplaced
    rrScenePath = originalScenePath.replace(toBeReplaced,
                                            toReplace)

    return rrScenePath
