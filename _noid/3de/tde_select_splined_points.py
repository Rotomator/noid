# 3DE4.script.name: Select Splined Points...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Main Window::Playback
# 3DE4.script.gui:	Timeline Editor::Edit
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment:	Select splined points...


def selectSplinedPoints():
	cam = tde4.getCurrentCamera()
	pg = tde4.getCurrentPGroup()
	points = tde4.getPointList(pg, 0)
	frames = tde4.getCameraPlaybackRange(cam)
	firstFrame = frames[0]
	lastFrame = frames[1]
	pList = []
	for point in points:
		currentFrame = firstFrame
		tde4.setPointSelectionFlag(pg, point, 0)
		while currentFrame < lastFrame:
			status = tde4.getPointStatus2D(pg, point, cam, currentFrame)
			if status == "POINT_INTERPOLATED":
				isValid = tde4.isPointPos2DValid(pg, point, cam, currentFrame)
				if isValid == 1:
					tde4.setPointSelectionFlag(pg, point, 1)
					name = tde4.getPointName(pg, point)
					if name not in pList:
						pList.append(name)
			currentFrame +=1
	if len(pList) > 0:
		listString = '\n'.join(pList)
		print ('Splined points in current sequence:\n' + listString)
	else:
		print "No splined points in current sequence..."
selectSplinedPoints()
