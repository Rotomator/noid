# 3DE4.script.name: Set Selected Points To Tracked...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Main Window::Playback
# 3DE4.script.gui:	Timeline Editor::Edit
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment:	Set Selected Points To Tracked...


def setSplinedPointsToTracked():
	cam = tde4.getCurrentCamera()
	pg = tde4.getCurrentPGroup()
	points = tde4.getPointList(pg, 0)
	frames = tde4.getCameraPlaybackRange(cam)
	firstFrame = frames[0]
	lastFrame = frames[1]
	for point in points:
		isSel = tde4.getPointSelectionFlag(pg, point)
		if isSel == 1:
			name = tde4.getPointName(pg, point)
			currentFrame = firstFrame
			while currentFrame < lastFrame:
				status = tde4.getPointStatus2D(pg, point, cam, currentFrame)
				if status == "POINT_INTERPOLATED" or status == "POINT_OBSOLETE":
					isValid = tde4.isPointPos2DValid(pg, point, cam, currentFrame)
					if isValid == 1:
						tde4.setPointStatus2D(pg, point, cam, currentFrame, "POINT_TRACKED")
				currentFrame +=1
			if currentFrame == lastFrame:
				tde4.setPointStatus2D(pg, point, cam, currentFrame, "POINT_KEYFRAME_END")
			print ('Point ' + name + ' > Set To Tracked...')
setSplinedPointsToTracked()
