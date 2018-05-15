# 3DE4.script.name: Set Jumpframe B
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Main Window::Playback
# 3DE4.script.gui:	Main Window::Special Frames
# 3DE4.script.gui:  Main Window::NOID::Scripts:Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment: Set Jumpframe B


def setJumpFrameB():
	cam = tde4.getCurrentCamera()
	global sjfB, jfB, cjfB
	sjfB = tde4.getCameraName(cam)
	cjfB = tde4.getCurrentCamera()
	if cam != None:
		initFrame = tde4.getCurrentFrame(cam)
		jfB = initFrame
		try:
			print ('\nJumpframe A : ' + str(jfA) + ' : ' + str(sjfA) + '\nJumpframe B : ' + str(jfB) + ' : ' + str(sjfB))
		except:
			pass
setJumpFrameB()
