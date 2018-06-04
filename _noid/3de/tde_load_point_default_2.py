#
#
# 3DE4.script.name:	Load Point Default 2...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui.button: Manual Tracking Controls::Load PointDefault, align-top-left, 120, 20
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All
#
#
# 3DE4.script.comment:	Load Point Default 2...

import getpass

userName = getpass.getuser()
prefFile = ('//ad01/folderredirection$/' + str(userName) + '/Documents/' + str(userName) + '_3de_pointPref.3pp')
print ('Pref Loading : ' + str(prefFile))

def _loadPointDefault2(pg,p):
	tde4.setPointColor2D(pg,p,int(__color2D))
	tde4.setPointColor3D(pg,p,int(__color3D))
	tde4.setPointHideFlag(pg,p,int(__hideFlag))
	tde4.setPointTrackingMode(pg,p,__trackingMode)
	tde4.setPointTrackingDirection(pg,p,__direction)
	tde4.setPointRGBWeights(pg,p,float(__rWeight),float(__gWeight),float(__bWeight))
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
	tde4.setPointPositionWeightBlending(pg,p,float(__positionBlendX),float(__positionBlendY))
	tde4.setPointTimelineWeightBlendingFlag(pg,p,int(__timelineBlendFlag))
	tde4.setPointTimelineWeightBlending(pg,p,int(__timelineBlend))
	tde4.setPointMocapZDepthFilter(pg,p,float(__mocapZfilter))
	tde4.setPointSurveyMode(pg,p,__surveyMode)
	tde4.setPointSurveyXYZEnabledFlags(pg,p,int(__surveyXenableFlag),int(__surveyYenableFlag),int(__surveyZenableFlag))
	tde4.setPointApproxSurveyRange(pg,p,float(__surveyRadius))
	#tde4.setPointSurveyPosition3D(pg,p,([float(__surveyXYZ[0]),float(__surveyXYZ[1]),float(__surveyXYZ[2])]))

def _setLoadedPointDefault():
	global __color2D,__color3D,__hideFlag,__trackingMode,__direction,__rWeight,__gWeight,__bWeight,__bluring,__deepTracking,__luminanceFlag,__refPatternMode,__refPatternFrame,__rotatePattern,__scalePattern,__autoKeyframes,__sensivity,__stopLowQuality,__splineBoxes,__calcMode,__triangulation,__surveyMode,__surveyXYZ,__surveyXenableFlag,__surveyYenableFlag,__surveyZenableFlag,__surveyRadius,__inifinite,__validMode,__weightingMode,__weight,__positionBlendFlag,__positionBlendX,__positionBlendY,__timelineBlendFlag,__timelineBlend,__mocapZfilter
	pg	= tde4.getCurrentPGroup()
	if pg != None:
		try:
			f = open(prefFile,"r")
			checkFile = f.readline()
			if '<tde point pref v2.0>\n' in checkFile:
				__color2D				= int(f.readline())
				__color3D				= int(f.readline())
				__hideFlag				= int(f.readline())
				__trackingMode			= str(f.readline())
				if 'PATTERN' in __trackingMode:
					__trackingMode = 'TRACKING_PATTERN'
				if 'MARKER' in __trackingMode:
					__trackingMode = 'TRACKING_MARKER'
				if 'CORNER' in __trackingMode:
					__trackingMode = 'TRACKING_CORNER'
				__direction				= str(f.readline())
				if 'TRACKING_FW_BW' in __direction:
					__direction = 'TRACKING_FW_BW'
				else:
					if 'TRACKING_BW' in __direction:
						__direction = 'TRACKING_BW'
					if 'TRACKING_FW' in __direction:
						__direction = 'TRACKING_FW'
				__rWeight				= float(f.readline())
				__gWeight				= float(f.readline())
				__bWeight				= float(f.readline())
				__bluring				= str(f.readline())
				if 'BLUR_NONE' in __bluring:
					__bluring = 'BLUR_NONE'
				if 'BLUR_3X3' in __bluring:
					__bluring = 'BLUR_3X3'
				if 'BLUR_5X5' in __bluring:
					__bluring = 'BLUR_5X5'
				__deepTracking			= float(f.readline())
				__luminanceFlag			= int(f.readline())
				__refPatternMode		= str(f.readline())
				if 'REF_PATTERN_PREVIOUS_FRAME' in __refPatternMode:
					__refPatternMode = 'REF_PATTERN_PREVIOUS_FRAME'
				if 'REF_PATTERN_PREVIOUS_KEYFRAME' in __refPatternMode:
					__refPatternMode = 'REF_PATTERN_PREVIOUS_KEYFRAME'
				if 'REF_PATTERN_FIRST_KEYFRAME' in __refPatternMode:
					__refPatternMode = 'REF_PATTERN_FIRST_KEYFRAME'
				if 'REF_PATTERN_EXPLICIT_FRAME' in __refPatternMode:
					__refPatternMode = 'REF_PATTERN_EXPLICIT_FRAME'
				__refPatternFrame		= int(f.readline())
				__rotatePattern			= int(f.readline())
				__scalePattern			= int(f.readline())
				__autoKeyframes			= int(f.readline())
				__sensivity				= float(f.readline())
				__stopLowQuality		= int(f.readline())
				__splineBoxes			= int(f.readline())
				__calcMode 				= str(f.readline())
				if 'CALC_OFF' in __calcMode:
					__calcMode = 'CALC_OFF'
				if 'CALC_PASSIVE' in __calcMode:
					__calcMode = 'CALC_PASSIVE'
				if 'CALC_ACTIVE' in __calcMode:
					__calcMode = 'CALC_ACTIVE'
				__triangulation			= int(f.readline())
				__surveyMode			= str(f.readline())
				if 'SURVEY_FREE' in __surveyMode:
					__surveyMode = 'SURVEY_FREE'
				if 'SURVEY_APPROX' in __surveyMode:
					__surveyMode = 'SURVEY_APPROX'
				if 'SURVEY_EXACT' in __surveyMode:
					__surveyMode = 'SURVEY_EXACT'
				if 'SURVEY_LINEUP' in __surveyMode:
					__surveyMode = 'SURVEY_LINEUP'
				__surveyXenableFlag		= int(f.readline())
				__surveyYenableFlag		= int(f.readline())
				__surveyZenableFlag		= int(f.readline())
				__surveyRadius			= float(f.readline())
				__inifinite				= int(f.readline())
				__validMode				= str(f.readline())
				if 'POINT_VALID_INSIDE_FOV' in __validMode:
					__validMode = 'POINT_VALID_INSIDE_FOV'
				if 'POINT_VALID_INSIDE_FRAME' in __validMode:
					__validMode = 'POINT_VALID_INSIDE_FRAME'
				if 'POINT_VALID_ALWAYS' in __validMode:
					__validMode = 'POINT_VALID_ALWAYS'
				__weightingMode			= str(f.readline())
				if 'POINT_WEIGHT_STATIC' in __weightingMode:
					__weightingMode = 'POINT_WEIGHT_STATIC'
				if 'POINT_WEIGHT_AUTO' in __weightingMode:
					__weightingMode = 'POINT_WEIGHT_AUTO'
				if 'POINT_WEIGHT_DYNAMIC' in __weightingMode:
					__weightingMode = 'POINT_WEIGHT_DYNAMIC'
				__weight				= float(f.readline())
				__positionBlendFlag		= int(f.readline())
				__positionBlendX		= float(f.readline())
				__positionBlendY		= float(f.readline())
				__timelineBlendFlag		= int(f.readline())
				__timelineBlend			= int(f.readline())
				__mocapZfilter			= float(f.readline())
				#__surveyXYZ			= f.readline()
				tde4.setCreateNewPointCallbackFunction("_loadPointDefault2")
				print ('Point default : Loaded')
			else:
				tde4.postQuestionRequester("Load Point Default 2...","Bad pref file...","Ok")
		except:
			tde4.postQuestionRequester("Load Point Default 2...","No pref file found...\nSave default before...","Ok")
_setLoadedPointDefault()
