#
#
# 3DE4.script.name:	Set Exr Sequences To Linear Workflow...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Object Browser::Context Menu Camera
# 3DE4.script.gui:	Object Browser::Context Menu Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

#
#
# 3DE4.script.comment: Set Exr Sequences To Linear Workflow...
#
#

#
# main script...

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
setLinWorkflow()
