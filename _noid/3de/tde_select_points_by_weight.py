# 3DE4.script.name: Select Points By Weight...
# 3DE4.script.version:	v0.1
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Main Window::Playback
# 3DE4.script.gui:  Main Window::NOID::Scripts:Points
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.comment:	Select points by weight...

def selectPointByWeight():
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	pgn	= tde4.getPGroupName(pg)
	cn	= tde4.getCameraName(cam)
	if pg!=None:
		points = tde4.getPointList(pg, 0)
		if points!=None:
			req	= tde4.createCustomRequester()
			tde4.addTextFieldWidget(req,"activeCam","Current Sequence ",cn)
			tde4.addTextFieldWidget(req,"activePg","Current PointGroup ",pgn)
			tde4.setWidgetBGColor(req, "activePg", .3, .3, .3)
			tde4.setWidgetSensitiveFlag(req, "activePg", 0)
			tde4.setWidgetBGColor(req, "activeCam", .3, .3, .3)
			tde4.setWidgetSensitiveFlag(req, "activeCam", 0)
			tde4.addSeparatorWidget(req, "sep" "activePg")
			tde4.addTextFieldWidget(req,"help1","","Select points :")
			tde4.setWidgetSensitiveFlag(req, "help1", 0)
			tde4.addOptionMenuWidget(req,"option","","Equal = ","Higher >","Lower <")
			tde4.addTextFieldWidget(req,"weight","Weight ","1")
			tde4.setWidgetBGColor(req, "weight", 0, 0, 0)
			ret	= tde4.postCustomRequester(req,"Select points by weight",430,220,"Ok","Cancel")
			if ret==1:
				selOption = tde4.getWidgetValue(req,"option")
				pw	= tde4.getWidgetValue(req,"weight")
				if pw == "all":
					for point in points:
						tde4.setPointSelectionFlag(pg, point, 1)
				else:
					pw	= float(tde4.getWidgetValue(req,"weight"))
					for point in points:
						tde4.setPointSelectionFlag(pg, point, 0)
						cw = tde4.getPointWeight(pg, point)
						if selOption == 1 :
							if cw == pw:
								tde4.setPointSelectionFlag(pg, point, 1)
						if selOption == 2 :
							if cw > pw:
								tde4.setPointSelectionFlag(pg, point, 1)
						if selOption == 3 :
							if cw < pw:
								tde4.setPointSelectionFlag(pg, point, 1)
selectPointByWeight()
