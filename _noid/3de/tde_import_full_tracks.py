# 3DE4.script.name: Import Full 2D Tracks...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Main Window::3DE4::File::Import
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Object Browser::Context Menu PGroup
# 3DE4.script.gui:	Timeline Editor::Edit
# 3DE4.script.gui.button: Manual Tracking Controls::Import Full 2D Tracks, align-top-right, 120, 20
# 3DE4.script.gui.button: Lineup Controls::Import Full 2D Tracks, align-top-right, 120, 20
# 3DE4.script.gui.button: Orientation Controls::Import Full 2D Tracks, align-top-right, 120, 20
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment:	Import Full 2D Tracks...


def importFullTracks():
	cam	= tde4.getCurrentCamera()
	pg	= tde4.getCurrentPGroup()
	if cam != None and pg != None:
		global exportFullTracksPath
		frames	= tde4.getCameraNoFrames(cam)
		pgn		= tde4.getPGroupName(pg)
		cn		= tde4.getCameraName(cam)
		cnl		= (cn + ' (' + str(frames) + ' frames)')
		width	= tde4.getCameraImageWidth(cam)
		height	= tde4.getCameraImageHeight(cam)
		req	= tde4.createCustomRequester()
		try:
			tde4.addFileWidget(req,"file_browser","Browse...","*.txt", exportFullTracksPath)
		except:
			tde4.addFileWidget(req,"file_browser","Browse...","*.txt", )
		tde4.addOptionMenuWidget(req,"mode_menu","","Replace Existing Points If Possible","Always Create New Points")
		tde4.addSeparatorWidget(req, "sep" "mode_menu")
		tde4.addTextFieldWidget(req,"activeCam","Current Sequence",cnl)
		tde4.setWidgetBGColor(req, "activeCam", .3, .3, .3)
		tde4.setWidgetSensitiveFlag(req, "activeCam", 0)
		tde4.addSeparatorWidget(req, "sep" "activeCam")
		tde4.addTextFieldWidget(req,"line1","","Options :")
		tde4.setWidgetSensitiveFlag(req, "line1", 0)
		tde4.addToggleWidget(req,"Set_TrackingBoxes","Set Tracking Boxes",1)
		tde4.addToggleWidget(req,"Set_Attributes","Set Attributes",1)
		tde4.addToggleWidget(req,"Set_Surveys","Set Surveys",1)
		ret	= tde4.postCustomRequester(req,"Import Full 2D Tracks...",700,300,"Ok","Cancel")
		if ret == 1:
			exportFullTracksPath = tde4.getWidgetValue(req,"file_browser")
			create_new 		= tde4.getWidgetValue(req,"mode_menu")
			setBoxes 		= tde4.getWidgetValue(req,"Set_TrackingBoxes")
			setAttributes 	= tde4.getWidgetValue(req,"Set_Attributes")
			setSurveys 		= tde4.getWidgetValue(req,"Set_Surveys")
			path = tde4.getWidgetValue(req,"file_browser")
			if path != None:
				f = open(path,"r")
				checkFile = f.readline()
				if '<tde 2d tracks full description v0.1>' in checkFile:
					fileFrames	 	= int(f.readline())
					tracksNum 		= int(f.readline())
					num 			= 1
					current 		= 1
					correctRange 	= 1
					count			= 0
					tde4.postProgressRequesterAndContinue("Import Full 2D Tracks...", "Import Full 2D Tracks...", tracksNum, "...")
					if frames != fileFrames:
						correctRange = 0
					while num <= tracksNum:
						name = f.readline()
						name = name[:-1]
						p = tde4.findPointByName(pg,name)
						if create_new == 2 or p == None:
							p = tde4.createPoint(pg)
							tde4.setPointName(pg,p,name)
						while current <= fileFrames:
							line = f.readline()
							line 	= str(line).split()
							frame 	= int(line[0])
							status 	= line[1]
							if 'POINT_OBSOLETE' in status or 'POINT_TRACKED' in status or 'POINT_SPLINED' in status:
								pos = [float(line[2]), float(line[3])]
								if frame <= frames:
									tde4.setPointPosition2D(pg,p,cam,frame,pos)
									tde4.setPointStatus2D(pg,p,cam,frame,status)
							if 'POINT_KEYFRAME' in status or 'POINT_KEYFRAME_END' in status:
								pos = [float(line[2]), float(line[3])]
								box0 = [float(line[4]), float(line[5])]
								box1 = [float(line[6]), float(line[7])]
								box2 = [float(line[8]), float(line[9])]
								box3 = float(line[10])
								if frame <= frames:
									tde4.setPointPosition2D(pg,p,cam,frame,pos)
									if setBoxes == 1:
										tde4.setPointTrackingBoxes2D(pg,p,cam,frame,box0,box1,box2,box3)
									tde4.setPointStatus2D(pg,p,cam,frame,status)
							current +=1
						line = f.readline() # <point_attributes>
						if '<point_attributes>' in line:
							line 	= str(f.readline()).split()
							color2D 			= (line[1])
							line 	= str(f.readline()).split()
							color3D 			= (line[1])
							line 	= str(f.readline()).split()
							hideFlag 			= (line[1])
							line 	= str(f.readline()).split()
							trackingMode 		= (line[1])
							line 	= str(f.readline()).split()
							direction 			= (line[1])
							line 	= str(f.readline()).split()
							rWeight				= (line[1])
							line 	= str(f.readline()).split()
							gWeight				= (line[1])
							line 	= str(f.readline()).split()
							bWeight				= (line[1])
							line 	= str(f.readline()).split()
							bluring 			= (line[1])
							line 	= str(f.readline()).split()
							deepTracking 		= (line[1])
							line 	= str(f.readline()).split()
							luminanceFlag 		= (line[1])
							line 	= str(f.readline()).split()
							refPatternMode 		= (line[1])
							line 	= str(f.readline()).split()
							refPatternFrame 	= (line[1])
							line 	= str(f.readline()).split()
							rotatePattern 		= (line[1])
							line 	= str(f.readline()).split()
							scalePattern 		= (line[1])
							line 	= str(f.readline()).split()
							autoKeyframes 		= (line[1])
							line 	= str(f.readline()).split()
							sensivity 			= (line[1])
							line 	= str(f.readline()).split()
							stopLowQuality 		= (line[1])
							line 	= str(f.readline()).split()
							splineBoxes 		= (line[1])
							line 	= str(f.readline()).split()
							calcMode 			= (line[1])
							line 	= str(f.readline()).split()
							triangulation 		= (line[1])
							line 	= str(f.readline()).split()
							surveyMode 			= (line[1])
							line 	= str(f.readline()).split()
							surveyX 			= (line[1])
							line 	= str(f.readline()).split()
							surveyY 			= (line[1])
							line 	= str(f.readline()).split()
							surveyZ 			= (line[1])
							line 	= str(f.readline()).split()
							surveyXFlag			= (line[1])
							line 	= str(f.readline()).split()
							surveyYFlag			= (line[1])
							line 	= str(f.readline()).split()
							surveyZFlag			= (line[1])
							line 	= str(f.readline()).split()
							surveyRadius 		= (line[1])
							line 	= str(f.readline()).split()
							inifinite 			= (line[1])
							line 	= str(f.readline()).split()
							validMode 			= (line[1])
							line 	= str(f.readline()).split()
							weightingMode 		= (line[1])
							line 	= str(f.readline()).split()
							weight 				= (line[1])
							line 	= str(f.readline()).split()
							positionBlendFlag 	= (line[1])
							line 	= str(f.readline()).split()
							positionBlendX 		= (line[1])
							line 	= str(f.readline()).split()
							positionBlendY 		= (line[1])
							line 	= str(f.readline()).split()
							timelineBlendFlag 	= (line[1])
							line 	= str(f.readline()).split()
							timelineBlend 		= (line[1])
							line 	= str(f.readline()).split()
							mocapZfilter 		= (line[1])
							if setAttributes == 1:
								tde4.setPointColor2D(pg,p,int(color2D))
								tde4.setPointColor3D(pg,p,int(color3D))
								tde4.setPointHideFlag(pg,p,int(hideFlag))
								tde4.setPointTrackingMode(pg,p,trackingMode)
								tde4.setPointTrackingDirection(pg,p,direction)
								tde4.setPointRGBWeights(pg,p,float(rWeight),float(gWeight),float(bWeight))
								tde4.setPointBlurring(pg,p,bluring)
								tde4.setPointDeepTracking(pg,p,float(deepTracking))
								tde4.setPointLuminanceChangesFlag(pg,p,int(luminanceFlag))
								tde4.setPointReferencePatternMode(pg,p,refPatternMode)
								tde4.setPointReferencePatternExplicitFrame(pg,p,int(refPatternFrame))
								tde4.setPointRotatePatternFlag(pg,p,int(rotatePattern))
								tde4.setPointScalePatternFlag(pg,p,int(scalePattern))
								tde4.setPointCreateAutoKeyframesFlag(pg,p,int(autoKeyframes))
								tde4.setPointAutoKeyframeSensitivity(pg,p,float(sensivity))
								tde4.setPointStopLowQualityTrackingFlag(pg,p,int(stopLowQuality))
								tde4.setPointSplineBoxesFlag(pg,p,int(splineBoxes))
								tde4.setPointCalcMode(pg,p,calcMode)
								tde4.setPointAllowTriangulateFlag(pg,p,int(triangulation))
								tde4.setPointInfiniteDistantFlag(pg,p,int(inifinite))
								tde4.setPointValidMode(pg,p,validMode)
								tde4.setPointWeightingMode(pg,p,weightingMode)
								tde4.setPointWeight(pg,p,float(weight))
								tde4.setPointPositionWeightBlendingFlag(pg,p,int(positionBlendFlag))
								tde4.setPointPositionWeightBlending(pg,p,float(positionBlendX),float(positionBlendY))
								tde4.setPointTimelineWeightBlendingFlag(pg,p,int(timelineBlendFlag))
								tde4.setPointTimelineWeightBlending(pg,p,int(timelineBlend))
								tde4.setPointMocapZDepthFilter(pg,p,float(mocapZfilter))
							if setSurveys == 1:
								tde4.setPointSurveyMode(pg,p,surveyMode)
								tde4.setPointSurveyPosition3D(pg,p,([float(surveyX),float(surveyY),float(surveyZ)]))
								tde4.setPointSurveyXYZEnabledFlags(pg,p,int(surveyXFlag),int(surveyYFlag),int(surveyZFlag))
								tde4.setPointApproxSurveyRange(pg,p,float(surveyRadius))
							line = f.readline() # <end_point>
							current = 1
							count += 1
							tde4.updateProgressRequester(count,("Import Full 2D Tracks... \nPoint ") + str(name) + "...")
						num +=1
					if tracksNum > 1:
						trString = 'Tracks'
					else:
						trString = 'Track'
					#tde4.postQuestionRequester("Import Full 2D Tracks...",(str(tracksNum) + " " + trString + " imported...\n" + exportFullTracksPath),"Ok")
					if correctRange == 0:
						tde4.postQuestionRequester("Import Full 2D Tracks...","Frame range is not similar to track file\nImport done with current frame range...","Ok")
				else:
					tde4.postQuestionRequester("Import Full 2D Tracks...","Not a full 2D tracks file...","Ok")
	else:
		tde4.postQuestionRequester("Export Full 2D Tracks...","No cam or pointgroup...","Ok")
importFullTracks()
