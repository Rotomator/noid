# 3DE4.script.name: Jump Between Jumpframes
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Main Window::Playback
# 3DE4.script.gui:	Main Window::Special Frames
# 3DE4.script.gui:  Main Window::NOID::Scripts:Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment: Jump Between Jumpframes...


def jumpFrames():
	cam = tde4.getCurrentCamera()
	initFrame = initFrame = tde4.getCurrentFrame(cam)
	if cam != None:
		try:
			if jfA != None and jfB != None:
				if cjfA != cjfB:
					if cam == cjfA:
							tde4.setCurrentCamera(cjfB)
							tde4.setCurrentFrame(cjfB, jfB)
					elif cam == cjfB:
							tde4.setCurrentCamera(cjfA)
							tde4.setCurrentFrame(cjfA, jfA)
					else:
						tde4.setCurrentCamera(cjfA)
						tde4.setCurrentFrame(cjfA, jfA)
				else:
					if initFrame == jfA:
						tde4.setCurrentCamera(cjfB)
						tde4.setCurrentFrame(cjfB, jfB)
					elif initFrame == jfB:
						tde4.setCurrentCamera(cjfA)
						tde4.setCurrentFrame(cjfA, jfA)
					else:
						tde4.setCurrentCamera(cjfA)
						tde4.setCurrentFrame(cjfA, jfA)
		except:
			tde4.postQuestionRequester("Jump Between Jumpframes...","Set Jumpframes A and B","Ok")
jumpFrames()
