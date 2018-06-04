#
#
# 3DE4.script.name:	Match Point To Other Camera...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:All
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Manual Tracking Controls::Tracking
# 3DE4.script.comment:	Match Point To Other Camera...


def scaleTrackingBoxes(b0,s):
	b0[0][0]	= b0[0][0]*s
	b0[0][1]	= b0[0][1]*s
	b0[1][0]	= b0[1][0]*s
	b0[1][1]	= b0[1][1]*s
	b0[2][0]	= b0[2][0]*s
	b0[2][1]	= b0[2][1]*s
	return(b0)

global keySeqMaster, keySeqSlave

cameraList 	= tde4.getCameraList()
cameraSel	= []
if len(cameraList) > 0:
	for currentCam in cameraList:
		isSel = tde4.getCameraSelectionFlag(currentCam)
		if isSel == 1:
			cameraSel.append(currentCam)
	if len(cameraSel) == 2:
		cam = cameraSel[1]
		cam0 = cameraSel[0]
		keySeqMaster = cam0
		keySeqSlave = cam
		rs = tde4.getCameraName(cam0)
		ds = tde4.getCameraName(cam)
		print ('\nReference Sequence > ' + rs)
		print ('Destination Sequence > ' + ds)
		try:
			pg	= tde4.getCurrentPGroup()
			f	= tde4.getCurrentFrame(cam)
			ex = 1
		except:
			ex = 0
	else :
		try:
			if keySeqMaster != None and keySeqSlave != None :
				cam0 = keySeqMaster
				cam = keySeqSlave
				try:
					pg	= tde4.getCurrentPGroup()
					f	= tde4.getCurrentFrame(cam)
					ex = 1
				except:
					ex = 0
		except:
			tde4.postQuestionRequester("Match Point To Other Camera...","Error...\r\nSelect Ref Sequence, Then New Sequence...","Ok")
else:
	tde4.postQuestionRequester("Match Point To Other Camera...","Error, No Cameras In Scene...","Ok")

try:
	if cam != None and cam0 != None and pg != None and ex == 1:
		pl	= tde4.getPointList(pg,1)
		if len(pl) > 0:
			scale_x		= 1.2
			scale_y		= 1.2
			sensitivity	= 1.5
			frames		= tde4.getCameraNoFrames(cam)
			tde4.setTrackEngineMode("TRACKING_PATTERN")
			tde4.setTrackEngineFlags(1,1,1,1)
			tde4.setTrackEngineRGBWeights(1.0,1.0,1.0)
			tde4.setTrackEngineBlurring("BLUR_5X5")
			for p in pl:
				visible	= tde4.isPointPos2DValid(pg,p,cam0,f)
				if visible == 1:
					s0		= tde4.getPointStatus2D(pg,p,cam0,f)
					v0		= tde4.getPointPosition2D(pg,p,cam0,f)
					b0		= tde4.getPointTrackingBoxes2D(pg,p,cam0,f)

					if f > 1:
						startframe = not tde4.isPointPos2DValid(pg,p,cam0,f-1)
					else:
						startframe = tde4.isPointPos2DValid(pg,p,cam0,f)

					prev_ok	= 0
					if f > 1:
						status	= tde4.getPointStatus2D(pg,p,cam,f-1)
						if status == "POINT_KEYFRAME" or status == "POINT_KEYFRAME_END" or status == "POINT_TRACKED":
							prev_ok = 1

					tde4.setTrackEngineRefPattern(cam0,f,v0,b0[1],b0[2],b0[3])

					if startframe or not prev_ok:
						tde4.setTrackEnginePattern(cam,f,v0,[ b0[0][0]*scale_x,b0[0][1]*scale_y ],b0[1],b0[2],b0[3])
					else:
						v = tde4.getPointPosition2D(pg,p,cam,f-1)
						tde4.setTrackEnginePattern(cam,f,v,b0[0],b0[1],b0[2],b0[3])

					p2d	= tde4.runTrackEngineProcedure("TRACK_ENGINE_USE_DEFAULT_TRANSFORM")
					dev	= tde4.getTrackEngineProcedureDeviation()

					if dev < sensitivity:
						tde4.pushPointsToUndoStack()
						tde4.setPointPosition2D(pg,p,cam,f,p2d)
						if prev_ok:
							tde4.setPointStatus2D(pg,p,cam,f,"POINT_KEYFRAME")
						else:
							tde4.setPointStatus2D(pg,p,cam,f,"POINT_KEYFRAME")
							tde4.setPointTrackingBoxes2D(pg,p,cam,f,b0[0],b0[1],b0[2],b0[3])
						if s0 == "POINT_KEYFRAME_END":
							tde4.setPointStatus2D(pg,p,cam,f,"POINT_KEYFRAME_END")
							tde4.setPointTrackingBoxes2D(pg,p,cam,f,b0[0],b0[1],b0[2],b0[3])
						tde4.splinePointPositions2D(pg,p,cam)
					else:
						name = tde4.getPointName(pg,p)
						print "Point ",name," not found or too high deviation : ",dev
except:
	pass
