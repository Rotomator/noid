# 3DE4.script.name: Manage Tracking Boxes...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All
# 3DE4.script.gui.config_menus: true

# 3DE4.script.comment:	Manage Tracking Boxes...


#pos = tde4.getPointPosition2D(pg,point,cam,frame)

def _boxPlus(req,widget,action):
	pg =   tde4.getCurrentPGroup()
	cam =   tde4.getCurrentCamera()
	if cam != None and pg != None:
		points = tde4.getPointList(pg,1)
		if len(points) >= 1:
			frame = tde4.getCurrentFrame(cam)
			for point in points:
				boxes = tde4.getPointTrackingBoxes2D(pg,point,cam,frame)
				search   	= boxes[0]
				pattern  	= boxes[1]
				offset   	= boxes[2]
				rotation 	= boxes[3]
				boxOuterU 	= search[0]
				boxOuterV 	= search[1]
				boxInnerU 	= pattern[0]
				boxInnerV 	= pattern[1]
				boxOuterU 	= boxOuterU * 1.1
				boxOuterV 	= boxOuterV * 1.1
				boxInnerU 	= boxInnerU * 1.1
				boxInnerV 	= boxInnerV * 1.1
				#offsetX   = offset[0]
				#offsetY   = offset[1]
				offsetX 	= boxInnerU / 2
				offsetY 	= boxInnerV / 2
				tde4.setPointTrackingBoxes2D(pg,point,cam,frame,[boxOuterU,boxOuterV],[boxInnerU,boxInnerV],[offsetX,offsetY],rotation)

def _boxMinus(req,widget,action):
	pg =   tde4.getCurrentPGroup()
	cam =   tde4.getCurrentCamera()
	if cam != None and pg != None:
		points = tde4.getPointList(pg,1)
		if len(points) >= 1:
			frame = tde4.getCurrentFrame(cam)
			for point in points:
				boxes = tde4.getPointTrackingBoxes2D(pg,point,cam,frame)
				search   	= boxes[0]
				pattern  	= boxes[1]
				offset   	= boxes[2]
				rotation 	= boxes[3]
				boxOuterU 	= search[0]
				boxOuterV 	= search[1]
				boxInnerU 	= pattern[0]
				boxInnerV 	= pattern[1]
				boxOuterU 	= boxOuterU * 0.9
				boxOuterV 	= boxOuterV * 0.9
				boxInnerU 	= boxInnerU * 0.9
				boxInnerV 	= boxInnerV * 0.9
				#offsetX   = offset[0]
				#offsetY   = offset[1]
				offsetX 	= boxInnerU / 2
				offsetY 	= boxInnerV / 2
				tde4.setPointTrackingBoxes2D(pg,point,cam,frame,[boxOuterU,boxOuterV],[boxInnerU,boxInnerV],[offsetX,offsetY],rotation)

def _boxCenter(req,widget,action):
	pg =   tde4.getCurrentPGroup()
	cam =   tde4.getCurrentCamera()
	if cam != None and pg != None:
		points = tde4.getPointList(pg,1)
		if len(points) >= 1:
			frame = tde4.getCurrentFrame(cam)
			for point in points:
				boxes = tde4.getPointTrackingBoxes2D(pg,point,cam,frame)
				search   	= boxes[0]
				pattern  	= boxes[1]
				offset   	= boxes[2]
				rotation 	= boxes[3]
				boxOuterU 	= search[0]
				boxOuterV 	= search[1]
				boxInnerU 	= pattern[0]
				boxInnerV 	= pattern[1]
				boxOuterU 	= boxOuterU
				boxOuterV 	= boxOuterV
				boxInnerU 	= boxInnerU
				boxInnerV 	= boxInnerV
				offsetX 	= boxInnerU / 2
				offsetY 	= boxInnerV / 2
				tde4.setPointTrackingBoxes2D(pg,point,cam,frame,[boxOuterU,boxOuterV],[boxInnerU,boxInnerV],[offsetX,offsetY],rotation)

def _boxSquare(req,widget,action):
	pg =   tde4.getCurrentPGroup()
	cam =   tde4.getCurrentCamera()
	if cam != None and pg != None:
		points = tde4.getPointList(pg,1)
		if len(points) >= 1:
			frame 	= tde4.getCurrentFrame(cam)
			lens 	= tde4.getCameraLens(cam)
			aspect	= tde4.getLensFilmAspect(lens)
			for point in points:
				boxes = tde4.getPointTrackingBoxes2D(pg,point,cam,frame)
				search   	= boxes[0]
				pattern  	= boxes[1]
				offset   	= boxes[2]
				rotation 	= boxes[3]
				boxOuterU 	= search[0]
				boxOuterV 	= boxOuterU * aspect
				boxInnerU 	= pattern[0]
				boxInnerV 	= boxInnerU * aspect
				#offsetX   = offset[0]
				#offsetY   = offset[1]
				offsetX 	= boxInnerU / 2
				offsetY 	= boxInnerV / 2

				tde4.setPointTrackingBoxes2D(pg,point,cam,frame,[boxOuterU,boxOuterV],[boxInnerU,boxInnerV],[offsetX,offsetY],rotation)

def _boxReset(req,widget,action):
	pg =   tde4.getCurrentPGroup()
	cam =   tde4.getCurrentCamera()
	if cam != None and pg != None:
		points = tde4.getPointList(pg,1)
		if len(points) >= 1:
			frame = tde4.getCurrentFrame(cam)
			imageWidth  = float(tde4.getCameraImageWidth(cam))
			imageHeight = float(tde4.getCameraImageHeight(cam))
			for point in points:
				boxOuterU 	= 0.05
				boxOuterV 	= 0.0666666666667
				boxInnerU 	= 0.025
				boxInnerV 	= 0.0333333333333
				offsetX 	= 0.0125
				offsetY 	= 0.0166666666667
				rotation	= 0
				tde4.setPointTrackingBoxes2D(pg,point,cam,frame,[boxOuterU,boxOuterV],[boxInnerU,boxInnerV],[offsetX,offsetY],rotation)

def manageTrackingBoxes():
	req	= tde4.createCustomRequester()
	tde4.addButtonWidget(req,"box_plus","+",150,5)
	tde4.setWidgetCallbackFunction(req,"box_plus","_boxPlus")
	tde4.setWidgetOffsets(req,"box_plus",5,100,5,-1000)
	tde4.setWidgetAttachModes(req,"box_plus","ATTACH_AS_IS","ATTACH_POSITION","ATTACH_AS_IS","ATTACH_AS_IS")

	tde4.addButtonWidget(req,"box_minus","-",150,5)
	tde4.setWidgetCallbackFunction(req,"box_minus","_boxMinus")
	tde4.setWidgetOffsets(req,"box_minus",5,100,5,-1000)
	tde4.setWidgetAttachModes(req,"box_minus","ATTACH_AS_IS","ATTACH_POSITION","ATTACH_AS_IS","ATTACH_AS_IS")

	tde4.addButtonWidget(req,"box_center","Center",150,5)
	tde4.setWidgetCallbackFunction(req,"box_center","_boxCenter")
	tde4.setWidgetOffsets(req,"box_center",5,100,5,-1000)
	tde4.setWidgetAttachModes(req,"box_center","ATTACH_AS_IS","ATTACH_POSITION","ATTACH_AS_IS","ATTACH_AS_IS")

	tde4.addButtonWidget(req,"box_square","Square",150,5)
	tde4.setWidgetCallbackFunction(req,"box_square","_boxSquare")
	tde4.setWidgetOffsets(req,"box_square",5,100,5,-1000)
	tde4.setWidgetAttachModes(req,"box_square","ATTACH_AS_IS","ATTACH_POSITION","ATTACH_AS_IS","ATTACH_AS_IS")

	tde4.addButtonWidget(req,"box_reset","Reset",150,5)
	tde4.setWidgetCallbackFunction(req,"box_reset","_boxReset")
	tde4.setWidgetOffsets(req,"box_reset",5,100,5,-1000)
	tde4.setWidgetAttachModes(req,"box_reset","ATTACH_AS_IS","ATTACH_POSITION","ATTACH_AS_IS","ATTACH_AS_IS")

	ret	= tde4.postCustomRequesterAndContinue(req,"Manage Tracking Boxes...",200,130)
manageTrackingBoxes()
