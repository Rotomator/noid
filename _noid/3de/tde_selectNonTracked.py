# 3DE4.script.name: Select Non Tracked...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Main Window::3DE4::File::Export
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Object Browser::Context Menu PGroup
# 3DE4.script.gui:	Timeline Editor::Edit
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment:	Select Non Tracked...

def selectNonTracked():
	camList = tde4.getCameraList()
	pg	= tde4.getCurrentPGroup()
	if len(camList) > 0 and pg != None:
		points = tde4.getPointList(pg, 0)
		pList = []
		for point in points:
			tracked = 0
			for currentCam in camList:
				frames = tde4.getCameraPlaybackRange(currentCam)
				firstFrame = frames[0]
				lastFrame = frames[1]
				currentFrame = firstFrame
				tde4.setPointSelectionFlag(pg, point, 0)
				while currentFrame < lastFrame:
					status = tde4.getPointStatus2D(pg, point, currentCam, currentFrame)
					if "POINT_KEYFRAME" in status or "POINT_OBSOLETE" in status or "POINT_TRACKED" in status or "POINT_INTERPOLATED" in status:
						tracked = 1
					currentFrame +=1
			name = tde4.getPointName(pg, point)
			if tracked == 0:
				tde4.setPointSelectionFlag(pg, point, 1)
				if name not in pList:
					pList.append(name)
		if len(pList) > 0:
			listString = '\n'.join(pList)
			print ('Non tracked points in scene:\n' + listString)
		else:
			print "No untracked points in scene..."
	else:
		tde4.postQuestionRequester("Select Non Tracked...","No cameras or no pointgroup in scene...","Ok")
selectNonTracked()
