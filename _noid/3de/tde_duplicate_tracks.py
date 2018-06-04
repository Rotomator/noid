#
#
# 3DE4.script.name:	Duplicate 2D Tracks...
#
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Object Browser::Context Menu PGroup
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All
#
#
# 3DE4.script.comment:	Duplicate 2D Tracks...

c	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()
if c!=None and pg!=None:
	frames	= tde4.getCameraNoFrames(c)
	width	= tde4.getCameraImageWidth(c)
	height	= tde4.getCameraImageHeight(c)
	p	= tde4.getContextMenuObject()
	if p!=None:
		pg	= tde4.getContextMenuParentObject()
		l	= tde4.getPointList(pg,1)
	else:
		l	= tde4.getPointList(pg,1)
	if len(l)>0:
		for point in l:
			name	= tde4.getPointName(pg,point)
			newName = name + "_1"
			p = tde4.createPoint(pg)
			tde4.setPointName(pg,p,newName)
			pl = tde4.getPointPosition2DBlock(pg,point,c,1,frames)
			tde4.setPointPosition2DBlock(pg,p,c,1,pl)
	else:
		tde4.postQuestionRequester("Duplicate 2D Tracks...","There are no selected points.","Ok")
else:
	tde4.postQuestionRequester("Duplicate 2D Tracks...","There is no current Point Group or Camera.","Ok")
