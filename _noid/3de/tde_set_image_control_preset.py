#
#
# 3DE4.script.name:	Set ImageControl Presets...
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:  Main Window::NOID::Scripts:Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

# 3DE4.script.gui:	Object Browser::Context Menu Camera
# 3DE4.script.gui:	Object Browser::Context Menu Cameras
#
# 3DE4.script.comment:	Set ImageControl Presets For Current Camera...
#
#

#
# main script...

c	= tde4.getCurrentCamera()
global iPreset1, iPreset2, iPreset3, iPreset4, iPreset5, iPreset6, iPreset7, iPreset8, iPreset9, iPreset10

if c != None :
	cn		= tde4.getCameraName(c)
	nf		= tde4.getCameraNoFrames(c)
	cnl		= (cn + ' (' + str(nf) + ' frames)')
	req	= tde4.createCustomRequester()
	tde4.addTextFieldWidget(req,"help1","","Sequence :")
	tde4.setWidgetSensitiveFlag(req, "help1", 0)
	tde4.addTextFieldWidget(req,"activeCam","Current Sequence",cnl)
	tde4.setWidgetSensitiveFlag(req, "activeCam", 0)
	tde4.addSeparatorWidget(req, "sep" "activeCam")
	tde4.addOptionMenuWidget(req,"Preset","","Preset #1","Preset #2","Preset #3","Preset #4","Preset #5","Preset #6","Preset #7","Preset #8","Preset #9","Preset #10")
	ret	= tde4.postCustomRequester(req,"Set ImageControl Presets For Current Camera...",500,350,"Ok","Cancel")

	if ret == 1:
		presetNum = tde4.getWidgetValue(req,"Preset")
		if presetNum == 1 :
			iPreset1 = cn
			tde4.setIControlsCurrentPreset(1)
			print (cn + ' > Preset #1')
		if presetNum == 2 :
			iPreset2 = cn
			tde4.setIControlsCurrentPreset(2)
			print (cn + ' > Preset #2')
		if presetNum == 3 :
			iPreset3 = cn
			tde4.setIControlsCurrentPreset(3)
			print (cn + ' > Preset #3')
		if presetNum == 4 :
			iPreset4 = cn
			tde4.setIControlsCurrentPreset(4)
			print (cn + ' > Preset #4')
		if presetNum == 5 :
			iPreset5 = cn
			tde4.setIControlsCurrentPreset(5)
			print (cn + ' > Preset #5')
		if presetNum == 6 :
			iPreset6 = cn
			tde4.setIControlsCurrentPreset(6)
			print (cn + ' > Preset #6')
		if presetNum == 7 :
			iPreset7 = cn
			tde4.setIControlsCurrentPreset(7)
			print (cn + ' > Preset #7')
		if presetNum == 8 :
			iPreset8 = cn
			tde4.setIControlsCurrentPreset(8)
			print (cn + ' > Preset #8')
		if presetNum == 9 :
			iPreset9 = cn
			tde4.setIControlsCurrentPreset(9)
			print (cn + ' > Preset #9')
		if presetNum == 10 :
			iPreset10 = cn
			tde4.setIControlsCurrentPreset(10)
			print (cn + ' > Preset #10')
