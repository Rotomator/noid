# 3DE4.script.name: Average 3d Points...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui.button: Lineup Controls::Average 3d Points, align-bottom-left, 80, 20
# 3DE4.script.gui.button: Orientation Controls::Average 3d Points, align-bottom-left, 80, 20
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment:	Average 3d Points...


def average3dPoints():
	pg = tde4.getCurrentPGroup()
	points = tde4.getPointList(pg,1)
	if pg != None:
		if len(points) == 2:
			pointOne = points[0]
			pointTwo = points[1]
			oneCalc = tde4.isPointCalculated3D(pg, pointOne)
			twoCalc = tde4.isPointCalculated3D(pg, pointTwo)
			if oneCalc == 1 and twoCalc == 1:
				pointTree = tde4.createPoint(pg)
				onePos = tde4.getPointCalcPosition3D(pg, pointOne)
				twoPos = tde4.getPointCalcPosition3D(pg, pointTwo)
				xMid = (onePos[0] + twoPos[0]) / 2
				yMid = (onePos[1] + twoPos[1]) / 2
				zMid = (onePos[2] + twoPos[2]) / 2
				tde4.setPointCalcPosition3D(pg, pointTree, [xMid, yMid, zMid])
				tde4.setPointSurveyPosition3D(pg, pointTree, [xMid, yMid, zMid])
				tde4.setPointSurveyMode(pg, pointTree, 'SURVEY_EXACT')
			else:
				tde4.postQuestionRequester('Average 3d Points...', 'Points must be calculated', 'Ok')
		else:
			tde4.postQuestionRequester('Average 3d Points...', 'Select two points', 'Ok')
average3dPoints()
