# 3DE4.script.name: Cache All Frames...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Main Window::Playback
# 3DE4.script.gui:	Object Browser::Context Menu Scene
# 3DE4.script.gui:	Object Browser::Context Menu Camera
# 3DE4.script.gui:	Object Browser::Context Menu Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment:	Cache all frames...


from cgev.common.system import MachineInfo
import time

def setLinWorkflow():
	cameraList = tde4.getCameraList()
	if len(cameraList) > 0:
		for currentCam in cameraList:
			cn		= tde4.getCameraName(currentCam)
			path	= tde4.getCameraPath(currentCam)
			ext		= path.split('.')[-1]
			if 'exr' in ext and 'labo\lin' in path:
				tde4.setCamera8BitColorGamma(currentCam, 2.2)
				tde4.setCamera8BitColorSoftclip(currentCam, 1)
				print (cn + ' > linear workflow...')
	else:
		print "\nNo cameras in scene..."


def cacheFrames():
	setLinWorkflow()
	cameraList = tde4.getCameraList()
	rTime = 0.000
	if len(cameraList) > 0:
		initCam = tde4.getCurrentCamera()
		initFrame = tde4.getCurrentFrame(initCam)
		camId = 0
		totalFrames = 0
		oTime = time.clock()
		iFlag = tde4.getIControlsEnabledFlag()
		if iFlag == 1:
			tde4.setIControlsEnabledFlag(0)
		for currentCam in cameraList:
			status = tde4.getCameraEnabledFlag(currentCam)
			if status == 1:
				frames = tde4.getCameraPlaybackRange(currentCam)
				numFrames = int(frames[1] - frames[0] + 1)
				totalFrames = totalFrames + numFrames
		tde4.postProgressRequesterAndContinue("Fill imagebuffers...", "Cache all frames...", totalFrames, "...")
		count = 0
		for currentCam in cameraList:
			status = tde4.getCameraEnabledFlag(currentCam)
			if status == 0:
				camId += 1
			else:
				tde4.setCurrentCamera(cameraList[camId])
				frames = tde4.getCameraPlaybackRange(cameraList[camId])
				firstFrame = frames[0]
				lastFrame = frames[1]
				if firstFrame != 0 and lastFrame != 0:
					tde4.setCurrentFrame(cameraList[camId], firstFrame)
					currentFrame = firstFrame
					count +=1
					tde4.updateProgressRequester(count,("Cache all frames... ") + str(count) + "/" + str(totalFrames))
					while currentFrame < lastFrame:
						#fTime = time.clock()
						currentFrame +=1
						tde4.setCurrentFrame(cameraList[camId], currentFrame)
						count +=1
						mi = MachineInfo()
						ram = mi.getRamValues()
						tTime = time.clock() - oTime
						sec = ((( tTime / count ) * ( totalFrames - count) ) + 1 )
						sec %= 3600
						min = sec/60
						sec%=60
						remainingTime = (str(int(min)) + " min " + str(int(sec)) + " sec remaining...")
						if min < 1:
							remainingTime = (str(int(sec)) + " sec remaning...")
						tde4.updateProgressRequester(count,("Cache all frames...  ") + str(count) + "/" + str(totalFrames) + "...  " + str(100 - ram[0]) + " % free memory...  " + remainingTime)
						tde4.updateGUI()
				camId += 1
		if initFrame != 0:
			tde4.setCurrentCamera(initCam)
			tde4.setCurrentFrame(initCam, initFrame)
		if iFlag == 1:
			tde4.setIControlsEnabledFlag(1)
	else:
		print "\nNo cameras in scene..."
cacheFrames()
