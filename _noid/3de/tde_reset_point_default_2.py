#
#
# 3DE4.script.name:	Reset Point Default 2...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui.button: Manual Tracking Controls::Reset PointDefault, align-top-left, 120, 20
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All
#
#
# 3DE4.script.comment:	Reset Point Default 2...


def _resetPointDefault2(pg,p):
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

def _setResetPointDefault():
	global __color2D,__color3D,__hideFlag,__trackingMode,__direction,__rgbWeights,__bluring,__deepTracking,__luminanceFlag,__refPatternMode,__refPatternFrame,__rotatePattern,__scalePattern,__autoKeyframes,__sensivity,__stopLowQuality,__splineBoxes,__calcMode,__triangulation,__surveyMode,__surveyXYZ,__surveyXYZenableFlag,__surveyRadius,__inifinite,__validMode,__weightingMode,__weight,__positionBlendFlag,__positionBlend,__timelineBlendFlag,__timelineBlend,__mocapZfilter
	pg	= tde4.getCurrentPGroup()
	if pg != None:
		__color2D				= 0
		__color3D				= 1
		__hideFlag				= 0
		__trackingMode			= 'TRACKING_PATTERN'
		__direction				= 'TRACKING_FW'
		__rgbWeights			= [1.0, 1.0, 1.0]
		__bluring				= 'BLUR_5X5'
		__deepTracking			= 0.0
		__luminanceFlag			= 1
		__refPatternMode		= 'REF_PATTERN_PREVIOUS_KEYFRAME'
		__refPatternFrame		= 1
		__rotatePattern			= 1
		__scalePattern			= 1
		__autoKeyframes			= 0
		__sensivity				= 0.75
		__stopLowQuality		= 1
		__splineBoxes			= 1
		__calcMode 				= 'CALC_ACTIVE'
		__triangulation			= 1
		__surveyMode			= 'SURVEY_FREE'
		__surveyXYZenableFlag	= [1, 1, 1]
		__surveyRadius			= 10.0
		__inifinite				= 0
		__validMode				= 'POINT_VALID_INSIDE_FRAME'
		__weightingMode			= 'POINT_WEIGHT_STATIC'
		__weight				= 1.0
		__positionBlendFlag		= 0
		__positionBlend			= [0.25, 0.25]
		__timelineBlendFlag		= 0
		__timelineBlend			= 10
		__mocapZfilter			= 2.0
		#__surveyXYZ			= [0.0, 0.0, 0.0]
		tde4.setCreateNewPointCallbackFunction("_resetPointDefault2")
		print ('Point default : Reset')
_setResetPointDefault()
