# 3DE4.script.name: Set Jumpframe A
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Main Window::Playback
# 3DE4.script.gui:	Main Window::Special Frames
# 3DE4.script.gui:  Main Window::NOID::Scripts:Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment: Set Jumpframe A


def setJumpFrameA():
	cam = tde4.getCurrentCamera()
	global sjfA, jfA, cjfA
	sjfA = tde4.getCameraName(cam)
	cjfA = tde4.getCurrentCamera()
	if cam != None:
		initFrame = tde4.getCurrentFrame(cam)
		jfA = initFrame
		try:
			print ('\nJumpframe A : ' + str(jfA) + ' : ' + str(sjfA) + '\nJumpframe B : ' + str(jfB) + ' : ' + str(sjfB))
		except:
			pass
setJumpFrameA()
