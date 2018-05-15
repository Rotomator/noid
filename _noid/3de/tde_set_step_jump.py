# 3DE4.script.name: Set Step Jump...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Main Window::Playback
# 3DE4.script.gui:	Main Window::Special Frames
# 3DE4.script.gui:  Main Window::NOID::Scripts:Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment: Set Step Jump...


def setStepJump():
	global stepJump
	req	= tde4.createCustomRequester()
	tde4.addTextFieldWidget(req,"step","Step ","1")
	ret	= tde4.postCustomRequester(req,"Set Step",430,0,"Ok","Cancel")
	if ret==1:
		stepJump = tde4.getWidgetValue(req,"step")
		cam = tde4.getCurrentCamera()
		length = tde4.getCameraNoFrames(cam)
		frame = tde4.getCurrentFrame(cam)
		if cam != None:
			try:
				stepJump = int(stepJump)
				print ('Step > ' + str(stepJump) + ' frames...')
			except:
				print ('Bad step value')
setStepJump()
