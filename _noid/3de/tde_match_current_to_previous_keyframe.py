#
#
# 3DE4.script.name:	Match Current To Previous Keyframe...
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Manual Tracking Controls::Tracking
#
# 3DE4.script.comment:	Match Current To Previous Keyframe...
#
#

#
# main script...

cam	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()
try:
	if cam != None and pg != None:
		w = tde4.getCameraImageWidth(cam)
		h = tde4.getCameraImageHeight(cam)
		pl	= tde4.getPointList(pg,1)
		if len(pl) >= 1:
			for point in pl:
				frames = tde4.getCameraPlaybackRange(cam)
				firstFrame = frames[0]
				lastFrame = frames[1]
				initFrame = tde4.getCurrentFrame(cam)
				currentFrame = initFrame
				keyframe = 0
				while currentFrame >= firstFrame:
					currentFrame -=1
					status = tde4.getPointStatus2D(pg, point, cam, currentFrame)
					if status == "POINT_KEYFRAME" or status == "POINT_KEYFRAME_END":
						pos0 = tde4.getPointPosition2D(pg,point,cam,currentFrame)
						box0 = tde4.getPointTrackingBoxes2D(pg,point,cam,currentFrame)
						keyframe = 1
						refFrame = currentFrame
						break
				if keyframe == 1:
					status = tde4.getPointStatus2D(pg, point, cam, initFrame)
					if status == "POINT_KEYFRAME" or status == "POINT_KEYFRAME_END":
						pos1 = tde4.getPointPosition2D(pg,point,cam,initFrame)
						box1 = tde4.getPointTrackingBoxes2D(pg,point,cam,initFrame)
						tde4.setTrackEngineRefPattern(cam,refFrame,pos0,box0[1],box0[2],box0[3])
						tde4.setTrackEnginePattern(cam,initFrame,pos1,box1[0],box1[1],box1[2],box1[3])
						p2d = tde4.runTrackEngineProcedure("TRACK_ENGINE_USE_DEFAULT_TRANSFORM")
						dev	= tde4.getTrackEngineProcedureDeviation()*10
						if p2d[0] < 0 or p2d[0] > w or p2d[1] < 0 or p2d[1] > h:
							tde4.postQuestionRequester("Match Current To Next Keyframe...","Warning, Position Not Found...","Ok")
						else:
							tde4.pushPointsToUndoStack()
							tde4.setPointPosition2D(pg,point,cam,initFrame,p2d)
							tde4.setPointStatus2D(pg,point,cam,initFrame,"POINT_KEYFRAME")
							if dev > 1:
								tde4.postQuestionRequester("Match Current To Next Keyframe...",('Check Bad Position : Deviation > ' + str(dev)),"Ok")
					else:
						tde4.postQuestionRequester("Match Current To Previous Keyframe...","Warning, Create A Keyframe To Improve...","Ok")
				else:
					tde4.postQuestionRequester("Match Current To Previous Keyframe...","Warning, No Previous Keyframe...","Ok")
		else:
			tde4.postQuestionRequester("Match Current To Previous Keyframe...","Warning, Select At Least 1 Point...","Ok")
except:
	tde4.postQuestionRequester("Match Current To Next Keyframe...","Undetermined Error...","Ok")
