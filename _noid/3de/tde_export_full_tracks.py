# 3DE4.script.name: Export Full 2D Tracks...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Main Window::3DE4::File::Export
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Object Browser::Context Menu PGroup
# 3DE4.script.gui:	Timeline Editor::Edit
# 3DE4.script.gui.button: Manual Tracking Controls::Export Full 2D Tracks, align-top-right, 120, 20
# 3DE4.script.gui.button: Lineup Controls::Export Full 2D Tracks, align-top-right, 120, 20
# 3DE4.script.gui.button: Orientation Controls::Export Full 2D Tracks, align-top-right, 120, 20
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment:	Export Full 2D Tracks...


def exportFullTracks():
	cam	= tde4.getCurrentCamera()
	pg	= tde4.getCurrentPGroup()
	if cam != None and pg != None:
		tracks = tde4.getPointList(pg,1)
		tracksNum = len(tracks)
		if len(tracks) >= 1:
			global exportFullTracksPath
			frames 	= tde4.getCameraNoFrames(cam)
			pgn		= tde4.getPGroupName(pg)
			cn		= tde4.getCameraName(cam)
			cnl		= (cn + ' (' + str(frames) + ' frames)')
			req	= tde4.createCustomRequester()
			try:
				tde4.addFileWidget(req,"file_browser","Browse...","*.txt", exportFullTracksPath)
			except:
				tde4.addFileWidget(req,"file_browser","Browse...","*.txt", )
			tde4.addSeparatorWidget(req, "sep" "file_browser")
			tde4.addTextFieldWidget(req,"activeCam","Current Sequence",cnl)
			tde4.setWidgetBGColor(req, "activeCam", .3, .3, .3)
			tde4.setWidgetSensitiveFlag(req, "activeCam", 0)
			tde4.addSeparatorWidget(req, "sep" "activeCam")
			tde4.addTextFieldWidget(req,"line1","","Options :")
			tde4.setWidgetSensitiveFlag(req, "line1", 0)
			tde4.addTextFieldWidget(req,"line2","","	Tracking Boxes")
			tde4.setWidgetSensitiveFlag(req, "line2", 0)
			tde4.addTextFieldWidget(req,"line3","","	Attributes")
			tde4.setWidgetSensitiveFlag(req, "line3", 0)
			tde4.addTextFieldWidget(req,"line4","","	Surveys")
			tde4.setWidgetSensitiveFlag(req, "line4", 0)
			ret	= tde4.postCustomRequester(req,"Export Full 2D Tracks...",700,270,"Ok","Cancel")
			if ret == 1:
				exportFullTracksPath = tde4.getWidgetValue(req,"file_browser")
				f = open(exportFullTracksPath,"w")
				f.write('<tde 2d tracks full description v0.1>\n')
				f.write(str(frames) + '\n')
				tracksNum = len(tracks)
				f.write(str(tracksNum) + '\n')
				for track in tracks:
					frame = 1
					name = tde4.getPointName(pg,track)
					f.write(name + '\n')
					while frame <= frames:
						status 	= tde4.getPointStatus2D(pg,track,cam,frame)
						pos 	= tde4.getPointPosition2D(pg,track,cam,frame)
						if status == 'POINT_KEYFRAME' or status == 'POINT_KEYFRAME_END':
							box 	= tde4.getPointTrackingBoxes2D(pg,track,cam,frame)
							search 	= box[0]
							pattern	= box[1]
							offset	= box[2]
							rot 	= box[3]
							f.write(str(frame) + ' ' + status)
							f.write(' ' + str(pos[0]) + ' ' + str(pos[1]))
							f.write(' ' + str(search[0]) + ' ' + str(search[1]))
							f.write(' ' + str(pattern[0]) + ' ' + str(pattern[1]))
							f.write(' ' + str(offset[0]) + ' ' + str(offset[1]))
							f.write(' ' + str(rot) + '\n')
						if status == 'POINT_OBSOLETE' or status == 'POINT_TRACKED' or status == 'POINT_INTERPOLATED':
							f.write(str(frame) + ' ' + status)
							f.write(' ' + str(pos[0]) + ' ' + str(pos[1]) + '\n')
						if status == 'POINT_UNDEFINED':
							f.write(str(frame) + ' ' + status + '\n')
						frame += 1
					f.write('<point_attributes>\n')
					color2D				= tde4.getPointColor2D(pg,track)
					color3D				= tde4.getPointColor3D(pg,track)
					hideFlag			= tde4.getPointHideFlag(pg,track)
					trackingMode		= tde4.getPointTrackingMode(pg,track)
					direction			= tde4.getPointTrackingDirection(pg,track)
					rgbWeights			= tde4.getPointRGBWeights(pg,track)
					bluring				= tde4.getPointBlurring(pg,track)
					deepTracking		= tde4.getPointDeepTracking(pg,track)
					luminanceFlag		= tde4.getPointLuminanceChangesFlag(pg,track)
					refPatternMode		= tde4.getPointReferencePatternMode(pg,track)
					refPatternFrame		= tde4.getPointReferencePatternExplicitFrame(pg,track)
					rotatePattern		= tde4.getPointRotatePatternFlag(pg,track)
					scalePattern		= tde4.getPointScalePatternFlag(pg,track)
					autoKeyframes		= tde4.getPointCreateAutoKeyframesFlag(pg,track)
					sensivity			= tde4.getPointAutoKeyframeSensitivity(pg,track)
					stopLowQuality		= tde4.getPointStopLowQualityTrackingFlag(pg,track)
					splineBoxes			= tde4.getPointSplineBoxesFlag(pg,track)
					calcMode 			= tde4.getPointCalcMode(pg,track)
					triangulation		= tde4.getPointAllowTriangulateFlag(pg,track)
					surveyMode			= tde4.getPointSurveyMode(pg,track)
					surveyXYZ			= tde4.getPointSurveyPosition3D(pg,track)
					surveyXYZenableFlag	= tde4.getPointSurveyXYZEnabledFlags(pg,track)
					surveyRadius		= tde4.getPointApproxSurveyRange(pg,track)
					inifinite			= tde4.getPointInfiniteDistantFlag(pg,track)
					validMode			= tde4.getPointValidMode(pg,track)
					weightingMode		= tde4.getPointWeightingMode(pg,track)
					weight				= tde4.getPointWeight(pg,track)
					positionBlendFlag	= tde4.getPointPositionWeightBlendingFlag(pg,track)
					positionBlend		= tde4.getPointPositionWeightBlending(pg,track)
					timelineBlendFlag	= tde4.getPointTimelineWeightBlendingFlag(pg,track)
					timelineBlend		= tde4.getPointTimelineWeightBlending(pg,track)
					mocapZfilter		= tde4.getPointMocapZDepthFilter(pg,track)
					f.write('color2D ' + str(color2D) + '\n')
					f.write('color3D ' + str(color3D) + '\n')
					f.write('hideFlag ' + str(hideFlag) + '\n')
					f.write('trackingMode ' + str(trackingMode) + '\n')
					f.write('direction ' + str(direction) + '\n')
					f.write('rWeight ' + str(rgbWeights[0]) + '\n')
					f.write('gWeight ' + str(rgbWeights[1]) + '\n')
					f.write('bWeight ' + str(rgbWeights[2]) + '\n')
					f.write('bluring ' + str(bluring) + '\n')
					f.write('deepTracking ' + str(deepTracking) + '\n')
					f.write('luminanceFlag ' + str(luminanceFlag) + '\n')
					f.write('refPatternMode ' + str(refPatternMode) + '\n')
					f.write('refPatternFrame ' + str(refPatternFrame) + '\n')
					f.write('rotatePattern ' + str(rotatePattern) + '\n')
					f.write('scalePattern ' + str(scalePattern) + '\n')
					f.write('autoKeyframes ' + str(autoKeyframes) + '\n')
					f.write('sensivity ' + str(sensivity) + '\n')
					f.write('stopLowQuality ' + str(stopLowQuality) + '\n')
					f.write('splineBoxes ' + str(splineBoxes) + '\n')
					f.write('calcMode ' + str(calcMode) + '\n')
					f.write('triangulation ' + str(triangulation) + '\n')
					f.write('surveyMode ' + str(surveyMode) + '\n')
					f.write('surveyX ' + str(surveyXYZ[0]) + '\n')
					f.write('surveyY ' + str(surveyXYZ[1]) + '\n')
					f.write('surveyZ ' + str(surveyXYZ[2]) + '\n')
					f.write('surveyXFlag ' + str(surveyXYZenableFlag[0]) + '\n')
					f.write('surveyYFlag ' + str(surveyXYZenableFlag[1]) + '\n')
					f.write('surveyZFlag ' + str(surveyXYZenableFlag[2]) + '\n')
					f.write('surveyRadius ' + str(surveyRadius) + '\n')
					f.write('inifinite ' + str(inifinite) + '\n')
					f.write('validMode ' + str(validMode) + '\n')
					f.write('weightingMode ' + str(weightingMode) + '\n')
					f.write('weight ' + str(weight) + '\n')
					f.write('positionBlendFlag ' + str(positionBlendFlag) + '\n')
					f.write('positionBlendX ' + str(positionBlend[0]) + '\n')
					f.write('positionBlendY ' + str(positionBlend[1]) + '\n')
					f.write('timelineBlendFlag ' + str(timelineBlendFlag) + '\n')
					f.write('timelineBlend ' + str(timelineBlend) + '\n')
					f.write('mocapZfilter ' + str(mocapZfilter) + '\n')
					f.write('<end_point>\n')
				f.write('<end_file>')
				if tracksNum > 1:
					trString = 'Tracks'
				else:
					trString = 'Track'
				tde4.postQuestionRequester("Export Full 2D Tracks...",(str(tracksNum) + " " + trString + " exported...\n" + exportFullTracksPath),"Ok")
		else:
			tde4.postQuestionRequester("Export Full 2D Tracks...","Select at least one point...","Ok")
	else:
		tde4.postQuestionRequester("Export Full 2D Tracks...","No cam or pointgroup...","Ok")
exportFullTracks()
