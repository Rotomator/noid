# 3DE4.script.name: Merge Two Points...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment:	Merge two points...


def mergeTwoPoints():
	cam = tde4.getCurrentCamera()
	pg = tde4.getCurrentPGroup()
	points = tde4.getPointList(pg, 1)
	framesNo = tde4.getCameraNoFrames(cam)
	frames = tde4.getCameraPlaybackRange(cam)
	firstFrame = frames[0]
	lastFrame = frames[1]
	if len(points)==2:
		pointPrim = points[0]
		pointSec = points[1]
		namePrim = tde4.getPointName(pg,pointPrim)
		nameSec = tde4.getPointName(pg,pointSec)
		rename = (namePrim + '_' + nameSec)
		p = tde4.createPoint(pg)
		currentFrame = firstFrame
		warnStatus = False
		while currentFrame < lastFrame:
			isPrimValid = tde4.isPointPos2DValid(pg, pointPrim, cam, currentFrame)
			isSecValid = tde4.isPointPos2DValid(pg, pointSec, cam, currentFrame)
			if isPrimValid == 1:
				pos = tde4.getPointPosition2D(pg, pointPrim, cam, currentFrame)
				tde4.setPointPosition2D(pg, p, cam, currentFrame, pos)
			else:
				if isSecValid == 1:
					pos = tde4.getPointPosition2D(pg, pointSec, cam, currentFrame)
					tde4.setPointPosition2D(pg, p, cam, currentFrame, pos)
			if isPrimValid == 1 and isSecValid == 1:
				warnStatus = True
			currentFrame +=1
		if warnStatus == True:
			tde4.postQuestionRequester('mergeTwoPoints', 'If selected points are both tracked on a frame,\n the first selected point is kept for this frame...', 'Ok')
		pl = tde4.getPointPosition2DBlock(pg, p, cam, 1, framesNo)
		pN = tde4.createPoint(pg)
		tde4.setPointPosition2DBlock(pg, pN, cam, 1 ,pl)
		tde4.setPointName(pg,pN,rename)
		tde4.deletePoint(pg, p)
	else:
		tde4.postQuestionRequester('mergeTwoPoints', 'Select two points', 'Ok')
mergeTwoPoints()
