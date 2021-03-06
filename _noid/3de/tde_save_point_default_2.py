#
#
# 3DE4.script.name:	Save Point Default 2...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui.button: Manual Tracking Controls::Save PointDefault, align-top-left, 120, 20
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All
#
#
# 3DE4.script.comment:	Save Point Default 2...

import getpass

userName = getpass.getuser()
prefFile = ('//ad01/folderredirection$/' + str(userName) + '/Documents/' + str(userName) + '_3de_pointPref.3pp')
print ('Pref Saved : ' + str(prefFile))

def _savePointDefault2(pg,p):
	tde4.setPointColor2D(pg,p,int(__color2D))
	tde4.setPointColor3D(pg,p,int(__color3D))
	tde4.setPointHideFlag(pg,p,int(__hideFlag))
	tde4.setPointTrackingMode(pg,p,__trackingMode)
	tde4.setPointTrackingDirection(pg,p,__direction)
	tde4.setPointRGBWeights(pg,p,float(__rgbWeights[0]),float(__rgbWeights[1]),float(__rgbWeights[2]))
	tde4.setPointBlurring(pg,p,__bluring)
	tde4.setPointDeepTracking(pg,p,float(__deepTracking))
	tde4.setPointLuminanceChangesFlag(pg,p,int(__luminanceFlag))
	tde4.setPointReferencePatternMode(pg,p,__refPatternMode)
	tde4.setPointReferencePatternExplicitFrame(pg,p,int(__refPatternFrame))
	tde4.setPointRotatePatternFlag(pg,p,int(__rotatePattern))
	tde4.setPointScalePatternFlag(pg,p,int(__scalePattern))
	tde4.setPointCreateAutoKeyframesFlag(pg,p,int(__autoKeyframes))
	tde4.setPointAutoKeyframeSensitivity(pg,p,float(__sensivity))
	tde4.setPointStopLowQualityTrackingFlag(pg,p,int(__stopLowQuality))
	tde4.setPointSplineBoxesFlag(pg,p,int(__splineBoxes))
	tde4.setPointCalcMode(pg,p,__calcMode)
	tde4.setPointAllowTriangulateFlag(pg,p,int(__triangulation))
	tde4.setPointInfiniteDistantFlag(pg,p,int(__inifinite))
	tde4.setPointValidMode(pg,p,__validMode)
	tde4.setPointWeightingMode(pg,p,__weightingMode)
	tde4.setPointWeight(pg,p,float(__weight))
	tde4.setPointPositionWeightBlendingFlag(pg,p,int(__positionBlendFlag))
	tde4.setPointPositionWeightBlending(pg,p,float(__positionBlend[0]),float(__positionBlend[1]))
	tde4.setPointTimelineWeightBlendingFlag(pg,p,int(__timelineBlendFlag))
	tde4.setPointTimelineWeightBlending(pg,p,int(__timelineBlend))
	tde4.setPointMocapZDepthFilter(pg,p,float(__mocapZfilter))
	tde4.setPointSurveyMode(pg,p,__surveyMode)
	tde4.setPointSurveyXYZEnabledFlags(pg,p,int(__surveyXYZenableFlag[0]),int(__surveyXYZenableFlag[1]),int(__surveyXYZenableFlag[2]))
	tde4.setPointApproxSurveyRange(pg,p,float(__surveyRadius))
	#tde4.setPointSurveyPosition3D(pg,p,([float(__surveyXYZ[0]),float(__surveyXYZ[1]),float(__surveyXYZ[2])]))

def _setSavedPointDefault():
	global __color2D,__color3D,__hideFlag,__trackingMode,__direction,__rgbWeights,__bluring,__deepTracking,__luminanceFlag,__refPatternMode,__refPatternFrame,__rotatePattern,__scalePattern,__autoKeyframes,__sensivity,__stopLowQuality,__splineBoxes,__calcMode,__triangulation,__surveyMode,__surveyXYZ,__surveyXYZenableFlag,__surveyRadius,__inifinite,__validMode,__weightingMode,__weight,__positionBlendFlag,__positionBlend,__timelineBlendFlag,__timelineBlend,__mocapZfilter
	pg	= tde4.getCurrentPGroup()
	if pg != None:
		pl	= tde4.getPointList(pg,1)
		if len(pl) == 1:
			pRef = pl[0]
			__color2D				= tde4.getPointColor2D(pg,pRef)
			__color3D				= tde4.getPointColor3D(pg,pRef)
			__hideFlag				= tde4.getPointHideFlag(pg,pRef)
			__trackingMode			= tde4.getPointTrackingMode(pg,pRef)
			__direction				= tde4.getPointTrackingDirection(pg,pRef)
			__rgbWeights			= tde4.getPointRGBWeights(pg,pRef)
			__bluring				= tde4.getPointBlurring(pg,pRef)
			__deepTracking			= tde4.getPointDeepTracking(pg,pRef)
			__luminanceFlag			= tde4.getPointLuminanceChangesFlag(pg,pRef)
			__refPatternMode		= tde4.getPointReferencePatternMode(pg,pRef)
			__refPatternFrame		= tde4.getPointReferencePatternExplicitFrame(pg,pRef)
			__rotatePattern			= tde4.getPointRotatePatternFlag(pg,pRef)
			__scalePattern			= tde4.getPointScalePatternFlag(pg,pRef)
			__autoKeyframes			= tde4.getPointCreateAutoKeyframesFlag(pg,pRef)
			__sensivity				= tde4.getPointAutoKeyframeSensitivity(pg,pRef)
			__stopLowQuality		= tde4.getPointStopLowQualityTrackingFlag(pg,pRef)
			__splineBoxes			= tde4.getPointSplineBoxesFlag(pg,pRef)
			__calcMode 				= tde4.getPointCalcMode(pg,pRef)
			__triangulation			= tde4.getPointAllowTriangulateFlag(pg,pRef)
			__surveyMode			= tde4.getPointSurveyMode(pg,pRef)
			__surveyXYZenableFlag	= tde4.getPointSurveyXYZEnabledFlags(pg,pRef)
			__surveyRadius			= tde4.getPointApproxSurveyRange(pg,pRef)
			__inifinite				= tde4.getPointInfiniteDistantFlag(pg,pRef)
			__validMode				= tde4.getPointValidMode(pg,pRef)
			__weightingMode			= tde4.getPointWeightingMode(pg,pRef)
			__weight				= tde4.getPointWeight(pg,pRef)
			__positionBlendFlag		= tde4.getPointPositionWeightBlendingFlag(pg,pRef)
			__positionBlend			= tde4.getPointPositionWeightBlending(pg,pRef)
			__timelineBlendFlag		= tde4.getPointTimelineWeightBlendingFlag(pg,pRef)
			__timelineBlend			= tde4.getPointTimelineWeightBlending(pg,pRef)
			__mocapZfilter			= tde4.getPointMocapZDepthFilter(pg,pRef)
			#__surveyXYZ			= tde4.getPointSurveyPosition3D(pg,pRef)
			f = open(prefFile,"w")
			f.write('<tde point pref v2.0>\n')
			f.write(str(__color2D) + '\n')
			f.write(str(__color3D) + '\n')
			f.write(str(__hideFlag) + '\n')
			f.write(str(__trackingMode) + '\n')
			f.write(str(__direction) + '\n')
			f.write(str(__rgbWeights[0]) + '\n')
			f.write(str(__rgbWeights[1]) + '\n')
			f.write(str(__rgbWeights[2]) + '\n')
			f.write(str(__bluring) + '\n')
			f.write(str(__deepTracking) + '\n')
			f.write(str(__luminanceFlag) + '\n')
			f.write(str(__refPatternMode) + '\n')
			f.write(str(__refPatternFrame) + '\n')
			f.write(str(__rotatePattern) + '\n')
			f.write(str(__scalePattern) + '\n')
			f.write(str(__autoKeyframes) + '\n')
			f.write(str(__sensivity) + '\n')
			f.write(str(__stopLowQuality) + '\n')
			f.write(str(__splineBoxes) + '\n')
			f.write(str(__calcMode) + '\n')
			f.write(str(__triangulation) + '\n')
			f.write(str(__surveyMode) + '\n')
			f.write(str(__surveyXYZenableFlag[0]) + '\n')
			f.write(str(__surveyXYZenableFlag[1]) + '\n')
			f.write(str(__surveyXYZenableFlag[2]) + '\n')
			f.write(str(__surveyRadius) + '\n')
			f.write(str(__inifinite) + '\n')
			f.write(str(__validMode) + '\n')
			f.write(str(__weightingMode) + '\n')
			f.write(str(__weight) + '\n')
			f.write(str(__positionBlendFlag) + '\n')
			f.write(str(__positionBlend[0]) + '\n')
			f.write(str(__positionBlend[1]) + '\n')
			f.write(str(__timelineBlendFlag) + '\n')
			f.write(str(__timelineBlend) + '\n')
			f.write(str(__positionBlendFlag) + '\n')
			f.write(str(__mocapZfilter) + '\n')
			#f.write(__surveyXYZ + '\n')
			tde4.setCreateNewPointCallbackFunction("_savePointDefault2")
			pName = tde4.getPointName(pg,pRef)
			print ('Point default : ' + pName)
_setSavedPointDefault()
