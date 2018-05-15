#
#
# 3DE4.script.name:	Set Next Camera And Preset...
# 3DE4.script.version:	v0.1
#
# 3DE4.script.gui:  Main Window::NOID::Scripts:Cameras
# 3DE4.script.gui:  Main Window::NOID::Scripts:All

#
#
# 3DE4.script.comment:	Set Next Camera And Preset...
#
#

#
# main script...

cam	= tde4.getCurrentCamera()
if cam!=None:
	type	= tde4.getCameraType(cam)
	if type=="SEQUENCE":
		while cam!=None:
			cam	= tde4.getNextCamera(cam)
			if cam==None: cam = tde4.getFirstCamera()
			type	= tde4.getCameraType(cam)
			if type=="SEQUENCE":
				tde4.setCurrentCamera(cam)
				cn	= tde4.getCameraName(cam)
				try :
					if iPreset1 != None :
						if cn == iPreset1 :
							tde4.setIControlsCurrentPreset(1)
				except :
					pass
				try :
					if iPreset2 != None :
						if cn == iPreset2 :
							tde4.setIControlsCurrentPreset(2)
				except :
					pass
				try :
					if iPreset3 != None :
						if cn == iPreset3 :
							tde4.setIControlsCurrentPreset(3)
				except :
					pass
				try :
					if iPreset4 != None :
						if cn == iPreset4 :
							tde4.setIControlsCurrentPreset(4)
				except :
					pass
				try :
					if iPreset5 != None :
						if cn == iPreset5 :
							tde4.setIControlsCurrentPreset(5)
				except :
					pass
				try :
					if iPreset6 != None :
						if cn == iPreset6 :
							tde4.setIControlsCurrentPreset(6)
				except :
					pass
				try :
					if iPreset7 != None :
						if cn == iPreset7 :
							tde4.setIControlsCurrentPreset(7)
				except :
					pass
				try :
					if iPreset9 != None :
						if cn == iPreset8 :
							tde4.setIControlsCurrentPreset(8)
				except :
					pass
				try :
					if iPreset9 != None :
						if cn == iPreset9 :
							tde4.setIControlsCurrentPreset(9)
				except :
					pass
				try :
					if iPreset10 != None :
						if cn == iPreset10 :
							tde4.setIControlsCurrentPreset(10)
				except :
					pass
				tde4.updateGUI()
				break
